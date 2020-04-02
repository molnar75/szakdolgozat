from collections import Counter

background_intensity = 0
paragraph_min = 0
line_min = 0

def get_basic_datas(intensity_y, height):
    global background_intensity
    background_intensity = Counter(intensity_y).most_common()[0][0]
    same_intensity = 0
    intensity_list = []
    for i in range(0,height-1):
        if intensity_y[i] == intensity_y[i+1]:
            same_intensity = same_intensity+1
        else:
            if same_intensity != 0:
                intensity_list.append(same_intensity)
                same_intensity = 0
    intensity_list.append(same_intensity)
    spacing = get_spacing(Counter(intensity_list).most_common())
    global line_min
    line_min = spacing[0]
    global paragraph_min
    paragraph_min = spacing[1]
    
def get_spacing(count_list):
    values =  []
    values_number = []
    for i in count_list:
        values.append(i[0])
        values_number.append(i[1])
    max_value = max(values)
    values.sort()
    spacing = []
    start = 0
    i = 0
    not_saved = True
    while i < len(values):
        not_saved = True
        if(values[i] > 3):
            start = values[i]
            for j in range(i+1, len(values)):
                if (values[j]-values[i] > 10):
                    not_saved = False
                    spacing.append(values[i])
                    i = j
                    break
            if (not_saved):
                spacing.append(values[i])
                i = i+1
                not_saved = True
        else: 
            i = i+1
    return spacing

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
    global background_intensity
    global paragraph_min
    same_intensity = 0
    paragraph_coordinates = []
    not_saved = True
    for i in range(0,height-1):
        if intensity_y[i] == background_intensity:
            same_intensity = same_intensity+1
            if same_intensity > paragraph_min and not_saved:
                paragraph_coordinates.append(i-1)
                not_saved = False
        else:
            if intensity_y[i-1] == background_intensity and not(not_saved):
                paragraph_coordinates.append(i-1)
            same_intensity = 0
            not_saved = True
    paragraph_coordinates.append(height-1)
    return paragraph_coordinates

def get_lines(height, intensity_y):
    global background_intensity
    global line_min
    same_intensity = 0
    not_saved = True
    line_coordinates = []
    for i in range(0, height-1):
        if intensity_y[i] == background_intensity:
            same_intensity = same_intensity+1
            if same_intensity > line_min and not_saved:
                line_coordinates.append(i-same_intensity+2)
                not_saved=False
        else:
            if intensity_y[i-1] == background_intensity and not(not_saved):
                line_coordinates.append(i-2)
            same_intensity = 0
            not_saved = True
    return line_coordinates

def get_words(width, intensity_x):
    global background_intensity
    same_intensity = 0
    not_saved = True
    words_coordinates = []
    for i in range(0, width-1):
        if intensity_x[i] > background_intensity-5:
            same_intensity = same_intensity+1
            if same_intensity > 10 and not_saved:
                words_coordinates.append(i-same_intensity+4)
                not_saved=False
        else:
            if intensity_x[i-1] > background_intensity-5 and not(not_saved):
                words_coordinates.append(i-4)
            same_intensity = 0
            not_saved = True
    words_coordinates.append(width-1)
    return words_coordinates

def get_characters(width, intensity_x):
    not_saved = True
    characters_coordinates = []
    for i in range(0, width-1):
        if intensity_x[i] < background_intensity-5:
            if not_saved:
                characters_coordinates.append(i-1)
                not_saved=False
        else:
            if intensity_x[i-1] < background_intensity-5 and not(not_saved):
                characters_coordinates.append(i+1)
            not_saved = True
    characters_coordinates.append(width-1)
    return characters_coordinates