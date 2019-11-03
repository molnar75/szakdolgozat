import cv2
from PIL import Image
from pdf2image import convert_from_path
from matplotlib import pyplot as plt

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

plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([])
plt.yticks([])
plt.plot(intensity_x)
plt.plot(intensity_y)

plt.show()
