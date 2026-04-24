import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSizePolicy
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