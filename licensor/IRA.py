# from HomeFrame import *
# import config
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from validater import license_checker
# import myIra

#--------------------------------    
#--- set configurations
#--------------------------------    
# config.clear_contexts()
# config.clear_defaults()
# config.get_displayInfo()
#--------------------------------    
#--------------------------------    
def starting_up():
    """start up function"""
    try:
        checker = license_checker()
        if os.path.exists('ira.lic'):
            #check old license key
            checker.read_licInfo()
            if checker.time_left.days > 0:
                # config.load_defaults()
                
                #now start homeframe
                # hf = HomeFrame()
                # hf.get_tkItem().after(1, config.close_roots)
                # config.home_frame = hf
                messagebox.showinfo('Starting up existing license', 'Write start up code here')

                # #starting the myIRA guidance bot
                # MI = myIra.MyIRA()
                # config.MyIRA_guide = MI 
                # hf.add_buttons() #needs to be done again after creating MI to install guidance in homeframe buttons
                # hf.add_workflows() #needs to be done again for event binding

                # hf.show()
                # MI.show()
                # config.close_roots()

            else:
                messagebox.showinfo(title='License Expired', message="License Expired! Please contact IRA Customer Service.", parent=start_win)
        else:
            #get new license key
            new_key = simpledialog.askstring(title="Welcome to IRA by 27Two", prompt="Enter a valid license Key", parent=start_win )
            if( checker.verify_licKey(new_key) ):
                checker.save_licKey()
                # config.load_defaults()
                messagebox.showinfo('Starting up new license', 'Write start up code here')

                #now start homeframe
                # hf = HomeFrame()
                # hf.get_tkItem().after(1, config.close_roots)
                # config.home_frame = hf
                
                #starting the myIRA guidance bot
                # MI = myIra.MyIRA()
                # config.MyIRA_guide = MI 
                # hf.add_buttons() #needs to be done again after creating MI to install guidance in homeframe buttons
                # hf.add_workflows() #needs to be done again for event binding

                # hf.show()
                # MI.show()
                # config.close_roots()

            else:
                messagebox.showerror("Invalid License", "Please check the license key, enter or copy-paste carefully next time.", parent=start_win )

    except Exception as e:
        messagebox.showerror('Ooops!', "We experienced a license related issue. Kindly call IRA customer Care.")
        print(str(e))

#-------------------- start up code -------------
if __name__ == '__main__':
    start_win = tk.Tk()
    # import all_styles
    # config.all_roots.append(start_win)
    start_win.title('Starting up IRA...')
    start_win.geometry('200x200+50+50')
    start_win.withdraw()
    starting_up()
