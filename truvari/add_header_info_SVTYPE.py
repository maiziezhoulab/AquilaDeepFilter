vcf = '/data/maiziezhou_lab/huyf/DeepSVFilter/vcf_add_SV_header/stlfr/Aquila_final_sorted_reformat_sorted_del.vcf'
f = open(vcf, 'r')
lines = f.readlines()
f.close()
new = []

f_out = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf_add_SV_header/stlfr/Aquila_final_sorted_reformat_sorted_del_add_header.vcf', 'w')

for line in lines:
    if line == '##contig=<ID=chrX,length=155270560>\n':
        new.append('##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of SV:DEL=Deletion">\n')
    new.append(line)
    # print(split_line[7])

for line in new:
    f_out.write(line)
f_out.close()