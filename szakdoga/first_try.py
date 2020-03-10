import cv2
from PIL import Image
from pdf2image import convert_from_path
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
#my modules
import crop_methods as crop
import get_methods as get
import manage_directories as mdir

def draw_intensity(i):
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
    
    plt.savefig('img_intensity/test' + format(i) + '.png')

if __name__ == '__main__':
    mdir.manage_directories()
    images = convert_from_path('pdf_files/testpictures.pdf', size=(2500, None))
    numberOfPages = len(images)
    
    for i in range(numberOfPages): 
        images[i].save('img_pages/page' + format(i) + '.png', 'PNG')
    
    for i in range(numberOfPages):
        print(format(i + 1) + '/' + format(numberOfPages) + ' page', end='\r')        
        image_read = cv2.imread('img_pages/page' + format(i) + '.png')
        image_gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
        
        image = Image.fromarray(image_gray)
        pix = image.load()
        width = image.size[0]
        height = image.size[1]
        
        intensity_y = image_gray.sum(axis=1) / width
        intensity_x = image_gray.sum(axis=0) / height
        intensity_y = np.flip(intensity_y)
        
        draw_intensity(i)
        
        margins = get.get_margins(width, height, intensity_x, intensity_y)
        crop.crop_margins(i, image, margins, height)
        
        paragraph_coordinates = get.get_paragraphs(height, intensity_y)
        paragraph_number = crop.crop_paragraphs(paragraph_coordinates, image, margins, height)
    print('Crop paragraphs done!')
    for i in range(paragraph_number):
        print(format(i + 1) + '/' + format(paragraph_number) + ' paragraph', end='\r')
        paragraph_read =  cv2.imread('img_crop_paragraphs/paragraph_crop' + format(i) + '.png')
        paragraph_gray = cv2.cvtColor(paragraph_read, cv2.COLOR_BGR2GRAY)
        
        paragraph = Image.fromarray(paragraph_gray)
        width = paragraph.size[0]
        height = paragraph.size[1]
        
        intensity_y = paragraph_gray.sum(axis=1) / width
        intensity_y = np.flip(intensity_y)
        
        line_coordinates = get.get_lines(height, intensity_y)
        line_number = crop.crop_lines(line_coordinates, paragraph, width, height)
    print('Crop lines done!')
    for i in range(line_number):
        print(format(i + 1) + '/' + format(line_number) + ' line', end='\r')
        line_read = cv2.imread('img_crop_lines/line_crop' + format(i) + '.png')
        line_gray = cv2.cvtColor(line_read, cv2.COLOR_BGR2GRAY)
        
        line = Image.fromarray(line_gray)
        pix = line.load()
        width = line.size[0]
        height = line.size[1]
    
        intensity_x = line_gray.sum(axis=0) / height
        words_coordinates = get.get_words(width, intensity_x)
        word_number = crop.crop_words(words_coordinates, line, height, width) 
        
        characters_coordinates = get.get_characters(width, intensity_x)
        character_number = crop.crop_characters(characters_coordinates, line, height, width)
        crop.write_text_to_file()
    print('Crop words done!')
    pass
#TODO crop from the top of the page to the bottom