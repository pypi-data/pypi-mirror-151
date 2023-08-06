from price_val_engine.core.data import reader, writer
from price_val_engine.core.exceptions import ImproperlyConfigured
from price_val_engine.conf import settings
from price_val_engine.core import utils
# # __all__ = [
# #     "Engine"
# ]


class BaseValidationEngine(object):
    validation_rules = settings.VALIDATION_PIPELINES
    data_reader = None
    data_writer = None
    
    def __init__(self, 
        input_file_path, 
        output_file_path,
        storage_options=None
        ) -> None:
        
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.storage_options = storage_options or {}
        
        self.items = []
    
    def all(self):
        if self.data_reader is None:
            raise ImproperlyConfigured(
                "Invalid Data Reader class !"
            )
        rows = []
        
        for row in self.data_reader(
                    file_path=self.input_file_path
                ).read():
            rows.append(row)
        return rows
        
    def validate(self, row):
        for validation_cls in self.validation_rules:
            klass = utils.import_model(validation_cls)
            validation = klass()
            if not validation.is_valid(row):
                return False, validation.errors
        return True, {"category": "success", "severity": "",  "reason": "success"}
    
    def validate_all(self):
        for item in self.all():
            is_valid, response = self.validate(item)
            print(response)
            self.items.append({**item, 'is_valid': is_valid, **response})
        return self.items
    
    def save(self):
        if self.data_writer is None:
            raise ImproperlyConfigured(
                "Invalid Data Writer class"
            )  
        if len(self.items):
            fieldnames = list(self.items[0].keys())
            self.data_writer(
                file_path=self.output_file_path
            ).write(self.items, headers=fieldnames)
        
    
class ValidationEngine(BaseValidationEngine):
    data_reader = reader.CSVReader
    data_writer = writer.CSVWriter
    
    
Engine = ValidationEngine