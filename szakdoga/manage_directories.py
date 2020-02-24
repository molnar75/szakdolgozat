import os
import shutil

def delete_directory(path):
    try:
        shutil.rmtree(path) #delete directory with files
    except OSError:
        print ("Deletion of the directory %s failed" % path)
    else:
        create_directory(path)
def create_directory(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
def manage_directories():
    current_path = os.getcwd()
    directory_names = ['images', 'img_pages', 'img_intensity', 'img_crop_lines', 'img_crop_margins', 'img_crop_paragraphs', 'img_crop_words', 'img_crop_characters']
    size = len(directory_names)
    
    for i in range(size):
        path = current_path + '/' + directory_names[i]
        is_exists = os.path.isdir(path)
        if is_exists :
            delete_directory(path)
        else: 
            create_directory(path)