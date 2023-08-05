#!/usr/bin/env python3
import datetime

import argparse
import logging
from typing import Tuple
from bioblu.detectron import detectron
from detectron2.data import transforms as T


def main(ds_yolo, model_yaml, iterations, batch_size, base_lr, lr_decay, conf_thresh_train, conf_thresh_val, augs):
    detectron.run_training_on_cluster(dataset_dir=ds_yolo, model_yaml=model_yaml, iterations=iterations,
                                      batch_size=batch_size, base_lr=base_lr, lr_decay=lr_decay,
                                      conf_thresh_train=conf_thresh_train, conf_thresh_val=conf_thresh_val,
                                      augmentations=augs,
                                      )


if __name__ == "__main__":
    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    # logging.disable

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--ds-dir", help="Path to the yolo-styled dataset root folder.", type=str, default=None)
    parser.add_argument("-m", "--model-yaml", help="Path to the model yaml.", type=str, default=None)
    parser.add_argument("-i", "--iterations", help="NUmber of iterations.", type=int, default=10_000)
    parser.add_argument("-b", "--batch-size", help="ROI heads batch size per image")
    parser.add_argument("-lr", "--learning-rate", help="Learning rate.", type=float, default=0.00025)
    parser.add_argument("-ld", "--learning-rate-decay", help="Learning rate decay.", default=None)
    parser.add_argument("-ct", "--conf-train", help="Confidence threshold for training")
    parser.add_argument("-cv", "--conf-val", help="Confidence threshold for validation")
    # ToDo: Complete this
    parser.parse_args()

    ds_yolo = "/opt/nfs/shared/scratch/bioblu/datasets/dataset_01"
    output = "/opt/nfs/shared/scratch/bioblu/output"
    model = "COCO-Detection/faster_rcnn_R_101_C4_3x.yaml"
    # model = "COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"
    iterations = 5000
    base_lr = 0.00025
    conf_thresh_train = 0.2
    conf_thresh_val = 0.8
    batch_size = 64

    augmentations = [T.RandomBrightness(0.4, 1.6),
                     T.RandomFlip(0.5, horizontal=True, vertical=False),
                     T.RandomFlip(0.5, horizontal=False, vertical=True),
                     T.RandomRotation([0, 20])]
    augmentations = [T.RandomBrightness(0.4, 1.6),
                     T.RandomFlip(0.5, horizontal=True, vertical=False),
                     T.RandomFlip(0.5, horizontal=False, vertical=True),
                     T.RandomRotation([0, 20])]

    detectron.run_training_on_cluster(dataset_dir=ds_yolo, model_yaml=model, iterations=iterations,
                                      batch_size=batch_size, base_lr=base_lr,
                                      conf_thresh_train=conf_thresh_train, conf_thresh_val=conf_thresh_val,
                                      augmentations=augmentations,
                                      )

