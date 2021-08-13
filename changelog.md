### 2021-06-19
- added: base model and xception model
- [WIP] to create a model input pipeline

### 2021-06-20
- fixed: issues with the Xception model and removed base model arch
- added: trainer and model manager for managing the models file

### 2021-06-22
- added: data loader to load images from the file directories in a form of image tensor
- completed data loading pipeline
- added: driver code for training ops

### 2021-06-23
- feat: reimplemented base model arch
- updated: XceptionNet model arch based on base model arch
- added: architecture for DenseNet121, ResNet151V2, EfficientNetB0 and VGG16
- feat: added runner script and argument to select model architecture

### 2021-06-28
- added train test split script to split dataset into validation set and training set.
- added comments and documentation in the main script runner
- added parser for the fine tuning of the models

### 2021-06-30
- removed: preprocessing and data augmentation layer from the model
- added: support for mobilenet version
- added: prediction data loader for testing images
- added: prediction routing in model manager

### 2021-07-01
- fixed: image shape to 224x224 in models, image loaders, etc. 
- [WIP] for prediction set of data, added model compiling state for the prediction state. 
- fixed: prediction data loader for pointing data loader and added cache, prefetch in it.
- added: utils for writing data, creation of dirs and spiting string for result file
- completed: prediction co-routine for generation of prediction results
- added: parser for prediction part.

### 2021-07-04
- fixed: parser based issues for using both trainer and prediction mode from main runner
- deleted: seperate prediction runner 
- added: runner functions for train and predict ops

### 2021-07-05
- fixed: arg parser errors
- fixed: the arg parser params error

### 2021-07-06
- feat: added pipeline to move some data files randomly
- fixed: logger text for model training from scratch

### 2021-07-07
- added: mobilenet v1 model

### 2021-07-08
- feat: added params for changing the height width and channel

### 2021-07-10
- fixed: warning and weights saving in model checkpoints
- updated: instead of saving entire models we are not just saving weights

### 2021-07-30
- feat: added custom preprocessing units for the 400x200 images.

### 2021-08-13
- updated: added option for validation dataset