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

**1. image generation**
      This script is used to extract SV signals for image generation.

	python ./preprocess/image_generate.py 

		-- 

**2. augmentate**
      This script is used for data augmentation.

	python ./preprocess/image_generate.py 

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

## Output

1. The 'preprocess' command will take a SV bed file and output a SV image directory which contains  

1) image dir: storing all SV images  

2) SV image path file: storing the paths of all SV images  

2. The 'augmentate' command will take a SV image path file and also output a SV image directory after data augmentation.  

3. The 'train' command will take four SV image path files and output the trained model in the checkpoint directory.  

4. The 'predict' command will take the SV image path file got by the 'preprocess' command and output the filtering result  as follows.

Citation
--------


License
-------
