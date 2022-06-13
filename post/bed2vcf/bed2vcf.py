import argparse
import gzip
import copy
import os
"""
python bed2vcf.py \
      --path_to_original_bed_file /home/yunfei/workspace/AquilaDeepFilter/bed_files/HG002_60x_shortreads_raw/raw_deletion_50.bed \
      --path_to_predicted_bed_file /home/yunfei/workspace/AquilaDeepFilter/output/shortreads/0919/efficientnet/efficientnet.txt \
      --path_to_output_vcf_file_suffix /home/yunfei/workspace/AquilaDeepFilter/output/shortreads/0919/efficientnet/shortreads_efficientnet.vcf \
      --path_to_header_vcf_file /home/yunfei/workspace/shortreads_data/vcfs/HG002.hs37d5.60x_del_addheader.vcf \
      --add_chr False
"""

#ori_bed_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/Aquila_final_sorted_reformat_sorted_del_add_header_del_test.bed'  # input .bed for the model 
#predicted_bed_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/results/aquila_filter/filteredSVs/results.txt'  # output .bed for the model
#out_vcf_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/results/aquila_filter/filteredSVs/filteredSVs.vcf'  # output of this script bed2vcf.py
#header_vcf_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/Aquila_final_sorted_reformat_sorted_del_add_header.vcf'  # original vcf file for copying headers
#index_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/Aquila_final_sorted_reformat_sorted_del_add_header_del_mapping_to_vcf_test.txt'  # index of ori_bed_file
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='converting predicted results back to vcf format')
    parser.add_argument('--path_to_original_bed_file',
                        required=True,
                        help='path to training dataset directory')
    parser.add_argument('--path_to_predicted_bed_file',
                        required=True,
                        help='path to training dataset directory')
    parser.add_argument('--path_to_output_vcf_file_suffix',
                        required=True,
                        help='the suffix(path) for a series of files with ascending threshold gradient')
    parser.add_argument('--path_to_header_vcf_file',
                        required=True,
                        help='path to training dataset directory')
    # parser.add_argument('--path_to_index_file',
    #                     required=True,
    #                     help='path to training dataset directory')
    parser.add_argument('--add_chr',
                        required=True,
                        help='index as chr1 or 1. True == chr1 / False == 1')
    parser.add_argument('--confidence_threshold',
                        type=float,
                        default=0.1,
                        help='path to training dataset directory')
    parser.add_argument('--increment',
                        type=float,
                        default=0.1,
                        help='path to training dataset directory')
    args = parser.parse_args()

    ori_bed_file = args.path_to_original_bed_file
    predicted_bed_file = args.path_to_predicted_bed_file
    out_vcf_file = args.path_to_output_vcf_file_suffix
    header_vcf_file = args.path_to_header_vcf_file
    # index_file = args.path_to_index_file
    confidence_thres = args.confidence_threshold
    incremental = args.increment
    
    chr_list_ = ['20', '21', '22', '1', '3', '2', '5', '4', '7', '6', '9', '8', 
   'Y', 'X', '11', '10', '13', '12', '15', '14', '17', '16', '19', '18']

    ##################################################
    #  mapping original bed file to vcf line index   #
    ##################################################
    # f1 = open(ori_bed_file, 'r')
    # f2 = open(index_file, 'r')
    # lines1 = f1.readlines()
    # lines2 = f2.readlines()

    # index_dict = dict()
    # if len(lines1) != len(lines2):
    #     print("corrupted index file or bed file, please double check these 2 files")
    #     exit(-1)

    # for i in range(len(lines1)):

    #     print(lines2[i])
    #     split_ = lines1[i].split('\t')
    #     print(split_)
    #     index_dict[(split_[0], split_[1], split_[2])] = int(lines2[i].rstrip())
    # print(index_dict)
    # exit(-1)

    ##################################################
    #  rearrange the results also in ascending order #
    ##################################################
    f_result = open(predicted_bed_file, 'r')
    lines_predicted = f_result.readlines()  # not in ascending order!!!
    f_result.close()
    # reorder_f = open(out_vcf_file.split('.')[0] + '_reorder.txt', 'w')

    result_dict = dict()
    for line in lines_predicted:
        split_line = line.split('\t')
        # print(split_line[0])
        # print(split_line[0][3:])
        # print(args.add_chr)
        if args.add_chr is True:
            if split_line[0].startswith('chr'):
                # print("??")
                pass
            else:
                # print("add chr")
                split_line[0] = 'chr' + split_line[0]
        else:
            if split_line[0].startswith('chr'):
                # print("crop chr")
                split_line[0] = split_line[0][3:]
            else:
                # print("?")
                pass
        # exit(-1)
        # print(split_line[0])
        if split_line[0] not in result_dict.keys():
            result_dict[split_line[0]] = []
        # print(split_line)
        result_dict[split_line[0]].append(
            [split_line[1].rstrip('\n'), split_line[2].rstrip('\n'), split_line[3].rstrip('\n'),
             split_line[4].rstrip('\n')])
    # print(result_dict[split_line[0]])
    for k in result_dict:
        result_dict[k] = sorted(result_dict[k], key=lambda l: int(l[0]))
        # print(result_dict[k])
    #     for _ in result_dict[k]:
    #         reorder_f.write(str(k) + '\t' + str(_[0]) + '\t' + str(_[1]) + '\t' + str(_[2]) + '\t' + str(_[3]) + '\n')
    # reorder_f.close()

    new_vcf = []
    lines = []
    line_dict ={}
    if header_vcf_file.split('.')[-1] == 'gz':
        print("gz file")
        with gzip.open(header_vcf_file, 'rb') as fin:
            for line in fin:
                # print(line)
                line = str(line, 'utf-8')
                # print(line)
                lines.append(line)
                # exit(-1)
    elif header_vcf_file.split('.')[-1] == 'vcf':
        print("vcf file")
        f = open(header_vcf_file, 'r')
        lines = f.readlines()
        f.close()
    else:
        print("something wrong")
        exit(-1)
    # print(lines[0])
    for line in lines:
        # print(line)
        if line.startswith('#'):
            new_vcf.append(line)
            if line.startswith('##contig=<ID=chrX'):
                new_vcf.append('##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of SV:DEL=Deletion">\n')
        else:
            # if line.split('\t')[0] in chr_list_ and line.split('\t')[0] not in line_dict.keys():
            #     line_dict[] = [line.split('\t')[0]]
            split_line = line.split('\t')
            end_pos = str(len(split_line[3]) - len(split_line[4]) + int(split_line[1]))
            
            line_dict[(split_line[0][3:], split_line[1], end_pos)] = line
    print("#header lines:")
    print(len(new_vcf))
    # print(len(lines))
    # print(result_dict.keys())
    # print(index_dict.keys())
    # exit(-1)
    while confidence_thres <= 0.7:
        vcf_write = copy.deepcopy(new_vcf)
        for e in result_dict:
            chrind = e
            if e not in chr_list_:
                continue
            for i in range(len(result_dict[e])):
                # print(iter_)
                iter_ = result_dict[e][i]
                start = iter_[0]
                end = iter_[1]
                tag = iter_[2]
                confidence = iter_[3]
                # print(iter_)
                # print(index_dict.keys())
                # print((chrind, str(int(start) - 1), end))
                # print((chrind, str(int(start) - 1), end) in index_dict.keys())
                # print(chrind, str(int(start) - 1), end)
                # print(line_dict.keys())
                # print((chrind, str(int(start) - 1), end))
                # print((chrind, str(int(start) - 1), end) in line_dict.keys())
                # print((chrind, str(int(start)), end) in line_dict.keys())
                if (chrind, str(int(start) - 1), end) in line_dict.keys() and float(confidence) >= confidence_thres:
                    # print(len(lines))
                    # print(int(index_dict[(chrind, str(int(start)-1), end)]))
                    # print(index_dict[(chrind, str(int(start) - 1), end)])
                    # print(index_dict.values())
                    # print((chrind, str(int(start) - 1), end))
                    vcf_write.append(line_dict[(chrind, str(int(start) - 1), end)])
                # exit(-1)

        # print(out_vcf_file.split('.')[0], str(round(confidence_thres, 2)), out_vcf_file.split('.')[1])
        # exit(-1)
        # print(vcf_write)
        outfilename = out_vcf_file.split('.')[0] + str(round(confidence_thres, 2)) + '.vcf'
        print(outfilename)
        # exit(-1)
        f = open(outfilename, 'w')
        for _ in vcf_write:
            # print(_)
            f.write(_)
        f.close()
        confidence_thres += incremental
