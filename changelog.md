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