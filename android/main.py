from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from randomsentence import SentenceTool
import re
import string

from memorable_password import PasswordGenerator, ToSentence, Conformize, Mnemonic


class Mempass(BoxLayout):
    def toggle_btn_pressed(self, btn):
        print(btn.text)

    def generate_password(self):
        self.ids.password.text = 'asdhaskjd'
        self.ids.sentence.text = 'For cows, [b]feed[/b] providing an intake of 0.1 milligram of Aureomycin per pound of body weight daily aids in the reduction of bacterial diarrhea, in the prevention of foot rot, and in the reduction of losses due to respiratory infection ( infectious rhinotracheitis -- shipping fever complex'


class MempassApp(App):
    def build(self):
        return Mempass()


if __name__ == '__main__':
    # sentence_tool = SentenceTool()
    # to_sentence = ToSentence()
    # conformizer = Conformize()
    # mnemonic = Mnemonic()
    # pass_gen = PasswordGenerator(do_markovify=True)

    MempassApp().run()
