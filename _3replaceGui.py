''' _3replaceGui.py
    
    This is the windowed, user friendly version of the original.
    It finds a specified string in filenames, then replaces all.
    
    User defines:   Parent directory (Search is recursive-only)
                    String to find
                    String to replace with

    Requires _3replace.py be in the same directory.
'''

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from _3replace import replaceAll

class ReplaceApp:
    def __init__(self, root):
        # Creates main window and sets title.
        self.root = root
        self.root.title('_3replaceGUI.py')

        # Creates two frames to group widgets, and positions them.
        self.topFrame = tk.Frame(self.root)
        self.bottomFrame = tk.Frame(self.root)
        self.topFrame.pack(padx=10, pady=10)
        self.bottomFrame.pack(padx=10, pady=10)

        # Variables keep entry widgets and logic in sync.
        self.folderPath = tk.StringVar()
        self.findString = tk.StringVar()
        self.replaceString = tk.StringVar()

        # Creates widgets in the top frame.
        self.folderPath_label = tk.Label(
            self.topFrame,
            text='Copy File Path:',
            anchor='w'
        )
        self.folderPath_entry = tk.Entry(
            self.topFrame,
            textvariable=self.folderPath,
            width=50
        )
        self.fileBrowser_button = tk.Button(
            self.topFrame,
            text='Browse',
            command=self.browseFolder_click
        )
        self.findString_label = tk.Label(
            self.topFrame,
            text='Find:',
            anchor='w'
        )
        self.findString_entry = tk.Entry(
            self.topFrame,
            textvariable=self.findString,
            width=50
        )
        self.replaceString_label = tk.Label(
            self.topFrame,
            text='Replace with:',
            anchor='w'
        )
        self.replaceString_entry = tk.Entry(
            self.topFrame,
            textvariable=self.replaceString,
            width=50
        )

        # Positions widgets in the top frame.
        self.folderPath_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.folderPath_entry.grid(row=0, column=1, padx=5, pady=5)
        self.fileBrowser_button.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.findString_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.findString_entry.grid(row=2, column=1, padx=5, pady=5)
        self.replaceString_label.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.replaceString_entry.grid(row=3, column=1, padx=5, pady=5)

        # Creates buttons in the bottom frame
        self.replaceAll_button = tk.Button(
            self.bottomFrame,
            text='Replace All',
            command=self.replaceAll_click
        )
        self.quit_button = tk.Button(
            self.bottomFrame,
            text='Quit',
            command=self.root.destroy
        )

        # Positions buttons in the bottom frame
        self.replaceAll_button.grid(row=1, column=1, padx=5, pady=5)
        self.quit_button.grid(row=1, column=2, padx=5, pady=5)

    def browseFolder_click(self):
        # Opens native folder picker, returns the selected folder path as a string.
        folder = filedialog.askdirectory()
        if folder: # Checks if variable exists.
            self.folderPath.set(folder) # Sets the folderPath variable.


    def replaceAll_click(self):
        # Gets updated information from the gui.
        directory = self.folderPath.get()
        findString = self.findString.get()
        replaceString = self.replaceString.get()

        # Checks if the folder exists.
        if not os.path.isdir(directory):
            messagebox.showerror('Error', 'Selected folder does not exist.')
            return
        
        # Runs the replaceAll program and returns results list.
        results = replaceAll(directory, findString, replaceString)

        # Sends results to showResults.
        if results:
            self.showResults(results)
        else:
            messagebox.showinfo('Info', 'No files were renamed.')

    def showResults(self, results):
        #Creates a child window from the main.
        window = tk.Toplevel(self.root)
        window.title('Renamed Files')
        window.geometry('700x400')

        # Creates frame to store widgets
        frame = tk.Frame(window)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Creates table to display results.
        tree = ttk.Treeview(
            frame,
            columns=('old', 'new'),
            show='headings'
        )

        # Defines column headers.
        tree.heading('old', text='Old Name')
        tree.heading('new', text='New Name')

        # Configures column layout and alignment.
        tree.column('old', anchor='w', width=300)
        tree.column('new', anchor='w', width=300)

        # Adds each record into the table.
        for old, new in results:
            tree.insert('', 'end', values=(old, new))

        # Creates scroll bar.
        scrollbar = ttk.Scrollbar(
            frame,
            orient='vertical',
            command=tree.yview
        )
        # Attaches scroll bar to table.
        tree.configure(yscrollcommand=scrollbar.set)

        # Position table elements.
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

if __name__ == '__main__':
    root = tk.Tk()
    ReplaceApp(root)
    root.mainloop()
