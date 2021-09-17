from PIL import Image
import os

input_dir = "/data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb_500_200_raw/image/image/"
output_dir = "/data/maiziezhou_lab/huyf/DeepSVFilter/results/10xweb_400_raw/image/image/"
cropped_length = 400

images_path = os.listdir(input_dir)
count = 0
width = 0
heigt = 0
flank_length = 0
left = 0
top = 0
right = 0
bottom = 0
# Opens a image in RGB mode
for p in images_path:
    # print(p)
    # print(p.replace('_500', '_' + str(cropped_length)))
    # exit(-1)
    im = Image.open(os.path.join(input_dir, p))
     
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    if count == 0:
        width, height = im.size
        flank_length = (width - cropped_length) / 2
        if flank_length <= 0:
            print("double check the input param & image size")
            exit(-1)
        # Setting the points for cropped image
        left = flank_length
        top = 0
        right = width - flank_length
        bottom = height
        count = 1
        
     
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))
     
    # Shows the image in image viewer
    im1.save(os.path.join(output_dir, p.replace(str(width), str(cropped_length))))
    # exit(-1)