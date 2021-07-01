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
    parser_predict = subparsers.add_parser(
        'predict', help='make predications for candidate SVs')

    # arguments for predict section
    parser_predict.add_argument("--model_arch",
                                choices=[
                                    "xception", "densenet", "efficientnet",
                                    "vgg", "resnet", "mobilenet"
                                ],
                                default="xception")
    parser_predict.add_argument('--batch_size',
                                type=int,
                                default=64,
                                help='number of samples in one batch')
    parser_predict.add_argument('--path_to_images',
                                required=True,
                                help='path to prediction images directory')
    parser_predict.add_argument(
        '--output_file',
        required=True,
        help='path where output file needs to be saved')

    parser_predict.add_argument(
        '--checkpoint_dir',
        required=True,
        help='path to directory from which checkpoints needs to be loaded')

    parser_predict.add_argument(
        '--num_classes',
        help='number of classes to pick prediction from',
        default=2,
        type=int)

    # parse the args from arg parsers
    args = parser_predict.parse_args()
    prediction_data_loader = PredictionDataLoader(path=args.path_to_images)
    prediction_ds = prediction_data_loader.create_dataset(args.batch_size,
                                                          autotune=AUTOTUNE,
                                                          cache=True,
                                                          prefetch=True)

    # retrieve and define the model for the interconnection
    model = MODEL_ARCH.get(args.model_arch,
                           XceptionNetModel)(img_shape=(224, 224, 3),
                                             num_classes=args.num_classes)

    # print the model arch name for the logs
    print(f"{'='*30}{args.model_arch}{'='*30}")

    # init a model manager to start the training process
    model_manager = ModelManager(name=args.model_arch)
    model_manager.predict(
        model,
        checkpoint_dir=args.checkpoint_dir,
        prediction_dataset=prediction_ds,
        output_file=args.output_file,
        all_file_paths=prediction_data_loader.all_images_path)
