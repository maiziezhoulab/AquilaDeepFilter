"""
ori = '/data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del.vcf'
#ori = '/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/Aquila_final_sorted_reformat_sorted_del.vcf'

f = open(ori, 'r')

lines = f.readlines()
f.close()
new = []

f_out = open('/data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf', 'w')

for line in lines:
    if line == '##contig=<ID=MT,length=16569>\n':
        print(line)
        continue
    if line == '##contig=<ID=chrY,length=59373566>\n':
        print(line)
        continue
    if line[0] == '#':
        new.append(line)
        continue
    split_line = line.split('\t')
    if split_line[0] ==  'chrY':
        continue
    new.append(line)
    # print(split_line[7])

for line in new:
    f_out.write(line)
f_out.close()
"""

bed = '/data/maiziezhou_lab/Datasets/Benchmark0.6_chr/HG002_SVs_Tier1_v0.6_chr.bed'
f = open(bed, 'r')
lines = f.readlines()
f.close()
new = []

f_out = open('/data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/HG002_SVs_Tier1_v0.6_chr_removechrY.bed', 'w')

for line in lines:
    split_line = line.split('\t')
    if split_line[0] ==  'chrY':
        continue
    new.append(line)
    # print(split_line[7])

for line in new:
    f_out.write(line)
f_out.close()
