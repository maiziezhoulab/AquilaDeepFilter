nvidia-docker run -v /home:/home -it tensorflow/tensorflow:latest-gpu python /home/yunfei/workspace/AquilaDeepFilter/AquilaDeepFilter/main.py train \
    --epoch \
    --batch_size  \
    --path_to_train_dir */shortreads_data/experiment_data_shortreads_del/Aquila/NA24385_split_train \
    --path_to_eval_dir  */shortreads_data/experiment_data_shortreads_del/Aquila/NA24385_split_test \
    --checkpoint_dir */weights/ckpt/efficientnet/ \
    --tensorboard_log_dir */weights/tensorboard_logs/efficientnet/ \
    --model_arch efficientnet --fine_tune_at 

#  "xception" "densenet" "resnet" "mobilenet" "mobilenetv1" "efficientnet" "vgg"


singularity exec /data/maiziezhou_lab/sanidhya/docker_images/tf25-gpu.sif python /data/maiziezhou_lab/huyf/AquilaDeepFilter/AquilaDeepFilter/main.py train \
--model_arch=resnet \
--epoch= \
--batch_size= \
--lr= \
--fine_tune_at= \
--path_to_train_dir=*/use_phasing/10xweb/phased_train/ \
--path_to_eval_dir=*/use_phasing/10xweb/phased_test/ \
--checkpoint_dir=*/use_phasing/10xweb/resnet/ckpt/ \
--tensorboard_log_dir=*/use_phasing/10xweb/resnet/summary/
