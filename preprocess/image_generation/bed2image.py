#!/home/huangyalin/software/python3.6.4/bin/python3.6
# encoding: utf-8
'''
@author: hyl
@time: 2019/12/7 15:48
@desc:
'''
import sys
import os
from glob import glob
import argparse

from deepsvfilter.sv_image import *
#from sv_image_v1 import *


def draw_pic_customized(sam_file, sv_list, mean_size, std_size, output_dir, sv_type, width, height):  # deal with the situation when width != height
    l_extend, r_extend = width//2, width-width//2
    for i in range(len(sv_list)):
        print("===processing ", i, '/', len(sv_list), "===")
        
        imgs = []
        if sv_type=="DEL":
            drp_list=getDelDRPList(sam_file, sv_list[i], width, mean_size, std_size)
            for flag_LR in [1, 2]:
                bp_position = int(sv_list[i][flag_LR])
                pic_start, pic_end = bp_position - l_extend, bp_position + r_extend
                im = draw_deletion(sam_file, sv_list[i], pic_start, pic_end, flag_LR, drp_list)
                # print(im.size)
                #imgs.append([im, im_re])
                im = im.crop((0, 0, width, height//2))
                imgs.append(im)
        if sv_type=="DUP":  # not used for now... add later
            drp_list=getTandemDupDRPList(sam_file, sv_list[i], width)
            print(len(drp_list))
            for flag_LR in [1, 2]:
                bp_position = int(sv_list[i][flag_LR])
                pic_start, pic_end = bp_position - l_extend, bp_position + r_extend
                im =draw_tandem_duplication(sam_file, sv_list[i], pic_start, pic_end, flag_LR, drp_list)
                #imgs.append([im, im_re])
                imgs.append(im)
        if sv_type=="INS":
            drp_list=getDelDRPList(sam_file, sv_list[i], width, mean_size, std_size)
            for flag_LR in [1, 2]:
                bp_position = int(sv_list[i][flag_LR])
                pic_start, pic_end = bp_position - l_extend, bp_position + r_extend
                im = draw_deletion(sam_file, sv_list[i], pic_start, pic_end, flag_LR, drp_list)
                # print(im.size)
                #imgs.append([im, im_re])
                im = im.crop((0, 0, width, height//2))
                imgs.append(im)
        left_img = imgs[0]
        # save_path = os.path.join(output_dir, "test_left.png")
        right_img = imgs[1]
        # save_path = os.path.join(output_dir, "test_right.png")
        vertical_im = Image.new('RGB', (width, height), (0, 255, 255))
        vertical_im.paste(left_img, (0, 0))
        vertical_im.paste(right_img, (0, height//2+1))
        save_path = os.path.join(output_dir, str(sv_type) + '_' + ("chr" + sv_list[i][0]) + '_' + str(sv_list[i][1]) + '_' + str(sv_list[i][2]) + '_' + str(width) + '_' + str(height) + ".png")
        vertical_im.save(save_path, "PNG")
    return

def draw_pic(sam_file, sv_list, mean_size, std_size, output_dir, sv_type, patch_size):

    l_extend, r_extend = patch_size//2, patch_size-patch_size//2
    for i in range(len(sv_list)):
        print("===processing ", i, '/', len(sv_list), "===")
        
        imgs = []
        if sv_type=="DEL":
            drp_list=getDelDRPList(sam_file, sv_list[i], patch_size, mean_size, std_size)
            for flag_LR in [1, 2]:
                bp_position = int(sv_list[i][flag_LR])
                pic_start, pic_end = bp_position - l_extend, bp_position + r_extend
                im = draw_deletion(sam_file, sv_list[i], pic_start, pic_end, flag_LR, drp_list)
                #imgs.append([im, im_re])
                imgs.append(im)
        if sv_type=="DUP":
            drp_list=getTandemDupDRPList(sam_file, sv_list[i], patch_size)
            print(len(drp_list))
            for flag_LR in [1, 2]:
                bp_position = int(sv_list[i][flag_LR])
                pic_start, pic_end = bp_position - l_extend, bp_position + r_extend
                im =draw_tandem_duplication(sam_file, sv_list[i], pic_start, pic_end, flag_LR, drp_list)
                #imgs.append([im, im_re])
                imgs.append(im)
        left_img = imgs[0]
        right_img = imgs[1]
        vertical_im = Image.new('RGB', (patch_size, patch_size), (0, 255, 255))
        vertical_im.paste(left_img, (0, 0))
        vertical_im.paste(right_img, (0, patch_size//2+1))
        save_path = output_dir + '/'+ str(sv_type) + '_' + \
                    ("chr" + sv_list[i][0]) + '_' + str(sv_list[i][1]) + '_' + str(sv_list[i][2]) + '_' + str(patch_size) + '_' + str(patch_size) + ".png"
        vertical_im.save(save_path, "PNG")
    return

def generateImgPathFile(output_dir):
    image_output_dir = os.path.join(output_dir, "image")
    image_output_dir = os.path.abspath(image_output_dir)
    img_path_list = glob(image_output_dir + '/*.png')
    file_path = os.path.join(output_dir, "IMG_PATH.txt")
    f = open(file_path, 'w')
    for path in img_path_list:
        f.write(str(path) + '\n')
    f.flush()
    f.close()
    return

def parse_bed_file(bed_path):
    f = open(bed_path, 'r')
    if not f:
        print('[!] BED Path: [' + bed_path + '] is Empty')
        exit(1)
        return
    sv_list = []
    for line in f:
        line = line.rstrip('\n')
        if len(line.split('\t')) == 1:
            record = line.split(' ')
        else:
            record = line.split('\t')
        sv_list.append((record[0], int(record[1]) + 1, int(record[2]), record[3]))
    return sv_list

def trans2img(bam_path, sv_type, bed_path, output_dir, patch_size, mean_size, std_size):
 
    sv_list = parse_bed_file(bed_path)
    #mean_size, std_size = estimateInsertSizes(bam_path, alignments=1000000)
    
    print("[*] Start generating " + sv_type + " images ===")
    image_output_dir = os.path.join(output_dir, "image")
    if not os.path.exists(image_output_dir):
        os.makedirs(image_output_dir)
    print(patch_size)
    if patch_size[0] == patch_size[1]:  # square mode
        draw_pic(bam_path, sv_list, mean_size, std_size, image_output_dir, sv_type, int(patch_size[0]))
    else:  # rectangular mode
        draw_pic_customized(bam_path, sv_list, mean_size, std_size, image_output_dir, sv_type, int(patch_size[0]), int(patch_size[1]))
    generateImgPathFile(output_dir)
    print("[*] End generating " + sv_type + " images ===")


def size(s):
    try:
        w, h = map(int, s.split(','))
        return w, h
    except:
        raise argparse.ArgumentTypeError("Image size must be w, h")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    #subparsers = parser.add_subparsers(help='preprocess, augmentate, train or predict')
    
    #parser_preprocess = subparsers.add_parser('preprocess', help='generate SV images')

    parser.add_argument('--sv_type', dest='sv_type', required=True, help='SV type')
    parser.add_argument('--bam_path', dest='bam_path', required=True, help='BAM file')
    parser.add_argument('--bed_path', dest='bed_path', required=True, help='SV BED file')
    # parser_preprocess.add_argument('--patch_size', dest='patch_size', type=int, default=224, help='image patch size (224 or 299)')
    parser.add_argument('--patch_size', dest='patch_size', type=size, default=(224,224), help='image patch size like (224, 224)')
    parser.add_argument('--output_imgs_dir', dest='output_imgs_dir', required=True, help='output image folder')
    parser.add_argument('--mean_insert_size', dest='mean_insert_size',type=int, help='mean of the insert size')
    parser.add_argument('--sd_insert_size', dest='sd_insert_size',type=int, help='standard deviation of the insert size')
    
    # parser_preprocess.set_defaults(func=preprocess)
    
    args = parser.parse_args()
    # args.func(args)
    
    if args.mean_insert_size!=None and args.sd_insert_size!=None:
        trans2img(args.bam_path, args.sv_type, args.bed_path, args.output_imgs_dir, args.patch_size, args.mean_insert_size, args.sd_insert_size)
    else:
        mean_size, std_size = estimateInsertSizes(args.bam_path, alignments=1000000)
        trans2img(args.bam_path, args.sv_type, args.bed_path, args.output_imgs_dir, args.patch_size, mean_size, std_size)