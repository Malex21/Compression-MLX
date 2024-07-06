
from json import load as load_json
from sys import argv
from pickle import dump, load as load_pickle
from os.path import splitext
from bitIO import *
from string import punctuation
import re


def init():

    with open("wordsChar.json") as freqs_json:
        d = load_json(freqs_json)

    i_to_word = list(d.keys())
    i_to_word.sort(key=lambda x: d[x], reverse=True)

    i_to_word = separators + i_to_word

    word_to_i = {w:i for (i, w) in enumerate(i_to_word)}

    with open("i_to_word.pickle", "wb") as i_to_word_file:
        dump(i_to_word, i_to_word_file)

    with open("word_to_i.pickle", "wb") as word_to_i_file:
        dump(word_to_i, word_to_i_file)


def get_mappings():

    i_to_word = []
    word_to_i = dict()

    with open("i_to_word.pickle", "rb") as i_to_word_file:
        i_to_word = load_pickle(i_to_word_file)

    with open("word_to_i.pickle", "rb") as word_to_i_file:
        word_to_i = load_pickle(word_to_i_file)

    return i_to_word, word_to_i


def main():

    global separators
    separators = list(punctuation) + [" "]

    # init()

    i_to_word, word_to_i = get_mappings()

    re_syntax = "[" + punctuation + " \n\t" + "]"
    print(re_syntax)

    print(re.split(re_syntax, "Je suis d'accord, c'est ouf."))

    match argv[1]:
        case "-c":
            compress = True
        case "-d":
            compress = False
        case _:
            raise Exception("There must be a -c or -d flag to compress/decompress")

    if compress:

        with open(argv[2]) as text:
            words = text.read().split()

        output = [word_to_i[w.lower()] for w in words]
        rarete = max([x.bit_length() for x in output]) - 1

        filename = splitext(argv[2])[0] + ".mlx"

        with open(filename, "wb") as outfile:        
            with BitWriter(outfile) as writer:

                writer.writebits(rarete, 5)

                for i in output:
                    writer.writebits(i, rarete)
    
    else:

        filename = splitext(argv[2])[0] + "_decompressed" + ".txt"

        with open(argv[2], "rb") as mlx:
            with open(filename, "w") as outfile:        
                with BitReader(mlx) as reader:

                    rarete = reader.readbits(5)
                    words = []

                    while reader.read:

                        index = reader.readbits(rarete)
                        w = i_to_word[index]
                        words.append(w)
                    
                    outfile.write(" ".join(words))







main()

