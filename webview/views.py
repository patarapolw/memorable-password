from flask import request, render_template, Markup, jsonify
from randomsentence import SentenceTool

from memorable_password import PasswordGenerator, ToSentence
from webview import mempass
from webview.image import load_image

pass_gen = PasswordGenerator()
to_sentence = ToSentence()
sentence_tool = SentenceTool()


@mempass.route('/', methods=['GET', 'POST'])
def index():
    password = ''
    tagged_token = []

    if request.method == 'POST':
        data = request.form
        if data['generate'] == 'sentence':
            if data['from'] == 'pin':
                password, tagged_token = to_sentence.from_pin(data['material'])
            elif data['from'] == 'initials':
                password, tagged_token = to_sentence.from_initials(data['material'])
            elif data['from'] == 'keywords':
                password, tagged_token = to_sentence.from_keywords(
                    [keyword.strip() for keyword in data['material'].split(',')])
            else:
                if data['type'] == 'password':
                    password, tagged_token = pass_gen.new_password()
                else:
                    password, tagged_token = pass_gen.new_pin()
        elif data['generate'] == 'password':
            if data['type'] == 'password':
                password, tagged_token = pass_gen.new_password()
            else:
                password, tagged_token = pass_gen.new_pin()
        return jsonify({
            'password': password,
            'sentence': render_tokens(tagged_token)
        })
    else:
        password, tagged_token = pass_gen.new_password()

    return render_template('index.html', password=password, sentence=Markup(render_tokens(tagged_token)))


@mempass.route('/img', methods=['POST'])
def image():
    if request.method == 'POST':
        data = request.form
        return load_image(data['sentence'])

    return ''


def render_tokens(tagged_tokens):
    sentence = sentence_tool.detokenize_tagged(tagged_tokens)

    for token, is_overlap in tagged_tokens:
        if is_overlap:
            sentence = sentence.replace(token, '<b>{}</b>'.format(token))

    return sentence
