import formencode
from formencode import validators


def validate_data(**kwargs):
    """Creates a validated data dictionary by taking data posted by user
        """
    data = {}
    if kwargs.get('name'):
        data.update({'name': validators.String().to_python(kwargs.get('name', ''))})
    if kwargs.get('sizes'):
        data.update({'sizes': validators.String().to_python(kwargs.get('sizes', ''))})
    if kwargs.get('price'):
        data.update({'price': validators.Number().to_python(float(kwargs.get('price', 0)))})
    if kwargs.get('delivery'):
        data.update({'delivery': validators.String().to_python(kwargs.get('delivery', ''))})
    
    return data
