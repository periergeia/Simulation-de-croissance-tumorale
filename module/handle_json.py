import json
try:
    from useful import file_directory_issue
except:
    from module.useful import file_directory_issue


@file_directory_issue()
def get_dict(file_path):
    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)
    file.close()
    return data

@file_directory_issue()
def write(file_path, dict_key, new_data):
    """"""
    data = get_dict(file_path=file_path)
    data[dict_key] = new_data
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_value(file_path, key):
    """"""
    data = get_dict(file_path=file_path)
    return data[key]