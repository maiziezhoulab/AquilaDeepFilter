"""
author:Sanidhya Mangal
github:sanidhyamangal
"""
import os  # for os related ops
from typing import List


def create_folders_if_not_exists(path: str) -> None:
    if not os.path.exists(path):
        _path = path.split("/")[:-1]
        if path.startswith("/"):
            _path[0] = "/"

        os.makedirs(os.path.join(*_path), exist_ok=True)


def extract_chromosome_info(path: str) -> List[str]:
    _path_list = path.split("/")[-1].rstrip(".png").split("_")
    return _path_list[:4]


def spit_string_for_result_file(chr_array: List[str],
                                eval_array: List[float]) -> str:
    return f"{chr_array[1]}\t{chr_array[2]}\t{chr_array[3]}\t{chr_array[0]}\t{float(eval_array[0])}\n"
