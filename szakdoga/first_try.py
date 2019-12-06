import cv2
from PIL import Image
from pdf2image import convert_from_path
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

images = convert_from_path('pdf_files/testpdf.pdf')

numberOfPages = len(images)
for i in range(numberOfPages): 
    images[i].save('images/test' + format(i) + '.png', 'PNG')

img = cv2.imread('images/test0.png')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

test = Image.fromarray(img_gray)
pix = test.load()
width = test.size[0]
height = test.size[1]

intensity_y = img_gray.sum(axis=1) / width
intensity_x = img_gray.sum(axis=0) / height
intensity_y = np.flip(intensity_y)

fig, ax1 = plt.subplots(figsize=(8,8))
ax1.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.setp(ax1.set_xticks([]))
plt.setp(ax1.set_yticks([]))

divider = make_axes_locatable(ax1)

ax2 = divider.append_axes("right", size=1, pad=0.1)
ax2.plot(intensity_y, range(height))
plt.setp(ax2.set_yticks([]))

ax3 = divider.append_axes("bottom", size=1, pad=0.1, sharex=ax1)
ax3.plot(intensity_x)

plt.savefig('img_intensity/test.png')

#get coordinates to crop margins
for i in range(1,width-1):
    if intensity_x[i] != intensity_x[i-1]:
        left_margin = i
        break

for i in range(width-2,0,-1):
    if intensity_x[i] != intensity_x[i+1]:
        right_margin = i
        break
    
for i in range(1,height-1):
    if intensity_y[i] != intensity_y[i-1]:
        bottom_margin = i
        break
for i in range(height-2,0,-1):
    if intensity_y[i] != intensity_y[i+1]:
        top_margin = i
        break

#crop margins
im1 = test.crop((left_margin, height-top_margin, right_margin,height-bottom_margin))
im1.save('img_crop_margin/testcrop.png', 'PNG')

#get coordinates to crop paragraphs
same_intensity = 0
paragraph_coordinates = []
not_saved = True
max_spacing = 0
for i in range(0,height-1):
    if intensity_y[i] == 255.0:
        same_intensity = same_intensity+1
        if same_intensity > 10 and not_saved:
            paragraph_coordinates.append(i-10)
            not_saved = False
    else:
        if same_intensity > max_spacing and same_intensity != bottom_margin and same_intensity != top_margin:
            max_spacing = same_intensity
        if intensity_y[i-1] == 255.0 and not(not_saved):
            paragraph_coordinates.append(i-1)
        same_intensity = 0
        not_saved = True
paragraph_coordinates.append(height-1)

#crop paragraphs
paragraph_number = 0
for i in range(1,len(paragraph_coordinates)-2,2):
    im = test.crop((left_margin, height-paragraph_coordinates[i+1], right_margin,height-paragraph_coordinates[i]))
    im.save('img_crop_paragraphs/testcrop'+ format(paragraph_number) +'.png', 'PNG')
    paragraph_number = paragraph_number+1

#get coordinates to crop lines
same_intensity = 0
not_saved = True
line_coordinates = []
for i in range(0, height-1):
    if intensity_y[i] == 255.0:
        same_intensity = same_intensity+1
        if same_intensity < max_spacing and same_intensity > 1 and not_saved:
            line_coordinates.append(i-same_intensity+1)
            not_saved=False
    else:
        if intensity_y[i-1] == 255.0 and not(not_saved):
            line_coordinates.append(i-1)
        same_intensity = 0
        not_saved = True
line_coordinates.append(height-1)

#crop lines
line_number = 0
for i in range(1,len(line_coordinates)-2,2):
    im = test.crop((left_margin, height-line_coordinates[i+1], right_margin,height-line_coordinates[i]))
    im.save('img_crop_lines/testcrop'+ format(line_number) +'.png', 'PNG')
    line_number = line_number+1