# Copyright (C) 2024-2026 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
from NLUtils.Logger import NLLogger

import npnuklear as nk

def Baker(mtds:list[tuple[object,tuple]]):
    env = {}
    body = []

    for i, (method,args) in enumerate(mtds):
        mtdKey = f'm{i}'
        env[mtdKey] = method
        argKeys = []
        for j,arg in enumerate(args):
            argKey = f'a{i}_{j}'
            env[argKey] = arg
            argKeys.append(argKey)

        body.append(f'{mtdKey}({','.join(argKeys)})')

    pre = 'def baked():\n    ' + '\n    '.join(body)
    exec(pre,env)

    return env['baked']




class NGTWidget:
    def __init__(self,name):
        self.ctx = None
        self.app = None
        self.production = False
        self.childs = []
        self.Logger = NLLogger(self.production,name)
        self.name = name

    def update(self):
        for child in self.childs:
            child.update()

    def request(self,req):
        self.app.mainQueue.put(req)

    def addWidget(self,widget:'NGTWidget'):
        widget.app = self.app
        widget.ctx = self.ctx
        widget.production = self.production
        self.childs.append(widget)
    def delWidget(self,widget):
        self.childs.remove(widget)


class NGTButton(NGTWidget):
    def __init__(self,label:str | None = None,icon:nk.nk_image | None = None,NK_TEXT_FLAG:int | None = None):
        super().__init__('Button')
        self.rmb = None
        self.lmb = None
        self.label = label
        self.icon = icon
        self.baked = None
        self.flag = NK_TEXT_FLAG


        self.mode = 0
        if icon:
            self.mode = 1
        if icon and label and not type(self.flag) is type(None):
            self.mode = 2
        
    def clickHandle(self):
        if self.ctx.input.mouse.buttons[1].clicked:
            self.app.EventQueue.put(('call',self.lmb,False))
        else:
            self.app.EventQueue.put(('call',self.rmb,False))


    def update(self):
        """if self.ctx.input.mouse.buttons[1].down:
            self.ctx.input.mouse.buttons[0].down = True
        if self.ctx.input.mouse.buttons[1].clicked:
            self.ctx.input.mouse.buttons[0].clicked = True"""
        
        if self.mode == 1:
            if (nk.mnk_button_image(self.ctx,self.icon)):
                self.clickHandle()
        elif self.mode == 2:
            if (nk.mnk_button_image_label(self.ctx,self.icon,self.label,self.flag)):
                self.clickHandle()
        else:
            if (nk.mnk_button_label(self.ctx, self.label)):
                self.clickHandle()
        super().update()

    def RMBBind(self,call):
        self.rmb = call
        self.app.EventQueue.put(('add',self.rmb,False))

    def LMBBind(self,call):
        self.lmb = call
        self.app.EventQueue.put(('add',self.lmb,False))

class NGTRowLayout(NGTWidget):
    def __init__(self,y:int):
        super().__init__('RowLayout')
        self.y = y
        self.els = []
        self.mtd = None


    def addWidget(self, widget:NGTWidget,static:bool,x:int = 20):
        if static:
            self.els.append((nk.mnk_layout_row_template_push_static,(self.ctx,x)))
        else:
            self.els.append((nk.mnk_layout_row_template_push_dynamic,(self.ctx,)))
        return super().addWidget(widget)

    def update(self):
        if not self.mtd:
            self.mtd = Baker(self.els)
        nk.mnk_layout_row_template_begin(self.ctx,self.y)
        self.mtd()
        nk.mnk_layout_row_template_end(self.ctx)
        super().update()

class NGTGroup(NGTWidget):
    def __init__(self,name:str,NK_WINDOW_FLAGS:int):
        super().__init__(f'Group {name}')
        self.lname = name
        self.flags = NK_WINDOW_FLAGS
        self.toScroll = False
        self.x = 0
        self.y = 0
        self.toX = 0
        self.toY = 0
        self.speed = 0.2

    def SetScroll(self,x:int,y:int):

        self.toX = max(x,0)
        self.toY = max(y,0)
        self.toScroll = True

    def GetScroll(self) -> tuple[int,int]:
        return self.x,self.y

    def update(self):
        if self.toScroll:
            self.x = int(self.x + (self.toX - self.x) * self.speed)
            self.y = int(self.y + (self.toY - self.y) * self.speed)
            nk.mnk_group_set_scroll(self.ctx,self.lname,self.x,self.y)
            if (self.toY -1 <= self.y <= self.toY + 1) and (self.toX - 1 <= self.x <= self.toX + 1):
                self.toScroll = False
        
        nk.mnk_group_begin(self.ctx,self.lname,self.flags)
        super().update()
        nk.mnk_group_end(self.ctx)
        if self.app.counter == 6:
            nk.mnk_group_get_scroll(self.ctx,self.lname,self.x,self.y)


class NGTLabel(NGTWidget):
    def __init__(self, name,NK_TEXT_FLAG):
        super().__init__(name)
        self.flag = NK_TEXT_FLAG
        self.lname = name

    def update(self):
        nk.mnk_label(self.ctx,self.lname,self.flag)
        super().update()
