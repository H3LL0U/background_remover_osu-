from typing import Tuple
import background_remover_functions
from customtkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import *


class change_backgrounds_selector(CTkToplevel):
    '''
    Window for selecting and uploading default backgrounds to set in place of the old ones
    '''
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.main_frame = CTkFrame(self)
        self.main_frame.pack()
        
        self.label = CTkLabel(self.main_frame,text="Select an image to replace all your backgrounds with")
        self.label.pack(pady = 10)
        self.image_combobox_var = list(background_remover_functions.find_all_default_images_paths())
        self.image_combobox = CTkComboBox(master=self.main_frame,variable=self.image_combobox_var)
        
        
        self.image_combobox.pack(pady = 10)