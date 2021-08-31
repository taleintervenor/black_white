from typing import List, Mapping, Tuple
import tkinter

map_empty = 0
map_point_black = 1
map_point_white = 2
map_point_fix = 3
map_line_x = 4
map_line_y = 5
str_btn_draw = ['确定地图', '重设地图']
str_btn_walk = ['确定起点', '结束行走']

# init map number matrix with all points and routes
map_size = 3
map_number: List[List[int]]
map_number_record: List[List[int]]
map_button: List[List[tkinter.Button]] = []
start_x, start_y = 0, 0
player_x, player_y = -1, -1


def init_map(size: int) -> List[List[int]]:
    matrix: List[List[int]] = [[map_point_black]]
    for y in range(1, size):
        matrix[0].extend([map_line_y, map_point_black])
    for x in range(1, size):
        matrix.extend([[map_line_x], [map_point_black]])
        for y in range(1, size):
            matrix[x * 2 - 1].extend([map_empty, map_line_x])
            matrix[x * 2].extend([map_line_y, map_point_black])
    return matrix


def clean_map_button():
    global map_button
    for x in range(len(map_button)):
        for y in range(len(map_button[x])):
            map_button[x][y].destroy()
            map_button[x][y] = None
        map_button[x] = []
    map_button = []


def draw_map_button(map_num: List[List[int]], parent: tkinter.Frame):
    global map_button
    clean_map_button()
    for x in range(len(map_num)):
        map_button.append([])
        for y in range(len(map_num)):
            btn_new = tkinter.Button(parent, image=map_pattern[map_num[x][y]], bd=0, state=tkinter.NORMAL)
            if x & 0x1 == 0x0 and y & 0x1 == 0x0:
                btn_new.configure(command=lambda bx=x, by=y: on_click_point_edit(bx, by))
            elif x & 0x1 == 0x0 or y & 0x1 == 0x0:
                btn_new.configure(command=lambda bx=x, by=y: on_click_line_edit(bx, by))
            else:
                btn_new.configure(state=tkinter.DISABLED)
            btn_new.grid(row=y, column=x)
            map_button[x].append(btn_new)
    return map_button


def move_player(x, y, color='dodger blue'):
    global player_x, player_y, map_button
    if player_x >= 0 and player_y >= 0:
        map_button[player_x][player_y].configure(bg='SystemButtonFace')
    if x >= 0 and y >= 0:
        map_button[x][y].configure(bg=color)
    player_x = x
    player_y = y


def record_insert(widget: tkinter.Text, msg: str):
    widget.configure(state=tkinter.NORMAL)
    widget.insert(tkinter.INSERT, msg)
    widget.configure(state=tkinter.DISABLED)


def no_route(x, y) -> bool:
    if x < 0 or x >= len(map_number):
        return True
    if y < 0 or y >= len(map_number):
        return True
    return map_number[x][y] == map_empty


def step_on_point(x, y):
    global map_number, map_button
    if map_number[x][y] == map_point_fix:
        return
    map_number[x][y] = map_point_white + map_point_black - map_number[x][y]
    map_button[x][y].configure(image=map_pattern[map_number[x][y]])


def on_click_point_edit(x: int, y: int):
    global map_number, map_button
    map_number[x][y] = map_number[x][y] % 3 + 1  # loop from 1-3, also can transfer 0 to 1
    map_button[x][y].configure(image=map_pattern[map_number[x][y]])


