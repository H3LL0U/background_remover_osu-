import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import shutil

#ask user
def create_ask_window(text_to_display = "", title = "remove the backgrounds"):
    response = messagebox.askyesnocancel(title ,f"{text_to_display}")
    if response is None:
        return None
    elif response:
        return True
    else:
        return False
    
#find the directories that match the pattern
def find_directories(root_dir, pattern, root):
    
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        root.update()
        
        if pattern in dirpath and dirpath[-len(pattern):]==pattern:
            yield dirpath

    

        


    #takes in the osu!/Songs path returns the paths of the background-images 
def get_background_images_paths(the_osu_directory_path =None,ask_user = True):
    if the_osu_directory_path is None:
       the_osu_directory_path =filedialog.askdirectory(title="select the 'osu!/Songs' folder (from there all the images that are more than 100000 bytes will be removed)")
    
#store the osu song directory
    
    osu_directory = the_osu_directory_path 

    #checks if the directory has osu! in the path just in case
    if not(osu_directory) or ((osu_directory[-10:]!="osu!\\Songs")and (osu_directory[-10:]!="osu!/Songs")):
        
        raise(
            Exception("The drectory you specified does not contain 'osu!/Songs in it. Please select one that does.\n (It is done for the safety of your files)")
        )

    files_inside_the_folder = ""
    #get every ellement in the song directory (maps)
    try:
        every_map = os.listdir(osu_directory)
    except:
        raise (
            Exception("this directory does not exist")
            )
    #stores the paths of every folder with map's assets inside
    every_map_path = [f"{osu_directory}/{i}" for i in every_map]


    #path to files to remove (the background images)
    try:
        path_items_to_remove = []
        for folder in every_map_path[0:]:
            
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
        #remove images that are bigger than 100000 bytes (so that most of the time only background images get removed)
        if (i[-4:] == ".png" or i[-4:]== ".jpg") :
                
            #checks if the path exists and i is not "" just in case
            if os.path.exists(i) and i:
                
                if user_answer:
                    yield i
                    #os.remove(i)
def remove_backgrounds_fully(iterable_with_paths, full_removal = False):

    if iterable_with_paths.__name__ == "get_background_images_paths":
        for i in iterable_with_paths:
            
            os.remove(i)


#Copies the names of the directories with map names from osu directory-----
    
def copy_directories(iterable_with_paths,program_root_path = os.getcwd()):
    if iterable_with_paths.__name__ !="get_background_images_paths":
        raise(Exception("The iterable provided wasn't created by get_osu_backgrounds function"))
    backed_up_bg_dir = program_root_path+"\\backed up backgrounds"

    if not(os.path.exists(backed_up_bg_dir)):
        os.makedirs('backed up backgrounds')
    #Create the directories to store backgrounds: backed up backgrounds\mapname
    for image_path in iterable_with_paths:
        if os.path.exists(backed_up_bg_dir):
            osu_map_name = os.path.basename(os.path.dirname(image_path))
            
            
            backed_up_map_dir = backed_up_bg_dir+'\\'+osu_map_name
            
            if not(os.path.exists(backed_up_map_dir)):
                
                os.makedirs(backed_up_map_dir)
            if '.' in image_path:

                shutil.move(image_path,backed_up_map_dir)

#Gets images from the backed up backgrounds folder and puts them back into the folder of the song it was taken from
def restore_bgs(osu_songs_dir, backed_up_bgs_dir):
    if not(os.path.exists(backed_up_bgs_dir)):
        raise(Exception('No backgrounds saved yet!'))

    saved_maps_names= os.walk(backed_up_bgs_dir).__next__()[1]
    
    for saved_map in saved_maps_names:
        backed_up_dir_contents_paths = [backed_up_bgs_dir+'\\'+saved_map+'\\'+i for i in os.walk(backed_up_bgs_dir+'\\'+saved_map).__next__()[2]]
        
        for image_path in backed_up_dir_contents_paths:
            if os.path.exists(osu_songs_dir+'\\'+saved_map):

                shutil.move(image_path,osu_songs_dir+'\\'+saved_map)
            
        

