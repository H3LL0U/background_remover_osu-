from typing import Tuple
import background_remover_functions
from customtkinter import *
from customtkinter import CTkImage
import tkinter.scrolledtext as scrolledtext
from tkinter import *
from PIL import Image

class change_backgrounds_selector(CTkToplevel):
    '''
    Window for selecting and uploading default backgrounds to set in place of the old ones
    '''
    def __init__(self, button_command = None, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
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
            
        self.image_combobox = CTkComboBox(master=self.main_frame,values=self.image_combobox_var, state='readonly', command=on_image_select)
        
        
        self.image_combobox.pack(pady = 10)

        self.confirm_select_button = CTkButton(self.main_frame,text="confirm", command= button_command)
        self.confirm_select_button.pack(pady = 10)
        self.label_text_image = CTkLabel(self.main_frame, text="")
        self.label_text_image.pack(pady = 10, padx = 10)
        self.image_label = CTkLabel(self.main_frame,image=None, text="")
        self.image_label.pack(padx = 10,pady=10)
        



        