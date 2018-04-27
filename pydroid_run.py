import os
import sys
import subprocess

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open('requirements.txt') as f:
        for row in f:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', row.strip()])

    import nltk
    with open('nltk.txt') as f:
        for row in f:
            nltk.download(row.strip())

    from kivy_app.main import main
    main()
