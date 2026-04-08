# Copyright (C) 2024-2026 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import queue
import threading
import npnuklear as nk
from npnk_wbackend import Bk
from Widgets import *
from NLUtils.Logger import NLLogger


def flag(flag) -> int:
    return int(flag.value)

class NGTApp():
    def __init__(self,width,height,name,production):
        self.Logger = NLLogger(production,'app: ' + name)

        self.production = production
        self.win = Bk()
        self.win.GLFWInit()
        self.running = False
        self.w = width
        self.h = height
        self.name = name
        self.counter = 0
        self.win.CreateWindow(self.w, self.h, self.name, True, False)
        self.ctx = self.win.GetNKContext()
        self.win.InitFont(True,'DroidSans.ttf',18)

        self.widgets:list[NGTWidget] = []

        #multiobject
        self.EventQueue = queue.Queue()
        #cycle object
        self.toCall = [] # storage cycle callables

    def Start(self):
        self.running = True
        ev = threading.Thread(target=self.callbacks,daemon=True)
        ev.start()
        self.cycle()
        
    def callbacks(self):
        try:
            while self.running:
                if not self.EventQueue.empty():
                    request:tuple[str,object,object] = self.EventQueue.get() 
                    self.handleRequest(request)
    
        except Exception as E:
            print(E)

    def cycle(self):
        try:
            winflags = flag(nk.NK_WINDOW_BACKGROUND)
            while self.running:
                self.win.PollEvents()
                self.win.NewFrame()

                if self.counter > 32:
                    self.counter = 0
                    self.running = not self.win.ShouldClose()
                else:
                    self.counter += 1

                x,y = self.win.GetWindowSize()
                if (nk.mnk_begin(self.ctx, self.name, nk.mnk_rect(0, 0, x+10, y),winflags)):
                    for NGTWidget in self.widgets:
                        NGTWidget.update()
                nk.mnk_end(self.ctx)
    
                self.win.Render()
            self.win.Shutdown()
        except Exception as E:
            print(E)

    def handleRequest(self,request:tuple[str,object,object]):
        if request[0] == 'call':
            self.toCall[self.toCall.index(request[1])](request[2])
        if request[0] == 'add':
            self.toCall.append(request[1])
            self.Logger.Info(f'Callback {request[1]} added',NLLogger.ConColors.G,False)
        if request[0] == 'del':
            self.toCall.remove(request[1])
            self.Logger.Info(f'Callback {request[1]} removed',NLLogger.ConColors.G,False)

    def addWidget(self,widget:NGTWidget):
        widget.app = self
        widget.ctx = self.ctx
        widget.production = self.production
        self.widgets.append(widget)
        self.Logger.Info(f'Widget {widget.name} added',NLLogger.ConColors.G,False)
    def delWidget(self,widget:NGTWidget):
        self.widgets.remove(widget)
    

        
