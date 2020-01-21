def crop_margins(i, image, margins, height):
    image_crop = image.crop((margins[0], height-margins[1], margins[2],height-margins[3]))
    image_crop.save('img_crop_margins/testcrop' + format(i) + '.png', 'PNG')

def crop_paragraphs(paragraph_coordinates, image, margins, height):
    paragraph_number = 0
    for i in range(1,len(paragraph_coordinates)-2,2):
        image_crop = image.crop((margins[0], height-paragraph_coordinates[i+1], margins[2], height-paragraph_coordinates[i]))
        image_crop.save('img_crop_paragraphs/testcrop'+ format(paragraph_number) +'.png', 'PNG')
        paragraph_number = paragraph_number+1
        
def crop_lines(line_coordinates, image, margins, height):
    line_number = 0
    for i in range(1,len(line_coordinates)-2,2):
        image_crop = image.crop((margins[0], height-line_coordinates[i+1], margins[2], height-line_coordinates[i]))
        image_crop.save('img_crop_lines/testcrop'+ format(line_number) +'.png', 'PNG')
        line_number = line_number+1
    return line_number

def crop_words(words_coordinates, image, height, width):
    word_number = 0
    for i in range(1,len(words_coordinates)-2,2):
        image_crop = image.crop((words_coordinates[i], 0, words_coordinates[i+1], height))
        image_crop.save('img_crop_words/testcrop'+ format(word_number) +'.png', 'PNG')
        word_number = word_number+1
    return word_number