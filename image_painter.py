
from typing import List

from PySide6.QtGui import QPixmap, QFont, QColor, QPainter
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QLabel

from models import Field

class ImagePainter:
    fields: List[Field] = []
    
    original_pixmap: QPixmap
    rendered_pixmap: QPixmap
    
    # UI Elements
    preview_label: QLabel
    
    def __init__(self):
        self.font_color = QColor(0, 0, 0)

    def update_pixmap(self, fields: list[list[Field]] = [], field_index: int = 0):
        if self.original_pixmap:
            self.rendered_pixmap = self.original_pixmap.copy()
        if self.original_pixmap is None or self.original_pixmap.isNull() or not fields or field_index >= len(fields):
            return
        
        self.rendered_pixmap = self.original_pixmap.copy()
        
        for field in fields[field_index]:
            if field.value.strip():
                # Process each field and add text to pixmap
                new_x = int((field.properties.x / 100.0) * self.rendered_pixmap.width())
                new_y = int((field.properties.y / 100.0) * self.rendered_pixmap.height())
                
                # Add text based on field properties
                self.rendered_pixmap = self.add_text_to_pixmap(
                    self.rendered_pixmap,
                    field.value,
                    position = QPoint(new_x, new_y),
                    text_color = field.properties.color,
                    font = field.properties.font
                )
        self.update_display()
        
    def update_display(self):
        # This method should update the QLabel or any widget displaying the pixmap
        self.preview_label.setPixmap(self.rendered_pixmap)

    def add_text_to_pixmap(
            self,
            pixmap: QPixmap,
            text: str,
            position: QPoint,
            text_color: QColor,
            font: QFont,
    ) -> QPixmap:
        painter = QPainter(pixmap)
        painter.setFont(font)
        painter.setPen(text_color)
        painter.drawText(position, text)
        painter.end()
        return pixmap