from flask import request, render_template, jsonify

from randomsentence import SentenceTool
import re
import string

from threading import Thread

from memorable_password import PasswordGenerator, ToSentence, Conformize, Mnemonic
from webview import mempass
from webview.image import load_image

sentence_tool = SentenceTool()
pass_gen = PasswordGenerator()
to_sentence = ToSentence()
conformizer = Conformize()
mnemonic = Mnemonic()

Thread(target=pass_gen.init_brown, args=(True,))


@mempass.route('/', methods=['GET', 'POST'])
def index():
    global pass_gen

    if request.method == 'POST':
        data = request.form
        if data['from'] == 'random':
            if data['type'] == 'initials':
                tagged_password = pass_gen.new_initial_password()
            elif data['type'] == 'diceware':
                tagged_password = pass_gen.new_diceware_password()
            else:
                tagged_password = pass_gen.new_pin()

            if tagged_password is not None:
                password, tagged_sentence = tagged_password
            else:
                password = tagged_sentence = ''

        elif data['from'] == 'keywords':
            keywords = [keyword.strip() for keyword in data['material'].replace(' ', ',').split(',')]
            tagged_sentence = to_sentence.from_keywords(keywords)
            if data['type'] in ['initials', 'diceware']:
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
            if data['type'] == 'initials':
                password = conformizer.conformize(initials)
            elif data['type'] == 'diceware':
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
        return render_template('index.html')


@mempass.route('/img', methods=['POST'])
def image():
    if request.method == 'POST':
        data = request.form
        return load_image(data['sentence'])

    return ''


def render_tokens(tagged_tokens):
    def boldify(match_obj):
        to_consider = match_obj.group(0)
        if to_consider.lower() == token.lower():
            return '<b>{}</b>'.format(to_consider)
        else:
            return to_consider

    sentence = sentence_tool.detokenize_tagged(tagged_tokens)

    for token, is_overlap in sorted(tagged_tokens, key=len):
        if is_overlap:
            sentence = re.sub('(\w+)', boldify, sentence)

    return sentence
