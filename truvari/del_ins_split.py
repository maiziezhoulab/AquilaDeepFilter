#ori = '/data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf'
ori = '/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/Aquila_final_sorted_reformat_sorted_del.vcf'

f = open(ori, 'r')

lines = f.readlines()
f.close()
ins = 0
del_ = 0
del_list = []
ins_list = []
header = []
Y = 0
s_ = set()

for line in lines:
    if line[0] == '#':
        header.append(line)
        continue
    split_line = line.split('\t')
    if split_line[0] not in  s_:
        s_.add(split_line[0])
    # print(split_line[7])
print(s_)
print(len(s_))
"""
    if split_line[7][7:len(split_line[7])] == 'SNP':
        continue
    else:
        print(split_line[7][7:len(split_line[7])])
        if split_line[7][7:len(split_line[7])] == 'INS':
            ins += 1
            ins_list .append(line)
        elif split_line[7][7:len(split_line[7])] == 'DEL':
            del_ += 1
            del_list.append(line)
print(del_, ins)


#out_del = '/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/Aquila_final_sorted_reformat_sorted_del.vcf'
#out_ins = '/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/Aquila_final_sorted_reformat_sorted_ins.vcf'

#f1 = open(out_del, 'w')
#f2 = open(out_ins, 'w')


for line in header:
    f1.write(line)
    f2.write(line)
for line in del_list:
    f1.write(line)
for line in ins_list:
    f2.write(line)
f1.close()

f2.close()
"""