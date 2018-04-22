from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior

from randomsentence import SentenceTool
import re
import string

from memorable_password import PasswordGenerator, ToSentence, Conformize, Mnemonic

ToggleButtonBehavior.allow_no_selection = False


class Mempass(BoxLayout):
    def __init__(self):
        self.controller = Controller()
        super().__init__()

    def from_pressed(self, btn):
        if btn.text == 'Random':
            self.ids.from_text.readonly = True
        else:
            self.ids.from_text.readonly = False

    def generate_password(self):
        password_from = 'random'
        password_type = 'initials'
        password_material = ''

        for k, v in self.ids.items():
            if k == 'from_text':
                password_material = v.text
            if isinstance(v, ToggleButton):
                if k.startswith('from_'):
                    if v.state == 'down':
                        password_from = v.text
                if k.startswith('type_'):
                    if v.state == 'down':
                        password_type = v.text

        self.ids.password.text, self.ids.sentence.text = self.controller.generate(password_from=password_from,
                                                                                  password_type=password_type,
                                                                                  password_material=password_material)


class MempassApp(App):
    def build(self):
        return Mempass()


class Controller:
    def __init__(self):
        self.sentence_tool = SentenceTool()
        self.to_sentence = ToSentence()
        self.conformizer = Conformize()
        self.mnemonic = Mnemonic()
        self.pass_gen = PasswordGenerator(do_markovify=True)

    def generate(self, password_from, password_type, password_material):
        print(password_from, password_type, password_material)
        if password_from == 'Random':
            if password_type == 'Initialism':
                tagged_password = self.pass_gen.new_initial_password()
            elif password_type == 'Diceware':
                tagged_password = self.pass_gen.new_diceware_password()
            else:
                tagged_password = self.pass_gen.new_pin()

            if tagged_password is not None:
                password, tagged_sentence = tagged_password
            else:
                password = tagged_sentence = ''

        elif password_from == 'Keywords':
            keywords = [keyword.strip() for keyword in password_material.replace(' ', ',').split(',')]
            tagged_sentence = self.to_sentence.from_keywords(keywords)
            if password_type in ['Initialism', 'Diceware']:
                password = self.conformizer.conformize(
                    re.sub('{}'.format(re.escape(string.punctuation)), '', ''.join(keywords)))
            else:
                password = ''.join([self.mnemonic.word_to_key('major_system', keyword.lower()) for keyword in keywords])
        elif password_from == 'PIN':
            tagged_sentence = self.to_sentence.from_pin(password_material)
            if password_type == 'Diceware':
                password = self.conformizer.conformize(''.join([token for token, overlap in tagged_sentence if overlap]))
            else:
                password = password_material
        else:  # from 'initials'
            initials = password_material
            tagged_sentence = self.to_sentence.from_initials(initials)
            if password_type == 'Initialism':
                password = self.conformizer.conformize(initials)
            elif password_type == 'Diceware':
                keywords = [token for token, overlap in tagged_sentence if overlap]
                password = self.conformizer.conformize(
                    re.sub('{}'.format(re.escape(string.punctuation)), '', ''.join(keywords)))
            else:
                password = ''.join([self.mnemonic.word_to_key('major_system', char.lower()) for char in initials])

        return password, self.render_tokens(tagged_sentence)

    def render_tokens(self, tagged_tokens):
        def boldify(match_obj):
            to_consider = match_obj.group(0)
            if to_consider.lower() == token.lower():
                return '[b]{}[/b]'.format(to_consider)
            else:
                return to_consider

        sentence = self.sentence_tool.detokenize_tagged(tagged_tokens)

        for token, is_overlap in sorted(tagged_tokens, key=len):
            if is_overlap:
                sentence = re.sub('(\w+)', boldify, sentence)

        return sentence


if __name__ == '__main__':
    MempassApp().run()
