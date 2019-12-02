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

im1 = test.crop((left_margin, height-top_margin, right_margin,height-bottom_margin))
im1.save('img_crop_margin/testcrop.png', 'PNG')