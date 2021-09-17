# 10xweb
python /data/maiziezhou_lab/huyf/DeepSVFilter_new/deepsvfilter/bed2image.py \
       --sv_type DEL \
       --bam_path /data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/longranger_align/possorted_bam.bam \
       --bed_path /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb_raw/10xweb_raw_deletion_50.bed \
       --output_imgs_dir /data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb_600_raw/ \
       --patch_size 600,200
       
       
# stlfr
python /data/maiziezhou_lab/huyf/DeepSVFilter_new/deepsvfilter/bed2image.py \
       --sv_type DEL \
       --bam_path /data/maiziezhou_lab/Datasets/stLFR_data/NA24385_giab/NA24385_stlfr_giab_hg19.bam \
       --bed_path /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/stLFR_raw/stlfr_raw_deletion_50.bed \
       --output_imgs_dir /data/maiziezhou_lab/huyf/DeepSVFilter/results/stLFR_600_raw/ \
       --patch_size 600,200


# INS
python /data/maiziezhou_lab/huyf/DeepSVFilter_new/deepsvfilter/bed2image.py \
       --sv_type INS \
       --bam_path /data/maiziezhou_lab/Datasets/10xweb_NA24385_hg19/longranger_align/possorted_bam.bam \
       --bed_path /data/maiziezhou_lab/huyf/DeepSVFilter/bed_files/10xweb/10xweb_NA24385_insertion_low_conf.bed \
       --output_imgs_dir /data/maiziezhou_lab/huyf/DeepSVFilter/experiment_data_ins/training/10xweb_400_200/low_confidence \
       --patch_size 400,200