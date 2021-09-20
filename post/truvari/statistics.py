import os


def get_overlap(interval1, interval2):
    """
    interval1 is [a, b]
    interval2 is [c, d]
    """
    if int(interval1[0]) >= int(interval2[1]):
        return None, 'latter'
    if int(interval2[0]) >= int(interval1[1]):
        return None, 'former'
    smaller = max(int(interval1[0]), int(interval2[0]))
    bigger = min(int(interval1[1]), int(interval2[1]))
    return [smaller, bigger], '_'

##################################################
#  parameter settings                            #
##################################################
gold_path = '/data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_chr/HG002_SVs_Tier1_v0.6_chr21.bed'  # could be set to a args param later
input_for_model = '/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/Mybed/HG002_SVs_Tier1_v0.6_chr21_del.bed'
predicted_result_path_default = '/data/maiziezhou_lab/huyf/DeepSVFilter/results/test/filteredSVs/results.txt'
proj_name = 'test'  # could be set to a args param later
confidence_threshold_ = 0  # could be set to a args param later
coverage_threshold = 0.65  # could be set to a args param later

predicted_result_path = predicted_result_path_default.replace('test', proj_name)
print(predicted_result_path)

########################################################
#  get input file             #
########################################################
f_input = open(input_for_model, 'r')
lines = f_input.readlines()
f_input.close()

input_dict = dict()  # {key:chr index, value:[[s1, e1], [s2, e2], [s3, e3] ..., [sn, en]]}
for line in lines:
    split_line = line.split('\t')
    if split_line[0] not in input_dict.keys():
        input_dict[split_line[0]] = []
    input_dict[split_line[0]].append([split_line[1].rstrip('\n'), split_line[2].rstrip('\n')])
# print(input_dict)  # input intervals are in ascending order
# print(len(input_dict['chr21']))
# exit(-1)

########################################################
#  get gold for statistics and performance comparison  #
########################################################
f_gold = open(gold_path, 'r')
lines = f_gold.readlines()
f_gold.close()

gold_dict = dict()  # {key:chr index, value:[[s1, e1], [s2, e2], [s3, e3] ..., [sn, en]]}
for line in lines:
    split_line = line.split('\t')
    if split_line[0] not in gold_dict.keys():
        gold_dict[split_line[0]] = []
    gold_dict[split_line[0]].append([split_line[1].rstrip('\n'), split_line[2].rstrip('\n')])
# print(gold_dict)  # gold intervals are in ascending order

chr21_g_list = gold_dict['chr21']
chr21_in_list = input_dict['chr21']
i = 0
j = 0

miss = 0
hit = 0
while i < len(chr21_g_list) and j < len(chr21_in_list):
    #print(chr21_g_list[i], chr21_in_list[j])
    overlap_, signal_ = get_overlap(chr21_g_list[i], chr21_in_list[j])
    #print(overlap_, signal_)
    if overlap_ == None:  # miss
        # chr21_in_list[j].append('miss')
        if signal_ == 'latter':
            chr21_in_list[j].append('miss')
            miss += 1
            j+=1
            # print('latter')
            continue
        if signal_ == 'former':
            i+=1
            continue
    else:  # hit!
        chr21_in_list[j].append('hit')
        hit += 1
        j+=1
#print(chr21_in_list)  # col1: start, col2: end, col3: input/gold, col4: input/predicted
                      # use col3 and col4 to get the accuracy of each result.
                      # overlap/confidence threshold could be added later...
print(hit, miss)  # input/gold
# exit(-1)

##################################################
#  rearrange the results also in ascending order #
##################################################
f_result = open(predicted_result_path, 'r')
lines = f_result.readlines()  # not in ascending order!!!
f_result.close()

result_dict = dict()
for line in lines:
    split_line = line.split('\t')
    if len(split_line[0]) >= 6 and split_line[0][3:6] == 'chr':
        split_line[0] = split_line[0][0:3] + split_line[0][6:len(split_line[0])]
    else:
        pass
    if split_line[0] not in result_dict.keys():
        result_dict[split_line[0]] = []
    result_dict[split_line[0]].append([split_line[1].rstrip('\n'), split_line[2].rstrip('\n')])
#print(result_dict[split_line[0]])
result_dict[split_line[0]] = sorted(result_dict[split_line[0]], key=lambda l:int(l[0]))
#print(result_dict[split_line[0]])


chr21_r_list = result_dict['chr21']
chr21_in_list = input_dict['chr21']
i = 0
j = 0

miss = 0
hit = 0
print(len(chr21_r_list))
while i < len(chr21_r_list) and j < len(chr21_in_list):
    #print(chr21_g_list[i], chr21_in_list[j])
    overlap_, signal_ = get_overlap(chr21_r_list[i], [chr21_in_list[j][0], chr21_in_list[j][1]])
    #print(overlap_, signal_)
    if overlap_ == None:  # miss
        # chr21_in_list[j].append('miss')
        if signal_ == 'latter':
            chr21_in_list[j].append('miss')
            miss += 1
            j+=1
            # print('latter')
            continue
        if signal_ == 'former':
            i+=1
            continue
    else:  # hit!
        chr21_in_list[j].append('hit')
        hit += 1
        j+=1
print(chr21_in_list)  # col1: start, col2: end, col3: input/gold, col4: input/predicted
                      # use col3 and col4 to get the accuracy of each result.
                      # overlap/confidence threshold could be added later...
print(hit, miss)  # input/predicted

total = 315
tp = 0
tn = 0
for _ in chr21_in_list:
    if _[2] == 'hit' and _[3] == 'hit':
        tp += 1
    if _[2] == 'miss' and _[3] == 'miss':
        tn += 1
print(tp)
print(tn)
print((tp+tn) / 315.0)
    