import pickle

from memorable_password.password import PasswordGenerator

if __name__ == '__main__':
    with open('pass_gen.pkl', 'wb') as f:
        pickle.dump(PasswordGenerator(), f)
