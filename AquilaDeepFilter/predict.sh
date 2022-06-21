nvidia-docker run -v /home:/home -it tensorflow/tensorflow:latest-gpu python /home/yunfei/workspace/AquilaDeepFilter/AquilaDeepFilter/main.py predict \
    --path_to_images /home/yunfei/workspace/shortreads_data/experiment_data_shortreads_del/HG002_60x/raw/image/ \
    --output_file /home/yunfei/workspace/AquilaDeepFilter/output/shortreads/0919/efficientnet.txt \
    --num_classes 2 \
    --checkpoint_dir /home/yunfei/workspace/weights/ckpt/efficientnet/ \
    --model_arch efficientnet
