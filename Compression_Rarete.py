
from sys import argv
from pickle import dump, load as load
from os.path import splitext
from bitIO import *
from string import punctuation
import re


def get_mappings():

    with open("top_english_words_mixed_1000000.txt", encoding="utf-8") as top_words:
        i_to_word = top_words.read().splitlines()

    i_to_word_copy = i_to_word.copy()

    for i, word in enumerate(i_to_word):

        if "'" in word:
            new_word = word.replace("'", "")
            i_to_word_copy.insert(i, new_word)

    i_to_word = special_chars + i_to_word_copy

    word_to_i = {w:i for (i, w) in enumerate(i_to_word)}

    return i_to_word, word_to_i


def main():

    global special_chars
    special_chars = [" ", "", "\n", "\t"] + list(punctuation)

    i_to_word, word_to_i = get_mappings()

    match argv[1]:
        case "-c":
            compress = True
        case "-d":
            compress = False
        case _:
            raise Exception("There must be a -c or -d flag to compress/decompress")

    if compress:

        with open(argv[2]) as text:
            words = re.findall(r"[\w']+|[.,!?;:%\n\t]", text.read())

        output = [word_to_i[w] for w in words]

        rarete = max([x.bit_length() for x in output])

        filename = splitext(argv[2])[0] + ".mlx"

        with open(filename, "wb") as outfile:        
            with BitWriter(outfile) as writer:

                writer.writebits(rarete, 5)

                for i in output:
                    writer.writebits(i + 1, rarete)
                
                writer.writebits(0, rarete)
    
    else:

        filename = splitext(argv[2])[0] + "_decompressed" + ".txt"

        with open(argv[2], "rb") as mlx:
            with open(filename, "w") as outfile:        
                with BitReader(mlx) as reader:

                    rarete = reader.readbits(5)
                    words = []

                    index = reader.readbits(rarete)

                    while index != 0:

                        w = i_to_word[index - 1]
                        words.append(w)
                        index = reader.readbits(rarete)           

                    sentence = " ".join(words)
                    to_correct = {f" {c}": f"{c}" for c in ",;.%\n\t"}
                    to_correct.update({"\n ": "\n", "\t ": "\t"})

                    for old, new in to_correct.items():
                        sentence = sentence.replace(old, new)

                    outfile.write(sentence)


main()

