"""module permettant de gérer un fichier un fichier JSON."""
# ## déplacement possible vers useful.py


# importations de modules
import json
try:
    from useful import file_directory_issue
except ModuleNotFoundError:
    from module.useful import file_directory_issue


@file_directory_issue()
def get_dict(file_path):
    """renvoie un dictionnaire, celui converti depuis le fichier
    JSON spécifié  par `file_path`."""
    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)
    file.close()
    return data


@file_directory_issue()
def write(file_path, dict_key, new_data):
    """modfifie le fichier JSON `file_path` en remplaçant la valeur
    de la clef `dict_key` par `new_data`."""
    data = get_dict(file_path=file_path)
    data[dict_key] = new_data
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_value(file_path, key):
    """permet d'obtenir une valeur (sous forme de dictionnaire
    au vu de la structure des fichiers JSON) de `file_path`
    d'après la clef `key`"""
    data = get_dict(file_path=file_path)
    return data[key]
