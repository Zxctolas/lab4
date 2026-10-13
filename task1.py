# task1.py
# L-системы. Загружаем правила из файла, строим фрактал.
# Скобки [ ] работают, случайность угла включается ползунком.
# Галочка "дерево" делает толщину и цвет по глубине ветки.

import tkinter as tk
from tkinter import filedialog, messagebox
import math
import random


# читаем файл с L-системой
def read_file(name):
    f = open(name, encoding='utf-8')
    lines = []
    for line in f:
        line = line.strip()
        if line != '' and not line.startswith('#'):
            lines.append(line)
    f.close()

    head = lines[0].split()
    axiom = head[0]
    angle = float(head[1])
    start_dir = float(head[2]) if len(head) > 2 else 90.0

    rules = {}
    for line in lines[1:]:
        if '->' in line:
            a, b = line.split('->')
            rules[a.strip()] = b.strip()
        elif '=' in line:
            a, b = line.split('=')
            rules[a.strip()] = b.strip()

    return axiom, angle, start_dir, rules


# разворачиваем строку нужное число раз
def make_string(axiom, rules, n):
    s = axiom
    for i in range(n):
        new_s = ''
        for ch in s:
            if ch in rules:
                new_s += rules[ch]
            else:
                new_s += ch
        s = new_s
    return s


# превращаем строку в отрезки
def make_segments(s, angle_deg, start_dir_deg, rand_deg):
    angle = math.radians(angle_deg)
    rand = math.radians(rand_deg)
    x = 0.0
    y = 0.0
    d = math.radians(start_dir_deg)

    stack = []
    segments = []
    depth = 0
    max_depth = 0

    for ch in s:
        if ch == 'F' or ch == 'G':
            nx = x + math.cos(d)
            ny = y - math.sin(d)
            segments.append((x, y, nx, ny, depth))
            if depth > max_depth:
                max_depth = depth
            x = nx
            y = ny
        elif ch == 'f':
            x = x + math.cos(d)
            y = y - math.sin(d)
        elif ch == '+':
            if rand > 0:
                d = d + angle + random.uniform(-rand, rand)
            else:
                d = d + angle
        elif ch == '-':
            if rand > 0:
                d = d - angle + random.uniform(-rand, rand)
            else:
                d = d - angle
        elif ch == '@':
            d = d + random.uniform(-angle, angle)
        elif ch == '[':
            stack.append((x, y, d, depth))
            depth = depth + 1
        elif ch == ']':
            x, y, d, depth = stack.pop()

    return segments, max_depth


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('L-система')

        self.canvas = tk.Canvas(root, bg='white', width=900, height=650)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda e: self.draw())

        self.segments = []
        self.max_depth = 0

        # по умолчанию — куст
        self.axiom = 'X'
        self.angle = 22.5
        self.start_dir = 90.0
        self.rules = {'F': 'FF', 'X': 'F[+X][-X]FX'}

        panel = tk.Frame(root)
        panel.pack(fill='x')

        tk.Button(panel, text='Открыть файл...', command=self.open_file).pack(side='left')

        tk.Label(panel, text='  итераций:').pack(side='left')
        self.iters = tk.IntVar(value=5)
        tk.Spinbox(panel, from_=0, to=8, textvariable=self.iters, width=3).pack(side='left')

        tk.Label(panel, text='  случайность:').pack(side='left')
        self.rand = tk.DoubleVar(value=0)
        tk.Spinbox(panel, from_=0, to=30, textvariable=self.rand, width=4).pack(side='left')

        self.tree = tk.BooleanVar(value=False)
        tk.Checkbutton(panel, text=' дерево (толщина/цвет)',
                       variable=self.tree, command=self.draw).pack(side='left')

        tk.Button(panel, text='  Построить', command=self.build).pack(side='left')

        root.after(100, self.build)

    def open_file(self):
        name = filedialog.askopenfilename()
        if name == '':
            return
        try:
            self.axiom, self.angle, self.start_dir, self.rules = read_file(name)
            self.build()
        except Exception as e:
            messagebox.showerror('Ошибка', str(e))

    def build(self):
        s = make_string(self.axiom, self.rules, self.iters.get())
        self.segments, self.max_depth = make_segments(
            s, self.angle, self.start_dir, self.rand.get())
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        if len(self.segments) == 0:
            return

        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        if W < 10:
            return

        # находим границы картинки
        min_x = 1e9; max_x = -1e9
        min_y = 1e9; max_y = -1e9
        for seg in self.segments:
            x1, y1, x2, y2, d = seg
            if x1 < min_x: min_x = x1
            if x1 > max_x: max_x = x1
            if x2 < min_x: min_x = x2
            if x2 > max_x: max_x = x2
            if y1 < min_y: min_y = y1
            if y1 > max_y: max_y = y1
            if y2 < min_y: min_y = y2
            if y2 > max_y: max_y = y2

        w = max_x - min_x
        h = max_y - min_y
        if w == 0: w = 1
        if h == 0: h = 1

        margin = 20
        k = min((W - 2*margin) / w, (H - 2*margin) / h)
        ox = margin + ((W - 2*margin) - w*k) / 2 - min_x * k
        oy = margin + ((H - 2*margin) - h*k) / 2 - min_y * k

        use_tree = self.tree.get()
        md = self.max_depth
        if md == 0:
            md = 1

        for seg in self.segments:
            x1, y1, x2, y2, d = seg
            X1 = x1 * k + ox
            Y1 = y1 * k + oy
            X2 = x2 * k + ox
            Y2 = y2 * k + oy

            if use_tree:
                t = d / md
                # коричневый -> зелёный
                r = int(139 + (34 - 139) * t)
                g = int(69 + (139 - 69) * t)
                b = int(19 + (34 - 19) * t)
                color = '#%02x%02x%02x' % (r, g, b)
                width = int(8 * (1 - t) + 1)
                if width < 1:
                    width = 1
            else:
                color = 'black'
                width = 1

            self.canvas.create_line(X1, Y1, X2, Y2, fill=color, width=width)


root = tk.Tk()
App(root)
root.mainloop()