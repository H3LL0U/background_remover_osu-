from typing import Tuple, Callable
import background_remover_functions
from customtkinter import *
from customtkinter import CTkImage
import tkinter.scrolledtext as scrolledtext
from tkinter import *
from PIL import Image
from tkinter import filedialog, messagebox
from background_remover_functions import create_ask_window, find_all_osu_maps_folders, rename_image_to, copy_image_to_paths,copy_directories, get_background_images_paths, remove_backgrounds_fully

class change_backgrounds_selector(CTkToplevel):
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
        '''
        ans = create_ask_window("Are you sure you want to change all the backgrounds to the selected image?","change background images?")
        if ans:
                
            try:
                    
                all_osu_map_folders = find_all_osu_maps_folders(self.main_entry.osu_main_directory_var.get())
                self.remove_bg_confirm(self.main_entry.osu_main_directory_var)()
                self.log(["All of the images are being replaced..."])
                name, extension  = os.path.splitext(self.image_combobox.get())
                path_to_img = f"{os.getcwd()}\\default backgrounds\\{self.image_combobox.get()}"
                    
                if not(name.endswith("osu!_background_(re)mover")):
                    path_to_img = f"{os.getcwd()}\\default backgrounds\\{name+"osu!_background_(re)mover"+extension}"
                    rename_image_to(f"{os.getcwd()}\\default backgrounds\\{self.image_combobox.get()}", name+"osu!_background_(re)mover")
                    
                copy_image_to_paths(path_to_img,all_osu_map_folders)
                    
                rename_image_to(path_to_img,name.replace("osu!_background_(re)mover",''))
                self.log([f"the backgrounds have been replaced with {self.image_combobox.get()}"])







                    
            except Exception as error:
                    
                self.log([str(error)])  
                raise(error)

    def remove_bg_confirm(self,var) -> Callable[[], bool]:
        '''
        takes in a StringVar() that stores the osu directory and removes or stores the images dependent on the save mode
        if the images were saved successfuly the returned function returns True
        otherwise False
        '''
        
        def wrapper() -> bool:

            try:
                if self.menu.save_background_mode.get() and create_ask_window('Are you sure you want to move the files (They will be saved in a backed up backgrounds folder)', "remove the backgrounds?"):
                    copy_directories(self.winfo_toplevel(),get_background_images_paths(var.get(),False))
                    self.log(['ALL THE BACKGROUND IMAGES HAVE BEEN MOVED TO backed up backgrounds folder'])
                    
                elif self.menu.save_background_mode.get():
                    raise(Exception('The moving of the background images has been canceled'))
                else:
                    remove_backgrounds_fully(get_background_images_paths(var.get()))
                    self.log(["ALL THE BACKGROUND IMAGES HAVE BEEN DELETED!"])
                return True
            except Exception as error:
                messagebox.showerror("error",error)
                self.log([str(error)])
                return False
            
        return wrapper



    def log(self,text_to_add = []):
        self.log_area.log(text_to_add)


        