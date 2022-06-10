import os 
from PIL import Image

def concat_images(image1, image2):
    """Generate composite of all supplied images."""
    # Get the widest width.
    width = max(image1.width, image2.width)
    # Add up all the heights.
    height = sum(image1.height, image2.height)
    composite = Image.new('RGB', (width, height))
    # Paste each image below the one before it.
    y = 0
    for image in [image1, image2]:
        composite.paste(image, (0, y))
        y += image.height
    return composite

pos = '/data/maiziezhou_lab/huyf/DeepSVFilter/use_phasing/10xweb/positive/IMG_PATH.txt'
pos_aug = '/data/maiziezhou_lab/huyf/DeepSVFilter/use_phasing/10xweb/positive_aug/IMG_PATH.txt'
neg = '/data/maiziezhou_lab/huyf/DeepSVFilter/use_phasing/10xweb/negative/IMG_PATH.txt'
neg_aug = '/data/maiziezhou_lab/huyf/DeepSVFilter/use_phasing/10xweb/negative_aug/IMG_PATH.txt'

pos_hp1_dict = {}
pos_hp2_dict = {}
with open(pos, 'r') as f:
    lines = f.readlines()
for line in lines:
    abs_path = line.rstrip()
    hp_ind = line.split('/')[-1].split('.')[0].split('_')[6]
    chr_ind = line.split('/')[-1].split('_')[1]
    key = line.split('/')[-1].split('_')[2] + '_' + line.split('/')[-1].split('_')[3]
    # print(hp_ind, chr_ind, key, line.split('/')[-1].split('.')[0].split('_')[-1])
    if hp_ind == '1':
        if key in pos_hp1_dict.keys():
            pos_hp1_dict[key].append([abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]])
        else:
            pos_hp1_dict[key]=[[abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]]]
    if hp_ind == '2':
        if key in pos_hp2_dict.keys():
            pos_hp2_dict[key].append([abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]])
        else:
            pos_hp2_dict[key]=[abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]]

with open(pos_aug, 'r') as f:
    lines = f.readlines()
for line in lines:
    abs_path = line.rstrip()
    hp_ind = line.split('/')[-1].split('.')[0].split('_')[6]
    chr_ind = line.split('/')[-1].split('_')[1]
    key = line.split('/')[-1].split('_')[2] + '_' + line.split('/')[-1].split('_')[3]
    # print(hp_ind, chr_ind, key, line.split('/')[-1].split('.')[0].split('_')[-1])
    if hp_ind == '1':
        if key in pos_hp1_dict.keys():
            pos_hp1_dict[key].append([abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]])
        else:
            pos_hp1_dict[key]=[[abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]]]
    if hp_ind == '2':
        if key in pos_hp2_dict.keys():
            pos_hp2_dict[key].append([abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]])
        else:
            pos_hp2_dict[key]=[abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]]

# print(len(pos_hp1_dict.keys()), len(pos_hp2_dict.keys()))
# print(pos_hp1_dict)

# pos
#################
# neg

neg_hp1_dict = {}
neg_hp2_dict = {}
with open(neg, 'r') as f:
    lines = f.readlines()
for line in lines:
    abs_path = line.rstrip()
    hp_ind = line.split('/')[-1].split('.')[0].split('_')[6]
    chr_ind = line.split('/')[-1].split('_')[1]
    key = line.split('/')[-1].split('_')[2] + '_' + line.split('/')[-1].split('_')[3]
    # print(hp_ind, chr_ind, key, line.split('/')[-1].split('.')[0].split('_')[-1])
    if hp_ind == '1':
        if key in neg_hp1_dict.keys():
            neg_hp1_dict[key].append([abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]])
        else:
            neg_hp1_dict[key]=[[abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]]]
    if hp_ind == '2':
        if key in neg_hp2_dict.keys():
            neg_hp2_dict[key].append([abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]])
        else:
            neg_hp2_dict[key]=[abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]]

with open(neg_aug, 'r') as f:
    lines = f.readlines()
for line in lines:
    abs_path = line.rstrip()
    hp_ind = line.split('/')[-1].split('.')[0].split('_')[6]
    chr_ind = line.split('/')[-1].split('_')[1]
    key = line.split('/')[-1].split('_')[2] + '_' + line.split('/')[-1].split('_')[3]
    # print(hp_ind, chr_ind, key, line.split('/')[-1].split('.')[0].split('_')[-1])
    if hp_ind == '1':
        if key in neg_hp1_dict.keys():
            neg_hp1_dict[key].append([abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]])
        else:
            neg_hp1_dict[key]=[[abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]]]
    if hp_ind == '2':
        if key in neg_hp2_dict.keys():
            neg_hp2_dict[key].append([abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]])
        else:
            neg_hp2_dict[key]=[abs_path, chr_ind, line.split('/')[-1].split('_')[2], line.split('/')[-1].split('_')[3]]

# print(len(neg_hp1_dict.keys()), len(neg_hp2_dict.keys()))
# print(neg_hp1_dict)


#########################
# concatenate images    #
#########################

pos_concat_out_dir_ = '/data/maiziezhou_lab/huyf/DeepSVFilter/use_phasing/10xweb/pos_concat/'
for k in pos_hp1_dict.keys():
    count_ind = 0
    for hp1_half in pos_hp1_dict[k]:
        for hp2_half in pos_hp2_dict[k]:
            img1_p = hp1_half[0]
            img2_p = hp2_half[0]
            
            img1 = Image.open(img1_p)
            img2 = Image.open(img2_p)
            
            concat_img = concat_images(img1, img2)
            concat_img.save(os.path.join(output_dir, hp1_half[1] + '_' + hp1_half[2] + '_' + hp1_half[3] + '_' + str(count_ind) + '.png'))
            count_ind += 1
            
            
neg_concat_out_dir_ = '/data/maiziezhou_lab/huyf/DeepSVFilter/use_phasing/10xweb/neg_concat/'
for k in neg_hp1_dict.keys():
    count_ind = 0
    for hp1_half in neg_hp1_dict[k]:
        for hp2_half in neg_hp2_dict[k]:
            img1_p = hp1_half[0]
            img2_p = hp2_half[0]
            
            img1 = Image.open(img1_p)
            img2 = Image.open(img2_p)
            
            concat_img = concat_images(img1, img2)
            concat_img.save(os.path.join(output_dir, hp1_half[1] + '_' + hp1_half[2] + '_' + hp1_half[3] + '_' + str(count_ind) + '.png'))
            count_ind += 1            
            
