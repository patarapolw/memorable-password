from flask import request, render_template
from leetpass.strengthen import Strengthen

from mnemopass.mnemonic import MnemonicGenerator
from webview import app
from webview.image import load_image

mnemonic_generator = MnemonicGenerator()
strengthen = Strengthen()


@app.route('/', methods=['GET', 'POST'])
def index():
    content = dict()
    if request.method == 'POST':
        data = request.form
        if data['generate'] == 'mnemonic':
            content.update(mnemonic_generator.memorize_pin(data['password']))
        elif data['generate'] == 'password':
            content.update(mnemonic_generator.generate_pin(int(data['number_of_keywords'])))
            content['leetspeak'] = strengthen.strengthen(''.join(content['keywords']), target=150)
        content.update(data)
        content['image'] = load_image(' '.join(content['keywords']))
        content['number_of_keywords'] = len(content['keywords'])

    return render_template('index.html', content=content)
