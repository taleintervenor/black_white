from typing import List, Mapping, Tuple
import tkinter

map_size = 3

map_empty = 0
map_point_black = 1
map_point_white = 2
map_line_x = 3
map_line_y = 4
str_btn_draw = ['确定地图', '重设地图']
str_btn_walk = ['设置起点', '模拟行走']

# init map number matrix with all points and routes
map_number: List[List[int]] = [[map_point_black]]
for y in range(1, map_size):
    map_number[0].extend([map_line_y, map_point_black])
for x in range(1, map_size):
    map_number.extend([[map_line_x], [map_point_black]])
    for y in range(1, map_size):
        map_number[x * 2 - 1].extend([map_empty, map_line_x])
        map_number[x * 2].extend([map_line_y, map_point_black])


def on_click_btn_point(bx: int, by: int):
    map_number[bx][by] = map_point_black + map_point_white - map_number[bx][by]
    map_button[bx][by].configure(image=map_pattern[map_number[bx][by]])


def on_click_btn_line(bx: int, by: int):
    if map_number[bx][by] == map_empty:
        if by & 0x1 == 0x1:
            map_number[bx][by] = map_line_y
        else:
            map_number[bx][by] = map_line_x
    else:
        map_number[bx][by] = map_empty
    map_button[bx][by].configure(image=map_pattern[map_number[bx][by]])


def on_click_btn_draw():
    global map_size
    if btn_draw['text'] == str_btn_draw[0]:  #确定地图
        btn_draw.configure(text=str_btn_draw[1])
        btn_walk.configure(state=tkinter.NORMAL)
        map_size = int(ety_size.get())
        print(map_size)
    else:
        btn_draw.configure(text=str_btn_draw[0])
        btn_walk.configure(state=tkinter.DISABLED)


main_win = tkinter.Tk()

frm_top = tkinter.Frame(main_win)
lbl_size = tkinter.Label(frm_top, text='地图尺寸')
lbl_size.pack(side=tkinter.LEFT)
ety_size = tkinter.Entry(frm_top, width=5, relief=tkinter.RIDGE, bd=3)
ety_size.insert(0, '3')
ety_size.pack(side=tkinter.LEFT, padx=[0, 20])
btn_draw = tkinter.Button(frm_top, text=str_btn_draw[0], command=on_click_btn_draw)
btn_draw.pack(side=tkinter.LEFT)
btn_walk = tkinter.Button(frm_top, text=str_btn_walk[0], state=tkinter.DISABLED)
btn_walk.pack(side=tkinter.LEFT)
frm_top.pack(side=tkinter.TOP)

# draw init map with all point and route
frm_map = tkinter.Frame(main_win)
map_pattern = [tkinter.PhotoImage(file='img/map_empty.png'),
               tkinter.PhotoImage(file='img/point_black.png'),
               tkinter.PhotoImage(file='img/point_white.png'),
               tkinter.PhotoImage(file='img/route_x.png'),
               tkinter.PhotoImage(file='img/route_y.png')]
map_button: List[List[tkinter.Button]] = []
for x in range(2*map_size-1):
    map_button.append([])
    for y in range(2*map_size-1):
        btn_new = tkinter.Button(frm_map, image=map_pattern[map_number[x][y]], bd=0, state=tkinter.NORMAL)
        if map_number[x][y] == map_point_black or map_number[x][y] == map_point_white:
            btn_new.configure(command=lambda bx=x, by=y: on_click_btn_point(bx, by))
        elif map_number[x][y] == map_line_x or map_number[x][y] == map_line_y:
            btn_new.configure(command=lambda bx=x, by=y: on_click_btn_line(bx, by))
        else:
            btn_new.configure(state=tkinter.DISABLED)
        btn_new.grid(row=y, column=x)
        map_button[x].append(btn_new)
frm_map.pack(side=tkinter.TOP)

frm_bottom = tkinter.Frame(main_win)
txt_record = tkinter.Text(frm_bottom, state=tkinter.DISABLED)
txt_record.pack(side=tkinter.LEFT)
frm_bottom.pack(side=tkinter.BOTTOM)

main_win.mainloop()
