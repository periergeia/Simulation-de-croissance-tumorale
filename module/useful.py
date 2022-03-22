def file_directory_issue():
    """décorateur permettant de solutionner les erreurs liés aux
    chemins d'accès."""
    def inner(func):
        def wrapper(**kwargs):
            # teste si la fonction ne renvoie pas une erreur
            try:
                return func(**kwargs)
            # dan le cas où l'erreur `FileNotFound` est renvoyée
            except FileNotFoundError:
                # le premier argument de la fonction est changée
                # afin que le chemin d'accès désigne le répertoire
                # parent
                kwargs['file_path'] = './.' + kwargs['file_path']
                return func(**kwargs)
        return wrapper
    return inner