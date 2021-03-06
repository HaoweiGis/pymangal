import json

def makeschema(infos=None, name=None, title="Autogenerated JSON schema"):
    """ Generates a JSON scheme from a dict representing the schema sent by the API

    :param infos: A ``dict`` with the resource schema
    :param name: The name of the resource
    :param title: A description of the object
    """
    if not isinstance(infos, dict):
        raise TypeError("The infos must be passed as a dict")
    if name == None :
        raise ValueError("You must provide a name")
    if not isinstance(name, str):
        raise TypeError("The name must be a string")
    if not isinstance(title, str):
        raise TypeError("The title must be given as a string")
    # These are the top-level objects
    schema = {'title': title, 'type': 'object', '$schema': 'http://json-schema.org/draft-04/schema#'}
    required = []
    properties = {}
    fields = infos['fields']
    for field in fields.keys():
        # Is the field nullable?
        if (not fields[field]['nullable']) and (not field in ['id', 'resource_uri']) :
            required.append(field)
        properties[field] = {}
        # The help_text is the description
        properties[field]['description'] = fields[field]['help_text']
        # The type of the field depends on whether it's related
        if fields[field]['type'] == 'related':
            if fields[field]['related_type'] == 'to_one':
                properties[field]['type'] = 'string'
            else :
                properties[field]['type'] = 'array'
                properties[field]['items'] = {'type': 'string'}
        else :
            properties[field]['type'] = fields[field]['type']
            if fields[field]['type'] == 'float':
                properties[field]['type'] = 'number'
        # Fields with a choice key are enum
        if fields[field].has_key('choices'):
            properties[field]['enum'] = fields[field]['choices']
    schema['required'] = required
    schema['properties'] = properties
    return schema