def on_click_line_edit(x: int, y: int):
    if y & 0x1 == 0x1:  # it's y-axis line
        if map_number[x][y] == map_line_y:
            map_number[x][y] = map_empty
            # hide upper point if no route linked to it
            if no_route(x - 1, y - 1) and no_route(x + 1, y - 1) and no_route(x, y - 2):
                map_number[x][y - 1] = map_empty
                map_button[x][y - 1].configure(image=map_pattern[map_empty])
            # hide lower point if no route linked to it
            if no_route(x - 1, y + 1) and no_route(x + 1, y + 1) and no_route(x, y + 2):
                map_number[x][y + 1] = map_empty
                map_button[x][y + 1].configure(image=map_pattern[map_empty])
        else:
            map_number[x][y] = map_line_y
    else:  # it's x-axis line
        if map_number[x][y] == map_line_x:
            map_number[x][y] = map_empty
            # hide left point if no route linked to it
            if no_route(x - 1, y - 1) and no_route(x - 1, y + 1) and no_route(x - 2, y):
                map_number[x - 1][y] = map_empty
                map_button[x - 1][y].configure(image=map_pattern[map_empty])
            # hide right point if no route linked to it
            if no_route(x + 1, y - 1) and no_route(x + 1, y + 1) and no_route(x + 2, y):
                map_number[x + 1][y] = map_empty
                map_button[x + 1][y].configure(image=map_pattern[map_empty])
        else:
            map_number[x][y] = map_line_x
    map_button[x][y].configure(image=map_pattern[map_number[x][y]])


def on_click_point_start(x: int, y: int):
    if map_number[x][y] != map_empty:
        move_player(x, y, color='orange')


def on_click_point_walk(x: int, y: int):
    if map_number[x][y] == map_empty:
        return
    if x - player_x == 2 and y == player_y and map_number[x - 1][y] != map_empty:  # move right
        move_player(x, y)
        step_on_point(x, y)
        record_insert(txt_record, '→ ')
    elif x - player_x == -2 and y == player_y and map_number[x + 1][y] != map_empty:  # move left
        move_player(x, y)
        step_on_point(x, y)
        record_insert(txt_record, '← ')
    elif y - player_y == 2 and x == player_x and map_number[x][y - 1] != map_empty:  # move down
        move_player(x, y)
        step_on_point(x, y)
        record_insert(txt_record, '↓ ')
    elif y - player_y == -2 and x == player_x and map_number[x][y + 1] != map_empty:  # move up
        move_player(x, y)
        step_on_point(x, y)
        record_insert(txt_record, '↑ ')


def on_click_btn_draw():
    global map_size, map_button, map_number, map_number_record, player_x, player_y
    if btn_draw['text'] == str_btn_draw[0]:  # complete editing map and start to move
        btn_draw.configure(text=str_btn_draw[1])
        ety_size.configure(state=tkinter.DISABLED)
        on_focusout_ety_size(tkinter.Event())
        btn_walk.configure(state=tkinter.NORMAL)
        # make all line unable to be clicked
        for x in range(0, map_size * 2 - 1, 2):
            for y in range(1, map_size * 2 - 1, 2):
                map_button[x][y].configure(state=tkinter.DISABLED)
        for x in range(1, map_size * 2 - 1, 2):
            for y in range(0, map_size * 2 - 1, 2):
                map_button[x][y].configure(state=tkinter.DISABLED)
        # switch all points' onclick callback for setting start point
        for x in range(0, map_size * 2 - 1, 2):
            for y in range(0, map_size * 2 - 1, 2):
                map_button[x][y].configure(command=lambda bx=x, by=y: on_click_point_start(bx, by))
        # save the init state of map
        map_number_record = []
        for x in range(map_size * 2 - 1):
            map_number_record.append(map_number[x].copy())
        on_click_point_start(0, 0)
    else:  # re-edit the map
        btn_draw.configure(text=str_btn_draw[0])
        ety_size.configure(state=tkinter.NORMAL)
        btn_walk.configure(text=str_btn_walk[0], state=tkinter.DISABLED)
        # make all line able to be clicked
        for x in range(0, map_size * 2 - 1, 2):
            for y in range(1, map_size * 2 - 1, 2):
                map_button[x][y].configure(state=tkinter.NORMAL)
        for x in range(1, map_size * 2 - 1, 2):
            for y in range(0, map_size * 2 - 1, 2):
                map_button[x][y].configure(state=tkinter.NORMAL)
        # switch all points' onclick callback for edit map
        for x in range(0, map_size * 2 - 1, 2):
            for y in range(0, map_size * 2 - 1, 2):
                map_button[x][y].configure(command=lambda bx=x, by=y: on_click_point_edit(bx, by))
        move_player(-1, -1)


