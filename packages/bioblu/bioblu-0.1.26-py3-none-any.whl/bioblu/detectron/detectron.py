#!/usr/bin/env python3

import json
import logging
import os
from typing import List, Tuple, Union

import cv2
import numpy as np
import tensorflow as tf
import termcolor
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import build_detection_test_loader, build_detection_train_loader, dataset_mapper, MetadataCatalog, DatasetCatalog
from detectron2.data import transforms as T
from detectron2.engine import DefaultPredictor, DefaultTrainer  # overridden by custom_detectron_parts
from detectron2.evaluation import COCOEvaluator
from detectron2.evaluation import inference_on_dataset
from detectron2.structures import BoxMode
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import Visualizer

from bioblu.ds_manage import ds_convert
# from bioblu.detectron.custom_detectron_parts import DefaultTrainer


class CustomTrainer(DefaultTrainer):
    """
    Customized child of the DefaultTrainer class so that it accepts customized DataMapper.
    Except from the below method it inherits all other functionalities of the DefaultTrainer class.
    """
    def __init__(self, cfg):
        DefaultTrainer.__init__(self, cfg)  # Init parent DefaultTrainer

    @classmethod
    def build_train_loader(cls, cfg, mapper=None):
        if mapper is None:
            return build_detection_train_loader(cfg)
        return build_detection_train_loader(cfg, mapper=mapper)


def load_json(json_fpath: str) -> dict:
    """Returns json data as a dict."""
    with open(json_fpath, 'r') as f:
        data = json.load(f)
    logging.debug(f'Loaded json object (type): {type(data)}')
    return data


def parse_augs(brightness_minmax: Tuple[float, float] = None,
               flip_v: float = None, flip_h: float = None,
               rot_minmax: Tuple[Union[float, int], Union[float, int]] = None) -> list:
    """
    Takes the arguments for the augmentations and returns the detectron-readable augmentations list.
    :param brightness_minmax:
    :param flip_v:
    :param flip_h:
    :param rot_minmax:
    :return:
    """
    augs = []

    if brightness_minmax is not None:
        bmin, bmax = brightness_minmax
        augs.append(T.RandomBrightness(bmin, bmax))
    if flip_v is not None:
        augs.append(T.RandomFlip(prob=flip_v, horizontal=False, vertical=True))
    if flip_h is not None:
        augs.append(T.RandomFlip(prob=flip_h, horizontal=True, vertical=False))
    if rot_minmax is not None:
        augs.append(T.RandomRotation(list(rot_minmax)))

    return augs


def create_detectron_img_dict_list(detectron_json_fpath, bbox_format = BoxMode.XYWH_ABS) -> List[dict]:
    """
    Creates a list of dictionaries to be used in detectron.
    :param detectron_json_fpath:
    :return:
    """
    json_data = load_json(detectron_json_fpath)
    images = json_data.get("images", [])
    logging.debug(f"Images: {images}")
    annotations = json_data.get("annotations", [])
    dict_list = []
    for img in images:
        current_img = {"file_name": img["file_name"],
                       "image_id": img["id"],
                       "width": img["width"],
                       "height": img["height"],
                       "annotations": []}
        for annotation in annotations:
            if annotation["image_id"] == current_img["image_id"]:
                current_img["annotations"].append({"segmentation": [],
                                                   "area": None,  # ToDo: Check if this might have to be box area.
                                                   "iscrowd": 0,
                                                   "category_id": annotation["category_id"],
                                                   "bbox_mode": bbox_format,
                                                   "bbox": annotation["bbox"]})
        dict_list.append(current_img)
    return dict_list


def visualize_detectron_prediction(prediction: dict, save_as=None, show_img=True):
    if show_img or save_as is not None:
        metadata = MetadataCatalog.get("detectron_instances_train")
        metadata.thing_classes = list(prediction["materials_dict"].values())
        img = cv2.imread(prediction["img_fpath"])
        img_name = prediction["img_name"]
        v = Visualizer(img[:, :, ::-1], metadata, scale=1.2)
        out = v.draw_instance_predictions(prediction["instances"].to("cpu"))
        if save_as is not None:
            out_dir = os.path.split(save_as)[0]
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir)
            out.save(save_as)
        if show_img:
            cv2.namedWindow(img_name, cv2.WINDOW_NORMAL)
            cv2.imshow(img_name, out.get_image()[:, :, ::-1])
            cv2.waitKey(0)


