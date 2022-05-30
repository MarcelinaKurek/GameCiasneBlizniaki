class BNode(object):
    def __init__(self, letter, position, letters_in_path=0, nones_in_path=0, path_to_root=[]):
        self.letter = letter
        self.position = position
        self.letters_in_path = letters_in_path
        self.nones_in_path = nones_in_path

