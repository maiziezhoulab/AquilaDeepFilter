"""
author:Sanidhya Mangal
github:sanidhyamangal
"""

import argparse
from os import path  # for argument parsing

import tensorflow as tf

from datapipeline.load_imageds import (  # model pipeline for loading image datasets
    LoadData, PredictionDataLoader)
from models import EfficientNetB0Model  # models for training
from models import (DenseNetModel, MobileNetModel, ResnetV2Model, VGG16Model,
                    XceptionNetModel)
from trainer import ModelManager  # model manager for handing all the ops

MODEL_ARCH = {
    "xception": XceptionNetModel,
    "densenet": DenseNetModel,
    "vgg": VGG16Model,
    "efficientnet": EfficientNetB0Model,
    "resnet": ResnetV2Model,
    "mobilenet": MobileNetModel
}

if __name__ == "__main__":
    AUTOTUNE = tf.data.AUTOTUNE
    parser = argparse.ArgumentParser(
        description=
        "Script to train and predict the sv images using Xception models")
    subparsers = parser.add_subparsers(
        help='preprocess, augmentate, train or predict')

    # parser_train = subparsers.add_parser('train',
    #                                      help='train the classification model')

    # parse the args from arg parsers
    # args = parser_predict.parse_args()
