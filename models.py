import json
from dataclasses import dataclass, field
from typing import Dict, Any
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt 

@dataclass
class FieldProperties:
    """Свойства поля сертификата"""
    x: float = 50
    y: float = 50
    font: QFont = QFont()
    font_bold: bool = False
    font_italic: bool = False
    font_underline: bool = False
    font_strikeout: bool = False
    alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignHCenter
    color: QColor = field(default_factory=lambda: QColor(0, 0, 0))
    def __init__(self) -> None:
        self.x = 50
        self.y = 50
        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(14)
        self.font_bold = False
        self.font_italic = False
        self.font_underline = False
        self.font_strikeout = False
        self.alignment = Qt.AlignmentFlag.AlignHCenter
        self.color = QColor(0, 0, 0)
        self.outline_color = self.color

    def to_dict(self) -> Dict[str, Any]:
        return {
            'x': self.x, 'y': self.y,
            'font_family': self.font.family(),
            'font_size': self.font.pointSize(),
            'font_bold': self.font.bold(),
            'font_italic': self.font.italic(),
            'font_underline': self.font.underline(),
            'font_strikeout': self.font.strikeOut(),
            'alignment': self.alignment,
            'color': self.color.rgb() if self.color else 0,
            'outline_color': self.outline_color.rgb() if self.outline_color else 0
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FieldProperties':
        props = cls()
        props.x = data.get('x', 0.0)
        props.y = data.get('y', 0.0)
        props.font.setFamily(data.get('font_family', 'Arial'))
        props.font.setPointSize(data.get('font_size', 14))
        props.font.setBold(data.get('font_bold', False))
        props.font.setItalic(data.get('font_italic', False))
        props.font.setUnderline(data.get('font_underline', False))
        props.font.setStrikeOut(data.get('font_strikeout', False))
        props.alignment = data.get('alignment', Qt.AlignmentFlag.AlignHCenter)
        props.color = QColor(data.get('color', 0))
        if data.get('outline_color', 0):
            props.outline_color = QColor(data.get('outline_color', 0))
        return props
    
    def get_qfont(self) -> QFont:
        font = QFont(self.font.family(), self.font.pointSize())
        font.setBold(self.font_bold)
        font.setItalic(self.font_italic)
        font.setUnderline(self.font_underline)
        font.setStrikeOut(self.font_strikeout)
        return font

@dataclass
class Template:
    """Шаблон разметки"""
    name: str = "Новый шаблон"
    fields: Dict[str, FieldProperties] = field(default_factory=dict)
    
    def save(self, filepath: str):
        data = {
            'name': self.name,
            'fields': {name: props.to_dict() for name, props in self.fields.items()}
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'Template':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        template = cls(
            name=data.get('name', 'Шаблон'),
        )
        
        for field_name, props_data in data.get('fields', {}).items():
            template.fields[field_name] = FieldProperties.from_dict(props_data)
        
        return template
