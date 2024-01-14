import os
#import wxPython
import tkinter as tk
from tkinter import filedialog


#might imploment a propper GUI later
'''
def create_ask_window(text_to_display = ""):
    response = messagebox.askyesnocancel("remove_the_files",f"are you sure you want to remove\n{text_to_display}")
    if response is None:
        return None
    elif response:
        return True
    else:
        return False
''' 
    
    

#store the osu song directory
osu_directory = filedialog.askdirectory(title="select the 'osu!/Songs' folder (from there all the images that are more than 100000 bytes will be removed)")

#checks if the directory has !osu in the path just in case
if not(osu_directory) or(not("osu!" in osu_directory) and osu_directory[-6]!="/Songs"):
    raise(
        Exception("The drectory you specified does not have word osu! in it. Please select one that does.\n (It is made for the safety of your files)")
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

                
            if item[-4:] == ".jpg" or item[-4:] == ".png":
                path_items_to_remove.append(f"{folder}/{item}")
except:
    raise(
        Exception("you have chosen the wrong directory")
    )


#remove the files from the selected paths



for i in path_items_to_remove:
    #remove images that are bigger than 100000 bytes (so that most of the time only background images get removed)
    if (i[-4:] == ".png" or i[-4:]== ".jpg") and os.path.getsize(i)>100000:
            
        #checks if the path exists and i is not "" just in case
        if os.path.exists(i) and i:
            #ask user for confirmation
            
            
            
            
            os.remove(i)


