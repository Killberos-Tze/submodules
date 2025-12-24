#!/usr/bin/env python3

from tkinter import Frame, Tk, Button
import sys

class MultipleApps():
    def init_start(self):
        self.approot.bind("<1>", lambda event: event.widget.focus_set())
        self.approot.mainloop()

    def __init__(self,app_list={None:None},appgeometry=(350, 400, 50, 50)):
        self.approot = Tk()
        self.appgeometry=appgeometry
        self.approot.title('Application hub')
        self.approot.geometry('%dx%d+%d+%d' % self.appgeometry)
        self.frameroot = Frame(self.approot)
        self.frameroot.pack(pady = (25,25), padx = (25,25))
        self.landingframe=Frame(self.frameroot)
        self.landingframe.grid(row=0,column=0)
        if app_list=={None:None}:
            sys.exit()
        elif len(app_list)==1:
            self.landingframe.destroy()
            for item in app_list.values():
                tmp=item(parent=self.frameroot)
            tmp.grid(row=0,column=0)
            self.approot.title(str(tmp))
            try:
                self.approot.geometry('%dx%d+%d+%d' % tmp.appgeometry)
            except:
                pass
        else:
            self.apps_landing(self.landingframe,app_list)

    def apps_landing(self,parent,app_list):
        row=0
        for key, item in app_list.items():
            Button(self.landingframe, text=f"{key}", command=lambda app=item,apps=app_list: self.start_app(app,apps),width=12,bg='lightgray').grid(row=row,column=1)
            row+=1

    def single_app_landing(self,apps):
        self.sideframe=Frame(self.landingframe)
        self.sideframe.grid(row=0,column=0,sticky='NW')
        self.mainframe=Frame(self.landingframe)
        self.mainframe.grid(row=0,column=1,columnspan=10)
        Button(self.sideframe, text="Go back", command= lambda apps=apps: self.stop_app(apps),width=6,bg='lightgray').grid(row=0,column=0)

    def placeholder(self):
        pass

    def start_app(self,app,apps):
        self.landingframe.destroy()
        self.landingframe=Frame(self.frameroot)
        self.landingframe.grid(row=0,column=0)
        self.single_app_landing(apps)
        #AppWindow(parent=parent).grid(row=0,column=0)
        tmp=app(parent=self.mainframe)
        tmp.grid(row=0,column=0)
        self.approot.title(str(tmp))
        self.approot.geometry('%dx%d+%d+%d' % tmp.appgeometry)
        #Button(parent, text="Go back", command=lambda frame=parent: self.stop_app(parent),width=12,bg='lightgray').grid(row=rowcount,column=1)

    def stop_app(self,apps):
        self.landingframe.destroy()
        self.landingframe=Frame(self.frameroot)
        self.landingframe.grid(row=0,column=0)
        self.apps_landing(self.landingframe,app_list=apps)
        self.approot.title('Application hub')
        self.approot.geometry('%dx%d+%d+%d' % self.appgeometry)

