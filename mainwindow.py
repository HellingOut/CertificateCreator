# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from PySide6.QtGui import QAction, QColor, QPixmap, QFont
from PySide6.QtWidgets import QColorDialog
from PySide6.QtCore import QSettings
from data import DataLoader
from models import FieldProperties

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from image_painter import ImagePainter

class MainWindow(QMainWindow):
    selected_field_key: str = ""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize settings
        self.settings = QSettings("CertificateCreator", "CertificateCreator")
        recent = self.settings.value("recent_files", [])
        if isinstance(recent, list):
            self.recent_files = recent
        else:
            self.recent_files = []
        
        # Initialize ImagePainter
        self.data_loader = DataLoader()
        self.image_painter = ImagePainter()
        self.selected_field_key = ""
        self._setup_image_painter()
        self._connect_signals()
        self._populate_recent_menu()
    
    def _setup_image_painter(self):
        """Setup ImagePainter with UI elements"""
        self.image_painter.preview_label = self.ui.certificatePixmap
    
    def _connect_signals(self):
        """Connect UI signals to ImagePainter slots"""
        self.ui.fontComboBox.currentFontChanged.connect(self._set_font)
        self.ui.fontSizeSpinBox.valueChanged.connect(self._change_font_size)
        self.ui.pickColorButton.clicked.connect(self._on_pick_color)
        self.ui.textPositionXSlider.valueChanged.connect(self._on_position_changed)
        self.ui.textPositionYSlider.valueChanged.connect(self._on_position_changed)
        
        self.ui.certificateOpenAction.triggered.connect(self._on_open_certificate)
        self.ui.loadDataAction.triggered.connect(self._on_load_data)
        
        self.ui.fieldsListWidget.itemClicked.connect(self._on_field_selected)
    
    def _populate_recent_menu(self):
        """Populate the recent files menu"""
        self.ui.certificateRecentAction.clear()
        for path in self.recent_files:
            action = self.ui.certificateRecentAction.addAction(path)
            action.triggered.connect(lambda checked, p=path: self.load_image(p))
    
    def _add_recent_file(self, file_path):
        """Add a file to recent files list and save"""
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:10]  # limit to 10
        self.settings.setValue("recent_files", self.recent_files)
        self._populate_recent_menu()
    
    def _on_pick_color(self):
        """Handle color picker button click"""
        current_property = self._get_property(self.selected_field_key)
        color = QColorDialog.getColor(current_property.color, self, "Select Text Color")
        if color.isValid():
            current_property.color = color
            if self.selected_field_key:
                field = self._find_field(self.selected_field_key)
                if field:
                    current_property.color = color
    
    def _on_position_changed(self):
        """Handle position slider changes"""
        current_property = self._get_property(self.selected_field_key)
        if self.selected_field_key:
            field = self._find_field(self.selected_field_key)
            if field:
                current_property.x = self.ui.textPositionXSlider.value()
                current_property.y = self.ui.textPositionYSlider.value()
        self.image_painter.update_pixmap(fields=self.data_loader.data)
    
    def _set_font(self):
        current_property = self._get_property(self.selected_field_key)
        current_property.font.setFamily(self.ui.fontComboBox.currentFont().family())
        
        self.image_painter.update_pixmap(fields=self.data_loader.data)

    def _change_font_size(self):
        current_property = self._get_property(self.selected_field_key)
        if self.selected_field_key:
            field = self._find_field(self.selected_field_key)
            if field:
                current_property.font.setPointSize(self.ui.fontSizeSpinBox.value())
        self.image_painter.update_pixmap(fields=self.data_loader.data)
    
    def load_image(self, image_path: str):
        """Load image into ImagePainter"""
        self.image_painter.original_pixmap = QPixmap(image_path)
        self.image_painter.update_pixmap(fields=self.data_loader.data)
        self.ui.certificatePixmap.setPixmap(self.image_painter.rendered_pixmap)
    
    def _on_open_certificate(self):
        """Handle open certificate action"""
        file_path = QFileDialog.getOpenFileName(
            self,
            "Open Certificate Image",
            "",
            "Images (*.png *.jpg *.bmp)"
        )[0]
        if file_path:
            self.load_image(file_path)
            self._add_recent_file(file_path)
    
    def _on_load_data(self):
        """Handle load data action"""
        file_path = QFileDialog.getOpenFileName(
            self,
            "Load Data File",
            "",
            "Data Files (*.json *.csv)"
        )[0]
        if file_path:
            try:
                self.data_loader.load_data(file_path)
                self.update_data_list()
                # Update ImagePainter with loaded data
                self.image_painter.update_pixmap(fields=self.data_loader.data)
                self.ui.certificatePixmap.setPixmap(self.image_painter.rendered_pixmap)
                self._add_recent_file(file_path)
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def update_data_list(self):
        """Update the fields list widget with loaded data"""
        self.ui.fieldsListWidget.clear()
        unique_keys = self.data_loader.get_unique_keys()
        print(f"Unique keys found: {unique_keys}")
        for field_key in unique_keys:
            field_item = QListWidgetItem(field_key)
            self.ui.fieldsListWidget.addItem(field_item)
            print(f"Added field to list widget: {field_key}")
    
    def _on_field_selected(self, item: QListWidgetItem):
        """Handle field selection from the list widget"""
        selected_key = item.text()
        self.selected_field_key = selected_key
        print(f"Selected field: {selected_key}")
        self.selected_field_key = selected_key
        
        # Load field properties into UI
        field = self._find_field(selected_key)
        if field:
            current_property = self._get_property(self.selected_field_key)
            self.ui.fontComboBox.setCurrentFont(current_property.font)
            self.ui.fontSizeSpinBox.setValue(current_property.font.pointSize())

            self.ui.textPositionXSlider.blockSignals(True)
            self.ui.textPositionXSlider.setValue(int(current_property.x))
            self.ui.textPositionXSlider.blockSignals(False)

            self.ui.textPositionYSlider.blockSignals(True)
            self.ui.textPositionYSlider.setValue(int(current_property.y))
            self.ui.textPositionYSlider.blockSignals(False)

            current_property.color = current_property.color

    def _find_field(self, key: str) -> dict | None:
        """Find field in loaded data by key"""
        for record in self.data_loader.data:
            if key in record:
                return record
        return None

    def _get_property(self, key: str) -> FieldProperties:
        if key not in self.image_painter.properties:
            self.image_painter.properties[key] = FieldProperties()
        return self.image_painter.properties[key]
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())