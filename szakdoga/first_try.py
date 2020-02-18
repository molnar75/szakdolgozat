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
    images = convert_from_path('pdf_files/testpdf.pdf')
    numberOfPages = len(images)
    line_number = 0
    
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
        
        draw_intensity(i)
        
        margins = get.get_margins(width, height, intensity_x, intensity_y)
        crop.crop_margins(i, image, margins, height)
        
        paragraph_coordinates = get.get_paragraphs(height, intensity_y)
        crop.crop_paragraphs(i, paragraph_coordinates, image, margins, height)
        
        line_coordinates = get.get_lines(height, intensity_y)
        line_number = crop.crop_lines(i, line_coordinates, image, margins, height)
        
        params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
        params.minThreshold = 1
        params.maxThreshold = 200
        
        
        # Filter by Area.
        params.filterByArea = False
        params.minArea = 1
        
        # Filter by Circularity
        params.filterByCircularity = False
        params.minCircularity = 0.1
        
        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.1
            
        # Filter by Inertia
        params.filterByInertia = False
        params.minInertiaRatio = 0.01
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
        	detector = cv2.SimpleBlobDetector(params)
        else : 
        	detector = cv2.SimpleBlobDetector_create(params)
        for j in range(3):
            line_read = cv2.imread('img_crop_lines/' + format(i) + 'page_crop' + format(j) + '.png')
            line_gray = cv2.cvtColor(line_read, cv2.COLOR_BGR2GRAY)
            
            line = Image.fromarray(line_gray)
            pix = line.load()
            width = line.size[0]
            height = line.size[1]
                        
            keypoints = detector.detect(line_gray)
            im_with_keypoints = cv2.drawKeypoints(line_gray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv2.imshow("Keypoints", im_with_keypoints)
            
            intensity_x = line_gray.sum(axis=0) / height
            
            words_coordinates = get.get_words(width, intensity_x)
            word_number = crop.crop_words(j,words_coordinates, line, height, width) 
            
            characters_coordinates = get.get_characters(width, intensity_x)
            character_number = crop.crop_characters(j,characters_coordinates, line, height, width)
    pass
#TODO separate words with hyphen 
#TODO separate brackets from words, dot and comma too
#TODO crop from the top of the page to the bottom