def on_click_btn_walk():
    global start_x, start_y, map_number, map_number_record, map_button
    if btn_walk['text'] == str_btn_walk[0]:  # set start point and start to walk
        btn_walk.configure(text=str_btn_walk[1])
        # switch all points' onclick callback for move
        for x in range(0, map_size * 2 - 1, 2):
            for y in range(0, map_size * 2 - 1, 2):
                map_button[x][y].configure(command=lambda bx=x, by=y: on_click_point_walk(bx, by))
        start_x, start_y = player_x, player_y
        move_player(start_x, start_y)
        record_insert(txt_record, '起点 ')
    else:  # end walk and reset start point
        btn_walk.configure(text=str_btn_walk[0])
        record_insert(txt_record, '终点\n')
        # reset map state to init record
        map_number = map_number_record
        draw_map_button(map_number, frm_map)
        # switch all points' onclick callback for setting start point
        for x in range(0, map_size * 2 - 1, 2):
            for y in range(0, map_size * 2 - 1, 2):
                map_button[x][y].configure(command=lambda bx=x, by=y: on_click_point_start(bx, by))
        on_click_point_start(start_x, start_y)


def on_focusout_ety_size(event):
    global map_size, map_number, map_button, frm_map
    # check user input size is valid
    valid = False
    new_size = 0
    size_str = ety_size.get()
    if str.isdigit(size_str):
        new_size = int(size_str)
        if 0 < new_size < 16:
            valid = True
    if not valid:
        ety_size.delete(0, tkinter.END)
        ety_size.insert(0, map_size)
        return
    if new_size == map_size:
        return
    # redraw the whole map
    map_size = new_size
    map_number = init_map(map_size)
    draw_map_button(map_number, frm_map)


main_win = tkinter.Tk()
main_win.title('黑白格')

frm_top = tkinter.Frame(main_win)
lbl_size = tkinter.Label(frm_top, text='地图尺寸')
lbl_size.pack(side=tkinter.LEFT)
ety_size = tkinter.Entry(frm_top, width=5, relief=tkinter.RIDGE, bd=3)
ety_size.insert(0, str(map_size))
ety_size.bind("<FocusOut>", on_focusout_ety_size)
ety_size.bind("<Return>", on_focusout_ety_size)
ety_size.pack(side=tkinter.LEFT, padx=[0, 20])
btn_draw = tkinter.Button(frm_top, text=str_btn_draw[0], command=on_click_btn_draw)
btn_draw.pack(side=tkinter.LEFT)
btn_walk = tkinter.Button(frm_top, text=str_btn_walk[0], state=tkinter.DISABLED, command=on_click_btn_walk)
btn_walk.pack(side=tkinter.LEFT)
frm_top.pack(side=tkinter.TOP)

# draw init map with all point and route
frm_map = tkinter.Frame(main_win)
map_pattern = [tkinter.PhotoImage(file='img/map_empty.png'),
               tkinter.PhotoImage(file='img/point_black.png'),
               tkinter.PhotoImage(file='img/point_white.png'),
               tkinter.PhotoImage(file='img/point_fix.png'),
               tkinter.PhotoImage(file='img/route_x.png'),
               tkinter.PhotoImage(file='img/route_y.png')]
map_number = init_map(map_size)
draw_map_button(map_number, frm_map)
frm_map.pack(side=tkinter.TOP)

frm_bottom = tkinter.Frame(main_win)
txt_record = tkinter.Text(frm_bottom, height=10, state=tkinter.DISABLED)
txt_record.pack(side=tkinter.LEFT)
frm_bottom.pack(side=tkinter.BOTTOM)

main_win.mainloop()
