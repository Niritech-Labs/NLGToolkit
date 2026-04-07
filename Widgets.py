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
    def __init__(self,label:str | None ,icon:nk.nk_image | None,NK_TEXT_FLAG:int | None):
        super().__init__('Button')
        self.callable = None
        self.label = label
        self.icon = icon
        self.mode = 0
        self.flag = NK_TEXT_FLAG
        if icon:
            self.mode = 1
        if icon and label and not type(self.flag) is type(None):
            self.mode = 2
        
        


    def update(self):
        if self.mode == 1:
            if (nk.mnk_button_image(self.ctx,self.icon)) and self.callable:
                self.app.EventQueue.put(('call',self.callable,False))
        elif self.mode == 2:
            if (nk.mnk_button_image_label(self.ctx,self.icon,self.label,self.flag)) and self.callable:
                self.app.EventQueue.put(('call',self.callable,False))
        else:
            if (nk.mnk_button_label(self.ctx, self.label)) and self.callable:
                self.app.EventQueue.put(('call',self.callable,False))
        super().update()

    def lmouseClickBind(self,callabl):
        self.callable = callabl
        self.app.EventQueue.put(('add',self.callable,False))

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

    def update(self):
        nk.mnk_group_begin(self.ctx,self.lname,self.flags)
        super().update()
        nk.mnk_group_end(self.ctx)

