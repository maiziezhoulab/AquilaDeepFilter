import argparse
import gzip
import copy

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
parser.add_argument('--path_to_index_file',
                              required=True,
                              help='path to training dataset directory')
parser.add_argument('--confidence_threshold',
                              type=float,
                              default=0.1,
                              help='path to training dataset directory')
parser.add_argument('--increment',
                              type=float,
                              default=0.1,
                              help='path to training dataset directory')
args = parser.parse_args()
#ori_bed_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/Aquila_final_sorted_reformat_sorted_del_add_header_del_test.bed'  # input .bed for the model 
#predicted_bed_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/results/aquila_filter/filteredSVs/results.txt'  # output .bed for the model
#out_vcf_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/results/aquila_filter/filteredSVs/filteredSVs.vcf'  # output of this script bed2vcf.py
#header_vcf_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/Aquila_final_sorted_reformat_sorted_del_add_header.vcf'  # original vcf file for copying headers
#index_file = '/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/Aquila_final_sorted_reformat_sorted_del_add_header_del_mapping_to_vcf_test.txt'  # index of ori_bed_file
ori_bed_file = args.path_to_original_bed_file
predicted_bed_file = args.path_to_predicted_bed_file
out_vcf_file = args.path_to_output_vcf_file_suffix
header_vcf_file = args.path_to_header_vcf_file
index_file = args.path_to_index_file
confidence_thres = args.confidence_threshold
incremental = args.increment

##################################################
#  mapping original bed file to vcf line index   #
##################################################
f1 = open(ori_bed_file, 'r')
f2 = open(index_file, 'r')
lines1 = f1.readlines()
lines2 = f2.readlines()

index_dict = dict()
if len(lines1) != len(lines2):
    print("corrupted index file or bed file, please double check these 2 files")
    exit(-1)

for i in range(len(lines1)):
    split_ = lines1[i].split('\t')
    index_dict[(split_[0], split_[1], split_[2])] = int(lines2[i].rstrip())
# print(index_dict)
# exit(-1)

##################################################
#  rearrange the results also in ascending order #
##################################################
f_result = open(predicted_bed_file, 'r')
lines_predicted = f_result.readlines()  # not in ascending order!!!
f_result.close()
reorder_f = open('/data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb_raw/filteredSVs_reorder.txt', 'w')

result_dict = dict()
for line in lines_predicted:
    split_line = line.split('\t')
    if len(split_line[0]) >= 6 and split_line[0][3:6] == 'chr':
        split_line[0] = split_line[0][0:3] + split_line[0][6:len(split_line[0])]
    else:
        pass
    if split_line[0] not in result_dict.keys():
        result_dict[split_line[0]] = []
    # print(split_line)
    result_dict[split_line[0]].append([split_line[1].rstrip('\n'), split_line[2].rstrip('\n'), split_line[3].rstrip('\n'), split_line[4].rstrip('\n')])
#print(result_dict[split_line[0]])
for k in result_dict:
    result_dict[k] = sorted(result_dict[k], key=lambda l:int(l[0]))
    # print(result_dict[k])
    for _ in result_dict[k]:
        reorder_f.write(str(k) + '\t' + str(_[0]) + '\t' + str(_[1]) + '\t' + str(_[2]) + '\t' + str(_[3]) + '\n')
reorder_f.close()

new_vcf = []
lines = []
if header_vcf_file.split('.')[-1] == 'gz':
    print("?")
    with gzip.open(header_vcf_file,'rb') as fin:        
        for line in fin:
            #print(line)
            line = str(line, 'utf-8')
            #print(line)
            lines.append(line)
            # exit(-1)
elif header_vcf_file.split('.')[-1] == 'vcf':
    print("??")
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
        break
print("header lines:")
print(len(new_vcf))
print(result_dict.keys())
# exit(-1)
while confidence_thres <= 0.7:
    vcf_write = copy.deepcopy(new_vcf)
    for e in result_dict:
        chrind = e
        for iter_ in result_dict[e]:
            start = iter_[0]
            end = iter_[1]
            tag = iter_[2]
            confidence = iter_[3]
            if (chrind, str(int(start)-1), end) in index_dict.keys() and float(confidence) >= confidence_thres:
                # print(len(lines))
                # print(int(index_dict[(chrind, str(int(start)-1), end)]))
                vcf_write.append(lines[int(index_dict[(chrind, str(int(start)-1), end)])])
    
    # print(out_vcf_file.split('.')[0], str(round(confidence_thres, 2)), out_vcf_file.split('.')[1])
    # exit(-1)
    outfilename = out_vcf_file.split('.')[0] + str(round(confidence_thres, 2)) + '.vcf'
    f = open(outfilename, 'w')
    for _ in vcf_write:
        # print(_)
        f.write(_)
    f.close()
    confidence_thres += incremental
