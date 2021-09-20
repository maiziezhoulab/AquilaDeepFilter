import os
import argparse
from pathlib import Path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='evaluate with Truvari')
    parser.add_argument('--path_to_folder_with_gradiant_vcf',
                        required=True,
                        help='path to training dataset directory')
    parser.add_argument('--path_to_output_folder',
                        required=True,
                        help='path to training dataset directory')
    parser.add_argument('--vcf_bench',
                        type=str,
                        default='/data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf.gz',
                        help='path to training dataset directory')
    parser.add_argument('--fasta',
                        type=str,
                        default='/data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa',
                        help='path to training dataset directory')
    parser.add_argument('--include_bed',
                        type=str,
                        default='/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/HG002_SVs_Tier1_v0.6_chr_removechrY.bed',
                        help='path to training dataset directory')
    parser.add_argument('--minimum',
                        type=int,
                        default=50,
                        help='truvari param min')
    parser.add_argument('--maximum',
                        type=int,
                        default=0,
                        help='truvari param max')
    args = parser.parse_args()

    root_d = args.path_to_folder_with_gradiant_vcf
    subdirs = os.listdir(root_d)
    # print(subdirs)
    # exit(-1)
    vcf_files = []
    for sub in subdirs:
        files = os.listdir(os.path.join(root_d, sub))
        for f in files:
            if f.endswith('.vcf'):
                vcf_files.append(os.path.join(root_d, sub, f))
    # print(vcf_files)
    ####################################
    #   sanity check: number of vcf files should = 7 * #subfolders
    #   3 subfolders ~ 21 vcf files
    ####################################
    print(len(vcf_files))
    # exit(-1)
    for f in vcf_files:
        # vcf_files = os.listdir(fd)
        # abs_path = os.path.join(root_d, f)
        # print(os.path.dirname(f))
        model_ = f.split('/')[-2]
        print(model_)
        # exit(-1)
        # print(Path(abs_path + '.gz').is_file(), Path(abs_path + '.gz.tbi').is_file())
        if not Path(f + '.gz').is_file():
            os.system('bgzip -c ' + f + ' > ' + f + '.gz')
        if not Path(f + '.gz.tbi').is_file():
            os.system('tabix -p vcf ' + f + '.gz')
        # exit(-1)
        """
        50 ~ 
        """
        thres_ = f.split('.')[-2]
        if args.maximum == 0:
            out_folder_name = os.path.join(os.path.dirname(f), model_ + '_0.' + thres_ + '_' + str(args.minimum) + 'up')
        else:
            out_folder_name = os.path.join(os.path.dirname(f),
                                           model_ + '_0.' + thres_ + '_' + str(args.minimum) + '_' + str(args.maximum))
        print(out_folder_name)
        # exit(-1)
        if args.maximum == 0:
            os.system('truvari bench -b ' + args.vcf_bench + ' \
                                     -c ' + f + '.gz \
                                     -o ' + out_folder_name + ' \
                                     -f ' + args.fasta + ' \
                                     --includebed ' + args.include_bed + ' \
                                     --passonly -p 0.1 -P 0.1 -r 200 --sizemin ' + str(args.minimum))
        else:
            os.system('truvari bench -b ' + args.vcf_bench + ' \
                                     -c ' + f + '.gz \
                                     -o ' + out_folder_name + ' \
                                     -f ' + args.fasta + ' \
                                     --includebed ' + args.include_bed + ' \
                                     --passonly -p 0.1 -P 0.1 -r 200 --sizemin ' + str(
                args.minimum) + ' --sizemax ' + str(args.maximum))
    
    
    
    
    
    
    
    
    
    