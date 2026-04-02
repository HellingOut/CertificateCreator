
import json
import chardet

from models import Field, FieldProperties

class DataLoader:
    
    data: list[list[Field]]
    
    def __init__(self) -> None:
        self.data = []
    
    def load_data(self, file_path: str):
        """Check file extension and load data accordingly"""
        if file_path.endswith('.json'):
            self.load_json(file_path)
        elif file_path.endswith('.csv'):
            self.load_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Please use .json or .csv")
    
    def load_json(self, file_path: str):
        """Load data from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            
            self.data = []
            for item in json_data:
                record = []
                for key, value in item.items():
                    field = Field(
                        key=key,
                        value=value,
                        properties=FieldProperties()
                    )
                    record.append(field)
                self.data.append(record)
    
    def _detect_encoding(self, file_path: str) -> str:
        """Detect file encoding"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'
    
    def load_csv(self, file_path: str):
        """Load data from CSV file"""
        import csv
        with open(file_path, 'r', encoding=self._detect_encoding(file_path)) as f:
            reader = csv.DictReader(f, delimiter=';')
            
            for row in reader:
                if not any(row.values()):
                    continue
                
                cleaned_row = {k: v.strip() if v else '' for k, v in row.items()}
                
                record = []
                
                for column_name, value in cleaned_row.items():
                    if column_name and column_name.strip() and value:
                        field = Field(
                            key=column_name.strip(),
                            value=value,
                            properties=FieldProperties()
                        )
                        record.append(field)
                
                if record:  # добавляем только непустые строки
                    self.data.append(record)

        
    def get_unique_keys(self) -> set:
        """Get unique keys from loaded data"""
        return {
            field.key
            for record in self.data
            for field in record
        }