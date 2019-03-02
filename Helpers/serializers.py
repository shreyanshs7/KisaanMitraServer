import datetime
from django.db.models import Model

def get_model_json(instance):
    data = {}
    fields = get_model_fields(instance)
    model_properties = get_model_properties(instance.__class__)
    if model_properties is not None:
        fields = fields + model_properties
    for field in fields:
        # temp = {}
        value = getattr(instance, field, None)
        if isinstance(value, datetime.datetime):
            value = str(value)
        if isinstance(value, Model):
            value = get_model_json(value)
        data[field] = value
        # data.append(temp)
    return data

def get_model_fields(instance):
    return [ f.name for f in instance._meta.fields ]

def get_model_properties(model):
    property_names = [ name for name in dir(model) if isinstance(getattr(model, name), property) ]
    return property_names