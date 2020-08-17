'''File Explorer
This Tk based GUI application allows the user to explore the files in their system.
User can navigate through the folders but cannot open the files from this application.
Includes features like like searching and copy-paste. 
'''

from myobjects import *

#creating the application main window.   
top = Tk()
top.title("File Explorer")

mlb = ExplorerFrame(top, (('Name', 60), ('Type', 10)))
mlb.pack(expand=YES,fill=BOTH)

#Entering the event main loop  
top.mainloop()  
