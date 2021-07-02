"""
author:Sanidhya Mangal
github:sanidhyamangal
"""

from typing import Tuple

import tensorflow as tf  # for deep learning stuff


class BaseNetModel(tf.keras.models.Model):
    """
    Base model for confining all the base logic for model arch defination and call function for overriding it. 
    """
    model_config = {
    }  # model configs to be used to overriding the base layer and preprocessing units

    def __init__(self,
                 img_shape: Tuple[int],
                 num_classes: int,
                 fine_tune_at: int = 0,
                 train_from_scratch: bool = False,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        # checker for model param types
        self._check_config_hyperparams('model_layer')
        self._check_config_hyperparams('preprocess_input')
        #TODO: remove model arch
        # define preprocessing arch for performing the data augmentation tasks
        # _pre_model_arch = [
        #     tf.keras.layers.L
        # ]

        # add rescaling node if the present node is not added
        # _rescaling = kwargs.get('rescaling', False)
        # if _rescaling:
        #     _pre_model_arch.append(
        #         tf.keras.layers.experimental.preprocessing.Rescaling(
        #             1. / 127.5, offset=-1))

        # # define preprocessing model right before input to the base model
        # self.preprocess = tf.keras.models.Sequential(_pre_model_arch)

        # define base model for the training purpose
        self.base_model = self.model_config.get('model_layer')(
            input_shape=img_shape, include_top=False, weights='imagenet')

        if not train_from_scratch:
            # freeze the base models to restrict further training
            self.base_model.trainable = False
            print("=" * 100)
            print(f"Training Entire Model from Scratch")
            print("=" * 100)

        # check if fine tuning of model is required or not,
        # if required simply iterate it from the point
        if fine_tune_at:
            print("=" * 100)
            print(f"Fine tuning model from {fine_tune_at}")
            print("=" * 100)
            for layer in self.base_model.layers[fine_tune_at:]:
                layer.trainable = True

        # define the post base model layer to use it for specific use cases.
        self.post_base_model = tf.keras.models.Sequential([
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dropout(kwargs.get('dropout', 0.2)),
            tf.keras.layers.Dense(num_classes)
        ])

        self.preprocess_input = self.model_config.get('preprocess_input')

    def _check_config_hyperparams(self,
                                  param_name: str,
                                  check_callable: bool = True) -> None:
        """
        Function to check if the hyper param is defined or not during model initialization
        """
        _model_layer = self.model_config.get(param_name, '')

        if not _model_layer:
            raise KeyError(
                f"{param_name} needs to be passed to generate a model architecture"
            )

        if not callable(_model_layer):
            raise TypeError(f"{param_name} must be a callable object")

    def call(self, inputs, training):
        # call to the preprocessing input unit for the model nased preprocessing
        x = self.preprocess_input(inputs)

        # preprocessing layer called for data augmentation part
        # x = self.preprocess(x, training=training)
        # called base model layer the base SOTA arch for learning the cardinal cases
        x = self.base_model(x, training=training)
        # call posterior ops to the base sota model to classify the images on specific dataset
        x = self.post_base_model(x, training=training)

        # return the dataset for the
        return x


class XceptionNetModel(BaseNetModel):
    model_config = {
        'model_layer': tf.keras.applications.Xception,
        'preprocess_input': tf.keras.applications.xception.preprocess_input
    }


class ResnetV2Model(BaseNetModel):
    model_config = {
        "model_layer": tf.keras.applications.ResNet152V2,
        "preprocess_input": tf.keras.applications.resnet_v2.preprocess_input
    }


class DenseNetModel(BaseNetModel):
    model_config = {
        "model_layer": tf.keras.applications.DenseNet121,
        "preprocess_input": tf.keras.applications.densenet.preprocess_input
    }


class VGG16Model(BaseNetModel):
    model_config = {
        "model_layer": tf.keras.applications.VGG16,
        "preprocess_input": tf.keras.applications.vgg16.preprocess_input
    }


class EfficientNetB0Model(BaseNetModel):
    model_config = {
        "model_layer": tf.keras.applications.EfficientNetB0,
        "preprocess_input": tf.keras.applications.efficientnet.preprocess_input
    }


class MobileNetModel(BaseNetModel):
    model_config = {
        "model_layer": tf.keras.applications.MobileNetV2,
        "preprocess_input": tf.keras.applications.mobilenet.preprocess_input
    }
