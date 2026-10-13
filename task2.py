# task2.py
# Горный массив методом midpoint displacement.
# По лекции:  h = (hL + hR)/2 + random(-R*L, R*L)
# R — шероховатость, L — длина отрезка.

import tkinter as tk
import random


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Midpoint displacement')

        self.canvas = tk.Canvas(root, bg='white', width=900, height=500)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda e: self.rebuild())

        panel = tk.Frame(root)
        panel.pack(fill='x')

        tk.Label(panel, text='шероховатость R:').pack(side='left')
        self.rough = tk.DoubleVar(value=0.5)
        tk.Scale(panel, from_=0.05, to=0.9, resolution=0.05,
                 orient='horizontal', length=200,
                 variable=self.rough,
                 command=lambda v: self.rebuild()).pack(side='left')

        tk.Label(panel, text='  шаг:').pack(side='left')
        self.level = tk.IntVar(value=0)
        tk.Scale(panel, from_=0, to=9, resolution=1,
                 orient='horizontal', length=300,
                 variable=self.level,
                 command=lambda v: self.draw()).pack(side='left')

        tk.Button(panel, text='Заново', command=self.new).pack(side='left')

        self.start = []
        self.levels = []

        root.after(100, self.new)

    def new(self):
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        if W < 10:
            W = 900
            H = 500

        y = H * 0.7
        d = H * 0.15
        # две начальные точки
        self.start = [(0, y + random.uniform(-d, d)),
                      (W - 1, y + random.uniform(-d, d))]
        self.rebuild()

    def rebuild(self):
        # заново прогоняем весь алгоритм с текущим R
        R = self.rough.get()
        self.levels = [self.start[:]]
        cur = self.start[:]

        for step in range(9):
            cur = self.make_one_step(cur, R)
            self.levels.append(cur)

        self.draw()

    def make_one_step(self, pts, R):
        # одна итерация midpoint displacement
        result = [pts[0]]
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]

            # длина отрезка
            L = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            mx = (x1 + x2) / 2.0
            my = (y1 + y2) / 2.0 + random.uniform(-R * L, R * L)

            result.append((mx, my))
            result.append((x2, y2))
        return result

    def draw(self):
        self.canvas.delete('all')
        if len(self.levels) == 0:
            return

        n = self.level.get()
        if n >= len(self.levels):
            n = len(self.levels) - 1

        # все предыдущие уровни серым, текущий — чёрным
        for i in range(n + 1):
            pts = self.levels[i]
            coords = []
            for p in pts:
                coords.append(p[0])
                coords.append(p[1])

            if i == n:
                color = 'black'
                w = 2
            else:
                color = '#cccccc'
                w = 1
            self.canvas.create_line(coords, fill=color, width=w)


import math

root = tk.Tk()
App(root)
root.mainloop()