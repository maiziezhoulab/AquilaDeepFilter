import os
from PIL import Image
import argparse

def data_augmentation(image_path_file,patch_size,output_imgs_dir):
    
    if not os.path.exists(output_imgs_dir):
        os.makedirs(output_imgs_dir)
    image_output_dir = os.path.join(output_imgs_dir, "image")
    image_output_dir = os.path.abspath(image_output_dir)
    if not os.path.exists(image_output_dir):
        os.makedirs(image_output_dir)
    
    file_path = os.path.join(output_imgs_dir, "IMG_PATH.txt")

    image_path_file_reader = open(image_path_file, 'r')
    image_path_list = [line.rstrip('\n') for line in image_path_file_reader]
    
    f = open(file_path, 'w')
    for image_path in image_path_list:
        im = Image.open(image_path)
        left_image=im.crop((0,0,patch_size,patch_size//2))
        right_image=im.crop((0,patch_size//2+1,patch_size, patch_size))
        vertical_im = Image.new('RGB', (patch_size, patch_size), (0, 255, 255))
        vertical_im.paste(right_image.transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
        vertical_im.paste(left_image.transpose(Image.FLIP_LEFT_RIGHT), (0, patch_size//2+1))
        
        raw_file_name=os.path.basename(image_path)
        new_file_name=raw_file_name[0:-4]+'_DA'+raw_file_name[-4:]
 
        save_path = os.path.join(image_output_dir, new_file_name)
        vertical_im.save(save_path, "PNG")
        f.write(str(save_path) + '\n')
    f.close()


def data_augmentation_rectangular(image_path_file,patch_size,output_imgs_dir):
    width = patch_size[0]
    height = patch_size[1]
    
    if not os.path.exists(output_imgs_dir):
        os.makedirs(output_imgs_dir)
    image_output_dir = os.path.join(output_imgs_dir, "image")
    image_output_dir = os.path.abspath(image_output_dir)
    if not os.path.exists(image_output_dir):
        os.makedirs(image_output_dir)
    
    file_path = os.path.join(output_imgs_dir, "IMG_PATH.txt")

    image_path_file_reader = open(image_path_file, 'r')
    image_path_list = [line.rstrip('\n') for line in image_path_file_reader]
    
    f = open(file_path, 'w')
    for image_path in image_path_list:
        im = Image.open(image_path)
        print(im.size)
        left_image=im.crop((0,0,width,height//2))
        right_image=im.crop((0,height//2+1,width, height))
        vertical_im = Image.new('RGB', (width, height), (0, 255, 255))
        vertical_im.paste(right_image.transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
        vertical_im.paste(left_image.transpose(Image.FLIP_LEFT_RIGHT), (0, height//2+1))
        
        raw_file_name=os.path.basename(image_path)
        new_file_name=raw_file_name[0:-4]+'_DA'+raw_file_name[-4:]
 
        save_path = os.path.join(image_output_dir, new_file_name)
        vertical_im.save(save_path, "PNG")
        f.write(str(save_path) + '\n')
    f.close()


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
    parser.add_argument('--output_imgs_dir', dest='output_imgs_dir', required=True,help='output image folder')
    parser.add_argument('--image_path_file', dest='image_path_file', required=True,help='input typical true or false image folder')
    parser.add_argument('--patch_size', dest='patch_size', type=size, required=True, help='image patch size like 224,224')
    # parser.add_argument('--sv_type', dest='sv_type', required=True, help='SV type')
    # parser.add_argument('--bam_path', dest='bam_path', required=True, help='BAM file')
    # parser.add_argument('--bed_path', dest='bed_path', required=True, help='SV BED file')
    # # parser_preprocess.add_argument('--patch_size', dest='patch_size', type=int, default=224, help='image patch size (224 or 299)')
    # parser.add_argument('--patch_size', dest='patch_size', type=size, default=224,224, help='image patch size like (224, 224)')
    # parser.add_argument('--output_imgs_dir', dest='output_imgs_dir', required=True, help='output image folder')
    # parser.add_argument('--mean_insert_size', dest='mean_insert_size',type=int, help='mean of the insert size')
    # parser.add_argument('--sd_insert_size', dest='sd_insert_size',type=int, help='standard deviation of the insert size')
    
    # parser_preprocess.set_defaults(func=preprocess)
    
    args = parser.parse_args()
    # args.func(args)
    
    # if args.mean_insert_size!=None and args.sd_insert_size!=None:
    #     trans2img(args.bam_path, args.sv_type, args.bed_path, args.output_imgs_dir, args.patch_size, args.mean_insert_size, args.sd_insert_size)
    # else:
    #     mean_size, std_size = estimateInsertSizes(args.bam_path, alignments=1000000)
    #     trans2img(args.bam_path, args.sv_type, args.bed_path, args.output_imgs_dir, args.patch_size, mean_size, std_size)
    # image_path_file='/data/maiziezhou_lab/huyf/DeepSVFilter_new/example/result/images/IMG_PATH.txt'
    # output_imgs_dir='/data/maiziezhou_lab/huyf/DeepSVFilter_new/example/result/images/test'
    if args.patch_size[0] == args.patch_size[1]:
        data_augmentation(args.image_path_file,args.patch_size[0],args.output_imgs_dir)
    else:
        data_augmentation_rectangular(args.image_path_file,args.patch_size,args.output_imgs_dir)

