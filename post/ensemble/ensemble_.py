import os
import numpy as np
import argparse


def softmax(x):
    """Compute the softmax of dict value x."""
    list_ = []
    keys = x.keys()
    for e in keys:
        list_.append(x[e])
    exp_x = np.exp(list_)
    softmax_x = exp_x / np.sum(exp_x)
    
    i = 0
    for e in keys:
        x[e] = softmax_x[i]
        i+= 1
    return softmax_x 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ensemble strategy')
    parser.add_argument('--path_to_models_results',
                        required=True,
                        help='path to training dataset directory')
    parser.add_argument('--ensemble_output',
                        required=True,
                        help='path to training dataset directory')
    args = parser.parse_args()
    root_folder = args.path_to_models_results #  '/data/maiziezhou_lab/huyf/DeepSVFilter/results/stLFR_500_200_raw/0719/'
    ensemble_out_bed = args.ensemble_output  # '/data/maiziezhou_lab/huyf/DeepSVFilter/results/stLFR_500_200_raw/ensemble_test0719.txt'
    voting_weights = dict()

    sub_folder = os.listdir(root_folder)

    bed_files_abs_path_list = []
    for sub_f in sub_folder:
        voting_weights[sub_f] = 0
        p_ = os.path.join(root_folder, sub_f)

        files = os.listdir(p_)
        for f in files:
            if f.endswith('.txt'):
                bed_files_abs_path_list.append(os.path.join(root_folder, sub_f, f))

    # print(bed_files_abs_path_list)
    # print(voting_weights[''])
    voting_weights['mobilenet'] = 0.5
    voting_weights['resnet'] = 0.85
    voting_weights['efficientdet'] = 0.85
    voting_weights['xception'] = 0.6
    voting_weights['densenet'] = 0.85

    print(voting_weights)
    print(softmax(voting_weights))
    multiple_lines = []
    # for i in range(5):
    #     multiple_lines.append([])

    order_dict = dict()
    for i in range(len(bed_files_abs_path_list)):
        print(bed_files_abs_path_list[i])
        order_dict[i] = bed_files_abs_path_list[i].split('/')[-2]
        # os.system('cat ' + f + ' | tail -n 5')
        fh = open(bed_files_abs_path_list[i], 'r')
        lines = fh.readlines()
        multiple_lines.append(lines)
        fh.close()

    # for i in range(5):
    #     print(len(multiple_lines[i]))
    print(order_dict)
    out_f = open(ensemble_out_bed, 'w')
    for i in range(len(multiple_lines[0])):
        split_line = multiple_lines[0][i].split('\t')
        out_line = split_line[:4]
        # print(split_line)
        # print(out_line)
        weighted_conf = 0
        for j in range(5):
            #print(multiple_lines[j][i].split('\t')[-1].strip('\n'))
            weighted_conf += float(multiple_lines[j][i].split('\t')[-1].strip('\n')) * voting_weights[order_dict[j]]
        #print(weighted_conf)
        #exit(-1)
        out_f.write(out_line[0] + '\t' + out_line[1] + '\t' + out_line[2] + '\t' + out_line[3] + '\t' + str(weighted_conf) + '\n')


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
