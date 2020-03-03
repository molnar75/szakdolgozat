def get_margins(width, height, intensity_x, intensity_y):
    for i in range(1, width - 1):
        if intensity_x[i] != intensity_x[i - 1]:
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
    margins = (left_margin, top_margin, right_margin, bottom_margin)
    return margins

def get_paragraphs(height, intensity_y):
    same_intensity = 0
    paragraph_coordinates = []
    not_saved = True
    for i in range(0,height-1):
        if intensity_y[i] == 255.0:
            same_intensity = same_intensity+1
            if same_intensity > 10 and not_saved:
                paragraph_coordinates.append(i-10)
                not_saved = False
        else:
            if intensity_y[i-1] == 255.0 and not(not_saved):
                paragraph_coordinates.append(i-1)
            same_intensity = 0
            not_saved = True
    paragraph_coordinates.append(height-1)
    return paragraph_coordinates

def get_lines(height, intensity_y):
    same_intensity = 0
    not_saved = True
    line_coordinates = []
    for i in range(0, height-1):
        if intensity_y[i] == 255.0:
            same_intensity = same_intensity+1
            if same_intensity > 2 and not_saved:
                line_coordinates.append(i-same_intensity+1)
                not_saved=False
        else:
            if intensity_y[i-1] == 255.0 and not(not_saved):
                line_coordinates.append(i-1)
            same_intensity = 0
            not_saved = True
    return line_coordinates

def get_words(width, intensity_x):
    same_intensity = 0
    not_saved = True
    words_coordinates = []
    for i in range(0, width-1):
        if intensity_x[i] > 240:
            same_intensity = same_intensity+1
            if same_intensity > 5 and not_saved:
                words_coordinates.append(i-same_intensity+5)
                not_saved=False
        else:
            if intensity_x[i-1] > 240 and not(not_saved):
                words_coordinates.append(i-5)
            same_intensity = 0
            not_saved = True
    words_coordinates.append(width-1)
    return words_coordinates

def get_characters(width, intensity_x):
    not_saved = True
    characters_coordinates = []
    for i in range(0, width-1):
        if intensity_x[i] < 248:
            if not_saved:
                characters_coordinates.append(i)
                not_saved=False
        else:
            if intensity_x[i-1] < 248 and not(not_saved):
                characters_coordinates.append(i-1)
            not_saved = True
    characters_coordinates.append(width-1)
    return characters_coordinates