from background_remover_functions import remove_backgrounds_fully, os , find_directories, filedialog , messagebox , get_background_images_paths, shutil, copy_directories , create_ask_window, restore_bgs
from customtkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import *

    
#==========================ROOT==================================================
root = CTk()
root.resizable(False, False)
root.geometry("500x575")
root.title("Osu! background remover")



#======================search through the directories to find the location that has osu!/Songs at the end (see AUTO SEARCH)========================
possible_directory = []
possible_directory_generator = find_directories("C:\\", "osu!\\Songs", root=root)
searching = False
def find_next_possible_location():
    
    global possible_directory , searching, searching_indicator

    try:
        
        if searching:
            log(['The auto search was already started!'])
            return
        searching = True
        
        searching_indicator.configure(text='Searching...')
        
        possible_directory.append(possible_directory_generator.__next__())
        searching_indicator.configure(text='                  ')
        searching = False
        

        possible_osu_directory_path_listbox.insert(END,possible_directory[-1])
        log([f"NEW POSSIBLE DIRECTORY HAS BEEN FOUND:\n{possible_directory[-1]}"])
        #possible_osu_directory_path_listbox.config(width= max((len(i) for i in possible_directory),default=1))
    except Exception as error:
        searching_indicator.grid_forget()
        search_button.grid_forget()
        log(["ALL THE DIRECTORIES ON YOUR COMPUTER HAVE BEEN CHECKED", str(error)])
        

#========================Settings menu============================
main_frame = CTkFrame(root)
main_frame.pack()


menu = Menu(root,tearoff=0)
menu_cascade = Menu(menu,tearoff=0)

save_background_mode = BooleanVar()
save_background_mode.set(True)
menu_cascade.add_checkbutton(label='Save the backgrounds', variable=save_background_mode)

