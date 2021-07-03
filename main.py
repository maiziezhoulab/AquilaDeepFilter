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


def train_model(model_arch: str, epoch: str, batch_size: int, lr: float,
                path_to_train_dir: str, path_to_eval_dir: str,
                train_from_scratch: str, fine_tune_at: int,
                checkpoint_dir: str, tensorboard_log_dir: str) -> None:
    """
    Helper function for train arg subparser to train the entire network
    """
    # define data loader for the validation and trainer set
    train_dataset_loader = LoadData(path=path_to_train_dir)
    val_dataset_loader = LoadData(path=path_to_eval_dir)

    # retrieve and define the model for the interconnection
    model = MODEL_ARCH.get(model_arch, XceptionNetModel)(
        img_shape=(224, 224, 3),
        num_classes=len(train_dataset_loader.root_labels),
        fine_tune_at=fine_tune_at,
        train_from_scratch=train_from_scratch)

    # print the model arch name for the logs
    print(f"{'='*30}{model_arch}{'='*30}")

    # init a model manager to start the training process
    model_manager = ModelManager(name=model_arch)

    # prepare the training dataset for ingesting it into the model
    train_dataset = train_dataset_loader.create_dataset(batch_size=batch_size,
                                                        autotune=AUTOTUNE,
                                                        drop_remainder=True,
                                                        prefetch=True,
                                                        cache=True)

    # prepare validation dataset for the ingestion process
    validation_dataset = val_dataset_loader.create_dataset(
        batch_size=batch_size,
        autotune=AUTOTUNE,
        drop_remainder=True,
        prefetch=True,
        cache=True)

    # call train function for the training ops
    model_manager.train(
        model,
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        learning_rate=lr,
        trainer_dataset=train_dataset,
        validation_dataset=validation_dataset,
        check_point_dir=checkpoint_dir,
        tensorboard_log=tensorboard_log_dir,
        epochs=epoch)


def predict_run(model_arch: str, batch_size: int, path_to_images: str,
                output_file: str, checkpoint_dir: str,
                num_classes: int) -> None:
    """Runner function for runing the prediction ops for generating prediction files for sv data"""

    prediction_data_loader = PredictionDataLoader(path=path_to_images)
    prediction_ds = prediction_data_loader.create_dataset(batch_size,
                                                          autotune=AUTOTUNE,
                                                          cache=True,
                                                          prefetch=True)

    # retrieve and define the model for the interconnection
    model = MODEL_ARCH.get(model_arch,
                           XceptionNetModel)(img_shape=(224, 224, 3),
                                             num_classes=num_classes)

    # print the model arch name for the logs
    print(f"{'='*30}{model_arch}{'='*30}")

    # init a model manager to start the training process
    model_manager = ModelManager(name=model_arch)
    model_manager.predict(
        model,
        checkpoint_dir=checkpoint_dir,
        prediction_dataset=prediction_ds,
        output_file=output_file,
        all_file_paths=prediction_data_loader.all_images_path)


if __name__ == "__main__":
    AUTOTUNE = tf.data.AUTOTUNE
    parser = argparse.ArgumentParser(
        description=
        "Script to train and predict the sv images using Xception models")
    subparsers = parser.add_subparsers(
        help='preprocess, augmentate, train or predict')

    parser_train = subparsers.add_parser('train',
                                         help='train the classification model')
    parser_predict = subparsers.add_parser(
        'predict', help='make predications for candidate SVs')

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
    parser_train.add_argument('--train_from_scratch',
                              type=bool,
                              default=False,
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

    parser_train.set_defaults(func=train_model)

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

    parser_predict.set_defaults(func=predict_run)
