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

def get_paragraphs(height, intensity_y, margins):
    same_intensity = 0
    paragraph_coordinates = []
    not_saved = True
    global max_spacing 
    max_spacing = 0
    for i in range(0,height-1):
        if intensity_y[i] == 255.0:
            same_intensity = same_intensity+1
            if same_intensity > 10 and not_saved:
                paragraph_coordinates.append(i-10)
                not_saved = False
        else:
            if same_intensity > max_spacing and same_intensity != margins[3] and same_intensity != margins[1]:
                max_spacing = same_intensity
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
            if same_intensity < max_spacing and same_intensity > 1 and not_saved:
                line_coordinates.append(i-same_intensity+1)
                not_saved=False
        else:
            if intensity_y[i-1] == 255.0 and not(not_saved):
                line_coordinates.append(i-1)
            same_intensity = 0
            not_saved = True
    line_coordinates.append(height-1)
    return line_coordinates