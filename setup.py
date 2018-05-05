from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = ['nltk', 'PyYAML', 'markovify', 'randomsentence', 'diceware_utils']
web_requires = ['flask']
pytest_requires = ['xdist', 'repeat', 'timeout', 'doctestplus']
tests_require = ['pytest', 'passwordstrength', 'pronounceable'] \
                + ['pytest-{}'.format(req) for req in pytest_requires]

setup(
    name='memorable_password',  # Required
    version='0.3.0',  # Required
    description='Generate sentence of context, along with keywords/PIN/passwords '
                'to make sure you memorize it!!!',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/patarapolw/memorable-password',  # Optional
    author='Pacharapol Withayasakpunt',  # Optional
    author_email='patarapolw@gmail.com',  # Optional
    license='Apache',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Environment :: Handhelds/PDA\'s',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Android',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='random sentence random_sentence random_word password nltk',  # Optional
    packages=find_packages(exclude=['analysis', 'dev', 'tests']),  # Required
    install_requires=install_requires,  # Optional
    python_requires='>=3.5',
    tests_require=tests_require,
    extras_require={  # Optional
        'tests': tests_require,
        'web': web_requires,
        'heroku': web_requires + ['gunicorn'],  # and *.pkl
        'with-language-check': ['language-check']
    },
    package_data={  # Optional
        'memorable_password': ['database/*'],
    },
)
