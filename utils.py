#!/usr/bin/env python


def get_error(response, dest):
    r = (
        response.get_secure_cookie(dest) or b'').decode()
    response.clear_cookie(dest)
    return r


def set_error(response, k_v):
    for key, value in k_v.items():
        response.set_secure_cookie(key, value)
        # assert (response.get_secure_cookie(key)).decode() == value
    return response
