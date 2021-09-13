predicted_bed_file1 = '/data/maiziezhou_lab/sanidhya/Data_DSVF/result/efficientnet_low_conf.txt'
predicted_bed_file2 = '/data/maiziezhou_lab/sanidhya/Data_DSVF/result/efficientnet_pos.txt'

starting_confidence_thres = 0.1
incremental = 0.05

out_d = dict()

filtered_out_1 = open(predicted_bed_file1, 'r')
filtered_out_2 = open(predicted_bed_file2, 'r')
lines1 = filtered_out_1.readlines()  # not in ascending order!!!
lines2 = filtered_out_2.readlines()  # not in ascending order!!!
filtered_out_1.close()
filtered_out_2.close()

total = len(lines1) + len(lines2)
while starting_confidence_thres < 0.6:
    tp = 0
    fn = 0
    fp = 0
    tn = 0
    for line in lines1:
        split_line = line.rstrip('\n').split('\t')
        # print(split_line)
        if float(split_line[4]) > starting_confidence_thres:
            fp += 1
        else:
            tn += 1
    for line in lines2:
        split_line = line.rstrip('\n').split('\t')
        # print(split_line)
        if float(split_line[4]) > starting_confidence_thres:
            tp += 1
        else:
            fn += 1
    out_d[starting_confidence_thres] = [tp, fn, fp, tn, tp+fn+fp+tn]
    starting_confidence_thres += incremental
for k in out_d:
    # print(out_d[k])
    tp = out_d[k][0]
    fn = out_d[k][1]
    fp = out_d[k][2]
    tn = out_d[k][3]
    recall = tp*1.0/(tp+fn)
    precision = tp*1.0/(tp+fp)
    # print(recall, precision)
    f1 = 2*(recall * precision) / (recall + precision)
    accuracy = (tp+tn)*1.0/(tp+fp+fn+tn)
    print('\n')
    print("when threshold is "+ str(k))
    print("recall="+ str(recall))
    print("precision="+ str(precision))
    print("f1="+ str(f1))
    print("accuracy="+ str(accuracy))
