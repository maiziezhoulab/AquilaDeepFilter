"""
author:Sanidhya Mangal
github:sanidhyamangal
"""
import os  # for os related ops
from typing import List, Optional
from utils import create_folders_if_not_exists, extract_chromosome_info, spit_string_for_result_file

import tensorflow as tf  # for deep learning


class ModelManager(tf.Module):
    """
    TF model for performing training ops
    """
    def __init__(self, name):
        super().__init__(name=name)

    def train(self,
              model: tf.keras.Model,
              loss: tf.keras.losses.Loss,
              trainer_dataset: tf.data.Dataset,
              check_point_dir: Optional[str],
              validation_dataset: Optional[tf.data.Dataset] = None,
              optimizer=tf.keras.optimizers.Adam,
              learning_rate=1e-3,
              tensorboard_log="logs",
              save_checkpoints_at: int = 0,
              epochs: int = 0):

        if os.path.exists(check_point_dir):
            model.load_weights(check_point_dir).expect_partial()
            print(f"Loaded Weights from {check_point_dir} Sucessfully")

        model.compile(optimizer=optimizer(learning_rate=learning_rate),
                      loss=loss,
                      metrics=['accuracy'])

        _tb_callback = tf.keras.callbacks.TensorBoard(
            log_dir=tensorboard_log,
            histogram_freq=1 if validation_dataset else 0)

        _model_check_points = tf.keras.callbacks.ModelCheckpoint(
            filepath=check_point_dir, save_best_only=True)

        _early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss',
                                                           patience=5)
        _reduce_lr_on_plateue = tf.keras.callbacks.ReduceLROnPlateau(
            monitor="loss", patience=5)

        if validation_dataset:
            model.fit(trainer_dataset,
                      validation_data=validation_dataset,
                      epochs=epochs,
                      callbacks=[_tb_callback, _model_check_points])
        else:
            model.fit(trainer_dataset,
                      epochs=epochs,
                      callbacks=[
                          _tb_callback, _model_check_points, _early_stopping,
                          _reduce_lr_on_plateue
                      ])

    def predict(self,
                model: tf.keras.models.Model,
                checkpoint_dir: str,
                prediction_dataset: tf.data.Dataset,
                output_file: str,
                all_file_paths=List[str]) -> None:

        # load model checkpoints
        if os.path.exists(checkpoint_dir):
            model.load_weights(checkpoint_dir).expect_partial()
            print(f"Loaded Weights from {checkpoint_dir} Sucessfully")

        model.compile(optimizer=tf.keras.optimizers.Adam(),
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(
                          from_logits=True),
                      metrics=['accuracy'])

        _output = tf.nn.softmax(model.predict(prediction_dataset), axis=1)

        create_folders_if_not_exists(output_file)

        fp = open(output_file, "w+")

        for file_path, result in zip((all_file_paths), _output):
            fp.write(
                spit_string_for_result_file(extract_chromosome_info(file_path),
                                            result))

        fp.close()
