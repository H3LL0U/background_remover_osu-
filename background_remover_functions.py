import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import shutil
import imghdr
from typing import Generator
#ask user
def create_ask_window(text_to_display = "", title = "remove the backgrounds") -> bool | None:
    '''
    Creates ask window
    returns:
            user pressed yes -> True
            user pressed No -> False
            user pressed cancel or closed the window -> None
    '''
    response = messagebox.askyesnocancel(title ,f"{text_to_display}")
    if response is None:
        return None
    elif response:
        return True
    else:
        return False
    

def find_directories(root_dir, pattern, root)-> Generator[str, None, None] :
    '''
    finds the directories that match the pattern and yields them
    '''
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        root.update()
        
        if pattern in dirpath and dirpath[-len(pattern):]==pattern:
            yield dirpath

    
def find_all_osu_maps_folders(osu_directory: str)-> list[str]:

    
    '''
    takes in an a../osu!/Songs directory path and returns every folder inside of the path
    '''
    if not(os.path.exists(osu_directory)):
        raise(Exception("The path specified does not exist"))
    
    

    #checks if the directory has osu! in the path just in case
    if not(osu_directory) or ((osu_directory[-10:]!="osu!\\Songs")and (osu_directory[-10:]!="osu!/Songs")):
        
        raise(
            Exception("The drectory you specified does not contain 'osu!/Songs in it. Please select one that does.\n (It is done for the safety of your files)")
        )

    
    #get every ellement in the song directory (maps)
    try:
        every_map = os.listdir(osu_directory)
    except:
        raise (
            Exception("this directory does not exist")
            )
    return [f"{osu_directory}\\{i}".replace("\\",'/') for i in every_map if os.path.isdir(f"{osu_directory}\\{i}".replace("\\",'/'))]
        


    
def get_background_images_paths(the_osu_directory_path =None,ask_user = True)-> Generator[str, None, None]:
    '''
    takes in the osu!/Songs path returns the paths of the background-images 
    '''
    

    every_map_path = find_all_osu_maps_folders(the_osu_directory_path)


    #path to files to remove (the background images)
    try:
        path_items_to_remove = []
        for folder in every_map_path:
            
            files_inside_the_folder = os.listdir(folder)
            for item in files_inside_the_folder:

                    
                if item[-4:] == ".jpg" or item[-4:] == ".png" or item[-5:] == ".jpeg":
                    path_items_to_remove.append(f"{folder}/{item}")
    except Exception as error:
        raise(
            Exception("You have chosen the wrong directory or the directory has the files that are not other directories")
        )


    

    #ask user for confirmation
    if ask_user:
        user_answer = create_ask_window("are you sure you want to remove all the backgrounds?")
    else:
        user_answer = True
    if not(user_answer):
        raise(Exception('The deletion has been canceled'))
    #remove the files from the selected paths





    for i in path_items_to_remove:
        
        if (i[-4:] == ".png" or i[-4:]== ".jpg") :
                
            #checks if the path exists and i is not "" just in case
            if os.path.exists(i) and i:
                
                if user_answer:
                    yield i
                    #os.remove(i)
def remove_backgrounds_fully(iterable_with_paths) -> None:
    '''
    takes in: get_background_images_paths generator

    output: Removal of all backgrounds without saving

    remove all the backgrounds with the help of get_background_images_paths generator
    '''
    if iterable_with_paths.__name__ == "get_background_images_paths":
        for i in iterable_with_paths:
            
            os.remove(i)



    
def copy_directories(iterable_with_paths,program_root_path = os.getcwd())-> None:

    '''
    #Copies the names of the directories with map names from osu directory-----
    '''
    if iterable_with_paths.__name__ !="get_background_images_paths":
        raise(Exception("The iterable provided wasn't created by get_osu_backgrounds function"))
    backed_up_bg_dir = program_root_path+"\\backed up backgrounds"

    if not(os.path.exists(backed_up_bg_dir)):
        os.makedirs('backed up backgrounds')
    #Create the directories to store backgrounds: backed up backgrounds\mapname
    for image_path in iterable_with_paths:
        create_config(os.path.dirname(image_path))
        if os.path.exists(backed_up_bg_dir):
            osu_map_name = os.path.basename(os.path.dirname(image_path))
            
            
            backed_up_map_dir = backed_up_bg_dir+'\\'+osu_map_name
            
            if not(os.path.exists(backed_up_map_dir)):
                
                os.makedirs(backed_up_map_dir)
            if os.path.isfile(image_path):

                shutil.move(image_path,backed_up_map_dir)

