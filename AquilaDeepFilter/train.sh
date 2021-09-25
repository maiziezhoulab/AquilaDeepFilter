nvidia-docker run -v /home:/home -it tensorflow/tensorflow:latest-gpu python /home/yunfei/workspace/AquilaDeepFilter/AquilaDeepFilter/main.py train \
    --epoch 200 --batch_size 128 \
    --path_to_train_dir /home/yunfei/workspace/shortreads_data/experiment_data_shortreads_del/Aquila/NA24385_split_train \
    --path_to_eval_dir  /home/yunfei/workspace/shortreads_data/experiment_data_shortreads_del/Aquila/NA24385_split_test \
    --checkpoint_dir /home/yunfei/workspace/weights/ckpt/efficientnet/ \
    --tensorboard_log_dir /home/yunfei/workspace/weights/tensorboard_logs/efficientnet/ \
    --model_arch efficientnet --fine_tune_at 40 --height 200 --width 400 --custom_input_preprocessing True

#  "xception" "densenet" "resnet" "mobilenet" "mobilenetv1" "efficientnet" "vgg"