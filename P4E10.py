from random import randint


def get_random_password():
    random_num = ""
    while len(random_num) < 8:
        random_number = randint(40, 126)
        random_num += chr(random_number)
    return random_num