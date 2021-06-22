"""
author:Sanidhya Mangal
github:sanidhyamangal
"""

import argparse
from os import path  # for argument parsing

import tensorflow as tf

from models import XceptionNetModel  # xception net model for performing ops
from trainer import ModelManager  # model manager for handing all the ops
from datapipeline.load_imageds import LoadData  # model pipeline for loading image datasets

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
        '--checkpoint_dir',
        required=True,
        help='path to directory where checkpoints needs to be saved')
    parser_train.add_argument('--tensorboard_log_dir',
                              required=True,
                              help='tensorboard summary')

    args = parser_train.parse_args()
    train_dataset_loader = LoadData(path=args.path_to_train_dir)
    val_dataset_loader = LoadData(path=args.path_to_eval_dir)

    model = XceptionNetModel(img_shape=(244, 244, 3),
                             num_classes=len(train_dataset_loader.root_labels))
    model_manager = ModelManager(name="Xception Net")

    train_dataset = train_dataset_loader.create_dataset(
        batch_size=args.batch_size,
        autotune=AUTOTUNE,
        drop_remainder=True,
        prefetch=True,
        cache=True)
    validation_dataset = val_dataset_loader.create_dataset(
        batch_size=args.batch_size,
        autotune=AUTOTUNE,
        drop_remainder=True,
        prefetch=True,
        cache=True)

    model_manager.train(
        model,
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        trainer_dataset=train_dataset,
        validation_dataset=validation_dataset,
        check_point_dir=args.checkpoint_dir,
        tensorboard_log=args.tensorboard_log_dir,
        epochs=args.epoch
    )
