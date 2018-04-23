from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior

import pickle
import re

from randomsentence import SentenceTool

sentence_tool = SentenceTool()


class Mempass(BoxLayout):
    def __init__(self):
        self.pass_gen = None
        super().__init__()

    def from_pressed(self, btn):
        if btn.text == 'Random':
            self.ids.from_text.readonly = True
        else:
            self.ids.from_text.readonly = False

    def generate_password(self):
        if self.pass_gen is None:
            with open('generate_password.pkl', 'rb') as f:
                self.pass_gen = pickle.load(f)

        password_from = 'random'
        password_type = 'initials'
        password_material = ''

        for k, v in self.ids.items():
            if k == 'from_text':
                password_material = v.text.lower()
            if isinstance(v, ToggleButton):
                if k.startswith('from_'):
                    if v.state == 'down':
                        password_from = v.text.lower()
                if k.startswith('type_'):
                    if v.state == 'down':
                        password_type = v.text.lower() if v.text != 'Initialism' else 'initials'

        password, tagged_tokens = self.pass_gen.generate(password_from=password_from,
                                                        password_type=password_type,
                                                        password_material=password_material)
        if password is None:
            password = ''

        self.ids.password.text, self.ids.sentence.text = password, render_tokens(tagged_tokens)


class MempassApp(App):
    def build(self):
        return Mempass()


def render_tokens(tagged_tokens):
    def boldify(match_obj):
        to_consider = match_obj.group(0)
        if to_consider.lower() == token.lower():
            return '[b]{}[/b]'.format(to_consider)
        else:
            return to_consider

    sentence = sentence_tool.detokenize_tagged(tagged_tokens)

    for token, is_overlap in sorted(tagged_tokens, key=len):
        if is_overlap:
            sentence = re.sub('(\w+)', boldify, sentence)

    return sentence


def main():
    ToggleButtonBehavior.allow_no_selection = False
    MempassApp().run()


if __name__ == '__main__':
    main()
