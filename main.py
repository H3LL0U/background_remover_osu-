from background_remover import remove_backgrounds_fully, os , find_directories, filedialog
from tkinter import *
#try to find an osu! directory location
possible_directory = []
possible_directory_generator = find_directories("C:/", "osu!\Songs")
def find_next_possible_location():
    
    global possible_directory
    try:
    
        
        possible_directory.append(possible_directory_generator.__next__())
        #initialize first ellements in the listbox

        possible_osu_directory_path_listbox.insert(END,possible_directory[-1])
        possible_osu_directory_path_listbox.config(width= max((len(i) for i in possible_directory),default=1))
    except:
        search_button.grid_forget()
        print("all the directories have been looped through")


    
        



root = Tk()
root.geometry("500x500")
root.title("Osu! background remover")

main_frame = Frame(root)
main_frame.pack()


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



#create the Listbox with posible directories that the program has found
possible_osu_directory_path_listbox_frame = Frame(main_frame)
possible_osu_directory_path_listbox_frame.pack()
possible_osu_directory_path_listbox = Listbox(possible_osu_directory_path_listbox_frame, height=len(possible_directory), width = max((len(i) for i in possible_directory),default=1))





#change the entry value to the one of a selected ellement of the listbox
def auto_change_osu_path_entry(*ok):
    try:
        osu_main_directory_var.set(possible_directory[possible_osu_directory_path_listbox.curselection()[0]])
    except:
        pass

possible_osu_directory_path_listbox.bind("<<ListboxSelect>>",auto_change_osu_path_entry)

possible_osu_directory_path_listbox.grid(column=1,row=1)

#Create auto - search button
search_button = Button(possible_osu_directory_path_listbox_frame, text='🔍', command=find_next_possible_location)
search_button.grid(column=2,row=1)

#manual - search button
def manual_search_func():
    osu_main_directory_var.set(filedialog.askdirectory(parent=root ,title="Select osu!/songs folder"))
manual_search_button = Button(possible_osu_directory_path_listbox_frame,text="Manual Search",command=manual_search_func)
manual_search_button.grid(column=0,row=1)


#Create the confirm button

def remove_bg_confirm(var):
    def wrapper():
        
        remove_backgrounds_fully(var.get())
    return wrapper

confirm_the_removal = Button(root,text="Confirm", command=remove_bg_confirm(osu_main_directory_var))
confirm_the_removal.pack()


root.mainloop()
