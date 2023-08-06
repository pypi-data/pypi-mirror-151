def to_camel(key: str):
    try:
        attribute_names = key.split('_')
        return attribute_names[0] + ''.join(x.title() for x in attribute_names[1:])
        
    except:
        raise Exception("Invalid key")

def to_snake(key: str):
    try:
        for char in key:
            if char.isupper():
                key = key.replace(char, "_" + char.lower())
                
        return key.lstrip('_')
        
    except:
        raise Exception("Invalid key")
    
def dict_to_camel(dictionary: dict):
    try:
        new_dict = {}
        for key, value in dictionary.items():
            new_dict[to_camel(key)] = value
            
        return new_dict
        
    except:
        raise Exception("Invalid dictionary")
    
def dict_to_snake(dictionary: dict):
    try:
        new_dict = {}
        for key, value in dictionary.items():
            new_dict[to_snake(key)] = value
            
        return new_dict
        
    except:
        raise Exception("Invalid dictionary")
