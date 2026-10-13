# task3.py
# Составная кубическая кривая Безье.
# Управляем только точками: ЛКМ добавить / тащить, ПКМ удалить.
# Касательные считаются сами (Catmull-Rom), чтобы кривая была гладкой.

import tkinter as tk


# считаем 4 контрольных точки для одного сегмента Безье
# между точками p1 и p2. p0 и p3 — соседи (нужны для гладкости).
def bezier_controls(p0, p1, p2, p3):
    b0 = p1
    b3 = p2

    # направление касательной в p1 и p2
    b1 = (p1[0] + (p2[0] - p0[0]) / 6.0,
          p1[1] + (p2[1] - p0[1]) / 6.0)
    b2 = (p2[0] - (p3[0] - p1[0]) / 6.0,
          p2[1] - (p3[1] - p1[1]) / 6.0)

    return b0, b1, b2, b3


# точка на кубической кривой Безье
def bezier_point(b0, b1, b2, b3, t):
    u = 1 - t
    x = u*u*u * b0[0] + 3*u*u*t * b1[0] + 3*u*t*t * b2[0] + t*t*t * b3[0]
    y = u*u*u * b0[1] + 3*u*u*t * b1[1] + 3*u*t*t * b2[1] + t*t*t * b3[1]
    return x, y


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Кривая Безье')

        self.canvas = tk.Canvas(root, bg='white', width=900, height=600)
        self.canvas.pack(fill='both', expand=True)

        self.points = [(100, 400), (300, 150), (500, 500), (700, 200), (830, 400)]
        self.drag = -1   # индекс перетаскиваемой точки

        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind('<Button-3>', self.on_right)

        label = tk.Label(root, text='ЛКМ добавить / тащить точку, ПКМ удалить')
        label.pack()

        self.draw()

    def find_point(self, x, y):
        for i in range(len(self.points)):
            px, py = self.points[i]
            if (px - x) ** 2 + (py - y) ** 2 <= 12 * 12:
                return i
        return -1

    def on_press(self, e):
        i = self.find_point(e.x, e.y)
        if i == -1:
            self.points.append((e.x, e.y))
            i = len(self.points) - 1
        self.drag = i
        self.draw()

    def on_move(self, e):
        if self.drag != -1:
            self.points[self.drag] = (e.x, e.y)
            self.draw()

    def on_release(self, e):
        self.drag = -1
        self.draw()

    def on_right(self, e):
        i = self.find_point(e.x, e.y)
        if i != -1:
            self.points.pop(i)
            self.draw()

    def draw(self):
        self.canvas.delete('all')

        n = len(self.points)

        # рисуем сегменты Безье
        if n >= 2:
            for i in range(n - 1):
                # соседи для гладкости
                if i == 0:
                    p0 = self.points[0]
                else:
                    p0 = self.points[i - 1]

                if i + 2 < n:
                    p3 = self.points[i + 2]
                else:
                    p3 = self.points[n - 1]

                b0, b1, b2, b3 = bezier_controls(p0, self.points[i],
                                                 self.points[i + 1], p3)

                # ломаная из точек Безье
                coords = []
                for j in range(51):
                    t = j / 50.0
                    x, y = bezier_point(b0, b1, b2, b3, t)
                    coords.append(x)
                    coords.append(y)

                self.canvas.create_line(coords, fill='blue', width=3,
                                        smooth=True)

            # серая ломаная между опорными точками
            flat = []
            for p in self.points:
                flat.append(p[0])
                flat.append(p[1])
            self.canvas.create_line(flat, fill='lightgray', dash=(4, 3))

        # сами точки
        for i in range(n):
            x, y = self.points[i]
            if i == self.drag:
                color = 'red'
            else:
                color = 'orange'
            self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6,
                                    fill=color, outline='black')


root = tk.Tk()
App(root)
root.mainloop()