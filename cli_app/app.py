from getpass import getpass
from password_manager.vault import Vault
from randomsentence.sentence import SentenceTool
import re

from memorable_password import GeneratePassword

gp = GeneratePassword()
sentence_tool = SentenceTool()


def main():
    do_exit = False

    while not do_exit:
        try:
            while True:
                try:
                    vault = Vault(getpass('Please enter the master password : '))
                    break
                except ValueError:
                    continue

            while not do_exit:
                print('Password available for:', ', '.join(dict(vault).keys()))
                name = input('Please type the name of password to view or create a new one, or press q to exit. : ')
                if name == 'q':
                    do_exit = True
                    break

                password, token_list = gp.new_common_diceware_password(hint=name)

                new_entry = dict(vault).get(name, {
                    'password': password,
                    'note': render_tokens(token_list)
                })
                print(new_entry)
                if input('Do you want to save? Press [y/Y] to save: ').lower() == 'y':
                    vault[name] = new_entry

            vault.close()

        except AttributeError:
            continue


def render_tokens(tagged_tokens):
    def boldify(match_obj):
        to_consider = match_obj.group(0)
        if to_consider.lower() == token.lower():
            return '[{}]'.format(to_consider)
        else:
            return to_consider

    sentence = sentence_tool.detokenize_tagged(tagged_tokens)

    for token, is_overlap in sorted(tagged_tokens, key=len):
        if is_overlap:
            sentence = re.sub('(\w+)', boldify, sentence)

    return sentence


if __name__ == '__main__':
    main()
