# Copyright (C) 2024-2026 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
from threading import Thread
import queue
from Widgets import NKWidget
class NPAppManager:
    def __init__(self):
        #class object
        self.running = False

        #multiobject
        self.mainQueue = queue.Queue()

        #cycle object
        self.toCall:NKWidget = [] # storage cycle callables

    def Start(self):
        self.running = True
        cycle = Thread(target=self.cycle,daemon=True)
        cycle.start()

    def cycle(self):
        try:
            while self.running:
                if not self.mainQueue.empty():
                    request:tuple[str,object] = self.mainQueue.get() # command / class or none
                    self.handleRequest(request)
                for NKObject in self.toCall:
                    NKObject.update()


        except Exception as E:
            print(E)

    def handleRequest(self,request:tuple):
        if request[0] == 'stop':
            self.running = False
        if request[0] == 'add':
            self.toCall.append(request[1])
        if request[0] == 'del':
            self.toCall.remove(request[1])
        