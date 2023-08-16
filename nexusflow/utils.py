import uuid


def string_uuid() -> str:
    """
    Returns a string UUID.
    """
    return str(uuid.uuid4())




def datatype_to_str(type_) -> str:
    """ Serializes a python object to a string.

    :param type_: The type to serialize
    :type type_: type
    ...
    :raises TypeError: If the type is not supported
    ...
    :return: The serialized type
    :rtype: str
    """
    if type_ == str:
        return 'str'
    elif type_ == int:
        return 'int'
    elif type_ == float:
        return 'float'
    elif type_ == bool:
        return 'bool'
    elif type_ == list:
        return 'list'
    elif type_ == dict:
        return 'dict'
    elif type_ == tuple:
        return 'tuple'
    elif type_ == set:
        return 'set'
    else:
        raise TypeError(f"Type {type_} is not supported")


def str_to_datatype(type_: str) -> type:
    """ Deserializes a string to a python object.

    :param type_: The type to deserialize
    :type type_: str
    ...
    :raises TypeError: If the type is not supported
    ...
    :return: The deserialized type
    :rtype: type
    """
    if type_ == 'str':
        return str
    elif type_ == 'int':
        return int
    elif type_ == 'float':
        return float
    elif type_ == 'bool':
        return bool
    elif type_ == 'list':
        return list
    elif type_ == 'dict':
        return dict
    elif type_ == 'tuple':
        return tuple
    elif type_ == 'set':
        return set
    else:
        raise TypeError(f"Type {type_} is not supported")
