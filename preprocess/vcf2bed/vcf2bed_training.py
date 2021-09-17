import os

import argparse



def get_dels_in_bed_format(original_format):
    """
    original_format = [chr index, start coord, ref seq, alt seq]
    """
    if len(original_format[2]) <= len(original_format[3]):
        print("double check the inputs, ref seq shoule be longer in deletions")
        exit(-1)
    end = int(original_format[1]) + len(original_format[2]) - len(original_format[3])
    length = len(original_format[2]) - len(original_format[3])
    return [original_format[0], original_format[1], str(end), 'DEL', length]
    

def get_inss_in_bed_format(original_format):
    """
    original_format = [chr index, start coord, ref seq, alt seq]
    """
    if len(original_format[2]) >= len(original_format[3]):
        print("double check the inputs, ref seq shoule be shorter in insertions")
        exit(-1)
    length = len(original_format[3]) - len(original_format[2])
    return [original_format[0], original_format[1], original_format[1], 'INS', length]


def generating_bed_for_training(vcf_folder, SV, output_folder):
    vcf_file_fp = os.path.join(vcf_folder, "fp.vcf")
    vcf_file_fn = os.path.join(vcf_folder, "fn.vcf")  # '/data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/Aquila_VCF_reformat/N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50bp_up_ins/fn.vcf'
    vcf_file_tp_base = os.path.join(vcf_folder, "tp-base.vcf")  # '/data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/Aquila_VCF_reformat/N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50bp_up_ins/tp-base.vcf'
    
    f = open(vcf_file_fp, 'r')
    lines = f.readlines()
    f.close()
    
    del_count = 0
    ins_count = 0
    snp_count = 0
    total_count = 0
    dels = []
    dels_index = []
    index_ = 0
    inss = []
    for line in lines:
        if line.startswith('#'):
            index_ += 1
            continue
        total_count += 1
        split_line = line.split()
        reserve_ = (split_line[0], split_line[1], split_line[3], split_line[4])
        if len(reserve_[2]) > len(reserve_[3]):
            del_count += 1
            dels_index.append(index_)
            dels.append(get_dels_in_bed_format(reserve_))
        elif len(reserve_[2]) < len(reserve_[3]):
            ins_count += 1
            inss.append(get_inss_in_bed_format(reserve_))
        elif len(reserve_[2]) == len(reserve_[3]):
            snp_count += 1
        index_ += 1
    print("in truvari fp file:")
    print(del_count, ins_count, snp_count, total_count)
    
    
    if SV == 'INS':
        out_file_ins1 = open(os.path.join(output_folder, vcf_folder.split('/')[-2] + "_ins_negative.bed"), 'w')
        #########
        # mapping back to vcf file for truvari eval.
        #########
        # out_file_del_index = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/10xweb_NA24385_deletion_low_conf_index.txt', 'w')
        
        index_ = 0
        for line in inss:
            if line[-1] >= 50:
                out_file_ins1.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
                # out_file_del_index.write(str(dels_index[index_]) + '\n')
            index_ += 1
        # index_ = 0
        out_file_ins1.close()
    elif SV == 'DEL':
        out_file_del1 = open(os.path.join(output_folder, vcf_folder.split('/')[-2] + "_del_negative.bed"), 'w')
        # out_file_del1 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/NA24385_illumina_shortreads/NA24385_illumina_shortreads_deletion_low_conf.bed', 'w')
        #########
        # mapping back to vcf file for truvari eval.
        #########
        # out_file_del_index = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/10xweb_NA24385_deletion_low_conf_index.txt', 'w')
        
        index_ = 0
        for line in dels:
            if line[-1] >= 50:
                out_file_del1.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
                # out_file_del_index.write(str(dels_index[index_]) + '\n')
            index_ += 1
        # index_ = 0
        out_file_del1.close()
    else:
        print("run parameter for SV!")
    
    
    
    
    
    
    f = open(vcf_file_fn, 'r')
    lines = f.readlines()
    f.close()
    
    del_count = 0
    ins_count = 0
    snp_count = 0
    total_count = 0
    dels = []
    dels_index = []
    index_ = 0
    inss = []
    for line in lines:
        if line.startswith('#'):
            index_ += 1
            continue
        total_count += 1
        split_line = line.split()
        reserve_ = (split_line[0], split_line[1], split_line[3], split_line[4])
        if len(reserve_[2]) > len(reserve_[3]):
            del_count += 1
            # dels_index.append(index_)
            dels.append(get_dels_in_bed_format(reserve_))
        elif len(reserve_[2]) < len(reserve_[3]):
            ins_count += 1
            inss.append(get_inss_in_bed_format(reserve_))
        elif len(reserve_[2]) == len(reserve_[3]):
            snp_count += 1
        index_ += 1
    print("in truvari fn file:")
    print(del_count, ins_count, snp_count, total_count)
    
    f = open(vcf_file_tp_base, 'r')
    lines = f.readlines()
    f.close()
    
    del_count = 0
    ins_count = 0
    snp_count = 0
    total_count = 0
    dels2 = []
    dels_index2 = []
    index_2 = 0
    inss2 = []
    for line in lines:
        if line.startswith('#'):
            index_2 += 1
            continue
        total_count += 1
        split_line = line.split()
        reserve_ = (split_line[0], split_line[1], split_line[3], split_line[4])
        if len(reserve_[2]) > len(reserve_[3]):
            del_count += 1
            dels_index2.append(index_2)
            dels2.append(get_dels_in_bed_format(reserve_))
        elif len(reserve_[2]) < len(reserve_[3]):
            ins_count += 1
            inss2.append(get_inss_in_bed_format(reserve_))
        elif len(reserve_[2]) == len(reserve_[3]):
            snp_count += 1
        index_2 += 1
    print("in truvari tp file:")
    print(del_count, ins_count, snp_count, total_count)
    
    use = 0
    for del_ in dels:
        if del_[-1] >= 50:
            use += 1
            # print(del_)
    print(use)
    # out_file_ins = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/HG002_SVs_Tier1_v0.6_chr21_ins.bed', 'w')
    # out_file_del = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/HG002_SVs_Tier1_v0.6_chr21_del.bed', 'w')
    # Aquila_final_sorted_reformat_sorted_del_add_header.vcf
    # out_file_ins = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/Aquila_final_sorted_reformat_sorted_del_add_header_ins_test.bed', 'w')
    # out_file_del1 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/stLFR/10xweb_NA24385_deletion_GT1.bed', 'w')
    # out_file_del2 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/stLFR/10xweb_NA24385_deletion_GT2.bed', 'w')
    
    # # mapping back to vcf file for truvari eval.
    # #########
    # # out_file_del_index = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/Aquila_final_sorted_reformat_sorted_del_add_header_del_mapping_to_vcf_test.txt', 'w')
    
    # index_ = 0
    # for line in dels:
    #     if line[-1] >= 50:
    #         out_file_del1.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
    #         # out_file_del_index.write(str(dels_index[index_]) + '\n')
    #     index_ += 1
    # index_ = 0
    # for line in dels2:
    #     if line[-1] >= 50:
    #         out_file_del2.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
    #         # out_file_del_index.write(str(dels_index2[index_]) + '\n')
    #     index_ += 1
    # # for line in inss:
    # #     out_file_ins.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
    # # out_file_ins.close()
    # out_file_del1.close()
    # out_file_del2.close()
    
    
    
    
    
    
    
    
    if SV == 'INS':
        out_file_ins1 = open(os.path.join(output_folder, vcf_folder.split('/')[-2] + "_ins_positive1.bed"), 'w')
        out_file_ins2 = open(os.path.join(output_folder, vcf_folder.split('/')[-2] + "_ins_positive2.bed"), 'w')
        # out_file_ins1 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb/10xweb_NA24385_insertion_GT1.bed', 'w')
        # out_file_ins2 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb/10xweb_NA24385_insertion_GT2.bed', 'w')
        #########
        
        index_ = 0
        for line in inss:
            if line[-1] >= 50:
                out_file_ins1.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
                # out_file_del_index.write(str(dels_index[index_]) + '\n')
            index_ += 1
        index_ = 0
        for line in inss2:
            if line[-1] >= 50:
                out_file_ins2.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
                # out_file_del_index.write(str(dels_index2[index_]) + '\n')
            index_ += 1
        # for line in inss:
        #     out_file_ins.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
        # out_file_ins.close()
        out_file_ins1.close()
        out_file_ins2.close()
    elif SV == 'DEL':
        print(vcf_folder)
        print(vcf_folder.split('/'))
        out_file_del1 = open(os.path.join(output_folder, vcf_folder.split('/')[-2] + "_del_positive1.bed"), 'w')
        out_file_del2 = open(os.path.join(output_folder, vcf_folder.split('/')[-2] + "_del_positive2.bed"), 'w')
        # out_file_ins1 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb/10xweb_NA24385_insertion_GT1.bed', 'w')
        # out_file_ins2 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb/10xweb_NA24385_insertion_GT2.bed', 'w')
        #########
        
        index_ = 0
        for line in dels:
            if line[-1] >= 50:
                out_file_del1.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
                # out_file_del_index.write(str(dels_index[index_]) + '\n')
            index_ += 1
        index_ = 0
        for line in dels2:
            if line[-1] >= 50:
                out_file_del2.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
                # out_file_del_index.write(str(dels_index2[index_]) + '\n')
            index_ += 1
        # for line in inss:
        #     out_file_ins.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
        # out_file_ins.close()
        out_file_del1.close()
        out_file_del2.close()
    else:
        print("run parameter for SV!")







