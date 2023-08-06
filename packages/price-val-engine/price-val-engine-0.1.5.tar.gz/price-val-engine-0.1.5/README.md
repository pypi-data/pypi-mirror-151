# Price Validation Engine

## Overview

Price Validation Engine is framework to create skeleton to validate last price revision 


## requirements

- python 3.6+
- Linux, MacOS, windows


### install

    pip install price-val-engine


### Start Project
    python -m price_val_engine startproject project_name 


### Project template structure
    - base_dir
        - project_name 
            - __init__.py
            - settings.py
            - validtion_rules.py
        - run.py


### Run project

    python run.py --input=input.csv --output=output.csv 


### input as s3 csv file

    python run.py --input=s3://bucket_name/path/input.csv --output=s3://bucket_name/path/input.csv

### settings.py

 - default validation pipeline

        VALIDATION_PIPELINES = [  
            'price_val_engine.core.validations.general_rules.NullNegativeZeroValidationRule',  
            'price_val_engine.core.validations.general_rules.OutOfRangeValidationRule',  
            'price_val_engine.core.validations.revision_rules.DeltaPercentageFromLastDayRule',  
        ]


### Add new custom validation rule

    - step 1 you can define your custom validtion rules in the file `project_name/validation_rules.py`

        class MyValidationRule(BaseRule)
            name = "validation_rules.myvalidation_rule"
            message = "price could not be gte {max_price}"
            severity = ''

            def is_valid(self, item):
                max_price = 50
                if item['price'] >= max_price:
                    self.message.format(max_price)
                    self.severity = 'HIGH' # you can define severity LOW, MEDIUM and HIGH
    
    - step 2 add your newly defined rule in `setting.py`

        VALIDATION_PIPELINES = [  
            ...,
            'project_name.validation_rules.MyValidationRule
        ]

