import base64
import base64
def image_byte_to_base64(byte_str):
    if not isinstance(byte_str, bytes):
        raise TypeError("expecte bytes , not {}".format(type(byte_str)))
    return base64.b64encode(byte_str)

def image_base64_to_byte(b64_str):
    image_data = base64.b64decode(b64_str)
    return image_data