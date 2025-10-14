import sys
import random
import math
from PyQt6.QtCore import QSize, QTimer, QPoint, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush

class EngineFrog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FrogApp")
        #self.setMinimumSize(QSize(800, 600)) # Минимальный размер окна
        self.setFixedSize(800, 600)
        self.DataBase = list() # Список с информацией и всех кувшинках
        self.MaximumSize = 20 # Максимальное кол-во кувшинок

        # Таймер добавления кувшинок в приложении
        self.SpawnTimer = QTimer()
        self.SpawnTimer.timeout.connect(self.GenerateCircle)
        self.SpawnTimer.start(100)  

        # Таймер рендера кувшинок
        self.RenderTimer = QTimer()
        self.RenderTimer.timeout.connect(self.RenderCircle)
        self.RenderTimer.start(50)

        self.frog = {
            'x': 25,
            'y': self.height() // 2,
            'size': 15,
            'color': QColor(255, 0, 0),
            'direction': 1,  # 1 - вправо, -1 - влево
            'target': None,  # следующая кувшинка
        }
        self.trail = None

        # Таймер между прыжками лягушки
        self.JumpTimer = QTimer()
        self.JumpTimer.timeout.connect(self.frog_jump)
        self.JumpTimer.start(150)

    def GenerateCircle(self): # Генератор кувшинок
        if len(self.DataBase) >= self.MaximumSize: # Проверка
            self.DataBase.pop(0) # Удаление самой старой кувшинки в списке

        NewCircle = {
            'x': random.randint(50, self.width() - 50),
            'y': 0,
            'size': 20, 
            'color': QColor(138, 154, 91),
            'dy': 10,
            'life': 100
        }
        self.DataBase.append(NewCircle)

    def RenderCircle(self):
        StashData = list() # Список для удаления кувшинок

        for i, circle in enumerate(self.DataBase):

            circle['y'] += circle['dy']

            circle['life'] -= 0.5
            
            if circle['size'] <= 0 or circle['life'] <= 0 or circle['y'] > self.height() + circle['size']:
                StashData.append(i)

        for i in sorted(StashData, reverse=True):
            if i < len(self.DataBase):
                self.DataBase.pop(i)
        self.update()  # Перерисовка

    def find_next_target(self):
        if self.frog['direction'] == 1:
            candidates = [c for c in self.DataBase if c['x'] > self.frog['x'] and c['life'] > 0 and c['size'] > 0 and c['y'] < self.height()]
            bank_x = self.width() - 25
            bank_y = self.height() // 2
        else:
            candidates = [c for c in self.DataBase if c['x'] < self.frog['x'] and c['life'] > 0 and c['size'] > 0 and c['y'] < self.height()]
            bank_x = 25
            bank_y = self.height() // 2

        if candidates:
            return min(candidates, key = lambda c: abs(c['x'] - self.frog['x']))
        else:
            return {'x': bank_x, 'y': bank_y, 'is_bank': True}

    def frog_jump(self):
        target = self.find_next_target()
        
        self.trail = {
            'start_x': self.frog['x'],
            'start_y': self.frog['y'],
            'end_x': target['x'],
            'end_y': target['y']
        }

        self.frog['x'] = target['x']
        self.frog['y'] = target['y']

        if 'is_bank' in target:
            self.frog['direction'] *= -1
        else:
            self.DataBase = [c for c in self.DataBase if c != target] # Удаление кувшинки после приземления

        self.update()  # Перерисовка

    def paintEvent(self, event):
        render = QPainter(self)
        render.setRenderHint(QPainter.RenderHint.Antialiasing) # Сглаживание
        render.fillRect(self.rect(), QColor(240, 240, 240))
        
        # Левый берег
        render.setBrush(QBrush(QColor(194, 154, 74)))
        render.drawRect(0, 0, 50, self.height())

        # Правый берег
        render.drawRect(self.width() - 50, 0, 50, self.height())
        
        for circle in self.DataBase:
            self.renderCircle(render, circle)
        self.renderCircle(render, self.frog)

        if self.trail:
            render.setPen(QPen(QColor(0, 0, 0), 1, Qt.PenStyle.SolidLine))
            render.drawLine(
                int(self.trail['start_x']), int(self.trail['start_y']),
                int(self.trail['end_x']), int(self.trail['end_y'])
            )

        render.setPen(QPen(QColor(0, 0, 0)))
        render.drawText(10, 20, f'Кувшинок: {len(self.DataBase)}')

    def renderCircle(self, render, circle):
        value = QPen(QColor(0, 0, 0), 1)
        render.setPen(value)

        color = QBrush(circle['color'])
        render.setBrush(color)

        d = circle['size'] * 2
        render.drawEllipse(
            int(circle['x'] - circle['size']),
            int(circle['y'] - circle['size']),
            int(d),
            int(d)
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindowApp")
        self.setFixedSize(800, 600)
        #self.setGeometry(100, 100, 1000, 800)
        
        self.graph = EngineFrog()
        self.setCentralWidget(self.graph)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())