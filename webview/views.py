from flask import request, render_template

from memorable_password import PasswordGenerator, ToSentence
from webview import mempass
from webview.image import load_image

pass_gen = PasswordGenerator()
to_sentence = ToSentence()


@mempass.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        if data['generate'] == 'sentence':
            if 'pin' in data.keys():
                return to_sentence.from_pin(data['pin'])
            elif 'initial' in data.keys():
                return to_sentence.from_initials(data['initial'])
            elif 'keywords' in data.keys():
                return to_sentence.from_keywords(data['keywords'].split(' '))
        elif data['generate'] == 'password':
            if 'type' in data.keys():
                if data['type'] == 'password':
                    return pass_gen.new_password()
                elif data['type'] == 'pin':
                    return pass_gen.new_pin()

    content = pass_gen.new_password()
    return render_template('index.html', content=content)


@mempass.route('/img', methods=['POST'])
def image():
    if request.method == 'POST':
        data = request.form
        return load_image(data['sentence'])

    return ''
