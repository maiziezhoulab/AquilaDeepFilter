import argparse





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BED file util functions')
    #subparsers = parser.add_subparsers(help='preprocess, augmentate, train or predict')
    
    #parser_preprocess = subparsers.add_parser('preprocess', help='generate SV images')
    parser.add_argument('--bed_files', dest='output_imgs_dir', required=True,help='output image folder')
    parser.add_argument('--switch_chr', dest='image_path_file', required=True,help='input typical true or false image folder')
    # parser.add_argument('--patch_size', dest='patch_size', type=size, required=True, help='image patch size like 224,224')
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
    if args.switch_chr:
        pass