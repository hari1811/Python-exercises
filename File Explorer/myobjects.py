from tkinter import *  
from pathlib import *
from tkinter import messagebox
import shutil
import re

class ExplorerFrame(Frame):
    def __init__(self, master, lists):
        Frame.__init__(self, master)
        self.lists = []

        OptionsFrame = Frame(self)  
        OptionsFrame.pack(side = TOP, fill = X) 

        backBtn = Button(OptionsFrame, text="<-", command = self._back).pack(side = LEFT)
        forwBtn = Button(OptionsFrame, text="->", command = self._forw).pack(side = LEFT)

        self.PathEntry = Entry(OptionsFrame, textvariable='path', width = 56)
        self.PathEntry.pack(side = LEFT, expand=YES, fill = X)
        goBtn = Button(OptionsFrame, text="Go", command = self._go).pack(side = LEFT)
        self.PathEntry.bind('<Return>', self._go)

        self.SearchEntry = Entry(OptionsFrame, textvariable='Search', width = 20)
        self.SearchEntry.pack(side = LEFT, expand=YES, fill = X)
        self.SearchEntry.bind('<Button-1>', self._setSearch)
        self.SearchEntry.bind('<Return>', self._search)

        MainFrame = Frame(self, height = 500, relief = RAISED)  
        MainFrame.pack(expand=YES, fill=BOTH)  

        self.m = Menu(MainFrame, tearoff=0)
        self.m.add_command(label="Copy", command = self._copy)
        self.m.add_command(label="Paste", command = self._paste)
        self.m.entryconfigure(1, state = DISABLED)

        for l,w in lists:
            frame = Frame(MainFrame); frame.pack(side=LEFT, expand=YES, fill=BOTH)
            Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                         relief=FLAT, exportselection=FALSE)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<Button-3>', lambda e, s=self: s._popup(e))
            lb.bind("<MouseWheel>", self._OnMouseWheel)
            lb.bind('<Double-Button-1>', lambda e, s=self: s._open(e.y))


        sb = Scrollbar(MainFrame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)

        for l in self.lists:
            l['yscrollcommand']=sb.set
        self._openPath('/')



    ''' ---------------------------------------------------------
        Display and select related methods
        ---------------------------------------------------------'''

    # Selecting files and folders
    def _select(self, y):
        row = self.lists[0].nearest(y)
        self._selection_clear(0, END)
        self._selection_set(row)
        return 'break'

    # Change y view of the lists on scrolling the scrollbar
    def _scroll(self, *args):
        for l in self.lists:
            l.yview(*args)
    
    # change y view of lists on mousewheel rotation
    def _OnMouseWheel(self, event):
        for l in self.lists:
            l.yview("scroll", event.delta, "units")
        return "break"

    # get the index of the selected file/folder
    def _curselection(self):
        return self.lists[0].curselection()

    # Clear all the selections
    def _selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    # set the selection
    def _selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

    # remove the specified files from display
    def _delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    # Insert the file/folder at given index on display
    def _insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    ''' ---------------------------------------------------------
        Navigation and Path Entry related methods
        ---------------------------------------------------------'''

    # Opening Folders
    def _open(self, y):
        row = self.lists[0].nearest(y)
        self._selection_clear(0, END)
        self._selection_set(row)
        selection = self.lists[0].get(row)

        if(self.PathEntry.get() == "Search results in " + (str(self.path.name))):
            file = Path(selection) if(Path(selection).is_dir()) else Path(selection).parent
        else:
            file = self.path / selection

        if(file.is_dir()):
            self._openPath(file)
        else:
            pass
        return 'break'

    # Going back to the parent folder
    def _back(self):
        if( self.PathEntry.get() != str(self.path)):
            self._openPath(self.path)
        elif(self.path.parent != self.path):
            self._openPath(self.path.parent)

    # Going forward to the previously opened folder
    def _forw(self):
        if(self.path == self.prevPath.parent):
            self._openPath(self.prevPath)

    # Go to the folder given in the path Entry box
    def _go(self, event = None):
        path = Path(self.PathEntry.get())
        if(path.exists()):
            if(path.is_dir()):
                self._openPath(path)
            else:
                self._openPath(path.parent)
        else:
            messagebox.showerror("Error", "Invalid path!") 
            
    # Go to the given path
    def _openPath(self, path):

        try:
            for entry in Path(path).iterdir():
                break
        except PermissionError:
            messagebox.showerror("Error", "Permission Denied!") 
            return 'break'

        pathIter = Path(path).iterdir()
        if(isinstance(path, str)):
            path = Path(path)
            self.path = path
            self.prevPath = path
        else:
            self.prevPath = self.path
            self.path = path

        self.PathEntry.delete(0, END)
        self.PathEntry.insert(0, (str(self.path)))

        self.SearchEntry['fg'] = "grey"
        self.SearchEntry.delete(0, END)
        self.SearchEntry.insert(0, "Search " + (str(self.path.name)))

        self._delete(0, END)
        for entry in pathIter:
            if(entry.is_dir()):
                type = "Folder"
            else:
                type = entry.suffix
            self._insert(END, (entry.name, type))
        return 'break'


    ''' ---------------------------------------------------------
        Copy Paste related methods
        ---------------------------------------------------------'''

    # Pop up the copy-paste menubar on right click
    def _popup(self, event):
        row = self.lists[0].nearest(event.y)
        self._selection_clear(0, END)
        self._selection_set(row)
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    # copy the selected file/Folder
    def _copy(self):
        self.copypath = self.path / str(self.lists[0].get(self._curselection()[0]))
        self.m.entryconfigure(1, state = NORMAL)

    # paste the copied File/Folder in the current Folder
    def _paste(self):
        try:
            shutil.copy(str(self.copypath), str(self.path))
            self._openPath(self.path)
        except (shutil.SameFileError, PermissionError):
            messagebox.showerror("Error", "Oops! " + str(sys.exc_info()[0]) + " occurred.") 
        self.m.entryconfigure(1, state = DISABLED)


    ''' ---------------------------------------------------------
        Search Entry related methods
        ---------------------------------------------------------'''

    # Remove default text from search Entry on Click
    def _setSearch(self, event):
        self.SearchEntry['fg'] = "black"
        self.SearchEntry.delete(0, END)

    # Search for matches to input in Search entry on enter
    def _search(self, event):
        searchStr = self.SearchEntry.get()
        self.PathEntry.delete(0, END)
        self.PathEntry.insert(0, "Search results in " + (str(self.path.name)))
        self._delete(0, END)
        self._displayMatches(self.path, searchStr)

    # Display the found matches 
    def _displayMatches(self, path, searchStr):

        if(searchStr[0] == '*'):
            searchStr = " " + searchStr

        patt = re.compile(searchStr.encode('unicode_escape'))
        try:
            for entry in path.iterdir():
                if(patt.search(entry.name.encode('unicode_escape'))):
                    self._insert(END, (entry, "Folder" if entry.is_dir() else entry.suffix))
                if(entry.is_dir()):
                    self._displayMatches(entry, searchStr)
        except (PermissionError, OSError):
            pass


