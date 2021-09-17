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

	python ./preprocess/vcf2bed/.py 

		-- 

**2. image generation and augmentate**
      This script is used for data augmentation.

	python ./preprocess/image_generation/bed2image.py 

		--output_imgs_dir	
    
    python ./preprocess/image_generation/augmentate.py 

		--output_imgs_dir	

**3. train**
      This script is used to train a set of convolutional neural networks.  

	python ./CNN/train.py

		--		

**4. predict**
      This script is used to make predictions for candidate SVs.  

	python ./CNN/predict.py

		--

**5. evaluate**
	This script performs Truvari evaluation on the training models.  

	python ./post/truvari_eval.py

		--

**6. ensemble**
	This script is used to acquire majortiy voting results of all models.  

	python ./post/ensemble_.py 

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
