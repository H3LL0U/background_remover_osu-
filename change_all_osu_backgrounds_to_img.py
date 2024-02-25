from typing import Tuple, Callable
import background_remover_functions
from customtkinter import *
from customtkinter import CTkImage
import tkinter.scrolledtext as scrolledtext
from tkinter import *
from PIL import Image
from tkinter import filedialog, messagebox
from background_remover_functions import create_ask_window, find_all_osu_maps_folders, rename_image_to, copy_image_to_paths,copy_directories, get_background_images_paths, remove_backgrounds_fully
from widget_methods import Widget_methods




class change_backgrounds_selector(CTkToplevel,Widget_methods):
    '''
    Window for selecting and uploading default backgrounds to set in place of the old ones
    '''
    def __init__(self,pathfinder ,main_entry, log_area, menu, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        self.menu = menu
        self.pathfinder = pathfinder
        self.main_entry = main_entry
        self.log_area = log_area

        self.resizable(False,False)
        self.main_frame = CTkFrame(self)
        self.main_frame.pack()
        self.title("Change backgrounds to image")

        self.warning = CTkLabel(self.main_frame, bg_color='yellow',text='Warning: After you apply the background image all the maps will become unranked',text_color="black")
        self.warning.pack()

        self.label = CTkLabel(self.main_frame,text="Select an image to replace all your backgrounds with")
        self.label.pack(pady = 10,padx = 10)
        self.image_combobox_var = list(background_remover_functions.find_all_default_images_names())

        

        def on_image_select(*k):
            image_selected = self.image_combobox.get()
            image_path = os.getcwd()+"\\default backgrounds\\"+image_selected
            new_image = CTkImage(Image.open(image_path),size=(250,250))
            self.image_label.configure(image=new_image)
            self.label_text_image.configure(text = image_selected)
        self.image_combobox_frame = CTkFrame(self.main_frame)
        self.image_combobox_frame.pack(pady = 10)
        self.image_combobox = CTkComboBox(master=self.image_combobox_frame,values=self.image_combobox_var, state='readonly', command=on_image_select)

        
        self.image_combobox.grid(column = 0,row = 0)

        def refresh():
        
            self.image_combobox_var = list(background_remover_functions.find_all_default_images_names())
            self.image_combobox.configure(values = self.image_combobox_var )

        self.refresh_button = CTkButton(self.image_combobox_frame,width=28, text="⟳", command=refresh)
        self.refresh_button.grid(column=1,row = 0, padx = 5)

        def upload_image():
            selected_files = filedialog.askopenfilenames(title="Choose images you want to upload")
            for file in selected_files:
                background_remover_functions.copy_image_to_default_images(file)
            
        self.upload_button = CTkButton(self.main_frame, text="Upload image", command=upload_image)
        self.upload_button.pack(pady = 10)
        self.confirm_select_button = CTkButton(self.main_frame,text="Confirm", command= self.change_background_to_img_confirm)
        self.confirm_select_button.pack(pady = 10)
        self.label_text_image = CTkLabel(self.main_frame, text="")
        self.label_text_image.pack(pady = 10, padx = 10)
        self.image_label = CTkLabel(self.main_frame,image=None, text="")
        self.image_label.pack(padx = 10,pady=10)
    def change_background_to_img_confirm(self) -> None:
        '''
        Changes the background images in all osu maps to the selected image
        adds osu!_background_(re)mover at the end of the image's name
        '''
        try:
            ans = create_ask_window("Are you sure you want to change all the backgrounds to the selected image?","change background images?")
            if ans:
                    
                
                        
                all_osu_map_folders = find_all_osu_maps_folders(self.main_entry.osu_main_directory_var.get())
                ans = self.remove_bg_confirm(self.main_entry.osu_main_directory_var)()
                if not ans:
                    raise(Exception('The moving of the images has been canceled'))
                    
                name, extension  = os.path.splitext(self.image_combobox.get())
                path_to_img = f"{os.getcwd()}\\default backgrounds\\{self.image_combobox.get()}"
                        
                if not(name.endswith("osu!_background_(re)mover")):
                    path_to_img = f"{os.getcwd()}\\default backgrounds\\{name+"osu!_background_(re)mover"+extension}"
                    rename_image_to(f"{os.getcwd()}\\default backgrounds\\{self.image_combobox.get()}", name+"osu!_background_(re)mover")
                        
                copy_image_to_paths(path_to_img,all_osu_map_folders)
                        
                rename_image_to(path_to_img,name.replace("osu!_background_(re)mover",''))
                self.log([f"the backgrounds have been replaced with {self.image_combobox.get()}"])
            else:
                raise(Exception('The moving of the images has been canceled'))






                    
        except Exception as error:
                    
            self.log([str(error)])  
                






        