vcf_file_fn = '/data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/Aquila_VCF_reformat/N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50bp_up_del/fn.vcf'
vcf_file_tp_base = '/data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/Aquila_VCF_reformat/N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50bp_up_del/tp-base.vcf'
vcf_file_fp = "/data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/Aquila_VCF_reformat/N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50bp_up_del/fp.vcf"

f1 = open(vcf_file_fn, 'r')
hold_intervals = []
lines = f1.readlines()
for line in lines:
    if line.startswith('#'):
        continue
    else:
        print(line)
        
        split_line = line.split()
        print(split_line)
        exit(-1)
        # reserve_ = (split_line[0], split_line[1], split_line[3], split_line[4])
        start = int(split_line[1])
        end = int(split_line[1]) + len(split_line[3]) - len(split_line[4])
        # length = len(original_format[2]) - len(original_format[3])
        hold_intervals.append([split_line[0], start, end])

f2 = open(vcf_file_tp_base, 'r')
lines2 = f2.readlines()
for line in lines2:
    if line.startswith('#'):
        continue
    else:
        print(line)
        exit(-1)
        split_line = line.split()
        # reserve_ = (split_line[0], split_line[1], split_line[3], split_line[4])
        start = int(split_line[1])
        end = int(split_line[1]) + len(split_line[3]) - len(split_line[4])
        # length = len(original_format[2]) - len(original_format[3])
        hold_intervals.append([split_line[0], start, end]
        
f3 = open(vcf_file_fp, 'r')
lines3 = f3.readlines()
for line in lines3:
    if line.startswith('#'):
        continue
    else:
        print(line)
        exit(-1)
        split_line = line.split()
        # reserve_ = (split_line[0], split_line[1], split_line[3], split_line[4])
        start = int(split_line[1])
        end = int(split_line[1]) + len(split_line[3]) - len(split_line[4])
        # length = len(original_format[2]) - len(original_format[3])
        hold_intervals.append([split_line[0], start, end])

f1.close()
f2.close()
f3.close()






















