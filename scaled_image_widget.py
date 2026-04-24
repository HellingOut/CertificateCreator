import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSizePolicy, QApplication
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt


class ScaledImageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap()
        
        # Игнорируем подсказки размера, чтобы layout не блокировал сжатие окна
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setMinimumSize(1, 1)  # Разрешаем сжиматься вплоть до 1x1

    def setPixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        if self._pixmap.isNull():
            return

        painter = QPainter(self)
        # Включаем сглаживание для качественного масштабирования
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Вычисляем размер с сохранением пропорций
        scaled_size = self._pixmap.size().scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
        
        # Центрируем изображение в виджете
        x = (self.width() - scaled_size.width()) // 2
        y = (self.height() - scaled_size.height()) // 2
        
        # drawPixmap с указанием w и h автоматически масштабирует исходник
        painter.drawPixmap(x, y, scaled_size.width(), scaled_size.height(), self._pixmap)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пропорциональное масштабирование QPixmap")
        self.resize(500, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_widget = ScaledImageWidget()
        layout.addWidget(self.image_widget)

        # Пример загрузки (замените на свой путь)
        # self.image_widget.setPixmap(QPixmap("image.png"))
        
        # Для теста создадим пиксмапу программно
        pm = QPixmap(1200, 800)
        pm.fill(Qt.GlobalColor.darkGray)
        self.image_widget.setPixmap(pm)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())