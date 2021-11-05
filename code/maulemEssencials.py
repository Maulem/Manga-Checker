import win32gui, win32ui, win32api, win32con
from win32api import GetSystemMetrics

dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0,0))
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

red = win32api.RGB(255, 0, 0) # Red

past_coordinates = monitor

def clear_screen_drawings():
    rect = win32gui.CreateRoundRectRgn(*past_coordinates, 1960 , 1080)
    win32gui.RedrawWindow(hwnd, past_coordinates, rect, win32con.RDW_INVALIDATE)


def draw_box_on_screen(x0, y0, width, height, rgb = (255, 0, 0)):
    global past_coordinates
    m = win32gui.GetCursorPos()
    win32gui.InvalidateRect(hwnd, (m[0], m[1], GetSystemMetrics(0), GetSystemMetrics(1)), True)
    # rect = win32gui.CreateRoundRectRgn(*past_coordinates, 200 , 200)
    # win32gui.RedrawWindow(hwnd, past_coordinates, rect, win32con.RDW_INVALIDATE)
    thickness = 5

    color = win32api.RGB(rgb[0], rgb[1], rgb[2])
    print("Original:", x0, y0, width, height)

    x0 = int(x0)
    y0 = int(y0)
    width = int(width)
    height = int(height)

    if x0 < monitor[0]:
        x0 = monitor[0]
    
    if y0 < monitor[1]:
        y0 = monitor[1]
    
    if width > monitor[2]:
        width = monitor[2]

    if height > monitor[3]:
        height = monitor[3]

    print("Mod:", x0, y0, width, height)
    for x in range(width-x0):
        for t in range(thickness):
            win32gui.SetPixel(dc, x0+x, y0+t, color)
            win32gui.SetPixel(dc, x0+x, y0+height+t, color)
    for y in range(height-y0):
        for t in range(thickness):
            win32gui.SetPixel(dc, x0+t, y0+y, color)
            win32gui.SetPixel(dc, x0+width+t, y0+y, color)

    # past_coordinates = (m[0]-20, m[1]-20, m[0]+20, m[1]+20)