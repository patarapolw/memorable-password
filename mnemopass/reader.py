from random import choice

from mnemopass.dir import wordnet_path, database_path


class PartOfSpeech:
    def __init__(self, part_of_speech):
        with open(database_path('google-10000-english.txt')) as f:
            common = set(f.read().strip().split('\n'))
        self.entries = list()
        with open(wordnet_path('index.{}'.format(part_of_speech))) as f:
            for row in f:
                contents = row.split(' ')
                if contents[0]:
                    if contents[0] in common:
                        self.entries.append(contents[0])

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, item):
        return self.entries[item]


if __name__ == '__main__':
    for type_of_pos in ['adj', 'adv', 'noun', 'verb']:
        pos = PartOfSpeech(type_of_pos)
        print(type_of_pos, choice(pos), choice(pos))
