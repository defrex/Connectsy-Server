from db import CSEncoder

def json_encoder(obj): #FIXME: I'm not happy with this function's name
    return CSEncoder().encode(obj)