menu_cascade.add_command(label="info",command=lambda: log([
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
menu.add_cascade(menu=menu_cascade ,label='Settings')
#=========================RESTORE BACKGROUNDS BUTTON==========================

def restoration():
    try:
        ask_user = create_ask_window('Are you sure you want to restore the backgrounds you saved? to the selected osu!/Songs folder?')
        if ask_user:
            #checks if this directory can be considered as an osu dir
            list(get_background_images_paths(osu_main_directory_var.get(),False))
            restore_bgs(osu_main_directory_var.get(),os.getcwd()+'\\backed up backgrounds')
            log(['all the backgrounds have been restored!'])

            
    except Exception as error:
        log([str(error)])
        
menu.add_command(label='Restore backgrounds', command=restoration)
#==========================Dark/Lightmode switcher================================
Darkmode_checkbutton_var = BooleanVar()
Darkmode_checkbutton_var.set(True)

def change_visual_mode():
    if (Darkmode_checkbutton_var.get()):
        set_appearance_mode('dark')
        menu.entryconfigure('Dark mode', label='Light mode')
    else:
        menu.entryconfigure('Light mode', label='Dark mode')
        set_appearance_mode('light')

menu.add_checkbutton(label='Light mode',command=change_visual_mode,variable=Darkmode_checkbutton_var)
root.configure(menu=menu)
#Description label

CTkLabel(main_frame,text="Sellect the osu/songs path:").pack()

#===============================osu!/Songs PATH ENTRY============================
osu_main_directory_var = StringVar()
path_text_box = CTkEntry(main_frame,textvariable=osu_main_directory_var,)
path_text_box.pack()



def adjust_width(var,widget):
    def wrapper(*k):
        if len(var.get())>20:
            widget.configure(width = min(len(var.get())*7-5,400))
    return wrapper

osu_main_directory_var.trace_add(mode="write",callback=adjust_width(osu_main_directory_var,path_text_box))



#==========================LISTBOX FOR POSSIBLE PATHS==============================
possible_osu_directory_path_listbox_frame = CTkFrame(main_frame)
possible_osu_directory_path_listbox_frame.pack(pady = 25)
possible_osu_directory_path_listbox = Listbox(possible_osu_directory_path_listbox_frame, height=5, width=26,font=('Arial',13))#max((len(i) for i in possible_directory),default=10))





#=================================LISTBOX --> ENTRY ON SELECTION====================
def auto_change_osu_path_entry(*ok):
    
    try:
        osu_main_directory_var.set(possible_directory[possible_osu_directory_path_listbox.curselection()[0]])
    except:
        pass
    try:
        log(["PATHS TO BACKGROUNDS TO REMOVE ARE:", *get_background_images_paths(osu_main_directory_var.get(),False)])
        
    except Exception as error:
        log([str(error)])
possible_osu_directory_path_listbox.bind("<<ListboxSelect>>",auto_change_osu_path_entry)

possible_osu_directory_path_listbox.grid(column=1,row=1)



#================================Search indicator==============================
searching_indicator = CTkLabel(possible_osu_directory_path_listbox_frame, text='                     ')
searching_indicator.grid(column=4,row=1)




#================================AUTO SEARCH==================
search_button = CTkButton(possible_osu_directory_path_listbox_frame, text='🔍', command=find_next_possible_location,width=10)
search_button.grid(column=2,row=1,padx=20)

#===============================MANUAL SEARCH===================
def manual_search_func():
    global possible_directory
    try:
        possible_directory_to_add = filedialog.askdirectory(parent=root ,title="Select osu!/Songs folder")
        if possible_directory_to_add in possible_directory:
            raise(Exception("SELECTED DIRECTORY ALREADY EXISTS IN THE LISTBOX"))
        if not(possible_directory_to_add):
            raise(Exception("YOU DID NOT SELECT A DIRECTORY"))
        possible_directory.append(possible_directory_to_add)
        possible_osu_directory_path_listbox.insert(END,possible_directory[-1])
        log(["SELECTED DIRECTORY HAS BEEN ADDED:", possible_directory_to_add])
        
    except Exception as error:
        log([str(error)])
manual_search_button = CTkButton(possible_osu_directory_path_listbox_frame,text="Manual Search",command=manual_search_func, width=110)
manual_search_button.grid(column=0,row=1,padx=20)


#===========================Create the confirm button-----------------------------------------


def remove_bg_confirm(var):
    def wrapper():

        try:
            if save_background_mode.get() and create_ask_window('Are you sure you want to move the files (They will be saved in a backed up backgrounds folder)', "remove the backgrounds?"):
                copy_directories(get_background_images_paths(var.get(),False))
                log(['ALL THE BACKGROUND IMAGES HAVE BEEN MOVED TO backed up backgrounds folder'])
            
            elif save_background_mode.get():
                raise(Exception('The moving of the background images has been canceled'))

            else:
                remove_backgrounds_fully(get_background_images_paths(var.get()))
                log(["ALL THE BACKGROUND IMAGES HAVE BEEN DELETED!"])
        except Exception as error:
            messagebox.showerror("error",error)
            log([str(error)])
    return wrapper

confirm_the_removal = CTkButton(root,text="Confirm", command=remove_bg_confirm(osu_main_directory_var))
confirm_the_removal.pack()
#=========================LOG SPACE----------------------------------------
#takes in a tuple of strings and inserts it into the Log space 
def log(text_to_add = []):
    Log_textarea.configure(state=NORMAL)
    
    for i in text_to_add:

        Log_textarea.insert(END,i+"\n", 'center')
        Log_textarea.insert(END," \n")
    
    Log_textarea.insert(END,"="*50, 'center' )
    Log_textarea.insert(END, "\n")
    Log_textarea.yview_moveto(1)
    Log_textarea.configure(state = DISABLED)

Log_textarea_frame = CTkFrame(root)
Log_textarea_frame.pack()
Log_textarea = CTkTextbox(Log_textarea_frame,state = DISABLED, width=400, height=300,wrap=WORD )
Log_textarea.tag_config('center', justify= 'center')
log(["WELCOME TO OSU! BACKGROUND REMOVER!"])


Log_textarea.grid(row=0,column=0)
#=========================CLEAR BUTTON (LOG)----------------------------
def clear_Log():
    Log_textarea.configure(state=NORMAL)
    Log_textarea.delete(0.0,END)
    Log_textarea.configure(state=DISABLED)
    
    

clear_button_frame = CTkFrame(root)
clear_button_frame.pack()
clear_button = CTkButton(clear_button_frame,text='Clear Log',command=clear_Log)
clear_button.pack()

#=====================WARNING FOR DELETION==========================
warning_label = CTkLabel(root,text='WARNING: \n your backgrounds\n will not be saved', font = ('Arial', 7), bg_color='yellow', text_color='black')
if not(save_background_mode.get()):
    warning_label.place(x = 0,y=0)
def add_warning(*k):
    current_mode = save_background_mode.get()
    
        
    if current_mode:
        warning_label.place_forget()
    else:
        warning_label.place(x = 0, y =0)
    
save_background_mode.trace_add('write',callback=add_warning)

root.mainloop()
