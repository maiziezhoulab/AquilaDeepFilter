python /data/maiziezhou_lab/huyf/DeepSVFilter/truvari/truvariResult2excelMetrics.py \
       --root_folder /data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb_raw/0706ensemble/ \
       --output_excel /data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb_raw/0706ensemble/0706ensemble10xweb.xlsx \
       --ensemble True
       

python /data/maiziezhou_lab/huyf/DeepSVFilter/truvari/truvariResult2excelMetrics.py \
       --root_folder /data/maiziezhou_lab/huyf/DeepSVFilter/results/stLFR_raw/0706ensemble/ \
       --output_excel /data/maiziezhou_lab/huyf/DeepSVFilter/results/stLFR_raw/0706ensemble/0706ensemblestlfr.xlsx \
       --ensemble True       


##################################
python /data/maiziezhou_lab/huyf/DeepSVFilter/truvari/truvariResult2excelMetrics.py \
       --root_folder /data/maiziezhou_lab/huyf/DeepSVFilter/final_exps/del0815/2b/temp_10x/efficientnet/ \
       --output_excel /data/maiziezhou_lab/huyf/DeepSVFilter/final_exps/del0815/2b/temp_10x/0816_10x.xlsx \
       --models efficientnet



python /data/maiziezhou_lab/huyf/DeepSVFilter/truvari/truvariResult2excelMetrics.py \
       --root_folder /data/maiziezhou_lab/huyf/DeepSVFilter/final_exps/del0815/2b/temp_stlfr/ \
       --output_excel /data/maiziezhou_lab/huyf/DeepSVFilter/final_exps/del0815/2b/temp_stlfr/0816_stlfr.xlsx \
       --models efficientnet