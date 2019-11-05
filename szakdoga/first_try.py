import cv2
from PIL import Image
from pdf2image import convert_from_path
from matplotlib import pyplot as plt
import numpy as np

images = convert_from_path('pdf_files/testpdf.pdf')

numberOfPages = len(images)
for i in range(numberOfPages): 
    images[i].save('test' + format(i) + '.png', 'PNG')

img = cv2.imread('test0.png')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

test = Image.fromarray(img_gray)
pix = test.load()
width = test.size[0]
height = test.size[1]

intensity_y = img_gray.sum(axis=1) / width
intensity_x = img_gray.sum(axis=0) / height
intensity_y = np.flip(intensity_y)

plt.axes([0, 0.15, 1, .8])
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([])
plt.yticks([])
plt.axes([0.3, 0.03, .405, .1])
plt.xticks([])
plt.plot(intensity_x)

plt.axes([0.75, 0.15, .1, .8])
plt.yticks([])
plt.plot(intensity_y, range(height))

plt.show()

'''
intensity_y = np.flip(intensity_y)

ax = plt.axes()
ax.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([])
plt.yticks([])
ax.plot(intensity_x)

plt.yticks([])
ax.plot(intensity_y, range(height))

plt.show()
'''