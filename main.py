from main_widgets import *


if __name__ == "__main__":
    root = MainWindow()
    
    path_entry = MainEntry(root)
    log_area = LogSpace(root)
    
    

    menu = CustomMenuPart(log_area,path_entry,root,tearoff=0)
    find_path = PathFinder(root,path_entry,log_area,menu)

    path_entry.pack()
    find_path.pack()
    log_area.pack()

    root.configure(menu=menu)
    root.mainloop()