import argparse
import os

# def get_length(vcf_line):
    # return 0

folder = "/data/maiziezhou_lab/huyf/DeepSVFilter/shortreads_NA24385/delly/"
add_header = True
files  = os.listdir(folder)
print(files)
vcf_files = []

for f in files:
    if f.endswith('.vcf'):
        vcf_files.append(os.path.join(folder, f))
print(vcf_files)

for vcf in vcf_files:
    f = open(vcf, 'r')
    new_name_del = vcf.split('/')[-1][:-4] + '_del.vcf'
    new_name_ins = vcf.split('/')[-1][:-4] + '_ins.vcf'
    print(new_name_del)
    print(new_name_ins)
    lines = f.readlines()
    f.close()
    header_ins = []
    header_del = []
    del_ = 0
    ins_ = 0
    ins_list = []
    del_list = []
    
    # f_out = open(os.path.join(folder, new_name), 'w')
    
    for line in lines:
        if line.startswith('#'):  # it is header line
            header_del.append(line)
            header_ins.append(line)
            if add_header and line.startswith('##INFO='):
                header_del.append('##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of SV:DEL=Deletion">\n')
                print("added header for del")
                header_ins.append('##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of SV:INS=Insertion">\n')
                print("added header for ins")
                new_name_del = vcf.split('/')[-1][:-4] + '_del_addheader.vcf'
                new_name_ins = vcf.split('/')[-1][:-4] + '_ins_addheader.vcf'
                add_header = False
        else:  # otherwise it is vcf line
            split_line = line.split('\t')
            if split_line[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', 'X']:
                line = 'chr'+line
                # print(line)
                # exit(-1)
            # print(split_line[7])
            # print(split_line[7][15:15+len('INS')])
            # exit(-1)
            if split_line[7][15:15+len('SNP')] == 'SNP':  # this is for delly output, a customized version of splitter should be written for all vcf files
                continue
            else:
                # print(split_line[7][7:len(split_line[7])])
                if split_line[7][15:15+len('INS')] == 'INS':
                    if len(split_line[4]) - len(split_line[3]) >= 50:
                        ins_ += 1
                        ins_list.append(line)
                elif split_line[7][15:15+len('DEL')] == 'DEL':
                    if len(split_line[3]) - len(split_line[4]) >= 50:
                        del_ += 1
                        del_list.append(line)
    print(del_, ins_)
    # exit(-1)
        # print(split_line[7])
    
    f1 = open(os.path.join(folder, new_name_del), 'w')
    f2 = open(os.path.join(folder, new_name_ins), 'w')
    
    
    for line in header_del:
        f1.write(line)
    for line in header_ins:
        f2.write(line)
    for line in del_list:
        f1.write(line)
    for line in ins_list:
        f2.write(line)
    f1.close()
    
    f2.close()
