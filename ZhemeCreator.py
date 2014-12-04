#!/usr/bin/python                                                                                                                                                                                                                
# -*- coding: utf-8 -*-
"""                                                                                                                                                                                                                              
 This program is free software; you can redistribute it and/or modify                                                                                                                                                            
 it under the terms of the GNU General Public License as published by                                                                                                                                                            
 the Free Software Foundation; either version 2 of the License, or                                                                                                                                                               
 (at your option) any later version.                                                                                                                                                                                             
                                                                                                                                                                                                                                 
 This program is distributed in the hope that it will be useful,                                                                                                                                                                 
 but WITHOUT ANY WARRANTY; without even the implied warranty of                                                                                                                                                                  
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                                                                                                                                                   
 GNU General Public License for more details.                                                                                                                                                                                    
                                                                                                                                                                                                                                 
 You should have received a copy of the GNU General Public License                                                                                                                                                               
 along with this program; if not, write to the Free Software                                                                                                                                                                     
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA                                                                                                                                                       
"""   

from Tkinter import *
from tkFileDialog import askdirectory
import os

class GUI:
        def __init__(self):
                ##TK
                self.root = Tk()
                self.root.title("ZhemeCreator")

                self.editor = None
                self.sel = None
                self.menu = Menu(gui=self)

                self.zheme = None

                self.menu.show()

        #checks if the directory exists (when modifying a zheme), copies the necessary files
        def showEd(self, mode=0, name=None, direct=None):
                if not direct[-1] == "/":
                        direct += "/"

                fullDir = direct + name + "/"

                if not os.path.isdir(direct) or (mode == 1 and not os.path.isdir(fullDir)):
                        print "Error, this directory doesn't exist! Returning to menu"
                        self.menu.show()
                        return

                if mode == 0:
                        os.system("cp -R ./Base/ " + fullDir)
                        os.system("mv " + fullDir + "base.edj " + fullDir + name + ".edj")

                # check to see if .edj already decompiled (if not, decompile it)
                if not os.path.isfile(fullDir + name + "/background.png"):
                        os.system("cd " + fullDir + " && edje_decc " + name + ".edj")

                #load files from the decompiled dir
                self.zheme = Zheme(name=name, directory=fullDir)

                self.editor = Editor(gui=self)
                self.editor.show()

        def selDir(self, mode=0):
                self.sel = DirectSel(gui=self, mode=mode)
                self.sel.show()

class Menu:
        def __init__(self, gui=None):
                self.gui = gui
                self.canvas = Canvas(self.gui.root,width=300, height=100, highlightthickness=0)
                self.butNew = Button(master=self.canvas, command=self.newZheme, text="Create a new zheme", font=("Helvetica", 14))
                self.butModify = Button(master=self.canvas, command=self.modifyZheme, text="Modify a zheme", font=("Helvetica", 14))

                self.butNew.pack()
                self.butModify.pack()
                
        def show(self):
                self.canvas.place(x=0, y=0, anchor=NW)
                self.canvas.update()
                self.gui.root.geometry("%dx%d%+d%+d" % (self.canvas.winfo_width(), self.canvas.winfo_height(), 0, 0))

        def hide(self):
                self.canvas.place_forget()

        def newZheme(self):
                self.hide()
                self.gui.selDir(0)

        def modifyZheme(self):
                self.hide()
                self.gui.selDir(1)

class DirectSel:
        def __init__(self, gui=None, mode=0):
                self.gui = gui
                self.mode = mode
                self.canvas = Canvas(self.gui.root,width=300, height=100, highlightthickness=0)

                Label(self.canvas, text="Name: ").grid(row=0)
                self.name = Entry(self.canvas)
                self.name.grid(row=0, column=1)

                self.direct = Entry(self.canvas)
                if self.mode == 1:
                        Label(self.canvas, text="Path (the zheme's parent dir): ").grid(row=1)
                        self.direct.grid(row=1, column=1)
                else:
                        self.direct.insert(0, "./")

                self.butOk = Button(master=self.canvas, text="Ok", command=self.ok).grid(row=2)
                self.butCancel = Button(master=self.canvas, text="Cancel", command=self.cancel).grid(row=2, column=1)

                
        def show(self):
                self.canvas.place(x=0, y=0, anchor=NW)
                self.canvas.update()
                self.gui.root.geometry("%dx%d%+d%+d" % (self.canvas.winfo_width(), self.canvas.winfo_height(), 0, 0))

        def hide(self):
                self.canvas.place_forget()

        def ok(self):
                if self.name.get() and self.direct.get():
                                self.hide()
                                self.gui.showEd(self.mode, name=self.name.get(), direct=self.direct.get())

        def cancel(self):
                self.hide()
                self.gui.menu.show()

class Editor:
        def __init__(self, gui=None):
                self.gui = gui
                self.canvas = Canvas(self.gui.root,width=600, height=800, highlightthickness=0)

                Label(self.canvas, text="Editing zheme: "+self.gui.zheme.name).grid(row=0)
                Label(self.canvas, text="Wallpaper: ").grid(row=1)
                Label(self.canvas, text="Emblem: ").grid(row=2)
                Label(self.canvas, text="Panel: ").grid(row=3)

                self.wallpaper = Entry(self.canvas)
                self.wallpaper.grid(row=1, column=1)

                self.emblem = Entry(self.canvas)
                self.emblem.grid(row=2, column=1)

                self.panel = Entry(self.canvas)
                self.panel.grid(row=3, column=1)

                self.manV = IntVar()
                self.manual = Checkbutton(self.canvas, text="Manual mode (Edit the decompiled files, don't use the above fields)", variable=self.manV)
                self.manual.grid(row=4)


                self.btnOk = Button(master=self.canvas, text="Build!", command=self.build).grid(row=5)
                self.btnCancel = Button(master=self.canvas, text="Cancel", command=self.cancel).grid(row=5, column=1)

        def build(self):
                if self.manV.get() == 1:
                        os.system("cd " + self.gui.zheme.directory + self.gui.zheme.name + " && ./build.sh")
                        os.system("mv -f " + self.gui.zheme.directory + self.gui.zheme.name + "/" + self.gui.zheme.name + ".edj " + self.gui.zheme.directory + self.gui.zheme.name + ".edj")
                        os.system("rm -rf " + self.gui.zheme.directory + self.gui.zheme.name)
                        self.hide()
                        self.gui.menu.show()
                else:
                        pass #check si les champs sont remplis, copie les fichiers aux bonnes places ( + resize et convertit au bon format)
                #tar gz et/ou transfert

        def cancel(self):
                self.hide()
                os.system("rm -rf " + self.gui.zheme.directory + self.gui.zheme.name)
                self.gui.menu.show()

        def show(self):
                self.canvas.place(x=0, y=0, anchor=NW)
                self.canvas.update()
                self.gui.root.geometry("%dx%d%+d%+d" % (self.canvas.winfo_width(), self.canvas.winfo_height(), 0, 0))


        def hide(self):
                self.canvas.place_forget()

class Zheme:
        def __init__(self, name=None, directory=None, wallpaper=None, emblem=None, panel=None):
                self.name = name
                self.directory = directory
                self.wallpaper = wallpaper
                self.emblem = emblem
                self.panel = panel
                #icons, other params...

if __name__ == "__main__": 
        myGUI = GUI()
        myGUI.root.mainloop()
