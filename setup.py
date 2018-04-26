from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

related_projects = ['git+https://github.com/patarapolw/randomsentence.git',
                    'git+https://github.com/patarapolw/passwordstrength.git',
                    'git+https://github.com/patarapolw/pronounceable.git']
install_requires = ['nltk', 'PyYAML', 'markovify', 'flask']
android_requires = ['kivy']
pytest_requires = ['xdist', 'repeat', 'timeout', 'doctestplus']
tests_require = ['pytest'] + ['pytest-{}'.format(req) for req in pytest_requires]

setup(
    name='memorable_password',  # Required
    version='0.2.0',  # Required
    description='Generate sentence of context, along with keywords/PIN/passwords '
                'to make sure you memorize it!!!',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/patarapolw/memorable-password',  # Optional
    author='Pacharapol Withayasakpunt',  # Optional
    author_email='patarapolw@gmail.com',  # Optional
    # classifiers=[  # Optional
    #     # How mature is this project? Common values are
    #     #   3 - Alpha
    #     #   4 - Beta
    #     #   5 - Production/Stable
    #     'Development Status :: 3 - Alpha',
    #
    #     # Indicate who your project is intended for
    #     'Intended Audience :: Developers',
    #     'Topic :: Software Development :: Build Tools',
    #
    #     # Pick your license as you wish
    #     'License :: OSI Approved :: MIT License',
    #
    #     # Specify the Python versions you support here. In particular, ensure
    #     # that you indicate whether you support Python 2, Python 3 or both.
    #     'Programming Language :: Python :: 2',
    #     'Programming Language :: Python :: 2.7',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.4',
    #     'Programming Language :: Python :: 3.5',
    #     'Programming Language :: Python :: 3.6',
    # ],
    keywords='random sentence random_sentence random_word password nltk',  # Optional
    packages=find_packages(exclude=['tests']),  # Required
    install_requires=install_requires,  # Optional
    dependency_links=related_projects,
    python_requires='>=3',
    tests_require=pytest_requires,
    extras_require={  # Optional
        'test': ['tox'] + pytest_requires,
        'android': android_requires,
        'heroku': ['gunicorn'],  # and *.pkl
        'with-language-check': ['language-check']
    },
    package_data={  # Optional
        'memorable_password': ['database/*'],
    },
)