def unpack_2d_tensor(input_tensor: tf.Tensor) -> np.array:
    return np.array([row.detach().numpy() for row in input_tensor])


def serialize_instance(prediction_result: dict) -> dict:
    """Turns a prediction result as created by detectron2 into a dict that can be saved as json."""
    # Detectron2 boxes are stored as (x1, y1, x2, y2) tensors.
    instances = prediction_result["instances"]
    prediction_dict = {"img_name": prediction_result.get("img_name"),
                       "img_fpath": prediction_result.get("img_fpath"),
                       "instances": {"pred_boxes": unpack_2d_tensor(instances.get("pred_boxes")).tolist(),
                                     "box_centers": instances.get("pred_boxes").get_centers().detach().numpy().tolist(),
                                     "scores": unpack_2d_tensor(instances.get("scores")).tolist(),
                                     "pred_classes": unpack_2d_tensor(instances.get("pred_classes")).tolist(),
                                     },
                       "cfg": prediction_result.get("cfg"),
                       }
    return prediction_dict


def run_training(yolo_ds_root_dir: str, model_yaml: str, output_dir: str, materials_dict: dict,
                 train_json: str = None, val_json: str = None, iterations: int = 2500,
                 ds_cfg_savename="ds_catalog_train.json", ds_name_train="instances_detectron_train",
                 ds_name_val="instances_detectron_val", img_size_minmax: Tuple[int, int] = (1820, 1830), device="cuda",
                 filter_out_empty_imgs=False, max_detections_per_img=2000, number_of_workers=2, imgs_per_batch=2,
                 base_lr: float = 0.00025, lr_decay=None, roi_heads_batch_size_per_img=512,
                 training_confidence_threshold=0.5, validation_confidence_threshold=0.65,
                 iou_thresh = 0.5, nms_thresh: float = 0.7,
                 augmentations: list = None):
    """
    :param yolo_ds_root_dir:
    :param model_yaml: Must include parent dir, e.g. "COCO-Detection/faster_rcnn_R_101_C4_3x.yaml". Used to cfg.merge_from_file and to get cfg.MODEL.WEIGHTS and
    :param output_dir:
    :param materials_dict:
    :param train_json: defaults to "{detectron_ds_target_dir}/"annotations/{ds_name_train}.json"
    :param val_json: defaults to "{detectron_ds_target_dir}/"annotations/{ds_name_val}.json"
    :param iterations:
    :param ds_cfg_savename:
    :param ds_name_train: defaults to instances_detectron_train
    :param ds_name_val: defaults to instances_detectron_val
    :param img_size_minmax:
    :param device: "cpu" or "cuda". Fed into cfg.MODEL.DEVICE
    :param filter_out_empty_imgs:
    :param max_detections_per_img:
    :param number_of_workers:
    :param imgs_per_batch:
    :param base_lr:
    :param lr_decay:
    :param roi_heads_batch_size_per_img:
    :param training_confidence_threshold: first fed into cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST
    :param validation_confidence_threshold: later fed into cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST
    :param crop_type:
    :param use_cropping_aug:
    :param rpn_nms_thresh:
    :param augmentations: list of transforms
    :return:
    ```
    Model options (only for detection, other methods are not listed here):
    COCO-Detection/faster_rcnn_R_101_C4_3x.yaml
    COCO-Detection/faster_rcnn_R_101_DC5_3x.yaml
    COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml
    COCO-Detection/faster_rcnn_R_50_C4_1x.yaml
    COCO-Detection/faster_rcnn_R_50_C4_3x.yaml
    COCO-Detection/faster_rcnn_R_50_DC5_1x.yaml
    COCO-Detection/faster_rcnn_R_50_DC5_3x.yaml
    COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml
    COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml
    COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml
    COCO-Detection/fast_rcnn_R_50_FPN_1x.yaml
    COCO-Detection/fcos_R_50_FPN_1x.py
    COCO-Detection/retinanet_R_101_FPN_3x.yaml
    COCO-Detection/retinanet_R_50_FPN_1x.py
    COCO-Detection/retinanet_R_50_FPN_1x.yaml
    COCO-Detection/retinanet_R_50_FPN_3x.yaml
    COCO-Detection/rpn_R_50_C4_1x.yaml
    COCO-Detection/rpn_R_50_FPN_1x.yaml

    To see other options for segmentation, keypoints, panoptic segmentation, etc. refer to detectron2/configs in the repo.
    """
    if not os.path.isdir(yolo_ds_root_dir):
        raise FileNotFoundError(f"Yolo style root dir does not exist: {yolo_ds_root_dir}")

    detectron_ds_target_dir = os.path.join(yolo_ds_root_dir.rstrip("/") + "_detectron")

    # Assign default values where arguments are None
    if train_json is None:
        train_json = os.path.join(detectron_ds_target_dir, "annotations", ds_name_train + ".json")
    if val_json is None:
        val_json = os.path.join(detectron_ds_target_dir, "annotations", ds_name_val + ".json")
    lr_decay = [] if lr_decay is None else lr_decay
    augmentations = [] if augmentations is None else augmentations

    print("------------------------------------ TRAINING SETTINGS ----------------------------------------------------")
    print(f"Training on dataset {yolo_ds_root_dir}")
    print(f"Using model {model_yaml}")
    print(f"Running on device: {device}")
    print(f"Skipping empty imgs (i.e. background images): {filter_out_empty_imgs}")
    print(f"Iterations: {iterations}")
    print(f"Img. size (min, max): {img_size_minmax}")
    print(f"Max. detections per img: {max_detections_per_img}")
    print(f"Number of workers: {number_of_workers}")
    print(f"Base learning rate: {base_lr}")
    print(f"Learning rate decay: {lr_decay}")
    print(f"Training confidence threshold: {training_confidence_threshold}")
    print(f"Validation confidence threshold: {validation_confidence_threshold}")
    print(f"Images per batch: {imgs_per_batch}")
    print(f"ROI heads batch size: {roi_heads_batch_size_per_img}")
    print(f"RPN NMS threshold: {nms_thresh}")
    print(f"Using augmentations: {augmentations}")
    print(f"Training json: {train_json}")
    print(f"Validation json: {val_json}")
    print("-----------------------------------------------------------------------------------------------------------")

    ds_convert.cvt_yolo_to_detectron(yolo_ds_root_dir)

    setup_logger()  # Detectron2 logger
    ds_convert.cvt_yolo_to_detectron(yolo_ds_root_dir, materials_dict=materials_dict)
    # Extract image dict lists from jsons
    logging.info("Img. dict lists extracted.")
    # Register classes
    classes = materials_dict
    logging.info("Classes registered.")

    cfg = get_cfg()
    # Load model and model weights/checkpoint
    cfg.merge_from_file(model_zoo.get_config_file(model_yaml))
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(model_yaml)
    cfg.MODEL.DEVICE = device
    cfg.DATALOADER.FILTER_EMPTY_ANNOTATIONS = filter_out_empty_imgs
    # Override output dir to prevent "permission denied" error during mkdir
    cfg.OUTPUT_DIR = output_dir
    # Register datasets
    DatasetCatalog.register(ds_name_train, lambda: create_detectron_img_dict_list(train_json))
    DatasetCatalog.register(ds_name_val, lambda: create_detectron_img_dict_list(val_json))
    # Register metadata
    MetadataCatalog.get(ds_name_train).set(thing_classes=list(classes.values()))
    MetadataCatalog.get(ds_name_val).set(thing_classes=list(classes.values()))
    # Allocate datasets
    cfg.DATASETS.TRAIN = (ds_name_train,)
    cfg.DATASETS.TEST = (ds_name_val,)
    # Training parameters
    cfg.TEST.DETECTIONS_PER_IMAGE = max_detections_per_img  # set max detections per img
    cfg.INPUT.MIN_SIZE_TRAIN = (img_size_minmax[0],)  # minimum image size for the train set
    cfg.INPUT.MAX_SIZE_TRAIN = img_size_minmax[1]  # maximum image size for the train set
    cfg.INPUT.MIN_SIZE_TEST = img_size_minmax[0]  # minimum image size for the test set
    cfg.INPUT.MAX_SIZE_TEST = img_size_minmax[1]  # maximum image size for the test set

    cfg.DATALOADER.NUM_WORKERS = number_of_workers
    cfg.SOLVER.IMS_PER_BATCH = imgs_per_batch
    cfg.SOLVER.BASE_LR = base_lr
    cfg.SOLVER.MAX_ITER = iterations
    cfg.SOLVER.STEPS = lr_decay  # [] to not decay learning rate
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = roi_heads_batch_size_per_img
    # cfg.DATASETS.PROPOSAL_FILES_TRAIN =     # ToDo: Perhaps add the proposal files?

    # Set thresholds
    # cfg.MODEL.RPN.NMS_THRESH = nms_thresh
    cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = nms_thresh
    cfg.MODEL.ROI_HEADS.IOU_THRESHOLDS = [iou_thresh]
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(materials_dict.keys()) # NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrectly use num_classes+1 here.
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TRAIN = training_confidence_threshold  # 0.5  # set threshold for this model
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = validation_confidence_threshold  # 0.5  # set threshold for this model
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = validation_confidence_threshold

    # ToDo: check additional augmentation & hyperparameter options
    logging.info("cfg set up completed.")

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    logging.info("Output dir created")

    # Save dataset catalog entries:
    dataset_test_out = DatasetCatalog.get(ds_name_train)
    savefile = os.path.join(cfg.OUTPUT_DIR, ds_cfg_savename)
    with open(savefile, "w") as f:
        json.dump(dataset_test_out, f, indent=4)
        logging.info(f"Dataset Catalog (training) saved as {savefile}")

    # save training config cfg to yaml
    cfg_save_path = os.path.join(cfg.OUTPUT_DIR, "cfg.yaml")
    cfg_save_string = cfg.dump()
    with open(cfg_save_path, "w") as f:
        f.write(cfg_save_string)
    print(f"Saved model/training cfg in {cfg_save_path}")

    # Set up trainer
    trainer = DefaultTrainer(cfg)

    if augmentations:
        mapper_w_augs = dataset_mapper.DatasetMapper(cfg, augmentations=augmentations)
        trainer.build_train_loader(cfg)

    logging.debug("Done setting up trainer.")
    trainer.resume_or_load(resume=False)

    print()

    logging.debug("Starting training.")
    trainer.train()
    print("Done training. Proceeding to evaluation.")

    # Prep evaluation
    # pretrained_model = "/content/drive/MyDrive/colab_outputs/2022-04-30_1030/model_final.pth"
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")  # path to the model we just trained
    print(f"Evaluating model {os.path.join(cfg.OUTPUT_DIR, 'model_final.pth')}")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = validation_confidence_threshold  # set a custom testing threshold
    predictor = DefaultPredictor(cfg)

    # Evaluate
    evaluator = COCOEvaluator(ds_name_val,
                              tasks=("bbox",),
                              use_fast_impl=False,  # use a fast but unofficial implementation to compute AP
                              output_dir=output_dir)
    val_loader = build_detection_test_loader(cfg, ds_name_val)
    evaluation_results = inference_on_dataset(predictor.model, val_loader, evaluator)
    print(evaluation_results)

    # Save evaluation results
    eval_results_savepath = os.path.join(cfg.OUTPUT_DIR, "evaluation_results.txt")
    with open(eval_results_savepath, "w") as f:
        f.write(json.dumps(evaluation_results, indent=4))
    print("Done training and evaluating.")

    return evaluation_results


