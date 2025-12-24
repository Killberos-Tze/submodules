#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 07:37:01 2023

@author: tze
"""

from tkinter import Listbox, Frame, Button, Label, GROOVE, StringVar, Tk, SUNKEN, Entry, DoubleVar, IntVar, DISABLED, NORMAL,Canvas,Scrollbar
from tkinter.filedialog import askopenfilename,asksaveasfilename,askopenfilenames
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import ImageTk, Image
from submodules.RW_files import Write_to, Read_from
import os
from datetime import datetime
from tkinter import END

class HeaderListBox(Frame):
    def __init__(self,*args,parent=None,**kwargs):
        super().__init__(parent)
        tmp=self
        self._prepare_elements(tmp)

    def set_title(self,string):
        self._titlevar.set(string)

    def clear_title(self):
        self.set_title('')

    def _prepare_elements(self,tmpframe):
        self._rowindex=[]
        self._titlevar=StringVar()
        self._titlevar.set("Provide a title with insert_title function")
        label=Label(tmpframe, textvariable=self._titlevar, font='Courier', borderwidth=2,relief=GROOVE, width=45)
        label.grid(row=1,column=1)
        self.headerbox=Listbox(tmpframe, font='Courier',width=45,height=1)
        self.headerbox.grid(row = 2, column = 1)
        self.listbox=Listbox(tmpframe, font='Courier', selectbackground='red', selectmode='extended',width=45)#https://stackoverflow.com/questions/51376597/how-can-i-shift-select-multiple-items-in-tkinter-listbox
        self.listbox.grid(row = 4, column = 1, rowspan=4)
        self.listbox.bind("<Leave>",self.refocus)
        self.xscrollbar=Scrollbar(tmpframe,orient='horizontal')
        self.xscrollbar.grid(row = 3, column = 1, sticky='WE')
        self.yscrollbar=Scrollbar(tmpframe)
        self.yscrollbar.grid(row = 4, column = 2, rowspan=4, sticky='NS')
        self.listbox.config(yscrollcommand = self.yscrollbar.set)
        self.listbox.config(xscrollcommand = self.xscrollbar.set)
        self.headerbox.config(xscrollcommand = self.xscrollbar.set)
        self.headerbox.bind("<Leave>",self.refocus)
        self.yscrollbar.config(command = self.listbox.yview)
        self.xscrollbar.config(command = self.OnVsb)
        self.headerbox.bind("<Shift-MouseWheel>", self._on_mousewheel)
        self.headerbox.bind("<Shift-Button-4>", self._on_mousewheel)
        self.headerbox.bind("<Shift-Button-5>", self._on_mousewheel)
        self.listbox.bind("<Shift-MouseWheel>", self._on_mousewheel)
        self.listbox.bind("<Shift-Button-4>", self._on_mousewheel)
        self.listbox.bind("<Shift-Button-5>", self._on_mousewheel)
# =============================================================================
#         https://stackoverflow.com/questions/4066974/scrolling-multiple-tkinter-listboxes-together
# =============================================================================

    def OnVsb(self, *args):
        self.headerbox.xview(*args)
        self.listbox.xview(*args)

    def _on_mousewheel(self, event):
        if event.num==5 and event.state==1:
            self.listbox.xview_scroll(5, "units")
            self.headerbox.xview_scroll(5, "units")
        elif event.num==4 and event.state==1:
            self.listbox.xview_scroll(-5, "units")
            self.headerbox.xview_scroll(-5, "units")
        elif event.delta and event.state:
            self.listbox.xview_scroll(int(-5*event.delta/120), "units")
            self.headerbox.xview_scroll(int(-5*event.delta/120), "units")
        return "break"

    def refocus(self,event):
        self.master.focus()

    def clear_header(self):
        self.headerbox.delete(0,END)

    def set_header(self,string):
        self.clear_header()
        self.headerbox.insert(0,string)

    def clear_list(self):
        self.listbox.delete(0,END)
        self._rowindex=[]

    def clear_selected(self):
        self.listbox.selection_clear(0,END)

    def get_selected(self):
        selected=[]
        for item in self.listbox.curselection():
            selected.append((item,self._rowindex[item]))
        return selected

    def delete_selected(self):
        to_delete=[]
        selected_rows=[item for item in self.listbox.curselection()]
        selected_rows.sort(reverse=True)
        for item in selected_rows:
            self.listbox.delete(item)
            to_delete.append((item,self._rowindex.pop(item)))
        return to_delete

#to add single row at the list end
    def add_row(self,string):
        self.listbox.insert(len(self._rowindex),string)
        if len(self._rowindex)==0:
            self._rowindex.append(0)
        else:
            self._rowindex.append(self._rowindex[-1]+1)
#to add multiple rows at the list end
    def add_rows(self,string_list):
        for item in string_list:
            self.add_row(item)
        #self.master.update()
#to init list with of without predefined index_list
    def init_index_rows(self,string_list,index_list=None):
        self.clear_list()
        if index_list==None:
            self.add_rows(string_list)
        else:
            self._rowindex=[item for item in index_list]
            for idx,item in enumerate(string_list):
                self.listbox.insert(idx,item)
        #self.master.update()

#this is only for loading data files
class LoadSingleFile(Frame):

    def __init__(self,*args,parent=None,ini,write_ini=Write_to.ini_inst_proj,read=Read_from.ihtm,path='load_file_path',filetypes=[("All files","*.*")],**kwargs):
        super().__init__(parent)
        self._parent=self
        self.reset_data()
        self._init_references(ini,write_ini,read,filetypes,path)
        self._prepare_elements(**kwargs)
        if self._path=='ref_file_path' and 'ref_file_name' in self._ini:
            if self._ini['ref_file_name']!='':
                self._load_data(os.path.join(self._ini['ref_file_path'],self._ini['ref_file_name']))
    #action that has to be done if data is loaded or not loaded it has to check if data is there or not
    def add_action(self,action):
        self._action=action

    def _init_references(self,ini,write_ini,read,filetypes,path):
        self._filetypes=filetypes
        self._write_ini=write_ini
        self._filetype=StringVar()
        self._ini=ini
        self._read=read
        self._path=path

    def _action(self):
        pass

    def get_data(self):#it returns the pointer
        return self.data

    def get_filetype(self):
        return self._filetype.get()

    def reset(self):
        self.reset_label()
        self.reset_data()

    def reset_data(self):
        self.data=None

    def reset_label(self):
        self.labelbutton.reset()

    def _prepare_elements(self,*args,**kwargs):
        self.labelbutton=LabelButton(self._parent,command=self._get_file,**kwargs)
        self.labelbutton.grid(row=1,column=1)

    def _load_data(self,filename):
        self.data=self._read(filename,filetype=self._filetype.get())
        if self.data['error']=='':
            self.labelbutton.set_var(os.path.basename(filename))
            self._ini[self._path]=os.path.dirname(filename)
            if self._path=='ref_file_path':
                self._ini['ref_file_name']=os.path.basename(filename)
            self._write_ini()
        else:
            self.labelbutton.set_var(self.data['error'])
            self.reset_data()

    def _get_file(self):
        self.reset_label()
        filename=askopenfilename(title="Select file", initialdir=self._ini[self._path], typevariable=self._filetype, filetypes=self._filetypes)
        if filename:#to check if anything has been read out
            self._load_data(filename)
        else:
            self.reset_data()
        self._action()

    def config(self,*args,**kwargs):
        self.labelbutton.config(*args,**kwargs)

    def disable(self):
        self.labelbutton.config(state=DISABLED)

    def enable(self):
        self.labelbutton.config(state=NORMAL)

class SaveSingleFile(LoadSingleFile):
    def __init__(self,*args,write=Write_to.data,filename='File_name',filevariable=None,filetypes=[("E60 tab sep file","*.dtsp")],datetime=False,**kwargs):
        super().__init__(*args,filetypes=filetypes,path='save_file_path',**kwargs)
        self._write_file=write
        self._dateflag=datetime
        self._date_time=''
        self._filename=filename
        if filevariable==StringVar:
            self._filevar=filevariable()
        elif str(type(filevariable))=="<class 'tkinter.StringVar'>":
            self._filevar=filevariable
        else:
            self._filevar=None

    def _get_file(self,**kwargs):
        self.reset_label()
        if self._dateflag:
            self._data_time=datetime.now().strftime("%Y%M%D_%H%M%S_")
        if self._filevar!=None:
            self._filename=self._filevar.get()
        init_file=f'{self._date_time}{self._filename}.{self._filetypes[0][1]}'.replace('*.','')
        filename=asksaveasfilename(title="Select file", initialdir=self._ini[self._path], filetypes=self._filetypes, initialfile=init_file)
        if filename:#to check if anything has been read out
            self._ini[self._path]=os.path.dirname(filename)
            self._write_ini()
            self.disable()
            self._write_file(filename)

    def add_datetime(self,datetime):
        self._date_time=datetime

    def add_filename(self,filename):
        if self._filevar!=None:
            self._filevar.set(filename)
        else:
            self._filename=filename

class LabelButton(Button):
    def __init__(self,*args,textvariable=StringVar,**kwargs):
        if textvariable==StringVar:
            self.var=textvariable()
        else:
            self.var=textvariable

        if 'text' in kwargs:
            self.default=kwargs['text']
            kwargs.pop('text')
        else:
            self.default=''
        self.reset()
        super().__init__(*args,textvariable=self.var,**kwargs)
        self.bind("<Leave>",self.refocus)

    def refocus(self,event):
        self.master.focus()

    def set_var(self,text):
        self.var.set(text)

    def get_var(self):
        return self.var.get()

    def clear(self):
        self.var.set("");

    def reset(self):
        self.var.set(self.default);

class LabelFrame(Frame):
    def __init__(self,*args, parent=None, textvariable=StringVar, borderwidth=2,relief=SUNKEN,**kwargs):
        super().__init__(parent);
        parent=self;
        if textvariable==StringVar:
            self.var=textvariable()
        else:
            self.var=textvariable
        if 'text' in kwargs:
            self.default=kwargs['text']
            kwargs.pop('text')
        else:
            self.default=''
        tmp=Label(parent, textvariable=self.var, borderwidth=borderwidth, relief=relief,**kwargs)
        tmp.pack()
        self.reset()


    def set_var(self,string):
        self.var.set(string);
    def get_var(self):
        return self.var.get();
    def clear(self):
        self.var.set("");
    def reset(self):
        self.var.set(self.default);

class ErrorFrame(LabelFrame):
    def __init__(self,*args, parent=None, textvariable=StringVar, borderwidth=2,relief=SUNKEN,**kwargs):
        super().__init__(*args, parent=parent, textvariable=textvariable, borderwidth=borderwidth,relief=relief,**kwargs)

    def grid(self,**kwargs):
        super().grid(**kwargs)
        super().grid_remove()

    def grid_remove(self):
        super().grid_remove()
        self.clear()

    def set_var(self,string):
        super().grid()
        super().set_var(string);
        self.after(2000,self.grid_remove)

#you need to add full list of kwargs in init
class OnOffButton(Frame):
    def __init__(self,*args, parent=None, images=['on.png','off.png'],imageon=None, imageoff=None, imagepath=os.path.join(os.path.dirname(__file__), 'images'), command=None, commandon=None, commandoff=None, disable_enable=None, right_click=False, width=10):
        if command==None:
            command=self.placeholder
        if commandon==None:
            commandon=self.placeholder
        if commandoff==None:
            commandoff=self.placeholder
        if disable_enable==None:
            disable_enable=self.placeholder
        super().__init__(parent)
        self.parent=self
        self._imagepath=imagepath
        self.command=command
        self.commandon=commandon
        self.commandoff=commandoff
        self.disable_enable=disable_enable
        self._state='off'
        self._enable=False
        self.images={
        'on':ImageTk.PhotoImage(Image.open(os.path.join(imagepath,images[0]))),
        'off':ImageTk.PhotoImage(Image.open(os.path.join(imagepath,images[1])))
            }
        if imageon!=None:
            self.images['on']=ImageTk.PhotoImage(Image.open(os.path.join(imagepath,imageon)))
        if imageoff!=None:
            self.images['off']=ImageTk.PhotoImage(Image.open(os.path.join(imagepath,imageoff)))

        self.button=Button(self.parent, image=self.images[self._state], command=self.execute_press)
        self.button.grid(row=1,column=1)

        if right_click:
            self.button.bind('<Enter>', self._bound_to_click)
            self.button.bind('<Leave>', self._unbound_to_click)

    def _bound_to_click(self,event):
        self.button.bind_all("<Button-3>", self._on_mouseclick)

    def _unbound_to_click(self,event):
        self.button.unbind_all("<Button-3>")

    def _on_mouseclick(self,event):
        if self.is_enabled():
            self.disable_press()
        else:
            self.enable_press()
        self.disable_enable()

    def on_off_config(self,state):
        self.button.config(state=state)

    def get_state(self):
        return self._state

    def change_state(self,*args):
        if args:
           if args[0]=='on' or args[0]=='off':
               self._state=args[0]
               self.button.config(image=self.images[self._state])

    def execute_press(self):
        if self._enable:
            if self._state=='off':
                self._state='on'
                self.commandon()
            elif self._state=='on':
                self._state='off'
                self.commandoff()
            self.button.config(image=self.images[self._state])
            self.command()

    def enable_press(self):
        self._enable=True

    def disable_press(self):
        self._enable=False

    def is_enabled(self):
        return self._enable

    def placeholder(self,*args):
        pass

class CheckBox(OnOffButton):
    def __init__(self,*args, text='', textvariable=StringVar, orientation='EW',right_click=False,**kwargs):
        super().__init__(*args,imageon='box_on.png', imageoff='box_off.png',right_click=right_click,**kwargs)
        if right_click:
            self.images['on_disabled']=ImageTk.PhotoImage(Image.open(os.path.join(self._imagepath,'box_x.png')))
            self.images['off_disabled']=ImageTk.PhotoImage(Image.open(os.path.join(self._imagepath,'box_x.png')))
        else:
            self.images['on_disabled']=ImageTk.PhotoImage(Image.open(os.path.join(self._imagepath,'box_on_disabled.png')))
            self.images['off_disabled']=ImageTk.PhotoImage(Image.open(os.path.join(self._imagepath,'box_off_disabled.png')))
        self.label=LabelFrame(parent=self.parent,text=text,textvariable=textvariable)
        if orientation=='WE':
            self.label.grid(row=1,column=0)
        elif orientation=='NS':
            self.label.grid(row=2,column=1)
        elif orientation=='SN':
            self.label.grid(row=0,column=1)
        else:
            self.label.grid(row=1,column=2)
        self.enable_press()

    def change_state(self,*args):
        if args:
            if args[0]=='on' or args[0]=='off':
                self._state=args[0]
                if self._enable:
                    self.button.config(image=self.images[self._state])
                else:
                    self.button.config(image=self.images[self._state+'_disabled'])

    def enable_press(self):
        self._enable=True
        self.button.config(image=self.images[self._state])
    def disable_press(self):
        self._enable=False
        self.button.config(image=self.images[self._state+'_disabled'])

class ScrollFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent=self
        self.row=0
        # Canvas for scrolling
        self.canvas = Canvas(self.parent, borderwidth=0, background="#f0f0f0",width=150,height=100)
        self.frame_inside = Frame(self.canvas, background="#f0f0f0")

        # Vertical scrollbar
        self.v_scrollbar = Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.x_scrollbar = Scrollbar(self.parent, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.x_scrollbar.set)

        # Pack the scrollbar and canvas
        #self.v_scrollbar.pack(side="right", fill="y")
        #self.x_scrollbar.pack(side="top", fill="x")
        #self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.grid(row=1,column=1,sticky='NS')
        self.x_scrollbar.grid(row=0,column=0,sticky='EW')
        self.canvas.grid(row=1, column=0)

        # Embed the inner frame into the canvas
        self.canvas.create_window((4, 4), window=self.frame_inside, anchor="nw", tags="self.frame_inside")

        # Bind configure event to update scroll region
        self.frame_inside.bind("<Configure>", self.on_frame_configure)
        #Bind the mouse wheel
        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.frame_inside.bind_all("<MouseWheel>", self._on_mousewheel)
        self.frame_inside.bind_all("<Button-4>", self._on_mousewheel)
        self.frame_inside.bind_all("<Button-5>", self._on_mousewheel)
        self.frame_inside.bind_all("<Shift-MouseWheel>", self._on_mousewheel)
        self.frame_inside.bind_all("<Shift-Button-4>", self._on_mousewheel)
        self.frame_inside.bind_all("<Shift-Button-5>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.frame_inside.unbind_all("<Button-4>")
        self.frame_inside.unbind_all("<Button-5>")
        self.frame_inside.unbind_all("<MouseWheel>")
        self.frame_inside.unbind_all("<Shift-Button-4>")
        self.frame_inside.unbind_all("<Shift-Button-5>")
        self.frame_inside.unbind_all("<Shift-MouseWheel>")

    def _on_mousewheel(self, event):
        if event.num==5 and event.state==1:
            self.canvas.xview_scroll(1, "units")
        elif event.num==4 and event.state==1:
            self.canvas.xview_scroll(-1, "units")
        elif event.num==5:
            self.canvas.yview_scroll(1, "units")
        elif event.num==4:
            self.canvas.yview_scroll(-1, "units")
        elif event.delta and event.state:
            self.canvas.xview_scroll(int(-1*event.delta/120), "units")
        elif event.delta:
            self.canvas.yview_scroll(int(-1*event.delta/120), "units")

    def place_element(self,element):
        element.grid(row=self.row,column=1,sticky='W')
        self.row+=1

    #this is needed for element initialisation
    def provide_parent(self):
        return self.frame_inside

    def on_frame_configure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_scroll_region(self):
        "Update the canvas's scrollable region based on the contained frame's size"
        self.update_idletasks() # Process pending GUI updates
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

class LoadMultipleFiles(Frame):
    def __init__(self,*args,parent=None,ini,write_ini=Write_to.ini_inst_proj,read=Read_from.ihtm,path='load_file_path',filetypes=[("All files","*.*")],**kwargs):
        super().__init__(parent)
        self.parent=self
        self._init_variables()
        self._init_references(ini,write_ini,read,filetypes,path)
        self._prepare_elements()

    def _init_references(self,ini,write_ini,read,filetypes,path):
        self._filetypes=filetypes
        self._write_ini=write_ini
        self._ini=ini
        self._read=read
        self._path=path
        self._filetype=StringVar()

    def add_action(self,action):
        self._action=action

    def _action(self):
        pass

    def get_data(self):
        return self._data

    def get_mask(self):
        return self._data_check

    def _get_files(self):
        filenames=askopenfilenames(title="Select files", initialdir=self._ini[self._path], typevariable=self._filetype, filetypes=self._filetypes)
        if filenames:#to check if anything has been read out
            for filename in filenames:
                if filename not in self._fullfilenames:
                    tmp=self._read(filename,self._filetype.get())
                    if tmp['error']=='':
                        self._fullfilenames.append(filename)
                        self._ini[self._path]=os.path.dirname(filename)
                        self._write_ini()
                        self._data.append(tmp)
                        self._data_check.append(CheckBox(parent=self._list.provide_parent(),text=os.path.basename(filename),command=self._action,disable_enable=self._action,right_click=True))
                        self._list.place_element(self._data_check[-1])
                        self._list.update_scroll_region()
                    else:
                        self._errorlabel.grid()
                        self._errorlabel.set_var(tmp['error'])
                        self.after(2000,func=self._clear_label)
                else:
                    self._errorlabel.grid()
                    self._errorlabel.set_var('File/s already loaded!')
                    self.after(2000,func=self._clear_label)

    def _clear_label(self):
        self._errorlabel.clear()
        self._errorlabel.grid_remove()

    def _init_variables(self):
        self._data=[]
        self._data_check=[]
        self._fullfilenames=[]

    def clear_data(self):
        self._data=[]
        self._fullfilenames=[]
        if len(self._data_check):
            tmp=self._data_check.pop()
            tmp.destroy()

    def _prepare_elements(self):
        self._load=Button(self.parent,text='Load\nfiles',command=self._get_files)
        self._load.grid(row=0,column=0,sticky='EW')
        self._remove=Button(self.parent,text='Remove right\nclicked',command=self._remove_files)
        self._remove.grid(row=0,column=1,sticky='EW')
        self._select=Button(self.parent,text='Select all',command=self._select_all)
        self._select.grid(row=1,column=0,sticky='EW')
        self._deselect=Button(self.parent,text='Select none',command=self._deselect_all)
        self._deselect.grid(row=1,column=1,sticky='EW')
        self._errorlabel=LabelFrame(parent=self.parent,width=24)
        self._errorlabel.grid(row=2,column=0,columnspan=2,sticky='EW')
        self._errorlabel.grid_remove()
        self._list=ScrollFrame(self.parent)
        self._list.grid(row=3,column=0,columnspan=2)

    def _remove_files(self):
        for i in range(len(self._data_check)-1,-1,-1):
            if self._data_check[i].is_enabled()==False:
                tmp=self._data_check.pop(i)
                tmp.destroy()
                self._data.pop(i)
                self._fullfilenames.pop(i)
        self._action()
        self._list.update_scroll_region()

    def _select_all(self):
        for item in self._data_check:
            if item.get_state()=='off':
                item.execute_press()

    def _deselect_all(self):
        for item in self._data_check:
            if item.get_state()=='on':
                item.execute_press()

#you need to add full list of kwargs in init
class Rotate(Frame):
    def __init__(self,*args, parent=None, textvariable=StringVar, imagepath=os.path.join(os.path.dirname(__file__), 'images', "button.png"), choice_list=['a','b','c'], command=None, direction='horizontal', width=10):
        if command==None:
            command=self.placeholder
        super().__init__(parent)
        parent=self
        self.var=textvariable()
        self.choice_list=choice_list
        self.command=command
        if direction == 'horizontal' or direction != 'vertical':
            self.prepare_elements(0,180,parent=parent,imagepath=imagepath,width=width)
            self.direction_horizontal()
        else:
            self.prepare_elements(90,270,parent=parent,imagepath=imagepath,width=width)
            self.direction_vertical()
        self.var.set(self.choice_list[0])

    def prepare_elements(self,*args, parent,imagepath,width):
        image = Image.open(imagepath)
        self.imageminus=ImageTk.PhotoImage(image.rotate(args[0]))
        self.imageplus=ImageTk.PhotoImage(image.rotate(args[1]))
        self.minus=Button(parent, image=self.imageminus,command=lambda lidx=-1: self.choice_change(lidx),bg='lightblue')
        self.plus=Button(parent, image=self.imageplus,command=lambda lidx=+1: self.choice_change(lidx),bg='lightblue')
        self.label=Label(parent, textvariable=self.var, borderwidth=2,relief=GROOVE, width=width)

    def placeholder(self,*args):
        pass

    def direction_horizontal(self):
        self.minus.grid(row=1,column=1)
        self.label.grid(row=1,column=2)
        self.plus.grid(row=1,column=3)

    def direction_vertical(self):
        self.minus.grid(row=3,column=1)
        self.label.grid(row=2,column=1)
        self.plus.grid(row=1,column=1)

    def choice_change(self,idx):
        idx=(self.choice_list.index(self.var.get())+idx) % len(self.choice_list)
        self.var.set(self.choice_list[idx])
        self.command(self.var.get())

    def set_var(self,value):
        self.var.set(value);
    def get_var(self):
        return self.var.get();

class FigureFrame(Frame):
    def __init__(self,*args, parent=None, figclass=Figure,figkwargs={},figsize=(8.5/2.54,6/2.54), axsize=(0.2,0.2,0.7,0.7)):
        super().__init__(parent)
        parent=self

        self.plot=figclass(**figkwargs)
        if figclass==Figure:
            self.plot.set_size_inches(figsize)
            self.plot.myaxes=self.plot.add_axes(axsize)

        self.canvas=FigureCanvasTkAgg(self.plot,master=parent)
        self.canvas.get_tk_widget().grid(row=1,column=1)
        toolbar = NavigationToolbar2Tk(self.canvas, parent, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=2,column=1)
        if str(self.plot)=="v_draw":
            self.plot.add_canvas(self.canvas)
            self.plot.canvasdraw()
        else:
            self.canvas.draw()

    def __str__(self):
        return 'Regular App Frame'

class StringEntry(Frame):
    def __init__(self,*args, parent=None,textvariable=StringVar,validate="key",selectbackground='#f00',command=None,**kwargs):
        super().__init__(parent)
        parent=self
        if textvariable in [StringVar, DoubleVar, IntVar]:
            self.var=textvariable()
        else:
            self.var=textvariable
        if 'text' in kwargs:
            self.default=kwargs['text']
            kwargs.pop('text')
        else:
            self.default=''
        self.reset()
        if command==None:
            self._command=self._placeholder
        else:
            self._command=command
        self.Entry=Entry(parent,textvariable=self.var,validate=validate,selectbackground=selectbackground,**kwargs)
        self.Entry['validatecommand']=(self.Entry.register(self.Check_input), '%P','%d')
        self.Entry.bind('<Return>',self._action)
        self.Entry.bind('<FocusOut>',self._action)
        self.Entry.grid(row=1,column=1)

    def _placeholder(self):
        pass

    def _action(self,event):
        self._command()
        self.focus()

    def set_var(self,string):
        self.var.set(string);
    def get_var(self):
        return self.var.get();
    def clear(self):
        self.var.set("");
    def reset(self):
        self.var.set(self.default);

    def config(self,*args,**kwargs):
        self.Entry.config(*args,**kwargs)

    def disable(self):
        self.Entry.config(state=DISABLED)

    def enable(self):
        self.Entry.config(state=NORMAL)

    def Check_input(self,inStr,acttyp):
        if acttyp == '1': #insert
            try:
                float(inStr)
                return False
            except:
                return True #it returns only true of false allowing or not allwing the insert action
        return True


class FloatEntry(StringEntry):
    def __init__(self,*args, parent=None,textvariable=DoubleVar,**kwargs):
        super().__init__(*args, parent=parent,textvariable=textvariable,**kwargs)

    def Check_input(self,inStr,acttyp):
        if acttyp == '1': #insert
            try:
                float(inStr)
                if float(inStr)==0.:#this prevents that input string starts with zero so user can't set layer thickness to zero
                    return False
            except:
                return False #it returns only true of false allowing or not allwing the insert action
        return True

class IntEntry(StringEntry):
    def __init__(self,*args, parent=None,textvariable=IntVar,**kwargs):
        super().__init__(*args, parent=parent,textvariable=textvariable,**kwargs)

    def Check_input(self,inStr,acttyp):
        if acttyp == '1': #insert
            try:
                int(inStr)
            except:
                return False #it returns only true of false allowing or not allwing the insert action
        return True
#integer with limited number of digits
class IntLimEntry(StringEntry):
    def __init__(self,*args, parent=None,textvariable=IntVar,inlen=3,**kwargs):
        super().__init__(*args, parent=parent,textvariable=textvariable,**kwargs)
        self.inlen=inlen
    def Check_input(self,inStr,acttyp):
        if acttyp == '1': #insert
            try:
                int(inStr)
                if len(inStr)>self.inlen:
                    return False
            except:
                return False #it returns only true of false allowing or not allwing the insert action
        return True


class IPEntry(Frame):
    def __init__(self,*args,parent=None,address="None:None",**kwargs):
        if parent!=None:
            super().__init__(parent)
        else:
            super().__init__(*args,**kwargs)
        parent=self
        self.entry_list=[]
        self.ipfields=[IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]

        Label(parent,text="IP Address").grid(row=0,column=0,columnspan=6,sticky="W")
        Label(parent,text="Port").grid(row=0,column=7,columnspan=2,sticky="W")

        for i in range (0,7):
            if i%2==0:
                self.entry_list.append(IntLimEntry(parent=parent,textvariable=self.ipfields[int(i/2)],width=3))
                self.entry_list[-1].grid(row=1,column=i)
            else:
                Label(parent,text=".").grid(row=1,column=i)

        Label(parent,text=":").grid(row=1,column=7)
        self.entry_list.append(IntLimEntry(parent=parent,textvariable=self.ipfields[4],inlen=4,width=4))
        self.entry_list[-1].grid(row=1,column=8)

        if address=="None:None":
            self.set_address("127.0.0.1")
            self.set_port("5025")
        else:
            self.set_address_port(address)

    def set_address_port(self,string):
        self.set_address(string.split(":")[0])
        self.set_port(string.split(":")[1])

    def set_address(self,string):
        ipfields=string.split(".")
        for i in range(0,len(self.ipfields)-1):
            self.ipfields[i].set(int(ipfields[i]))

    def set_port(self,string):
        self.ipfields[-1].set(int(string))

    def get_address(self):
        out=""
        for item in self.ipfields[0:3]:
            out=out+str(item.get())+"."
        out=out+str(self.ipfields[3].get())
        return out

    def get_port(self):
        return self.ipfields[-1].get()

    def get_address_port(self):
        return self.get_address()+":"+str(self.get_port())

    def disable(self):
        for item in self.entry_list:
            item.disable()

    def enable(self):
        for item in self.entry_list:
            item.enable()

class AppFrame(Frame):
    def __init__(self, file, parent=Tk, appgeometry= (200,200,10,10)):
        self.appgeometry=appgeometry
        if parent==Tk:
            self.approot=parent()
            super().__init__(self.approot)
            self.frameroot=self
        else:
            super().__init__(parent)
            self.frameroot=self
            self.approot=None
        self.frameroot.bind("<1>", lambda event: event.widget.focus_set())
        self.ini=Read_from.ini(file)
        self.file=file
        init=False
        if self.ini['error']:
            self.ini={}
            self.ini['error']=''
            init=True
        if 'save_file_path' not in self.ini:
            self.ini['save_file_path']='Document'
            init=True
        if 'load_file_path' not in self.ini:
            self.ini['load_file_path']='Document'
            init=True
        if 'ref_file_path' not in self.ini:
            self.ini['ref_file_path']='Document'
            init=True
        if init:
            self.write_ini()

    def __str__(self):
        return 'Regular App Frame'

    def init_start(self):
        if self.approot!=None:
            self.frameroot.pack(pady = (25,25), padx = (25,25))
            self.approot.title(str(self))
            self.approot.geometry('%dx%d+%d+%d' % self.appgeometry)
            self.approot.mainloop()

    def clear_frameroot(self):
        for widget in self.frameroot.winfo_children():
            widget.destroy()

    def write_ini(self):
        Write_to.ini_inst_proj(self.file,self.ini)
