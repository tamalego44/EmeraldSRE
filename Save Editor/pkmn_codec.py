import codecs
import string

from typing import Tuple

# prepare map from numbers to letters
#_encode_table = {str(number): bytes(letter, 'ascii') for number, letter in enumerate(string.ascii_lowercase)}

_decode_table = {
    0: ' ',
    0xA0: "ʳᵉ",
    0xA1: "0",
    0xA2: "1",
    0xA3: "2",
    0xA4: "3",
    0xA5: "4",
    0xA6: "5",
    0xA7: "6",
    0xA8: "7",
    0xA9: "8",
    0xAA: "9",
    0xAB: "!",
    0xAC: "?",
    0xAD: ".",
    0xAE: "-",
    0xAF: "・",
    0xB0: "…", # …
    0xB1: "“",
    0xB2: "”",
    0xB3: "‘",
    0xB4: "’",
    0xB5: "♂",
    0xB6: "♀",
    0xB7: "$",
    0xB8: ",",
    0xB9: "×",
    0xBA: "/",
    0xBB: "A",
    0xBC: "B",
    0xBD: "C",
    0xBE: "D",
    0xBF: "E",
    0xC0: "F",
    0xC1: "G",
    0xC2: "H",
    0xC3: "I",
    0xC4: "J",
    0xC5: "K",
    0xC6: "L",
    0xC7: "M",
    0xC8: "N",
    0xC9: "O",
    0xCA: "P",
    0xCB: "Q",
    0xCC: "R",
    0xCD: "S",
    0xCE: "T",
    0xCF: "U",
    0xD0: "V",
    0xD1: "W",
    0xD2: "X",
    0xD3: "Y",
    0xD4: "Z",
    0xD5: "a",
    0xD6: "b",
    0xD7: "c",
    0xD8: "d",
    0xD9: "e",
    0xDA: "f",
    0xDB: "g",
    0xDC: "h",
    0xDD: "i",
    0xDE: "j",
    0xDF: "k",
    0xE0: "l",
    0xE1: "m",
    0xE2: "n",
    0xE3: "o",
    0xE4: "p",
    0xE5: "q",
    0xE6: "r",
    0xE7: "s",
    0xE8: "t",
    0xE9: "u",
    0xEA: "v",
    0xEB: "w",
    0xEC: "x",
    0xED: "y",
    0xEE: "z",
    0xEF: "▶",
    0xF0: ":",
    0xF1: "Ä",
    0xF2: "Ö",
    0xF3: "Ü",
    0xF4: "ä",
    0xF5: "ö",
    0xF6: "ü",
    0xF7: " ",
    0xF8: " ",
    0xF9: " ",
    0xFA: ".", # <ctrl char>
    0xFB: ".", # <ctrl char>
    0xFC: ".", # <ctrl char>
    0xFD: ".", # <ctrl char>
    0xFE: ".", # <ctrl char>
    0xFF: ".", # <ctrl char>
}



# prepare inverse map
_encode_table = {v: k for k, v in _decode_table.items()}


def custom_encode(text: str) -> Tuple[bytes, int]:
    # example encoder that converts ints to letters
    # see https://docs.python.org/3/library/codecs.html#codecs.Codec.encode
    return bytes([_encode_table[x] for x in text]), len(text)


def custom_decode(binary: bytes) -> Tuple[str, int]:
    # example decoder that converts letters to ints
    # see https://docs.python.org/3/library/codecs.html#codecs.Codec.decode
    #return '.', 1
    return ''.join((_decode_table[x] if (x in _decode_table) else '.') for x in binary), len(binary)



def custom_search_function(encoding_name):
    return codecs.CodecInfo(custom_encode, custom_decode, name='pkmn')


def main():

    # register your custom codec
    # note that CodecInfo.name is used later
    codecs.register(custom_search_function)
    
    binary = bytearray([0xC2, 0xC3])


    #binary = b'abcdefg'
    # decode letters to numbers
    text = codecs.decode(binary, encoding='pkmn')
    print(text)
    # encode numbers to letters
    binary2 = codecs.encode(text, encoding='pkmn')
    print(binary2)
    # encode(decode(...)) should be an identity function
    print(binary == binary2)


if __name__ == '__main__':
    main()