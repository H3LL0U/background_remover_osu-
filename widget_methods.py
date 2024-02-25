from background_remover_functions import *
from typing import *





class Widget_methods():
    def remove_bg_confirm(self,var) -> Callable[[], bool]:
        '''
        takes in a StringVar() that stores the osu directory and removes or stores the images dependent on the save mode
        if the images were saved successfuly the returned function returns True
        otherwise False
        '''
        
        def wrapper() -> bool:

            try:
                
                if self.menu.save_background_mode.get() and create_ask_window('Are you sure you want to move the files (They will be saved in a backed up backgrounds folder)', "remove the backgrounds?"):
                    copy_directories(self.winfo_toplevel(),get_background_images_paths(var.get(),False),self.main_entry.osu_main_directory_var.get())
                    
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
