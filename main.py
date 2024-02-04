from background_remover_functions import remove_backgrounds_fully, os , find_directories, filedialog , messagebox , get_background_images_paths,open_info_window, shutil, copy_directories , create_ask_window, restore_bgs
from tkinter import *
import tkinter.scrolledtext as scrolledtext


    

root = Tk()
root.resizable(False, False)
root.geometry("500x500")
root.title("Osu! background remover")



#search through the directories to find the location that has osu!/Songs at the end
possible_directory = []
possible_directory_generator = find_directories("C:\\", "osu!\\Songs", root=root)
searching = False
def find_next_possible_location():
    
    global possible_directory , searching

    try:
        #checks if the search has started or not
        if searching:
            log(['The auto search was already started!'])
            return
        searching = True
        label = Label(possible_osu_directory_path_listbox_frame,text='Searching...')
        label.grid(column=3,row=1)
        possible_directory.append(possible_directory_generator.__next__())
        label.grid_forget()
        searching = False
        

        possible_osu_directory_path_listbox.insert(END,possible_directory[-1])
        log([f"NEW POSSIBLE DIRECTORY HAS BEEN FOUND:\n{possible_directory[-1]}"])
        possible_osu_directory_path_listbox.config(width= max((len(i) for i in possible_directory),default=1))
    except:
        label.grid_forget()
        search_button.grid_forget()
        log(["ALL THE DIRECTORIES ON YOUR COMPUTER HAVE BEEN CHECKED"])


main_frame = Frame(root)
main_frame.pack()

#Settings menu------------------------------
menu = Menu(root,tearoff=0)
menu_cascade = Menu(menu,tearoff=0)

save_background_mode = BooleanVar()
save_background_mode.set(True)
menu_cascade.add_checkbutton(label='Save the backgrounds', variable=save_background_mode)

menu_cascade.add_command(label="info",command=lambda: log([
    '''How does it work?
You can download the repo and open the executable in the build folder.
From there you can select the osu!/Songs folder where all of your songs files are located.
(You can do it manually by pressing the Manual search button or let the app find the possible location for you by pressing the auto search button)
if you selected the right folder all the background images paths will be displayed bellow in the Log text area
You can then proceed by pressing the Confirm button and confirming your actions.
Congratulations! All of the backgrounds have been deleted!
''']
))
menu.add_cascade(menu=menu_cascade ,label='Settings')

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

root.configure(menu=menu)
#Description label

Label(main_frame,text="Sellect the osu/songs path:").pack()

#create entry for user to type his osu directory
osu_main_directory_var = StringVar()
path_text_box = Entry(main_frame,textvariable=osu_main_directory_var)
path_text_box.pack()


#adjust width with the input
def adjust_width(var,widget):
    def wrapper(*k):
        if len(var.get())>20:
            widget.config(width = len(var.get()))
    return wrapper

osu_main_directory_var.trace_add(mode="write",callback=adjust_width(osu_main_directory_var,path_text_box))



#create the Listbox with posible directories that were found by the auto or manual search
possible_osu_directory_path_listbox_frame = Frame(main_frame)
possible_osu_directory_path_listbox_frame.pack()
possible_osu_directory_path_listbox = Listbox(possible_osu_directory_path_listbox_frame, height=len(possible_directory), width = max((len(i) for i in possible_directory),default=1),)





#change the entry value to the one of a selected ellement of the listbox
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

#Create auto - search button
search_button = Button(possible_osu_directory_path_listbox_frame, text='🔍', command=find_next_possible_location,)
search_button.grid(column=2,row=1,padx=20)

#manual - search button-------------------------------
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
        possible_osu_directory_path_listbox.config(width= min(max((len(i) for i in possible_directory),default=1),40))
    except Exception as error:
        log([str(error)])
manual_search_button = Button(possible_osu_directory_path_listbox_frame,text="Manual Search",command=manual_search_func)
manual_search_button.grid(column=0,row=1,padx=20)


#Create the confirm button-----------------------------------------

#removesimages from osu!/Songs path is set correctly var = osu!/Songs directory
def remove_bg_confirm(var):
    def wrapper():

        try:
            if save_background_mode.get() and create_ask_window('Are you sure you want to move the files (They will be saved in a backed up backgrounds folder)'):
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

confirm_the_removal = Button(root,text="Confirm", command=remove_bg_confirm(osu_main_directory_var))
confirm_the_removal.pack()
#create the log space----------------------------------------
#takes in a tuple of strings and inserts it into the Log space 
def log(text_to_add = []):
    Log_textarea.config(state=NORMAL)
    
    for i in text_to_add:
        Log_textarea.insert(END,i+"\n")
        Log_textarea.insert(END," \n")
        
    Log_textarea.insert(END,"-"*50 )
    Log_textarea.config(state = DISABLED)

Log_textarea_frame = Frame(root)
Log_textarea_frame.pack()
Log_textarea = scrolledtext.ScrolledText(Log_textarea_frame, width = 50,state = DISABLED)
log(["WELCOME TO OSU! BACKGROUND REMOVER!"])


Log_textarea.grid(row=0,column=0)
#create clear button----------------------------
def clear_Log():
    Log_textarea.config(state=NORMAL)
    Log_textarea.delete(0.0,END)
    Log_textarea.config(state=DISABLED)
    
    

clear_button_frame = Frame(root)
clear_button_frame.pack()
clear_button = Button(clear_button_frame,text='Clear Log',command=clear_Log)
clear_button.pack()

#Create warning if the remove backgrounds fully is active:
warning_label = Label(root,text='WARNING: \n your backgrounds\n will not be saved', bg='yellow', font = ('Arial', 7))
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
