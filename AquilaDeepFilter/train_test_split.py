from pathlib import Path
import random
import os
import argparse
import glob


def split_train_test(namespace, out_dir, ratio):

    print("project root folder path : ", out_dir)

    TRAIN_PATH = os.path.join(out_dir, 'train')
    VAL_PATH = os.path.join(out_dir, 'test')
    print("project train/val folder path : ", TRAIN_PATH, TEST_PATH)
    # exit(-1)

    if not os.path.exists(VAL_PATH):
        os.mkdir(VAL_PATH)
    
    if not os.path.exists(TRAIN_PATH):
        os.mkdir(TRAIN_PATH)
    
    sub_f = ['positive', 'negative']
    for f in sub_f:
        p = os.path.join(namespace, f)
        _images_root = os.listdir(p)
        
        temp = []
        for image in _images_root:
            temp.append(os.path.join(p, image))
            # exit(-1)
            # if not os.path.exists(os.path.join(TRAIN_PATH, image)):
            #     os.rename(str(image), os.path.join(TRAIN_PATH, image.name))
        random.shuffle(temp)
        
        train_part = temp[:int(0.8*len(temp))]
        val_part = temp[1-int(0.8*len(temp)):]
        
        cp_out_dir_train = os.path.join(TRAIN_PATH, f)
        cp_out_dir_val = os.path.join(VAL_PATH, f)

        for e in train_part:
            os.system("cp " + e + " " + cp_out_dir_train)
        for e in val_part:
            os.system("cp " + e + " " + cp_out_dir_val)


if __name__ == '__main__':
    """
    
    """
    parser = argparse.ArgumentParser(description='train/val split script')
    parser.add_argument('--ratio', required=True, help='ratio for training set')
    parser.add_argument('--output_dir', required=True, help='path to output folder with split train/val folders')
    parser.add_argument('--input_dir', required=True, help='path to folder with generated images')
    
    args = parser.parse_args()
    
    split_train_test(args.input_dir, args.output_dir, args.ratio)
