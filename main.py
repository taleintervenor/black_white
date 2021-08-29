from typing import List, Mapping, Tuple
import tkinter

map_empty = 0
map_point_black = 1
map_point_white = 2
map_line_x = 3
map_line_y = 4
str_btn_draw = ['确定地图', '重设地图']
str_btn_walk = ['确定起点', '结束行走']

# init map number matrix with all points and routes
map_size = 3
map_number: List[List[int]]
map_number_record: List[List[int]]
map_button: List[List[tkinter.Button]]
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


def clean_map_button(button_matrix: List[List[tkinter.Button]]):
    for column in button_matrix:
        for button in column:
            button.destroy()


def draw_map_button(size: int) -> List[List[tkinter.Button]]:
    global frm_map, map_number
    btn_matrix: List[List[tkinter.Button]] = []
    for x in range(2 * size - 1):
        btn_matrix.append([])
        for y in range(2 * size - 1):
            btn_new = tkinter.Button(frm_map, image=map_pattern[map_number[x][y]], bd=0, state=tkinter.NORMAL)
            if map_number[x][y] == map_point_black or map_number[x][y] == map_point_white:
                btn_new.configure(command=lambda bx=x, by=y: on_click_point_edit(bx, by))
            elif map_number[x][y] == map_line_x or map_number[x][y] == map_line_y:
                btn_new.configure(command=lambda bx=x, by=y: on_click_line_edit(bx, by))
            else:
                btn_new.configure(state=tkinter.DISABLED)
            btn_new.grid(row=y, column=x)
            btn_matrix[x].append(btn_new)
    return btn_matrix


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


def on_click_point_edit(bx: int, by: int):
    global map_number, map_button
    map_number[bx][by] = map_point_black + map_point_white - map_number[bx][by]
    map_button[bx][by].configure(image=map_pattern[map_number[bx][by]])


def on_click_line_edit(bx: int, by: int):
    if map_number[bx][by] == map_empty:
        if by & 0x1 == 0x1:
            map_number[bx][by] = map_line_y
        else:
            map_number[bx][by] = map_line_x
    else:
        map_number[bx][by] = map_empty
    map_button[bx][by].configure(image=map_pattern[map_number[bx][by]])


def on_click_point_start(bx: int, by: int):
    move_player(bx, by, color='orange')


def on_click_point_walk(bx: int, by: int):
    if bx - player_x == 2 and by == player_y and map_number[bx-1][by] != map_empty:  # move right
        move_player(bx, by)
        on_click_point_edit(bx, by)
        record_insert(txt_record, '→ ')
    elif bx - player_x == -2 and by == player_y and map_number[bx+1][by] != map_empty:  # move left
        move_player(bx, by)
        on_click_point_edit(bx, by)
        record_insert(txt_record, '← ')
    elif by - player_y == 2 and bx == player_x and map_number[bx][by-1] != map_empty:  # move down
        move_player(bx, by)
        on_click_point_edit(bx, by)
        record_insert(txt_record, '↓ ')
    elif by - player_y == -2 and bx == player_x and map_number[bx][by+1] != map_empty:  # move up
        move_player(bx, by)
        on_click_point_edit(bx, by)
        record_insert(txt_record, '↑ ')


def on_click_btn_draw():
    global map_size, map_button, map_number, map_number_record, player_x, player_y
    if btn_draw['text'] == str_btn_draw[0]:  # complete editing map and start to move
        btn_draw.configure(text=str_btn_draw[1])
        ety_size.configure(state=tkinter.DISABLED)
        on_focusout_ety_size(tkinter.Event())
        btn_walk.configure(state=tkinter.NORMAL)
        # make all line unable to be clicked
        for x in range(0, map_size*2-1, 2):
            for y in range(1, map_size*2-1, 2):
                map_button[x][y].configure(state=tkinter.DISABLED)
        for x in range(1, map_size*2-1, 2):
            for y in range(0, map_size*2-1, 2):
                map_button[x][y].configure(state=tkinter.DISABLED)
        # switch all points' onclick callback for setting start point
        for x in range(0, map_size*2-1, 2):
            for y in range(0, map_size*2-1, 2):
                map_button[x][y].configure(command=lambda bx=x, by=y: on_click_point_start(bx, by))
        # save the init state of map
        map_number_record = []
        for x in range(map_size*2-1):
            map_number_record.append(map_number[x].copy())
        on_click_point_start(0, 0)
    else:  # re-edit the map
        btn_draw.configure(text=str_btn_draw[0])
        ety_size.configure(state=tkinter.NORMAL)
        btn_walk.configure(text=str_btn_walk[0], state=tkinter.DISABLED)
        # make all line able to be clicked
        for x in range(0, map_size*2-1, 2):
            for y in range(1, map_size*2-1, 2):
                map_button[x][y].configure(state=tkinter.NORMAL)
        for x in range(1, map_size*2-1, 2):
            for y in range(0, map_size*2-1, 2):
                map_button[x][y].configure(state=tkinter.NORMAL)
        # switch all points' onclick callback for edit map
        for x in range(0, map_size*2-1, 2):
            for y in range(0, map_size*2-1, 2):
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
        map_button = draw_map_button(map_size)
        # switch all points' onclick callback for setting start point
        for x in range(0, map_size * 2 - 1, 2):
            for y in range(0, map_size * 2 - 1, 2):
                map_button[x][y].configure(command=lambda bx=x, by=y: on_click_point_start(bx, by))
        on_click_point_start(start_x, start_y)


def on_focusout_ety_size(event):
    global map_size, map_number, map_button
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
    clean_map_button(map_button)
    map_button = draw_map_button(map_size)


main_win = tkinter.Tk()

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
               tkinter.PhotoImage(file='img/route_x.png'),
               tkinter.PhotoImage(file='img/route_y.png')]
map_number = init_map(map_size)
map_button = draw_map_button(map_size)
frm_map.pack(side=tkinter.TOP)

frm_bottom = tkinter.Frame(main_win)
txt_record = tkinter.Text(frm_bottom, height=10, state=tkinter.DISABLED)
txt_record.pack(side=tkinter.LEFT)
frm_bottom.pack(side=tkinter.BOTTOM)

main_win.mainloop()