def run_training_on_cluster(dataset_dir, model_yaml, iterations, base_lr, batch_size: int, lr_decay=None,
                            material_dict=None, train_json=None, val_json=None,
                            conf_thresh_train=0.2, conf_thresh_val=0.6,
                            augmentations=None, nms_thresh=0.5):

    if material_dict is None:
        material_dict = {0: "trash"}

    output_dir = "/opt/nfs/shared/scratch/bioblu/output"
    run_training(yolo_ds_root_dir=dataset_dir, model_yaml=model_yaml, output_dir=output_dir,
                 materials_dict=material_dict, train_json=train_json, val_json=val_json,
                 iterations=iterations, ds_cfg_savename="ds_catalog_train.json",
                 ds_name_train="instances_detectron_train", ds_name_val="instances_detectron_val",
                 img_size_minmax=(1820, 1830), device="cuda", filter_out_empty_imgs=False, max_detections_per_img=4000,
                 number_of_workers=2, imgs_per_batch=2, base_lr=base_lr, lr_decay=lr_decay,
                 roi_heads_batch_size_per_img=batch_size, training_confidence_threshold=conf_thresh_train,
                 validation_confidence_threshold=conf_thresh_val, augmentations=augmentations, nms_thresh=nms_thresh)


def evaluate_on_ds(model_output_dir: str, fpath_val_json: str, materials_dict=None, device="cpu"):
    if materials_dict is None:
        materials_dict = {0: "trash"}

    fpath_cfg = os.path.join(model_output_dir, "cfg.yaml")
    fpath_weights = os.path.join(model_output_dir, "model_final.pth")

    cfg = get_cfg()
    cfg.merge_from_file(fpath_cfg)
    cfg.MODEL.DEVICE = device
    cfg.MODEL.WEIGHTS = fpath_weights


