##########################
#              deletions #
##########################


def get_dels_in_bed_format(original_format):
    """
    original_format = [chr index, start coord, ref seq, alt seq]
    """
    if len(original_format[2]) <= len(original_format[3]):
        print("double check the inputs, ref seq shoule be longer in deletions")
        exit(-1)
    end = int(original_format[1]) + len(original_format[2]) - len(original_format[3])
    length = len(original_format[2]) - len(original_format[3])
    return [original_format[0], original_format[1], str(end), 'DEL', length]
    

def get_inss_in_bed_format(original_format):
    """
    original_format = [chr index, start coord, ref seq, alt seq]
    """
    if len(original_format[2]) >= len(original_format[3]):
        print("double check the inputs, ref seq shoule be shorter in insertions")
        exit(-1)
    length = len(original_format[3]) - len(original_format[2])
    return [original_format[0], original_format[1], original_format[1], 'INS', length]
    

#bam_file_path = "/data/maiziezhou_lab/Datasets/stLFR_data/NA24385_giab/NA24385_stlfr_giab_hg19_chr21.bam"
##########################
# L5 10x data            #
##########################
#vcf_file_fp = "/data/maiziezhou_lab/Datasets/L5_NA24385_10x/Aquila_VCF_reformat/N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50_1kb_del/fp.vcf"
##########################
# 10xweb data            #
##########################
vcf_file_fp = "/data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/Aquila_VCF_reformat/N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50bp_up_ins/fp.vcf"
##########################
# stlfr data            #
##########################
# vcf_file_fp = "/data/maiziezhou_lab/Datasets/stLFR_data/NA24385_giab/Aquila_stLFR_VCF_reformat/N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50up_del/fp.vcf"

f = open(vcf_file_fp, 'r')
lines = f.readlines()
f.close()

del_count = 0
ins_count = 0
snp_count = 0
total_count = 0
dels = []
dels_index = []
index_ = 0
inss = []
for line in lines:
    if line.startswith('#'):
        index_ += 1
        continue
    total_count += 1
    split_line = line.split()
    reserve_ = (split_line[0], split_line[1], split_line[3], split_line[4])
    if len(reserve_[2]) > len(reserve_[3]):
        del_count += 1
        dels_index.append(index_)
        dels.append(get_dels_in_bed_format(reserve_))
    elif len(reserve_[2]) < len(reserve_[3]):
        ins_count += 1
        inss.append(get_inss_in_bed_format(reserve_))
    elif len(reserve_[2]) == len(reserve_[3]):
        snp_count += 1
    index_ += 1
print(del_count, ins_count, snp_count, total_count)


# out_file_ins = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/HG002_SVs_Tier1_v0.6_chr21_ins.bed', 'w')
# out_file_del = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/HG002_SVs_Tier1_v0.6_chr21_del.bed', 'w')
# Aquila_final_sorted_reformat_sorted_del_add_header.vcf
# out_file_ins = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/Aquila_final_sorted_reformat_sorted_del_add_header_ins_test.bed', 'w')
# out_file_del1 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/L5_NA24385_10x_deletion_low_conf.bed', 'w')
# out_file_del1 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb/10xweb_NA24385_deletion_low_conf.bed', 'w')
# #########
# # mapping back to vcf file for truvari eval.
# #########
# # out_file_del_index = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/10xweb_NA24385_deletion_low_conf_index.txt', 'w')

# index_ = 0
# for line in dels:
#     if line[-1] >= 50:
#         out_file_del1.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
#         # out_file_del_index.write(str(dels_index[index_]) + '\n')
#     index_ += 1
# index_ = 0
# # for line in inss:
# #     out_file_ins.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
# # out_file_ins.close()
# out_file_del1.close()
# # out_file_del_index.close()



out_file_ins1 = open('/data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb/10xweb_NA24385_insertion_low_conf.bed', 'w')
#########
# mapping back to vcf file for truvari eval.
#########
# out_file_del_index = open('/data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/10xweb_NA24385_deletion_low_conf_index.txt', 'w')

index_ = 0
for line in inss:
    if line[-1] >= 50:
        out_file_ins1.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
        # out_file_del_index.write(str(dels_index[index_]) + '\n')
    index_ += 1
index_ = 0
# for line in inss:
#     out_file_ins.write(line[0] + '\t' + line[1] + '\t' + line[2] +'\t' + line[3] + '\n')
# out_file_ins.close()
out_file_ins1.close()


