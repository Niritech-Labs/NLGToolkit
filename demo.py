from Backends import NGTApp, flag
from Widgets import *

bk = NGTApp(800,600,'aga',False)

button = NGTButton("DroidSans.ttf",None,None)
button1 = NGTButton("DroidSans.ttf",None,None)
button2 = NGTButton("DroidSans.ttf",None,None)
button3 = NGTButton("DroidSans.ttf",None,None)
group = NGTGroup('mygroup',flag(nk.NK_WINDOW_BACKGROUND|nk.NK_WINDOW_NO_SCROLLBAR))
layout = NGTRowLayout(400)
bk.addWidget(layout)
layout.addWidget(button,True,200)
layout.addWidget(group,False)
layout.addWidget(button1,True,200)
layout1 = NGTRowLayout(40)
group.addWidget(layout1)
layout1.addWidget(button2,True,300)
layout1.addWidget(button3,True,300)

label = NGTLabel('laaaaaaaaaaaaaaaaaaaable',flag(nk.NK_TEXT_ALIGN_CENTERED))

layout1.addWidget(label,True,300)

def lms(var):
    x,y = group.GetScroll()
    group.SetScroll(x + 60,0)

def rms(var):
    x,y = group.GetScroll()
    group.SetScroll(x - 60,0)

button.LMBBind(lms)
button.RMBBind(rms)


bk.Start()