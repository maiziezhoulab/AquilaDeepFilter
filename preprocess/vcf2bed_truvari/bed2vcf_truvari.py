predicted_bed_file1 = '/data/maiziezhou_lab/sanidhya/Data_DSVF/result/efficientnet_low_conf.txt'
predicted_bed_file2 = '/data/maiziezhou_lab/sanidhya/Data_DSVF/result/efficientnet_pos.txt'


starting_confidence_thres = 0.1
incremental = 0.05

##################################################
#  rearrange the results also in ascending order #
##################################################
filtered_out_1 = open(predicted_bed_file1, 'r')
filtered_out_2 = open(predicted_bed_file2, 'r')
lines1 = filtered_out_1.readlines()  # not in ascending order!!!
lines2 = filtered_out_2.readlines()  # not in ascending order!!!
filtered_out_1.close()
filtered_out_2.close()
reorder_f = open('/data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb/filteredSVs/results_reorder.bed', 'w')

result_dict = dict()
for line in lines1:
    split_line = line.split('\t')
    if len(split_line[0]) >= 6 and split_line[0][3:6] == 'chr':
        split_line[0] = split_line[0][0:3] + split_line[0][6:len(split_line[0])]
    else:
        pass
    if split_line[0] not in result_dict.keys():
        result_dict[split_line[0]] = []
    result_dict[split_line[0]].append([split_line[1].rstrip('\n'), split_line[2].rstrip('\n'), split_line[3].rstrip('\n'), split_line[4].rstrip('\n')])
#print(result_dict[split_line[0]])
for line in lines2:
    split_line = line.split('\t')
    if len(split_line[0]) >= 6 and split_line[0][3:6] == 'chr':
        split_line[0] = split_line[0][0:3] + split_line[0][6:len(split_line[0])]
    else:
        pass
    if split_line[0] not in result_dict.keys():
        result_dict[split_line[0]] = []
    result_dict[split_line[0]].append([split_line[1].rstrip('\n'), split_line[2].rstrip('\n'), split_line[3].rstrip('\n'), split_line[4].rstrip('\n')])
for k in result_dict:
    result_dict[k] = sorted(result_dict[k], key=lambda l:int(l[0]))
    print(result_dict[k])
    for _ in result_dict[k]:
        reorder_f.write(str(k) + '\t' + str(_[0]) + '\t' + str(_[1]) + '\t' + str(_[2]) + '\t' + str(_[3]) + '\n')



reorder_f.close()
##############################
#   combine tp & fn to true vcf file (temporary)
##############################




##############################
#    add vcf headers for truvary
##############################
new_vcf = []
f = open(header_vcf_file, 'r')
lines = f.readlines()
f.close()
for line in lines:
    if line.startswith('#'):
        new_vcf.append(line)
    else:
        break
print("header lines:")
print(len(new_vcf))

##############################
#   write vcf lines back
##############################
for e in result_dict:
    chrind = e
    for iter_ in result_dict[e]:
        start = iter_[0]
        end = iter_[1]
        tag = iter_[2]
        confidence = iter_[3]
        if (chrind, str(int(start)-1), end) in index_dict.keys():
            new_vcf.append(lines[int(index_dict[(chrind, str(int(start)-1), end)])])

f = open(out_vcf_file, 'w')
for _ in new_vcf:
    f.write(_)
f.close()
