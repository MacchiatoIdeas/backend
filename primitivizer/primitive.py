import re

DEFAULT_REPLACES = {
    'á' : 'a',
    'é' : 'e',
    'í' : 'i',
    'ó' : 'o',
    'ú' : 'u',
    'ü' : 'u',
    'ñ' : 'n',
    'os ' : 'o ',
    'es ' : ' ',
    'as ' : 'a ',
    'ces ' : 'z ',
    'ca' : 'ka',
    'ce' : 'ze',
    'ci' : 'zi',
    'co' : 'ko',
    'cu' : 'ku',
    'ge' : 'je',
    'gi' : 'ji',
    'cs' : 'x',
    'que' : 'ke',
    'qui' : 'ki',
    's' : 'z',
    'h' : '',
    'v' : 'b',
    'll' : 'y',
    'rr' : 'r'
}


def primitivize_word(strin,replaces=DEFAULT_REPLACES):
    stri = strin.lower()+" "
    for k in replaces:
        stri = stri.replace(k,replaces[k])
    return stri[:-1]

def primitivize_string(stri,replaces=DEFAULT_REPLACES,ignore=[],minlen=4):
    words = re.sub(r'[^\wáéíóúñüÁÉÍÓÚÜ]+', ' ', stri)
    words = set(words.split(" "))
    words = [primitivize_word(x,replaces) for x in words if len(x)>=minlen and x not in ignore]
    words = sorted(words)
    return ' '.join(words)
