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
        self.setMinimumSize(QSize(800, 600)) # Минимальный размер окна

        # Определение списка для хранения кувшинок
        self.DataBase = list()
        self.MaximumSize = 20 # Максимальное кол-во кувшинок

        # Таймер добавления кувшинок
        self.SpawnTimer = QTimer()
        self.SpawnTimer.timeout.connect(self.GenerateCircle)
        self.SpawnTimer.start(250) # Появление кувшинок каждые 500мс    

        # Таймер рендера кувшинок
        self.RenderTimer = QTimer()
        self.RenderTimer.timeout.connect(self.RenderCircle)
        self.RenderTimer.start(50)

    def GenerateCircle(self):
        """Случайная генерация кувшинок"""
        if len(self.DataBase) >= self.MaximumSize: # Проверка на размер списка
            self.DataBase.pop(0) # Удаление самой старой кувшинки в списке

        NewCircle = {
            'x': random.randint(0, self.width()),
            'y': 0,
            'size': 20, 
            'color': QColor(138, 154, 91),
            'dy': 10,
            'life': 100 # Время жизни кувшинки в мс
        }

        self.DataBase.append(NewCircle)

    def RenderCircle(self):
        """Рендер/анимация кувшинок"""
        StashData = list()
        
        for i, circle in enumerate(self.DataBase):

            circle['y'] += circle['dy']

            circle['life'] -= 0.5
            
            if circle['size'] <= 0 or circle['life'] <= 0:
                StashData.append(i)

        for i in sorted(StashData, reverse=True):
            if i < len(self.DataBase):
                self.DataBase.pop(i)
        
        self.update()  # Перерисовка

    def paintEvent(self, event):
        render = QPainter(self)
        render.setRenderHint(QPainter.RenderHint.Antialiasing) # Сглаживание при рендере

        render.fillRect(self.rect(), QColor(240, 240, 240))
        
        for circle in self.DataBase:
            self.renderCircle(render, circle)

        render.setPen(QPen(QColor(0, 0, 0)))
        render.drawText(10, 20, f'Кувшинок: {len(self.DataBase)}')

    def renderCircle(self, render, circle):
        """Рендер кувшинки"""
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
        self.setGeometry(100, 100, 1000, 800)
        
        self.graph = EngineFrog()
        self.setCentralWidget(self.graph)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
