"""
author:Sanidhya Mangal
github:sanidhyamangal
"""

from pathlib import Path
import random
import os
import argparse  # for argument parsing


def move_data_randomly(base_dir: str, target_dir: str, seed: int,
                       file_extension: str) -> None:
    _path_to_files = Path(base_dir)

    _files = [
        _file for _file in _path_to_files.glob(f"*.{file_extension.lower()}")
    ]

    _get_random_images = random.sample(_files, len(_files) - seed)

    os.makedirs(target_dir, exist_ok=True)

    for _file in _get_random_images:
        NEW_NAME = os.path.join(target_dir, _file.name)
        print(f"Moving {str(_file)} ===> {NEW_NAME}")
        os.rename(_file, NEW_NAME)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Program to move files randomly from base dir to target dir"
    )

    argparser.add_argument(
        "--base_dir",
        help="path to directory from which files needs to be moved",
        required=True,
        type=str)
    argparser.add_argument(
        "--target_dir",
        help="path to directory where data needs to be moved",
        required=True,
        type=str)
    argparser.add_argument(
        "--seed",
        help=
        "The size of data set which needs to be kept in the base directory",
        required=True,
        type=int)
    argparser.add_argument(
        "--file_extension",
        help="file extension to specify which file type needs to be moved",
        required=True,
        type=str)

    args = argparser.parse_args()
    move_data_randomly(args.base_dir,
                       args.target_dir,
                       args.seed,
                       file_extension=args.file_extension)