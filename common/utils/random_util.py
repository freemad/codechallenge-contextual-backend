from django.utils.crypto import get_random_string

ALPHA_NUMERIC = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"


def generate_alphanumeric_uid(length):
    return get_random_string(length, ALPHA_NUMERIC)
