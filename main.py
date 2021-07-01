"""
author:Sanidhya Mangal
github:sanidhyamangal
"""

import argparse
from os import path  # for argument parsing

import tensorflow as tf

from datapipeline.load_imageds import \
    LoadData  # model pipeline for loading image datasets
from models import (
    DenseNetModel,
    EfficientNetB0Model,  # models for training
    ResnetV2Model,
    VGG16Model,
    XceptionNetModel,
    MobileNetModel)
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

    parser_train = subparsers.add_parser('train',
                                         help='train the classification model')
    # parser_predict = subparsers.add_parser('predict', help='make predications for candidate SVs')
    parser_train.add_argument("--model_arch",
                              choices=[
                                  "xception", "densenet", "efficientnet",
                                  "vgg", "resnet", "mobilenet"
                              ],
                              default="xception")
    parser_train.add_argument('--epoch',
                              type=int,
                              default=2,
                              help='number of total epoches')
    parser_train.add_argument('--batch_size',
                              type=int,
                              default=64,
                              help='number of samples in one batch')
    parser_train.add_argument('--lr',
                              type=float,
                              default=0.001,
                              help='initial learning rate for adam')
    parser_train.add_argument('--path_to_train_dir',
                              required=True,
                              help='path to training dataset directory')
    parser_train.add_argument('--path_to_eval_dir',
                              required=True,
                              help='path to evaluation dataset directory')
    parser_train.add_argument(
        "--fine_tune_at",
        type=int,
        default=0,
        help="fine tune network from the layer, default to none")
    parser_train.add_argument(
        '--checkpoint_dir',
        required=True,
        help='path to directory where checkpoints needs to be saved')
    parser_train.add_argument('--tensorboard_log_dir',
                              required=True,
                              help='tensorboard summary')

    # parse the args from arg parsers
    args = parser_train.parse_args()

    # define data loader for the validation and trainer set
    train_dataset_loader = LoadData(path=args.path_to_train_dir)
    val_dataset_loader = LoadData(path=args.path_to_eval_dir)

    # retrieve and define the model for the interconnection
    model = MODEL_ARCH.get(args.model_arch, XceptionNetModel)(
        img_shape=(224, 224, 3),
        num_classes=len(train_dataset_loader.root_labels),
        fine_tune_at=args.fine_tune_at)

    # print the model arch name for the logs
    print(f"{'='*30}{args.model_arch}{'='*30}")

    # init a model manager to start the training process
    model_manager = ModelManager(name=args.model_arch)

    # prepare the training dataset for ingesting it into the model
    train_dataset = train_dataset_loader.create_dataset(
        batch_size=args.batch_size,
        autotune=AUTOTUNE,
        drop_remainder=True,
        prefetch=True,
        cache=True)

    # prepare validation dataset for the ingestion process
    validation_dataset = val_dataset_loader.create_dataset(
        batch_size=args.batch_size,
        autotune=AUTOTUNE,
        drop_remainder=True,
        prefetch=True,
        cache=True)

    # call train function for the training ops
    model_manager.train(
        model,
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        learning_rate=args.lr,
        trainer_dataset=train_dataset,
        validation_dataset=validation_dataset,
        check_point_dir=args.checkpoint_dir,
        tensorboard_log=args.tensorboard_log_dir,
        epochs=args.epoch)
