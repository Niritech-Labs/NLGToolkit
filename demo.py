import npnuklear as nk
from npnk_wbackend import Bk
bk = Bk()
bk.GLFWInit()
bk.CreateWindow(800, 600, "Red Rectangle", True, False)


def flag(flag) -> int:
    return int(flag.value)

nk_ctx:nk.nk_context = bk.GetNKContext()

while not bk.ShouldClose():
    x,y = bk.GetWindowSize()
    bk.PollEvents()
    bk.NewFrame()

    if (nk.mnk_begin(nk_ctx, "Demo", nk.mnk_rect(0, 0, x, y),flag(nk.NK_WINDOW_BACKGROUND))):
        nk.mnk_layout_row_static(nk_ctx, 30, 80, 1)
        if (nk.mnk_button_label(nk_ctx, "button")):
                print("button pressed\n")
        if (nk.mnk_button_label(nk_ctx, "button")):
                print("button pressed\n")
        if (nk.mnk_button_label(nk_ctx, "button")):
                print("button pressed\n")
        if (nk.mnk_button_label(nk_ctx, "button")):
                print("button pressed\n")

        if (nk.mnk_button_label(nk_ctx, "button")):
                print("button pressed\n")
        

    nk.mnk_end(nk_ctx)
    
    bk.Render()
   

    

bk.Shutdown()
