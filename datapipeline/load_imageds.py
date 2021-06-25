"""
author: Sanidhya Mangal
github: sanidhyamangal
"""

# import random
import random
# import path for path functions
from pathlib import Path
from typing import Optional, Tuple

# import tensorflow
import tensorflow as tf


class LoadData(object):
    """
    A data loader class for loading images from the respective dirs
    """

    # constructor for loading data path
    def __init__(self, path, image_shape: Tuple[int] = (244, 244)):

        # load root path
        self.path_to_dir = Path(path)
        self.image_shape = image_shape
        self.all_images_labels = self.load_labels()

    def load_labels(self):

        # path to all the images in list of str
        self.all_images_path = [
            str(path) for path in self.path_to_dir.glob("*/*")
        ]

        # shuffle the images to add variance
        random.shuffle(self.all_images_path)

        # get the list of all the dirs
        all_root_labels = [
            str(path.name) for path in self.path_to_dir.glob("*")
            if path.is_dir()
        ]

        # design the dict of the labels
        self.root_labels = dict((c, i) for i, c in enumerate(all_root_labels))

        # add the labels for all the images
        all_images_labels = [
            self.root_labels[Path(image).parent.name]
            for image in self.all_images_path
        ]

        return all_images_labels

    # function to make process the images
    def process_image(self, image_path):
        # read image into a raw format
        raw_image = tf.io.read_file(image_path)
        # decode the image
        decode_image = tf.image.decode_png(raw_image, channels=3)

        # return the resized images
        return tf.image.resize(decode_image, self.image_shape)

    def create_dataset(self,
                       batch_size: int,
                       shuffle: bool = True,
                       autotune: Optional[int] = None,
                       drop_remainder: bool = False,
                       **kwargs):

        cache = kwargs.pop('cache', False)
        prefetch = kwargs.pop('prefetch', False)

        # make a dataset for the labels
        labels_dataset = tf.data.Dataset.from_tensor_slices(
            self.all_images_labels)

        # develop an image dataset
        image_dataset = tf.data.Dataset.from_tensor_slices(
            self.all_images_path)

        # process the image dataset
        image_dataset = image_dataset.map(self.process_image,
                                          num_parallel_calls=autotune)

        # combine and zip the dataset
        ds = tf.data.Dataset.zip((image_dataset, labels_dataset))

        # shuffle the dataset if present
        if shuffle:
            ds = ds.shuffle(len(self.all_images_labels))

        # create a batch of dataset
        ds = ds.batch(batch_size, drop_remainder=drop_remainder)

        # check if cache is enabled or not
        if cache:
            ds = ds.cache()

        # check if prefetch is specified or not
        if prefetch:
            ds = ds.prefetch(prefetch)

        return ds
