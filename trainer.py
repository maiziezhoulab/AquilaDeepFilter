"""
author:Sanidhya Mangal
github:sanidhyamangal
"""
from typing import Optional
import tensorflow as tf  # for deep learning
import os  # for os related ops


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
            model.load_weights(check_point_dir)
            print(f"Loaded Weights from {check_point_dir} Sucessfully")
        model.compile(optimizer=optimizer(learning_rate=learning_rate),
                      loss=loss,
                      metrics=['accuracy'])

        _tb_callback = tf.keras.callbacks.TensorBoard(
            log_dir=tensorboard_log,
            histogram_freq=1 if validation_dataset else 0)

        _model_check_points = tf.keras.callbacks.ModelCheckpoint(
            filepath=check_point_dir, save_best_only=True)
        if validation_dataset:
            model.fit(trainer_dataset,
                      validation_data=validation_dataset,
                      epochs=epochs,
                      callbacks=[_tb_callback, _model_check_points])
        else:
            model.fit(trainer_dataset,
                      epochs=epochs,
                      callbacks=[_tb_callback, _model_check_points])
