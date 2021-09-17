# AquilaDeepFilter

## Introduction 


## Installation
### Dependencies
tensorflow==2.5.0

tensorboard==2.5.0

matplotlib==3.1.0

numpy==1.19.5

opencv-python==3.1.0.4

Pillow==7.2.0

pysam==0.15.4

scikit-learn==0.19.2

scipy==1.5.4

### Install from github
1. git clone --recursive https://github.com/maiziezhoulab/AquilaDeepFilter.git
2. pip install requirements.txt

## Running
usage: DeepSVFilter [OPTIONS]  

**1. file format conversion**
      This script is used to extract SV signals for image generation.

	python ./preprocess/vcf2bed/vcf2bed_training.py 

		--vcf_dir [path of folder for GT vcf input]
        
        --output_folder [path to output folder]

        --SV_type [DEL or INS]

    python ./preprocess/vcf2bed/vcf2bed_val.py 

		--path_to_vcf [path to raw vcf file for validation]

        --path_to_output_folder [path to output folder]

        --SV_type [DEL or INS]

**2. image generation and augmentate**
      This script is used for data augmentation.

	python ./preprocess/image_generation/bed2image.py 

		--sv_type [DEL or INS]
        --bam_path [path to .BAM file]
        --bed_path [path to .BED file generated in step 1]
        --output_imgs_dir [path to output folder for images]
        --patch_size [width, height]
    
    python ./preprocess/image_generation/augmentate.py 

		--output_imgs_dir [path to output folder for augmentated images]
        --image_path_file [path to file that includes all the images for augmentation]
        --patch_size [wdith, height]

**3. train**
      This script is used to train a set of convolutional neural networks.  

	python ./AquilaDeepFilter/train.py

		--		

**4. predict**
      This script is used to make predictions for candidate SVs.  

	python ./AquilaDeepFilter/predict.py

		--

**5. evaluate**
	This script performs Truvari evaluation on the training models.  

	python ./post/truvari/truvari_evaluation.py

		--

**6. ensemble**
	This script is used to acquire majortiy voting results of all models.  

	python ./post/ensemble/ensemble_.py 

		--

## Repo Structure and Output

1. The   

2. The 

3. The 'train' command will take   

4. The 'predict' command will take t

Citation
--------


License
-------
