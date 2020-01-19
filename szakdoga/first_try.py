import cv2
from PIL import Image
from pdf2image import convert_from_path
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
#my modules
import crop_methods
import get_methods

#TODO delete the contents of directories

def draw_intensity():
    fig, ax1 = plt.subplots(figsize=(8,8))
    ax1.imshow(image_read, cmap = 'gray', interpolation = 'bicubic')
    plt.setp(ax1.set_xticks([]))
    plt.setp(ax1.set_yticks([]))
    
    divider = make_axes_locatable(ax1)
    
    ax2 = divider.append_axes("right", size=1, pad=0.1)
    ax2.plot(intensity_y, range(height))
    plt.setp(ax2.set_yticks([]))
    
    ax3 = divider.append_axes("bottom", size=1, pad=0.1, sharex=ax1)
    ax3.plot(intensity_x)
    
    plt.savefig('img_intensity/test.png')

if __name__ == '__main__':
    images = convert_from_path('pdf_files/testpdf.pdf')
    
    numberOfPages = len(images)
    for i in range(numberOfPages): 
        images[i].save('images/test' + format(i) + '.png', 'PNG')
    
    for i in range(numberOfPages):
        image_read = cv2.imread('images/test' + format(i) + '.png')
        image_gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
        
        image = Image.fromarray(image_gray)
        pix = image.load()
        width = image.size[0]
        height = image.size[1]
        
        intensity_y = image_gray.sum(axis=1) / width
        intensity_x = image_gray.sum(axis=0) / height
        intensity_y = np.flip(intensity_y)
        
        margins = get_methods.get_margins(width, height, intensity_x, intensity_y)
        crop_methods.crop_margins(i, image, margins, height)
        
        paragraph_coordinates = get_methods.get_paragraphs(height, intensity_y, margins)
        crop_methods.crop_paragraphs(paragraph_coordinates, image, margins, height)
        
        line_coordinates = get_methods.get_lines(height, intensity_y)
        crop_methods.crop_lines(line_coordinates, image, margins, height)
        
        draw_intensity()
    # marginal = draw_margins(image, margins)
    pass
