from enum import Enum

class DataType(Enum):
    STRING = 1
    NUMBER = 2
    BOOL = 3
    ARRAY = 4
    DICT = 5
    NONE = 6

def encode_type(data_type):
    return data_type.value.to_bytes(1, byteorder='big')

def encode_length(length):
    return length.to_bytes(1, byteorder='big')

def encode_string(string):
    encoded_string = string.encode('utf-8')
    length_bytes = encode_length(len(encoded_string))
    return encode_type(DataType.STRING) + length_bytes + encoded_string

def encode_number(number):
    encoded_number = number.to_bytes(4, byteorder='big', signed=True)
    return encode_type(DataType.NUMBER) + encoded_number

def encode_bool(boolean):
    return encode_type(DataType.BOOL) + (b'\x01' if boolean else b'\x00')

def encode_none():
    return encode_type(DataType.NONE)

def encode_array(array):
    encoded_elements = []
    for element in array:
        encoded_elements.append(encode(element))
    length_bytes = encode_length(len(encoded_elements))
    return encode_type(DataType.ARRAY) + length_bytes + b''.join(encoded_elements)

def encode_dict(dictionary):
    encoded_elements = []
    for key, value in dictionary.items():
        encoded_key = encode(key)
        encoded_value = encode(value)
        encoded_elements.append(encoded_key + encoded_value)
    length_bytes = encode_length(len(encoded_elements))
    return encode_type(DataType.DICT) + length_bytes + b''.join(encoded_elements)

def encode(data):
    if type(data) is str:
        return encode_string(data)
    elif type(data) is int or type(data) is float:
        return encode_number(data)
    elif type(data) is bool:
        return encode_bool(data)
    elif type(data) is list:
        return encode_array(data)
    elif type(data) is dict:
        return encode_dict(data)
    elif data is None:
        return encode_none()
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")




def decode_type(data):
    return DataType(data[0])

def read_length(data):
    length = 0
    shift = 0
    for byte in data:
        length |= (byte & 0x7F) << shift
        shift += 7
        if not (byte & 0x80):
            break
    return length

def decode_string(data):
    decoded_data = {
        "Type": None,
        "Length": None,
        "Data": None
    }
    length = read_length(data[1:])
    encoded_string = data[2:].decode('utf-8')
    decoded_data["Type"] = decode_type(data).name
    decoded_data["Length"] = length
    decoded_data["Data"] = encoded_string
    return decoded_data

def decode_number(data):
    decoded_data = {
        "Type": None,
        "Data": None,
    }
    number = int.from_bytes(data[1:], byteorder='big', signed=True)
    decoded_data["Type"] = decode_type(data).name
    decoded_data["Data"] = number
    return decoded_data

def decode_bool(data):
    decoded_data = {
        "Type": None,
        "Data": None,
    }
    value = bool(data[1])
    decoded_data["Type"] = decode_type(data).name
    decoded_data["Data"] = value
    return decoded_data

def decode_none():
    return None

def decode_array(data):
    length = read_length(data[1:])
    elements = []
    offset = 1 + len(length)
    for _ in range(length):
        data_type, value = decode(data[offset:])
        offset += len(data[offset:])
        elements.append(value)
    return decode_type(data).name, elements

def decode_dict(data):
    length = read_length(data[1:])
    elements = {}
    offset = 1 + len(length)
    for _ in range(length):
        key_type, key = decode(data[offset:])
        offset += len(data[offset:])
        value_type, value = decode(data[offset:])
        offset += len(data[offset:])
        elements[key] = value
    return decode_type(data).name, elements

def decode(data):
    data_type = decode_type(data)

    if data_type is DataType.STRING:
        return decode_string(data)
    elif data_type is DataType.NUMBER:
        return decode_number(data)
    elif data_type is DataType.BOOL:
        return decode_bool(data)
    elif data_type is DataType.ARRAY:
        return decode_array(data)
    elif data_type is DataType.DICT:
        return decode_dict(data)
    elif data_type is DataType.NONE:
        return decode_none()
    else:
        raise ValueError(f"Unknown data type: {data_type}")


data = 6585746
encoded_data = encode(data)
print("Encoded data:", encoded_data)

decoded_data = decode(encoded_data)
print("Decoded data:", decoded_data)












