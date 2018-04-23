#qpy:webapp:mempass
#qpy:fullscreen
#qpy://127.0.0.1:5000/

import os
os.environ['NLTK_DATA'] = '/sdcard/data/nltk_data'
os.chdir(os.path.dirname(os.path.abspath(__file__))) 

from webview import mempass

if __name__ == '__main__':
    mempass.run()
