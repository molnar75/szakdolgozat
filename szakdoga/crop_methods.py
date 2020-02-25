import numpy as np

paragraph_number = 0
image_number = 0
line_number = 0
word_number = 0
character_number = 0

def crop_margins(i, image, margins, height):
    image_crop = image.crop((margins[0], height-margins[1], margins[2],height-margins[3]))
    image_crop.save('img_crop_margins/testcrop' + format(i) + '.png', 'PNG')

def crop_paragraphs(paragraph_coordinates, image, margins, height):
    global paragraph_number
    for i in range(1,len(paragraph_coordinates)-2,2):
        image_crop = image.crop((margins[0], height-paragraph_coordinates[i+1], margins[2], height-paragraph_coordinates[i]))
        if not seek_for_columns(image_crop):     
            image_crop.save('img_crop_paragraphs/paragraph_crop'+ format(paragraph_number) +'.png', 'PNG')
            paragraph_number = paragraph_number+1
    return paragraph_number
        
def crop_lines(line_coordinates, image, width, height):
    global line_number 
    if line_coordinates and line_coordinates[0] == 0:  #there is some margins
        line_coordinates.pop(0)
    else:
        line_coordinates.insert(0,0) 
    if line_coordinates and line_coordinates[len(line_coordinates)-1] == height:
        line_coordinates.pop(len(line_coordinates)-1)
    else:
        line_coordinates.append(height)
    for i in range(0,len(line_coordinates)-1,2):
        image_crop = image.crop((0, height-line_coordinates[i+1], width, height-line_coordinates[i]))
        image_crop.save('img_crop_lines/line_crop'+ format(line_number) +'.png', 'PNG')
        line_number = line_number+1
    return line_number

def crop_words(words_coordinates, image, height, width):
    global word_number
    for i in range(1,len(words_coordinates)-2,2):
        image_crop = image.crop((words_coordinates[i], 0, words_coordinates[i+1], height))
        image_crop.save('img_crop_words/word_crop'+ format(word_number) +'.png', 'PNG')
        word_number = word_number+1
    return word_number

def crop_characters(characters_coordinates, image, height, width):
    global character_number
    for i in range(0,len(characters_coordinates)-2,2):
        image_crop = image.crop((characters_coordinates[i], 0, characters_coordinates[i+1], height))
        image_crop.save('img_crop_characters/character_crop'+ format(character_number) +'.png', 'PNG')
        character_number = character_number+1
    return character_number

def seek_for_columns(image):
    global paragraph_number
    global image_number
    width = image.size[0]
    height = image.size[1]
    
    image_numpy = np.array(image)
    intensity_x = image_numpy.sum(axis=0) / height
        
    coordinates = get_coordinates(width, intensity_x)
    if len(coordinates) > 1:
        if coordinates[0] == 0:  #there is some margins
            coordinates.pop(0)
        else:
            coordinates.insert(0,0) 
        if coordinates[len(coordinates)-1] == width:
            coordinates.pop(len(coordinates)-1)
        else:
            coordinates.append(width)
        for i in range(0,len(coordinates)-1,2):
            image_crop = image.crop((coordinates[i], 0, coordinates[i+1], height))
            if  is_paragraph(image_crop):
                image_crop.save('img_crop_paragraphs/paragraph_crop'+ format(paragraph_number) + '.png', 'PNG')
                paragraph_number = paragraph_number+1
            else:
                image_crop.save('images/image'+ format(image_number) + '.png', 'PNG')
                image_number = image_number+1
        return True
    else:
        return False
    
def is_paragraph(image):
    width = image.size[0]
    
    image_numpy = np.array(image)
    intensity_y = image_numpy.sum(axis=1) / width
    intensity_y = np.flip(intensity_y)
    
    is_paragraph = False
    same_bright_intensity = 0
    same_dark_intensity = 0
    
    for i in range(len(intensity_y)):
        if (intensity_y[i] > 240):
            same_bright_intensity = same_bright_intensity+1
            if (same_bright_intensity > 2):
                for j in range(i+1,len(intensity_y)):
                    if (intensity_y[j] < 240):
                        same_dark_intensity = same_dark_intensity+1
                        if (same_dark_intensity > 2):
                            for z in range (j+1, len(intensity_y)):
                                if (intensity_y[z] > 240):
                                    is_paragraph = True
                                    break;
                    else:
                        same_dark_intensity = 0
        else:
            same_bright_intensity = 0
    return is_paragraph

def get_coordinates(width, intensity_x):
    same_intensity = 0
    paragraph_coordinates = []
    not_saved = True
    for i in range(0,width-1):
        if intensity_x[i] == 255.0:
            same_intensity = same_intensity+1
            if same_intensity > 15 and not_saved:
                paragraph_coordinates.append(i-same_intensity+1)
                not_saved = False
        else:
            if intensity_x[i-1] == 255.0 and not(not_saved):
                paragraph_coordinates.append(i-1)
            same_intensity = 0
            not_saved = True
    return paragraph_coordinates
    
    