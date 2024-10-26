import json

def json_string(data):
    print(json.dumps(data, indent=2))


def json_file(data, filename, indent=2):
    with open(filename, "w") as f:
        json.dump(data, f, indent=indent)


# def reencode_unicode_escape(string):
#     return string.encode('unicode_escape').decode('unicode_escape')


def to_camel_case(snake_str, sep: str = "_"):
    first, *others = snake_str.split(sep)
    return ''.join([first.lower(), *map(str.title, others)])
