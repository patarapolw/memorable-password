from flask import request, render_template, Markup, jsonify

from randomsentence import SentenceTool
import re
import string

from memorable_password import PasswordGenerator, ToSentence, Conformize, Mnemonic
from webview import mempass
from webview.image import load_image

pass_gen = PasswordGenerator()
to_sentence = ToSentence()
sentence_tool = SentenceTool()
conformizer = Conformize()
mnemonic = Mnemonic()


@mempass.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        if data['from'] == 'random':
            if data['type'] == 'password':
                tagged_password = pass_gen.new_password()
            else:
                tagged_password = pass_gen.new_pin()

            if tagged_password is not None:
                password, tagged_sentence = tagged_password
            else:
                password = tagged_sentence = ''

        elif data['from'] == 'keywords':
            keywords = [keyword.strip() for keyword in data['material'].split(',')]
            tagged_sentence = to_sentence.from_keywords(keywords)
            if data['type'] == 'password':
                password = conformizer.conformize(
                    re.sub('{}'.format(re.escape(string.punctuation)), '', ''.join(keywords)))
            else:
                password = ''.join([mnemonic.word_to_key('major_system', keyword.lower()) for keyword in keywords])
        elif data['from'] == 'pin':
            tagged_sentence = to_sentence.from_pin(data['material'])
            if data['type'] == 'password':
                password = conformizer.conformize(''.join([token for token, overlap in tagged_sentence if overlap]))
            else:
                password = data['material']
        else:  # from 'initials'
            initials = data['material']
            tagged_sentence = to_sentence.from_initials(initials)
            if data['type'] == 'password':
                keywords = [token for token, overlap in tagged_sentence if overlap]
                password = conformizer.conformize(
                    re.sub('{}'.format(re.escape(string.punctuation)), '', ''.join(keywords)))
            else:
                password = ''.join([mnemonic.word_to_key('major_system', char.lower()) for char in initials])

        return jsonify({
            'password': password,
            'sentence': render_tokens(tagged_sentence)
        })
    else:
        tagged_password = pass_gen.new_password()
        if tagged_password is None:
            tagged_password = ('', '')

    return render_template('index.html',
                           password=tagged_password[0], sentence=Markup(render_tokens(tagged_password[1])))


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
