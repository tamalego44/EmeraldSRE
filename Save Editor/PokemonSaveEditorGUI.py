import tkinter as tk
from tkinter import *
from tkinter import ttk

class GUISave(Frame):
    def __init__(self, saveObj):
        self.saveObj = saveObj

        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Pokemon Emerald Save Modifer")

        self.tabControl = ttk.Notebook(self)
        # nameString = StringVar(self, value="test")
        # self.button = Entry(self, textvariable=nameString)
        # self.button.pack()

        self.tabs = []
        for section in self.saveObj.sections:
            self.tabs.append(GUISection(self.tabControl, section))
            self.tabControl.add(self.tabs[-1], text=section.name)
            #self.tabControl.add(GUISection(self.tabControl, section.data), text=section.name)
        
        self.tabControl.pack(side=TOP,expand=1, fill="both")

        settings = Frame(self)
        
        self.filenameVar = StringVar(settings, value='save2_modified.sav')
        filenameEntry = Entry(settings, textvariable=self.filenameVar)
        filenameEntry.grid(column=0, row=0, padx=1, pady=1)

        saveButton = Button(settings, text="Save", command=self.save)
        saveButton.grid(column=1, row=0, padx=1, pady=1)



        loadButton = Button(settings, text="Load", command=self.load)
        loadButton.grid(column=2, row=0, padx=1, pady=1)
        settings.pack(side=BOTTOM)

    def save(self):
        for widget in self.tabs:
            widget.save()
        self.saveObj.export(self.filenameVar.get())

    def load(self):
        print("//TODO: implement load")
        

class GUISection(Frame):
    def __init__(self, master, section, subSection=False):
        tk.Frame.__init__(self, master=master)
        #self.pack()
        if subSection:
            self.data = section
        else:
            self.data = section.data
            self.section = section
        
        self.dataFields = {}
        self.labels = {}
        self.elements = {}
        for (k,v), i in zip(self.data.items(), range(len(self.data))):
            #print(k,v)
            self.labels[k] = Label(self, text=k)
        
            if type(v) == dict:
                self.elements[k] = GUISection(self, v, subSection = True)
            else:
                if type(v) == str:
                    self.dataFields[k] = StringVar(self, value=v)
                elif type(v) == int:
                    self.dataFields[k] = IntVar(self, value=v)
                self.elements[k] = Entry(self, textvariable=self.dataFields[k])

            if (subSection):
                self.labels[k].grid(column=i, row=0, padx=1, pady=1)
                self.elements[k].grid(column=i, row=1, padx=1, pady=1)
            else:
                self.labels[k].grid(column=0, row=i * 2, padx=1, pady=1)
                self.elements[k].grid(column=0, row=i * 2 + 1, padx=1, pady=1)

    def save(self):
        change = {}
        for (k,v) in self.section.data.items():
            if k in self.dataFields:
                if v != self.dataFields[k].get():
                    change[k] = self.dataFields[k].get()
            else:
                None
                # this is subsection; handle appropriately
        if len(change) > 0:
            self.section.updateBuffer(change)