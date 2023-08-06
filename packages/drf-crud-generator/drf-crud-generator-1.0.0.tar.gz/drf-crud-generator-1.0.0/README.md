# DRF Crud API Generator

This project focuses on creating crud api for all custom django apps. This project handles content types in models. This project also provides url for api documentation. This project automatically finds out manually created apps listed in installed apps and reads their schema file to create all related crud api.

## Using crud generator
---
1. Create a python app and register it in settings.py
```
python manage.py startapp <app_name>
```
2. create <mark>schema.py</mark> inside <app_name> with syntax similar to below syntax<br>
```
app_config = {
    "app_name": "<app_name>",
    "content_type": <BooleanValue>,
    "models": {
        "<model_1>":{
            "<field_1>": {
                "datatype": "CharField",
                "blank": True,
                "null": True,
                "max_length": 50,
                "unique": True
            },
            "<field_2>": {
                "datatype": "ForeignKey",
                "model": "<model_to_be_used_for_foreignkey_reference>",
                "on_delete": "models.CASCADE",
                "blank": True,
                "null": True
            },
            "content_type_field": {
                "content_type_name": "<abc>",
                "object_id_name": "<deff>",
                "content_object_name": "<pqr>"             
            }
        },
        "<model_2>":{
            "<field_1>": {
                "datatype": "CharField",
                "blank": True,
                "null": True,
                "max_length": 50,
                "unique": True
            }
        }
    }
}
```
```
Placeholders ==> <app_name>, <model_1>, <model_2>, <field_1>, <field_2>
```

3. inside python shell run below command,
```
python manage.py generate_crud
```
[Note:
 
i)Can add any number of models and fields with comma separation

## Contributing
---
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
---
[MIT](https://choosealicense.com/licenses/mit/)