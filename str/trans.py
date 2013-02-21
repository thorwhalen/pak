__author__ = 'thorwhalen'


# input: string or list (of strings)
# output: string of ascii char correspondents
#   (replacing, for example, accentuated letters with non-accentuated versions of the latter)
def toascii(s):
    from unidecode import unidecode
    import codecs
    if isinstance(s,str):
        return unidecode(codecs.decode(s, 'utf-8'))
    elif isinstance(s,list):
        return map(lambda x:unidecode(codecs.decode(x, 'utf-8')),s)