if __name__ == '__main__':
    """
    python vcf2bed_training.py --vcf_dir /data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/delly_call_HG002hs37d5_60x_del_50/ --output_folder /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/HG002_60x_shortreads/ --SV_type DEL
    python vcf2bed_training.py --vcf_dir /data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/delly_call_NA24385_illumina_hg19_del_50/ --output_folder /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/NA24385_illumina_shortreads/ --SV_type DEL
    """
    parser = argparse.ArgumentParser(description='convert truvari vcfs to training .bed files')
    #subparsers = parser.add_subparsers(help='preprocess, augmentate, train or predict')
    
    #parser_preprocess = subparsers.add_parser('preprocess', help='generate SV images')
    parser.add_argument('--vcf_dir', dest='vcf_dir', required=True, help='path of folder for vcf input')
    parser.add_argument('--output_folder',
                              required=True,
                              help='path to output folder')
    parser.add_argument('--SV_type',
                              type=str,
                              required=True,
                              help='DEL, INS')
    # parser.add_argument('--mode', dest='mode', default='train', help='generating bed files for training or validation?')
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
    generating_bed_for_training(args.vcf_dir, args.SV_type, args.output_folder)
    # args.func(args)
    
    # if args.mean_insert_size!=None and args.sd_insert_size!=None:
    #     trans2img(args.bam_path, args.sv_type, args.bed_path, args.output_imgs_dir, args.patch_size, args.mean_insert_size, args.sd_insert_size)
    # else:
    #     mean_size, std_size = estimateInsertSizes(args.bam_path, alignments=1000000)
    #     trans2img(args.bam_path, args.sv_type, args.bed_path, args.output_imgs_dir, args.patch_size, mean_size, std_size)
    # image_path_file='/data/maiziezhou_lab/huyf/DeepSVFilter_new/example/result/images/IMG_PATH.txt'
    # output_imgs_dir='/data/maiziezhou_lab/huyf/DeepSVFilter_new/example/result/images/test'
    # if args.mode == 'train':
    #     generating_bed_for_training(args.vcf_dir)
    # else:
    #     generating_bed_for_validation(args.vcf_dir)