import random
import string

def random_string(length=16):
    letters_and_digits = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(letters_and_digits) for _ in range(length))
    return result_str

