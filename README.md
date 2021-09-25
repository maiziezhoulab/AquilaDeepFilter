# AquilaDeepFilter

## Introduction 
The general workflow of AquilaDeepFilter works as follows:

1.getting the vcf calls from the softwares.

2.preprocess to add header, make 1 -> chr1, split into INS and DEL for truvari calling.

3.get the truvari evaluated vcf results as the training bed files and raw vcf results as the validation files.  

4.converting to images and augmentation.

5.training with CNNs.

6.get the output bed back to vcfs.

7.ensemble strategy.

8.evaluate with truvari again to see the performance of our model.

## Installation
### Dependencies
truvari==3.0.0

tabix==1.11 [**bioconda**]

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
3. conda install -c bioconda tabix

## Running

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

    python ./post/vcf2bed/bed2vcf.py 

		--path_to_vcf [path to raw vcf file for validation]
            --path_to_original_bed_file [path to raw bed file with index]
            --path_to_index_file [path to the index]
            --path_to_predicted_bed_file []
            --path_to_output_vcf_file_suffix []
            --path_to_header_vcf_file []
            --add_chr [index as chr1 or 1. True/chr1 of False/1]
            --confidence_threshold [minimum confidence threshold]
            --increment [intervals for threshold gradient]

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
      This script is used to train AquilaDeepFilter.  

	python ./AquilaDeepFilter/main.py train

		--model_arch [xception,densenet,efficientnet,vgg,resnet,mobilenet]
            --batch_size BATCH_SIZE [number of samples in one batch]
            --path_to_images [path to prediction images directory]
            --output_file [path where output file needs to be saved]
            --checkpoint_dir [path to directory from which checkpoints needs to be loaded]
            --num_classes [number of classes to pick prediction from]
            --height HEIGHT [height of input images]
            --width WIDTH [width of input images, default value is 224]
            --channel CHANNEL [channel of input images, default value is 3]

  
**4. predict**
      This script is used to make predictions for candidate SVs.  

	python ./AquilaDeepFilter/main.py predict

		--model_arch [xception,densenet,efficientnet,vgg,resnet,mobilenet]
            --batch_size BATCH_SIZE [number of samples in one batch]
            --path_to_images [path to prediction images directory]
            --output_file [path where output file needs to be saved]
            --checkpoint_dir [path to directory from which checkpoints needs to be loaded]
            --num_classes [number of classes to pick prediction from]
            --height HEIGHT [height of input images]
            --width WIDTH [width of input images, default value is 224]
            --channel CHANNEL [channel of input images, default value is 3]

**5. evaluate**
	This script performs Truvari evaluation on the training models.  

	python ./post/truvari/truvari_evaluation.py

		--path_to_folder_with_gradiant_vcf
            path_to_folder_with_gradiant_vcf [folder for storing converted vcf files]
            --path_to_output_folder [path to the folder for generated evaluation result]
            --vcf_bench [path to the benchmark giab vcf file]
            --fasta [path to the reference genome]
            --include_bed [path to the giab gold standard bed file]
            --minimum [the lower length bound for evaluating SV detection]
            --maximum [the upper length bound for evaluating SV detection]

**6. ensemble**
	This script is used to acquire majortiy voting results of all models.  

	python ./post/ensemble/ensemble_.py 

		--path_to_models_results [input folder of models predition results]
            --ensemble_output [path of output file after voting]

## Repo Structure and Output

1. The folder of AquilaDeepFilter, post and preprocess have corresponding scripts and codes for Running the AuilaDeepFilter software

2. The dependencies are documented in the requirements.txt.

3. The 'train' command in 'main.py' script will constantly store the weights for the training epoch with the best validation Acc. and stops after the convergence is reached.

4. The 'predict' command in 'main.py' script will generate output in the BED structure (but in .txt file format). It can be then converted back to vcf for evaluation.

5. The docker image of this project will also be uploaded later after all the configuration and testing work are done.

6. The uploaded weights for our model and the toy dataset could be found in zenodo: ...

Citation
--------


License
-------
