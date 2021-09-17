import os
import argparse
import gzip
from pathlib import Path


# DEL
# parser.add_argument('--fasta',
#                               type=str,
#                               default='/data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa',
#                               help='path to training dataset directory')
# parser.add_argument('--include_bed',
#                               type=str,
#                               default='/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/HG002_SVs_Tier1_v0.6_chr_removechrY.bed',
#                               help='path to training dataset directory')
# parser.add_argument('--minimum',
#                               type=int,
#                               default=50,
#                               help='truvari param min')
# parser.add_argument('--maximum',
#                               type=int,
#                               default=0,
#                               help='truvari param max')
# args = parser.parse_args()

##########################
# insertions & deletions #
##########################


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
    
#######################
#   vcf or vcf.gz
#######################
#bam_file_path = "/data/maiziezhou_lab/Datasets/stLFR_data/NA24385_giab/NA24385_stlfr_giab_hg19_chr21.bam"

#vcf_file = "/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/Aquila_final_sorted_reformat_sorted_del_add_header.vcf"
#f = open(vcf_file, 'r')
#lines = f.readlines()
#f.close()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert .vcf file to .bed format')
    parser.add_argument('--path_to_vcf',
                                  required=True,
                                  help='path to vcf file')
    # '/data/maiziezhou_lab/Datasets/stLFR_data/NA24385_giab/Aquila_stLFR_VCF_reformat/Aquila_final_sorted_reformat_sorted_del.vcf.gz'
    # '/data/maiziezhou_lab/Datasets/L5_NA24385_10x/Aquila_VCF_reformat/Aquila_final_sorted_reformat_sorted_del.vcf.gz'
    # '/data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/Aquila_VCF_reformat/Aquila_final_sorted_reformat_sorted_del.vcf.gz'
    parser.add_argument('--path_to_output_folder',
                                  required=True,
                                  help='path to output folder')
    # '/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/stLFR_raw/'
    # '/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/L5_raw/'
    # '/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb_raw/'
    parser.add_argument('--SV_type',
                                  type=str,
                                  required=True,
                                  # default='/data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf.gz',
                                  help='DEL, INS')
    args = parser.parse_args()
    lines = []
    root_out_dir = args.path_to_output_folder
    vcf_file_gz = args.path_to_vcf
    if vcf_file_gz.endswith('.gz'):
        print('gz mode')
        with gzip.open(vcf_file_gz, 'r') as fin:        
            for line in fin:
                # print(str(line, 'UTF-8'))
                lines.append(str(line, 'UTF-8'))
    else:
        print('txt mode')
        with open(vcf_file_gz, 'r') as fin:        
            for line in fin:        
                lines.append(line)
    print(line[0], line[10])
    if args.SV_type == 'DEL' or args.SV_type == 'INS':
        snp_count = 0
        total_count = 0
        index_ = 0
        del_count = 0
        dels = []
        dels_index = []
        ins_count = 0
        inss_index = []
        
        inss = []
        if args.SV_type == 'DEL':
            
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
                    inss_index.append(index_)
                    inss.append(get_inss_in_bed_format(reserve_))
                elif len(reserve_[2]) == len(reserve_[3]):
                    snp_count += 1
                index_ += 1
            print(del_count, ins_count, snp_count, total_count)
            out_file_del = open(os.path.join(root_out_dir, 'raw_deletion_50.bed'), 'w')
            out_file_del_index = open(os.path.join(root_out_dir, 'deletion_mapping_index.txt'), 'w')
            index_ = 0
            for line in dels:
                if line[-1] >= 50:
                    out_file_del.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
                    out_file_del_index.write(str(dels_index[index_]) + '\n')
                index_ += 1
            out_file_del.close()
            out_file_del_index.close()
        if args.SV_type == 'INS':
            
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
                    inss_index.append(index_)
                    inss.append(get_inss_in_bed_format(reserve_))
                elif len(reserve_[2]) == len(reserve_[3]):
                    snp_count += 1
                index_ += 1
            print(del_count, ins_count, snp_count, total_count)
            out_file_ins = open(os.path.join(root_out_dir, 'raw_insertion_50.bed'), 'w')
            out_file_ins_index = open(os.path.join(root_out_dir, 'insertion_mapping_index.txt'), 'w')
            index_ = 0
            for line in inss:
                if line[-1] >= 50:
                    out_file_ins.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
                    out_file_ins_index.write(str(inss_index[index_]) + '\n')
                index_ += 1
            out_file_ins.close()
        
            out_file_ins_index.close()
    elif args.SV_type == 'DUP':
        # TODO
        # os.system("cp " + args.path_to_vcf + " " + args.path_to_output_folder)
        # os.system("gzip -d " + os.path.join(args.path_to_output_folder, args.path_to_vcf.split('/')[-1]))
        # os.system("python /data/maiziezhou_lab/huyf/DeepSVFilter_new/deepsvfilter/vcf2bed --sv_type " + args.SV_type + " --vcf_file " +  + "")
        print("no DUP in vcf for now")
    else:
        print("param wrong!")