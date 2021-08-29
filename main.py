from typing import List
import tkinter

map_size = 8
map_graph_patterns = [' ', 'e', 'o', '-', '|']
map_empty = 0
map_point_black = 1
map_point_white = 2
map_line_x = 3
map_line_y = 4

map_graph: List[List[int]] = []
for y in range(map_size):
    map_graph.extend([[map_point_black], [map_line_y]])
    for x in range(map_size):
        map_graph[y*2].extend([map_line_x, map_point_black])
        map_graph[y*2+1].extend([map_empty, map_line_y])

main_win = tkinter.Tk()
img_point_black = tkinter.PhotoImage(file='img/point_black.png')
btn_test = tkinter.Button(main_win, text='攻击', image=img_point_black, bd=0, bg='red', state='normal')
btn_test.grid(row=0, column=0)
main_win.mainloop()
# for y in range(2*map_size-1):
#     for x in range(2*map_size-1):
#         print("%s" % map_graph_patterns[map_graph[y][x]], end='')
#     print()

