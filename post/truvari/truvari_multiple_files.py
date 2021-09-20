import os
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='evaluate with Truvari')
    parser.add_argument('--result_folder',
                        required=True,
                        help='path to folder which has multiple subfolders for prediction result with gradient results in vcf formats')
    parser.add_argument('--path_to_truvari_output_folder',
                        required=True,
                        help='path to folder for truvari output')
    parser.add_argument('--batch_index',
                        required=True,
                        help='identifier1: training batch index')
    # parser.add_argument('--model_name',
    #                     required=True,
    #                     help='identifier2: ')
    args = parser.parse_args()
    # dir_stlfr = '/data/maiziezhou_lab/huyf/DeepSVFilter/results/stLFR_raw/'
    # dir_10xweb = '/data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb_raw/'
    batch_index = args.batch_index

    subforder_names = os.listdir(args.result_folder)
    print(subforder_names)
    # file2 = os.listdir(dir_10xweb)

    folder_list_1 = []
    # folder_list_2 = []

    for f in subforder_names:
        folder_list_1 = []
        model_name = f
        abs_subforder_name = os.path.join(args.result_folder, f)
        files = os.listdir(abs_subforder_name)
        print(files)
        for f_ in files:
            if f_.endswith('.vcf'):
                folder_list_1.append(os.path.join(abs_subforder_name, f_))
    # for f in file2:
    #     if f.endswith(batch_index):
    #         folder_list_2.append(os.path.join(dir_10xweb, f))

        print(folder_list_1)
        for f2 in folder_list_1:
            # print(f2, batch_index, model_name)
            os.system('bgzip -c ' + f2 + ' > ' + f2 + '.gz')
            os.system('tabix -p vcf ' + f2 +'.gz')
            """
            50 ~
            """
            os.system('truvari bench -b /data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf.gz \
                                     -c ' + f2 + '.gz \
                                     -o ./N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50up_del_' + f2 + '_' + batch_index + '_' + model_name + 'Filtered \
                                     -f /data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa \
                                     --includebed /data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/HG002_SVs_Tier1_v0.6_chr_removechrY.bed \
                                     --passonly -p 0.1 -P 0.1 -r 200 --sizemin 50')
    # print(folder_list_2)
    # exit(-1)
    # for fd in folder_list_1:
    #     vcf_files = os.listdir(fd)
    #     for f in vcf_files:
    #         if not f.endswith('.vcf'):
    #             continue
    #         abs_path = os.path.join(fd, f)
    #         model_ = fd.split('/')[-1]
    #         print(model_)
    # exit(-1)
    # os.system('bgzip -c ' + abs_path + ' > ' + abs_path + '.gz')
    # os.system('tabix -p vcf ' + abs_path +'.gz')
    # """
    # 50 ~
    # """
    # os.system('truvari bench -b /data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf.gz \
    #                          -c ' + abs_path + '.gz \
    #                          -o ./N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50up_del_' + f + '_' + batch_index + '_' + model_[:-4] + 'Filtered \
    #                          -f /data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa \
    #                          --includebed /data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/HG002_SVs_Tier1_v0.6_chr_removechrY.bed \
    #                          --passonly -p 0.1 -P 0.1 -r 200 --sizemin 50')

    """
    sample usage for truvari eval
    50 ~ 1000
    os.system('truvari bench -b /data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf.gz \
                             -c ' + abs_path + '.gz \
                             -o ./N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50_1k_del_' + f + '_0702ourModelFiltered \
                             -f /data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa \
                             --includebed /data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/HG002_SVs_Tier1_v0.6_chr_removechrY.bed \
                             --passonly -p 0.1 -P 0.1 -r 200 --sizemin 50 --sizemax 1000')
    os.system('truvari bench -b /data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf.gz \
                             -c /data/maiziezhou_lab/huyf/DeepSVFilter/vcf_add_SV_header/stlfr/Aquila_final_sorted_reformat_sorted_del_add_header.vcf.gz \
                             -o ./exp2/N24385_stlfr_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50_1k_del_raw_benchmark \
                             -f /data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa \
                             --includebed /data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/HG002_SVs_Tier1_v0.6_chr_removechrY.bed \
                             --passonly -p 0.1 -P 0.1 -r 200 --sizemin 50')
    os.system('truvari bench -b /data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf.gz \
                             -c /data/maiziezhou_lab/huyf/DeepSVFilter/vcf_add_SV_header/10xweb/Aquila_final_sorted_reformat_sorted_del_add_header.vcf.gz \
                             -o ./exp2/N24385_10xweb_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50_1k_del_raw_benchmark \
                             -f /data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa \
                             --includebed /data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/HG002_SVs_Tier1_v0.6_chr_removechrY.bed \
                             --passonly -p 0.1 -P 0.1 -r 200 --sizemin 50')
            """

    # for fd in folder_list_2:
    #     vcf_files = os.listdir(fd)
    #     for f in vcf_files:
    #         if not f.endswith('.vcf'):
    #             continue
    #         abs_path = os.path.join(fd, f)
    #         model_ = fd.split('/')[-1]
    #         print(model_)
    #         # exit(-1)
    #         os.system('bgzip -c ' + abs_path + ' > ' + abs_path + '.gz')
    #         os.system('tabix -p vcf ' + abs_path +'.gz')
    #         """
    #         50 ~
    #         """
    #         os.system('truvari bench -b /data/maiziezhou_lab/Datasets/Benchmark0.6_chr/by_type/HG002_SVs_Tier1_v0.6_chr_del_removechrY.vcf.gz \
    #                                  -c ' + abs_path + '.gz \
    #                                  -o ./N24385_10xweb_giab_hg19_v0.6_Tier1bed_0.1_0.1_200_WGS_reformat_50up_del_' + f + '_' + batch_index + '_' + model_[:-4] + 'Filtered \
    #                                  -f /data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa \
    #                                  --includebed /data/maiziezhou_lab/huyf/DeepSVFilter/Aquila_stLFR_/HG002_SVs_Tier1_v0.6_chr_removechrY.bed \
    #                                  --passonly -p 0.1 -P 0.1 -r 200 --sizemin 50')