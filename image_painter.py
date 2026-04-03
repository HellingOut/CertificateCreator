
from typing import List

from PySide6.QtGui import QPixmap, QFont, QColor, QPainter
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QLabel

from models import FieldProperties

class ImagePainter:
    properties: dict[str, FieldProperties]
    
    original_pixmap: QPixmap
    rendered_pixmap: QPixmap
    
    # UI Elements
    preview_label: QLabel
    
    def __init__(self):
        self.properties = {}

    def update_pixmap(self, fields: list[dict[str, str]] = [], field_index: int = 0):
        if self.original_pixmap:
            self.rendered_pixmap = self.original_pixmap.copy()
        if self.original_pixmap is None or self.original_pixmap.isNull() or not fields or field_index >= len(fields):
            return
        
        self.rendered_pixmap = self.original_pixmap.copy()
        
        for key, value in fields[field_index].items():
            # Process each field and add text to pixmap
            current_property = self.properties.get(key, FieldProperties())
            new_x = int((current_property.x / 100.0) * self.rendered_pixmap.width())
            new_y = int((current_property.y / 100.0) * self.rendered_pixmap.height())
            
            # Add text based on field properties
            self.rendered_pixmap = self.add_text_to_pixmap(
                self.rendered_pixmap,
                value,
                position = QPoint(new_x, new_y),
                text_color = current_property.color,
                font = current_property.font
            )
            self.properties[key] = FieldProperties(
                x=current_property.x,
                y=current_property.y,
                color=current_property.color,
                font=current_property.font
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