def evaluate(fpath_model_dir: str, fpath_json_val: str, output_dir, materials_dict: dict = None,
             device: str = "cpu", filter_out_empty_imgs: bool = False, ds_name_val: str = "instances_detectron_val"):

    if materials_dict is None:
        materials_dict = {0: "trash"}

    cfg = get_cfg()
    cfg.merge_from_file(os.path.join(fpath_model_dir, "cfg.yaml"))
    cfg.MODEL.WEIGHTS = os.path.join(fpath_model_dir, "model_final.pth")
    cfg.MODEL.DEVICE = device
    cfg.OUTPUT_DIR = output_dir
    cfg.DATALOADER.FILTER_EMPTY_ANNOTATIONS = filter_out_empty_imgs

    DatasetCatalog.register(fpath_json_val, lambda: create_detectron_img_dict_list(fpath_json_val))
    MetadataCatalog.get(fpath_json_val).set(thing_classes=list(materials_dict.values()))
    cfg.DATASETS.TEST = (fpath_json_val,)

    cfg.OUTPUT_DIR = output_dir
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

    evaluator = COCOEvaluator(fpath_json_val,
                              tasks=("bbox",),
                              use_fast_impl=False,  # use a fast but unofficial implementation to compute AP
                              output_dir=output_dir)
    predictor = DefaultPredictor(cfg)

    val_loader = build_detection_test_loader(cfg, fpath_json_val)
    print(termcolor.colored("Evaluating ...", "green"))

    evaluation_results = inference_on_dataset(predictor.model, val_loader, evaluator)
    print(evaluation_results)
    print("Finished evaluation.")


