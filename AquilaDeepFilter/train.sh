nvidia-docker run -v /home:/home -it tensorflow/tensorflow:latest-gpu python /home/yunfei/workspace/AquilaDeepFilter/AquilaDeepFilter/main.py train \
    --epoch 200 --batch_size 128 \
    --path_to_train_dir /home/yunfei/workspace/shortreads_data/experiment_data_shortreads_del/Aquila/NA24385_split_train \
    --path_to_eval_dir  /home/yunfei/workspace/shortreads_data/experiment_data_shortreads_del/Aquila/NA24385_split_test \
    --checkpoint_dir /home/yunfei/workspace/weights/ckpt/efficientnet/ \
    --tensorboard_log_dir /home/yunfei/workspace/weights/tensorboard_logs/efficientnet/ \
    --model_arch efficientnet --fine_tune_at 40

#  "xception" "densenet" "resnet" "mobilenet" "mobilenetv1" "efficientnet" "vgg"


singularity exec /data/maiziezhou_lab/sanidhya/docker_images/tf25-gpu.sif python /data/maiziezhou_lab/huyf/AquilaDeepFilter/AquilaDeepFilter/main.py train \
--model_arch=resnet \
--epoch=60 \
--batch_size=128 \
--lr=0.001 \
--fine_tune_at=45 \
--path_to_train_dir=*/use_phasing/10xweb/phased_train/ \
--path_to_eval_dir=*/use_phasing/10xweb/phased_test/ \
--checkpoint_dir=*/use_phasing/10xweb/resnet/ckpt/ \
--tensorboard_log_dir=*/use_phasing/10xweb/resnet/summary/
