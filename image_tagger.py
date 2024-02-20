import json
import os.path

from utils import tuple_to_str, str_to_tuple
from image_viewer import ASCIIImageViewer


class ASCIIImageTagger(ASCIIImageViewer):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.tags = {}
        self.data_filepath = self.filepath + ".json"
        self.load()

    def add(self, tag, list_of_positions=None):
        """Adds the tag to each positions tuple(x,y) in the list"""
        if not list_of_positions:
            list_of_positions = [(self.x, self.y)]
        for pos in list_of_positions:
            if not (pos[0], pos[1]) in self.tags.keys():
                self.tags[(pos[0], pos[1])] = []
            if tag not in self.tags[(pos[0], pos[1])]:
                self.tags[(pos[0], pos[1])].append(tag)

    def remove(self, tag, list_of_positions=None):
        """Removes the tag from each positions tuple(x,y) in the list"""
        if not list_of_positions:
            list_of_positions = [(self.x, self.y)]
        for pos in list_of_positions:
            if (pos[0], pos[1]) in self.tags.keys():
                self.tags[(pos[0], pos[1])].remove(tag)

    @property
    def all_tags(self):
        tag_list = []
        for key, value in self.tags.items():
            tag_list.append(*value)
        return list(set(tag_list))

    @property
    def tags_at_current(self):
        # Returns the tags for current position
        if (self.x, self.y) in self.tags.keys():
            return self.tags[(self.x, self.y)]
        return None

    def __repr__(self):
        r = super().__repr__()
        return f"{r} | {self.tags_at_current}"

    def save(self):
        # saves the data to filepath.json
        tags = {tuple_to_str(key): value for key, value in self.tags.items()}
        with open(self.data_filepath, 'w') as f:
            json.dump(tags, f, indent=4)

    def load(self):
        # Tries to load filepath.json from disc
        if os.path.exists(self.data_filepath):
            with open(self.data_filepath, 'r') as f:
                data_dict = json.load(f)
                self.tags = {str_to_tuple(key): value for key, value in data_dict.items()}