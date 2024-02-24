from typing import Tuple
from background_remover_functions import remove_backgrounds_fully , find_directories, filedialog , messagebox , get_background_images_paths, shutil, copy_directories , create_ask_window, restore_bgs,find_all_osu_maps_folders, rename_image_to, copy_image_to_paths
from customtkinter import *

import tkinter.scrolledtext as scrolledtext
from tkinter import *
from change_all_osu_backgrounds_to_img import change_backgrounds_selector
from typing import *
from typing import Any, Tuple


#==========================ROOT==================================================



class MainWindow(CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        self.resizable(False, False)
        
        self.title("Osu! background remover")


class MainEntry(CTkFrame):
    def __init__(self, master: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        CTkLabel(self,text="Sellect the osu/songs path:").pack()

#===============================osu!/Songs PATH ENTRY============================
        self.osu_main_directory_var = StringVar()
        self.path_text_box = CTkEntry(self,textvariable=self.osu_main_directory_var,)
        self.path_text_box.pack()



        def adjust_width(var,widget):
            def wrapper(*k):
                if len(var.get())>20:
                    widget.configure(width = min(len(var.get())*7-5,400))
            return wrapper

        self.osu_main_directory_var.trace_add(mode="write",callback=adjust_width(self.osu_main_directory_var,self.path_text_box))
        





class LogSpace(CTkFrame):
    def __init__(self, master: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        #=========================LOG SPACE----------------------------------------
#takes in a tuple of strings and inserts it into the Log space 
        

        Log_textarea_frame = CTkFrame(self)
        Log_textarea_frame.pack()
        self.Log_textarea = CTkTextbox(Log_textarea_frame,state = DISABLED, width=400, height=300,wrap=WORD )
        self.Log_textarea.tag_config('center', justify= 'center')
        self.log(["WELCOME TO OSU! BACKGROUND REMOVER!"])


        self.Log_textarea.grid(row=0,column=0)
        #=========================CLEAR BUTTON (LOG)----------------------------

            
            

        clear_button_frame = CTkFrame(self)
        clear_button_frame.pack()
        clear_button = CTkButton(clear_button_frame,text='Clear Log',command=self.clear_Log)
        clear_button.pack()
    def log(self,text_to_add = []):
        self.Log_textarea.configure(state=NORMAL)
            
        for i in text_to_add:

            self.Log_textarea.insert(END,i+"\n", 'center')
            self.Log_textarea.insert(END," \n")
            
        self.Log_textarea.insert(END,"="*50, 'center' )
        self.Log_textarea.insert(END, "\n")
        self.Log_textarea.yview_moveto(1)
        self.Log_textarea.configure(state = DISABLED)
    def clear_Log(self):
        self.Log_textarea.configure(state=NORMAL)
        self.Log_textarea.delete(0.0,END)
        self.Log_textarea.configure(state=DISABLED)

class PathFinder(CTkFrame):

    def __init__(self, master: Any, osu_main_directory_entry:MainEntry, logarea:LogSpace, menu, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        self.logarea = logarea
        self.menu = menu
        self.osu_main_directory_entry = osu_main_directory_entry
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        #======================search through the directories to find the location that has osu!/Songs at the end (see AUTO SEARCH)========================
        self.possible_directory = []
        self.possible_directory_generator = find_directories("C:\\", "osu!\\Songs", root=master)
        self.searching = False

        self.possible_osu_directory_path_listbox_frame = CTkFrame(self)
        self.possible_osu_directory_path_listbox_frame.pack(pady = 25)
        self.possible_osu_directory_path_listbox = Listbox(self.possible_osu_directory_path_listbox_frame, height=5, width=26,font=('Arial',13))#max((len(i) for i in possible_directory),default=10))





        #=================================LISTBOX --> ENTRY ON SELECTION====================

        self.possible_osu_directory_path_listbox.bind("<<ListboxSelect>>",self.auto_change_osu_path_entry)

        self.possible_osu_directory_path_listbox.grid(column=1,row=1)



        #================================Search indicator==============================
        self.searching_indicator = CTkLabel(self.possible_osu_directory_path_listbox_frame, text='                     ')
        self.searching_indicator.grid(column=4,row=1)




        #================================AUTO SEARCH==================
        self.search_button = CTkButton(self.possible_osu_directory_path_listbox_frame, text='🔍', command=self.find_next_possible_location,width=10)
        self.search_button.grid(column=2,row=1,padx=20)


        self.manual_search_button = CTkButton(self.possible_osu_directory_path_listbox_frame,text="Manual Search",command=self.manual_search_func, width=110)
        self.manual_search_button.grid(column=0,row=1,padx=20)


        #===========================Create the confirm button-----------------------------------------
        self.confirm_the_removal = CTkButton(self,text="Confirm", command=self.remove_bg_confirm(osu_main_directory_entry.osu_main_directory_var))
        self.confirm_the_removal.pack()
        
    def log(self,text_to_add = []):
        self.logarea.log(text_to_add)
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


    def find_next_possible_location(self):
            
            

        try:
                
            if self.searching:
                self.log(['The auto search was already started!'])
                return
            self.searching = True
                
            self.searching_indicator.configure(text='Searching...')
                
            self.possible_directory.append(self.possible_directory_generator.__next__())
            self.searching_indicator.configure(text='                  ')
            self.searching = False
                

            self.possible_osu_directory_path_listbox.insert(END,self.possible_directory[-1])
            self.log([f"NEW POSSIBLE DIRECTORY HAS BEEN FOUND:\n{self.possible_directory[-1]}"])
                #possible_osu_directory_path_listbox.config(width= max((len(i) for i in possible_directory),default=1))
        except Exception as error:
            self.searching_indicator.grid_forget()
            self.search_button.grid_forget()
            self.log(["ALL THE DIRECTORIES ON YOUR COMPUTER HAVE BEEN CHECKED", str(error)])
        #===============================MANUAL SEARCH===================
    def manual_search_func(self):
            
        try:
            possible_directory_to_add = filedialog.askdirectory(parent=self ,title="Select osu!/Songs folder")
            if possible_directory_to_add in self.possible_directory:
                 raise(Exception("SELECTED DIRECTORY ALREADY EXISTS IN THE LISTBOX"))
            if not(possible_directory_to_add):
                raise(Exception("YOU DID NOT SELECT A DIRECTORY"))
            self.possible_directory.append(possible_directory_to_add)
            self.possible_osu_directory_path_listbox.insert(END,self.possible_directory[-1])
            self.log(["SELECTED DIRECTORY HAS BEEN ADDED:", possible_directory_to_add])
                
        except Exception as error:
            self.log([str(error)])




    def auto_change_osu_path_entry(self,*ok):
        
        try:
            self.osu_main_directory_entry.osu_main_directory_var.set(self.possible_directory[self.possible_osu_directory_path_listbox.curselection()[0]])
        except:
            pass
        try:
            self.log(["PATHS TO BACKGROUNDS TO REMOVE ARE:", *get_background_images_paths(self.osu_main_directory_entry.osu_main_directory_var.get(),False)])
                
        except Exception as error:
            self.log([str(error)])







class CustomMenuPart(Menu):
    
    def __init__(self, logarea:LogSpace ,main_entry, pathfinder, root: Misc | None = None, activebackground: str = ..., activeborderwidth: str | float = ..., activeforeground: str = ..., background: str = ..., bd: str | float = ..., bg: str = ..., border: str | float = ..., borderwidth: str | float = ..., cursor: str | tuple[str] | tuple[str, str] | tuple[str, str, str] | tuple[str, str, str, str] = ..., disabledforeground: str = ..., fg: str = ..., foreground: str = ..., name: str = ..., postcommand: Callable[[], object] | str = ..., relief: Literal['raised', 'sunken', 'flat', 'ridge', 'solid', 'groove'] = ..., selectcolor: str = ..., takefocus: int | Callable[[str], bool | None] | Literal[''] = ..., tearoff: int = ..., tearoffcommand: Callable[[str, str], object] | str = ..., title: str = ..., type: Literal['menubar', 'tearoff', 'normal'] = ...) -> None:
        self.logarea = logarea
        self.main_entry = main_entry
        self.pathfinder = pathfinder
        super().__init__(root,tearoff=tearoff)
        
        self.menu_cascade = Menu(self,tearoff=0)

        self.save_background_mode = BooleanVar()
        self.save_background_mode.set(True)
        self.menu_cascade.add_checkbutton(label='Save the backgrounds', variable=self.save_background_mode)

        self.menu_cascade.add_command(label="info",command=lambda: self.log([
            '''
        How does it work?

        You can select the osu!/Songs folder where all of your songs files are located.(You can do it manually by pressing the Manual search button or let the app find the possible location for you by pressing the auto search button)if you selected the right folder all the background images paths will be displayed bellow in the Log text area. You can then proceed by pressing the Confirm button and confirming your actions.
        Congratulations! All of the backgrounds have been moved to the backed up backgrounds folder!

        Restoring previously saved backgrounds:

        If you want to restore your backgrounds that you previously saved you can select your osu!/Songsfolder once again and press 'restore backgrounds' in the upper menu. After confirming the backgrounds will be back for each song that you have previously saved!

        Deleting backgrounds permenantly:

        If you want to delete your backgrounds permenantly you can uncheck the 'Save backgrounds' from the settings. and proceed the same way as if you were saving the backgrounds.
        ''']
        ))
        #================A SEPERATE WINDOW FOR CHANGING BACKGROUNDS TO AN IMAGE=================



        self.change_background_to_img_window = None

        self.add_command(label="Change to selected background", command=self.open_change_background_selector)
        self.add_cascade(menu=self.menu_cascade ,label='Settings')
        #=========================RESTORE BACKGROUNDS BUTTON==========================


                
        self.add_command(label='Restore backgrounds', command=self.restoration)
        #==========================Dark/Lightmode switcher================================
        self.Darkmode_checkbutton_var = BooleanVar()
        self.Darkmode_checkbutton_var.set(True)



        self.add_checkbutton(label='Light mode',command=self.change_visual_mode,variable=self.Darkmode_checkbutton_var)
        #=====================WARNING FOR DELETION==========================
        self.warning_label = CTkLabel(root,text='WARNING: \n your backgrounds\n will not be saved', font = ('Arial', 7), bg_color='yellow', text_color='black')
        if not(self.save_background_mode.get()):
            self.warning_label.place(x = 0,y=0)

            
        self.save_background_mode.trace_add('write',callback=self.add_warning)
    def add_warning(self,*k):
        current_mode = self.save_background_mode.get()
            
                
        if current_mode:
            self.warning_label.place_forget()
        else:
            self.warning_label.place(x = 0, y =0)

    def open_change_background_selector(self) -> None:
            
        try:
            window_opened = self.change_background_to_img_window.winfo_exists()
        except:
            window_opened = False
        if not window_opened:
            self.change_background_to_img_window =change_backgrounds_selector(self.pathfinder,self.main_entry,self.logarea,self)
        else:
            self.log(['You have already opened up a window'])
    def change_visual_mode(self):
        if (self.Darkmode_checkbutton_var.get()):
            set_appearance_mode('dark')
            self.entryconfigure('Dark mode', label='Light mode')
        else:
            self.entryconfigure('Light mode', label='Dark mode')
            set_appearance_mode('light')

    def restoration(self):
        try:
            ask_user = create_ask_window('Are you sure you want to restore the backgrounds you saved? to the selected osu!/Songs folder?', "restore backgrounds?")
            if ask_user:
                #checks if this directory can be considered as an osu dir
                list(get_background_images_paths(self.main_entry.osu_main_directory_var.get(),False))
                restore_bgs(self.main_entry.osu_main_directory_var.get(),os.getcwd()+'\\backed up backgrounds')
                self.log(['all the backgrounds have been restored!'])

                    
        except Exception as error:
            self.log([str(error)])





    def log(self,text_to_add = []):
        self.logarea.log(text_to_add)