if __name__ == "__main__":
    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)

    # # Evaluation
    # ds_04 = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates/"
    # ds_convert.cvt_yolo_to_detectron(ds_04)
    # model_dir = "/media/findux/DATA/Documents/Malta_II/results/5343_2022-05-10_122636/"
    # json_val = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates_detectron/annotations/instances_detectron_val.json"
    # out_dir = "/home/findux/Desktop/out/"
    # evaluate(model_dir, json_val, out_dir)

    # Run training on cluster:

    # # Augmentations & Dataset mapper
    # augmentations = [T.RandomBrightness(0.4, 1.6),
    #                  T.RandomFlip(0.5, horizontal=True, vertical=False),
    #                  T.RandomFlip(0.5, horizontal=False, vertical=True)]
    # ds_root = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_05_mini_gnejna/"
    # model = "COCO-Detection/faster_rcnn_R_50_DC5_1x.yaml"
    # eval_results = run_training(ds_root,
    #                             model,
    #                             "/home/findux/Desktop/aug_out_test/",
    #                             {0: "trash"},
    #                             augmentations=augmentations,
    #                             device="cpu",
    #                             iterations=100,
    #                             roi_heads_batch_size_per_img=128,
    #                             number_of_workers=8)

    augs = parse_augs((0.3, 1.7), 0.5, 0.5, (0, 20))
    augs = parse_augs()
    print(augs)
