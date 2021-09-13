import os

root_dir_10xweb = '/data/maiziezhou_lab/huyf/DeepSVFilter/final_exps/del0815/1b/10xweb'
root_dir_stlfr = '/data/maiziezhou_lab/huyf/DeepSVFilter/final_exps/del0815/1b/stlfr'
batch_index = ''

r1 = os.listdir(root_dir_10xweb)
r2 = os.listdir(root_dir_stlfr)

model_results_10xweb=[]
model_results_stlfr=[]

for f in r1:
    if f.endswith(batch_index):
        model_results_10xweb.append(os.path.join(root_dir_10xweb, f))
for f in r2:
    if f.endswith(batch_index):
        model_results_stlfr.append(os.path.join(root_dir_stlfr, f))
print(model_results_10xweb)
print(model_results_stlfr)

# exit(-1)
for p in model_results_10xweb:
    # os.system('cd ' + p)
    # print(os.listdir(p))
    # subdirs = os.listdir(p)
    # for sub in p:
    # f = os.listdir(os.path.join(p, sub))[0]
    # print(p)
    # print(os.listdir(sub))
    f = os.listdir(p)[0]
    # print(p)
    # print(f)
    # exit(-1)
    os.system('python bed2vcf.py --path_to_original_bed_file /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb_raw/10xweb_raw_deletion_50.bed \
                                 --path_to_predicted_bed_file '+ os.path.join(p, f) +' \
                                 --path_to_output_vcf_file '+ os.path.join(p, f, 'filteredSVs.vcf') +' \
                                 --path_to_header_vcf_file /data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/Aquila_VCF_reformat/Aquila_final_sorted_reformat_sorted_del.vcf.gz \
                                 --path_to_index_file /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb_raw/deletion_mapping_index.txt')

for p in model_results_stlfr:
    # os.system('cd ' + p)
    # subdirs = os.listdir(p)
    # for sub in subdirs:
    f = os.listdir(p)[0]
    os.system('python bed2vcf.py --path_to_original_bed_file /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/stLFR_raw/stlfr_raw_deletion_50.bed \
                                 --path_to_predicted_bed_file '+ os.path.join(p, f) +' \
                                 --path_to_output_vcf_file '+ os.path.join(p, f, 'filteredSVs.vcf') +' \
                                 --path_to_header_vcf_file /data/maiziezhou_lab/Datasets/stLFR_data/NA24385_giab/Aquila_stLFR_VCF_reformat/Aquila_final_sorted_reformat_sorted_del.vcf.gz \
                                 --path_to_index_file /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/stLFR_raw/deletion_mapping_index.txt')


"""
python /data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/bed2vcf.py \
                  --path_to_original_bed_file /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb_raw/10xweb_raw_deletion_50.bed \
                  --path_to_predicted_bed_file /data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb_raw/ensemble_test0706.txt \
                  --path_to_output_vcf_file /data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb_raw/0706ensemble/filteredSVs_ensemble0706.vcf \
                  --path_to_header_vcf_file /data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/Aquila_VCF_reformat/Aquila_final_sorted_reformat_sorted_del.vcf.gz \
                  --path_to_index_file /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb_raw/deletion_mapping_index.txt


python /data/maiziezhou_lab/huyf/DeepSVFilter/vcf2bed/bed2vcf.py \
                  --path_to_original_bed_file /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/stLFR_raw/stlfr_raw_deletion_50.bed \
                  --path_to_predicted_bed_file /data/maiziezhou_lab/huyf/DeepSVFilter/results/stLFR_raw/ensemble_test0706.txt \
                  --path_to_output_vcf_file /data/maiziezhou_lab/huyf/DeepSVFilter/results/stLFR_raw/0706ensemble/filteredSVs_ensemble0706.vcf \
                  --path_to_header_vcf_file /data/maiziezhou_lab/Datasets/stLFR_data/NA24385_giab/Aquila_stLFR_VCF_reformat/Aquila_final_sorted_reformat_sorted_del.vcf.gz \
                  --path_to_index_file /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/stLFR_raw/deletion_mapping_index.txt
"""                 