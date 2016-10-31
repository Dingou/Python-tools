# *.* coding: utf-8 *.*

def Char_Rep(str,o_char,n_char):
    if o_char in str.replace(o_char, n_char):
        Char_Rep(str.replace(o_char, n_char),o_char,n_char)
    else:
        return str.replace(o_char, n_char)