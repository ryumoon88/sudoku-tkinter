from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from turtle import heading

import numpy as np


class App(tk.Tk):

    WINDOW_WIDTH = 550
    WINDOW_HEIGHT = 600

    DIFFICULTY = "easy"

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Sudoku")
        self.wm_title("Sudoku")
        self.minsize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.center_screen()
        container = tk.Frame(self, width=int(self.WINDOW_WIDTH),
                             height=int(self.WINDOW_HEIGHT))
        container.pack(side='top', fill=tk.BOTH, expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = dict()

        for F in (MenuPage, SudokuPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(MenuPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.init()
        frame.tkraise()

    def center_screen(self):
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = int((screen_width/2) - (self.WINDOW_WIDTH/2)
                   ), int((screen_height/2) - (self.WINDOW_HEIGHT/2))
        self.geometry("{}x{}+{}+{}".format(self.WINDOW_WIDTH,
                      self.WINDOW_HEIGHT, x, y))

        print('App initialized')


class MenuPage(tk.Frame):
    _controller = None
    _canvas = None

    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self._controller = controller
        self._canvas = tk.Canvas(self, width=200, height=300)
        self._canvas.pack(expand=True)

    def init(self):
        label_title = tk.Label(self._canvas, text="Sudoku",
                               font=('Comic Sans MS', 20, 'bold'))
        label_title.pack(expand=True, fill=tk.BOTH, pady=20)

        button_start = tk.Button(self._canvas,
                                 text='Start', bg='green', fg='white', font=('Comic Sans MS', 12, 'bold'),
                                 cursor='hand2', command=lambda: self._controller.show_frame(SudokuPage))
        button_solve = tk.Button(self._canvas,
                                 cursor='hand2', text='Solve', bg='blue', fg='white', font=('Comic Sans MS', 12, 'bold'))
        button_quit = tk.Button(self._canvas,
                                cursor='hand2', text='Quit', bg='black', fg='white', font=('Comic Sans MS', 12, 'bold'))

        button_start.pack(expand=True, fill='x', pady=5)
        button_solve.pack(expand=True, fill='x', pady=5)
        button_quit.pack(expand=True, fill='x', pady=5)
        print('Active Page: MenuPage')


# class DifficultyPage(tk.Frame):

#     def __init__(self, parent, controller) -> None:
#         tk.Frame.__init__(self, parent)

#         canvas = tk.Canvas(self, width=200, height=300)
#         canvas.pack(expand=True)
#         label_title = tk.Label(canvas, text="Difficulty",
#                                font=('Comic Sans MS', 18, 'bold'))
#         label_title.pack(expand=True, fill=tk.BOTH, pady=20)

#         def play(difficulty):
#             App.DIFFICULTY = difficulty
#             controller.show_frame(SudokuPage)

#         button_easy = tk.Button(canvas,
#                                 cursor='hand2', text='Easy', bg='green', fg='black', font=('Comic Sans MS', 10, 'bold'),
#                                 name='easy', command=lambda: play('easy'))
#         button_medium = tk.Button(canvas,
#                                   cursor='hand2', text='Medium', bg='yellow', fg='black', font=('Comic Sans MS', 10, 'bold'),
#                                   name='medium', command=lambda: play('medium'))
#         button_hard = tk.Button(canvas,
#                                 cursor='hand2', text='Hard', bg='red', fg='black', font=('Comic Sans MS', 10, 'bold'),
#                                 name='hard', command=lambda: play('hard'))
#         button_random = tk.Button(canvas,
#                                   cursor='hand2', text='Random', bg='black', fg='white', font=('Comic Sans MS', 10, 'bold'),
#                                   name='random', command=lambda: play('random'))
#         button_back = tk.Button(canvas,
#                                 cursor='hand2', text='< Back', bg='grey', fg='black', font=('Comic Sans MS', 8, 'bold'),
#                                 command=lambda: controller.show_frame(MenuPage))

#         button_easy.pack(expand=True, fill='x', pady=5)
#         button_medium.pack(expand=True, fill='x', pady=5)
#         button_hard.pack(expand=True, fill='x', pady=5)
#         button_random.pack(expand=True, fill='x', pady=5)

#         button_back.pack(expand=True, pady=5, ipadx=5)

#         print('DifficultyPage initialized')

#     def init(self):
#         pass


class SudokuPage(tk.Frame):

    _controller = None
    _canvas = None
    _top_canvas = None
    _grid_canvas = None
    _bottom_canvas = None

    GRID_SIZE = 9
    GRID_CELL_SIZE = 50

    lines = []

    _active_cell = [-1, -1]
    _grid_original = np.zeros((9, 9))
    _grid_tmp = np.zeros((9, 9))

    old_text = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._controller = controller
        self._canvas = tk.Canvas(self, bg='red')
        self._canvas.pack(expand=True)
        self._canvas.grid_rowconfigure(0, weight=1)
        self._canvas.grid_columnconfigure(0, weight=1)

        # Top Canvas
        self._top_canvas = tk.Canvas(
            self._canvas, width=450,  height=50)
        self._top_canvas.pack(fill='x', expand=True)

        # Grid canvas
        self._grid_canvas = tk.Canvas(
            self._canvas, height=460, width=460)
        self._grid_canvas.pack()

        # Bottom Canvas
        self._bottom_canvas = tk.Canvas(self._canvas, height=50)
        self._bottom_canvas.pack()

    def init(self):
        # Top Canvas widgets
        button_back = tk.Button(
            self._top_canvas, text='< Back', bg='grey', fg='black')
        button_back.pack(side=tk.LEFT)

        label_time = tk.Label(
            self._top_canvas, text="{}".format(datetime.now().strftime("%H:%M:%S")), font=("Comic Sans MS", 12, 'bold'))
        label_time.pack(side=tk.RIGHT)

        # Grid Canvas
        self.draw_grid()
        self.watch_grid()

    def draw_grid(self):
        print(self._grid_canvas.winfo_width())
        for i in range(self.GRID_SIZE+1):
            start = (i * self.GRID_CELL_SIZE) + 5
            length = 455
            width = 2
            if i % 3 == 0:
                width = 4
            self.lines.append(self._grid_canvas.create_line(
                start, 5, start, length, width=width))

            self.lines.append(self._grid_canvas.create_line(
                5, start, length, start, width=width))

    def get_cell_pos_by_frame_pos(self, x, y):
        return (y//50), (x // 50)

    def get_frame_pos_by_cell_pos(self, row, col):
        return col * 50, row * 50

    def watch_grid(self):
        self._grid_canvas.bind('<Button-1>', self.on_cell_click)

    def watch_cell(self):
        self._controller.bind('<Key>', self.on_user_input)

    def on_cell_click(self, event):
        x, y = event.x, event.y
        row, col = self.get_cell_pos_by_frame_pos(x, y)
        old_row, old_col = self._active_cell[0], self._active_cell[1]
        self.deactive_cell(old_row, old_col)
        self.active_cell(row, col)

    def on_user_input(self, event):
        key = event.keysym
        current_row, current_col = self._active_cell[0], self._active_cell[1]
        if str(key) == 'Escape':
            self.deactive_cell(current_row, current_col)

    def active_cell(self, row, col):
        print('Activing cell on [{}, {}]'.format(row, col))
        x, y = self.get_frame_pos_by_cell_pos(row, col)
        self._active_cell[0] = row
        self._active_cell[1] = col
        self._grid_canvas.create_rectangle(x+5, y+5, x+55, y+55, fill='grey')
        print('Cell on [{}, {}] actived'.format(row, col))
        self.draw_grid()
        print('Watching cell [{}, {}]'.format(row, col))
        self.watch_cell()

    def deactive_cell(self, row, col):
        print('Deactiving cell on [{}, {}]'.format(row, col))
        x, y = self.get_frame_pos_by_cell_pos(row, col)
        self._grid_canvas.create_rectangle(x+5, y+5, x+55, y+55, fill='white')
        self._active_cell[0] = -1
        self._active_cell[1] = -1
        print('Cell on [{}, {}] deactived'.format(row, col))
        self.draw_grid()


if __name__ == '__main__':
    App().mainloop()
