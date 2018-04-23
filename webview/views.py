from flask import request, render_template, jsonify

from randomsentence import SentenceTool
import re
import pickle

from webview import mempass

sentence_tool = SentenceTool()
pass_gen = None


@mempass.route('/', methods=['GET', 'POST'])
def index():
    global pass_gen

    if request.method == 'POST':
        if pass_gen is None:
            with open('generate_password.pkl', 'rb') as f:
                pass_gen = pickle.load(f)

        data = request.form
        password, tagged_sentence = pass_gen.generate(password_from=data['from'],
                                                      password_type=data['type'],
                                                      password_material=data.get('material', ''))

        return jsonify({
            'password': password,
            'sentence': render_tokens(tagged_sentence)
        })
    else:
        return render_template('index.html')


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