def create_config(path_to_map_folder:str)-> str:
    '''
    takes in a path to the song folder and creates a config in the backed up backgrounds that stores the initial configuration
    of the songs' background
    returns a string which contains contents of the config
    '''
    if not(os.path.exists(path_to_map_folder)):
        raise(Exception("The path to folder does not exist"))
    if os.path.isdir(path_to_map_folder):
        osu_map_files_paths = [f"{path_to_map_folder}/{i}" for i in os.listdir(path_to_map_folder) if i.endswith(".osu")]
        contents_of_config =  ""
        
        for file_to_read in osu_map_files_paths:
            found_background_part = False
            contents_of_config+=f"{os.path.basename(file_to_read)}:\n"
            
            if os.path.exists(file_to_read):
                
                with open(file_to_read,"r", encoding='utf-8') as file:

                    for line in file:
                        
                        if found_background_part and line.startswith("//"):
                            break

                        if found_background_part and not("osu!_background_(re)mover)" in line):
                            contents_of_config+=f"{line}\n"
                        
                        if "//Background and Video events" in line:
                            found_background_part = True
    path_to_backed_up_bg = f"{os.getcwd()}/backed up backgrounds/{os.path.basename(path_to_map_folder)}"
    if not(os.path.exists(path_to_backed_up_bg)):
        os.makedirs(path_to_backed_up_bg)
    with open(f"{path_to_backed_up_bg}/config.txt", "a+") as file:
        file.seek(0)
        read_lines = file.readlines()
        lines_to_add = contents_of_config.split("\n")
        file.write("\n")
        for i in lines_to_add:
            
            if not(i+"\n" in read_lines) and i!="":
                
                file.write(i+"\n")
            
        

    return contents_of_config


    
    





def restore_bgs(osu_songs_dir, backed_up_bgs_dir) -> None:
    '''
    #Gets images from the backed up backgrounds folder and puts them back into the folder of the song it was taken from
    '''
    if not(os.path.exists(backed_up_bgs_dir)):
        raise(Exception('No backgrounds saved yet!'))

    saved_maps_names= os.walk(backed_up_bgs_dir).__next__()[1]
    
    for saved_map in saved_maps_names:
        backed_up_dir_contents_paths = [backed_up_bgs_dir+'\\'+saved_map+'\\'+i for i in os.walk(backed_up_bgs_dir+'\\'+saved_map).__next__()[2]]
        
        for image_path in backed_up_dir_contents_paths:
            if os.path.exists(osu_songs_dir+'\\'+saved_map) and not(image_path.endswith('.txt')):

                shutil.move(image_path,osu_songs_dir+'\\'+saved_map)
            
def copy_image_to_default_images(image_path: str) -> None:
    '''
    copies an image from a selected path to default images that later can be selected as a replacement for all of the backgrounds
    '''
    if not(os.path.exists( os.getcwd()+r"\default backgrounds")):
        os.mkdir(os.getcwd()+r"\default backgrounds")
    if imghdr.what(image_path):

        shutil.copy2(image_path,os.getcwd()+r"\default backgrounds")

def find_all_default_images_paths():
    '''
    Yields all of the images' paths from default backgrounds
    '''
    path_to_default_bgs = os.getcwd()+r"\default backgrounds"
    if not(os.path.exists(path_to_default_bgs )):
        os.mkdir(path_to_default_bgs)
    for image in os.listdir(path_to_default_bgs):
        if imghdr.what(path_to_default_bgs+"\\"+image):

            yield path_to_default_bgs+"\\"+image
def find_all_default_images_names():
    '''
    Yields all of the images' names from default backgrounds
    '''
    path_to_default_bgs = os.getcwd()+r"\default backgrounds"
    if not(os.path.exists(path_to_default_bgs )):
        os.mkdir(path_to_default_bgs)
    for image in os.listdir(path_to_default_bgs):
        if imghdr.what(path_to_default_bgs+"\\"+image):

            yield image

def rename_image_to(image_path: str, new_name: str) -> None:
    '''
    takes in an image path and changes the image's name to a new one without changing the extension
    example:
        image_path = image/path/image.jpg
        new_name = new_image
        outcome -> image/path/new_image.jpg (the new path to the image)
    '''
    if not(os.path.exists(image_path)):
        raise(Exception("The path to rename does not exist"))
    if not(imghdr.what(image_path)):
        raise(Exception("The path you specified is not an image"))
    dir, extension = os.path.splitext(image_path)
    dir , file_name = os.path.split(dir)
    file_name = new_name
    new_path = f"{dir}\\{file_name}{extension}"
    os.rename(image_path,new_path)

def copy_image_to_paths(image_path: str, new_dirs_with_image : list[str])-> None:
    '''
    takes in image path to copy
    and new directories where the image will be copied to

    outcome -> image is copied to these paths if they exist
    '''
    if os.path.exists(image_path):
        for i in new_dirs_with_image:
            if os.path.exists(i):


                shutil.copy2(image_path,i)

    else:
        raise(Exception("The path of an image you selected does not exist"))
    


