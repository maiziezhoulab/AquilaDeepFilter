"""
author:Sanidhya Mangal
github:sanidhyamangal
"""

from typing import Tuple
import tensorflow as tf  # for deep learning stuff


class BaseNetModel(tf.keras.models.Model):
    preprocess_input = None
    model_layer = None

    def _assert_is_preprocess_input_defined(self):
        assert self.preprocess_input is not None, (
            "`preprocess_input` attr not defined in the %s",
            self.__class__.__name__)

    def _assert_is_model_layer_defined(self):
        assert self.model_layer is not None, (
            "`model_layer` attr not defined in the %s",
            self.__class__.__name__)

    def __init__(self,
                 img_shape: Tuple[int],
                 num_classes: int,
                 fine_tune_at: int = 0,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        # assert required params
        self._assert_is_preprocess_input_defined()
        self._assert_is_model_layer_defined()()

        # define preprocessing arch for performing the data augmentation tasks
        _pre_model_arch = [
            tf.keras.layers.experimental.preprocessing.RandomRotation(0.2)
        ]
        # add rescaling node if the present node is not added
        _rescaling = kwargs.get('rescaling', False)
        if _rescaling:
            _pre_model_arch.append(
                tf.keras.layers.experimental.preprocessing.Rescaling(
                    1. / 127.5, offset=-1))

        # define preprocessing model right before input to the base model
        self.preprocess = tf.keras.models.Sequential(_pre_model_arch)

        # define base model for the training purpose
        self.base_model = self.model_layer(input_shape=img_shape,
                                           include_top=False,
                                           weights='imagenet')
        # freeze the base models to restrict further training
        self.base_model.trainable = False

        # check if fine tuning of model is required or not,
        # if required simply iterate it from the point
        if fine_tune_at:
            for layer in self.base_model.layers[fine_tune_at:]:
                layer.trainable = True

        # define the post base model layer to use it for specific use cases.
        self.post_base_model = tf.keras.models.Sequential([
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dropout(kwargs.get('dropout', 0.2)),
            tf.keras.layers.Dense(num_classes)
        ])

    def call(self, inputs, training, mask):
        # call to the preprocessing input unit for the model nased preprocessing
        x = self.preprocess_input(inputs)

        # preprocessing layer called for data augmentation part
        x = self.preprocess(x, training=training)
        # called base model layer the base SOTA arch for learning the cardinal cases
        x = self.base_model(x, training=training)
        # call posterior ops to the base sota model to classify the images on specific dataset
        x = self.post_base_model(x, training=training)

        # return the dataset for the
        return x


class XceptionNetModel(BaseNetModel):
    preprocess_input = tf.keras.applications.xception.preprocess_input
    model_layer = tf.keras.applications.xception.Xception
