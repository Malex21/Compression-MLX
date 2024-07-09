
from bitIO import BitWriter
from re import findall

print(findall(r"[\w']+|[.,!?;:%\n]",
 """This is a test.
This is also a test, lol
This too !"""))

# with open("texte.mlx", "r") as output:

#     binary = output.readline()

#     print(' '.join(format(ord(x), 'b').zfill(8) for x in binary))

# with open("test.mlx", "wb") as test:

#     with BitWriter(test) as writer:

#         writer.writebits(14, 5)
    
# with open("test.mlx", "r") as output:

#     binary = output.readline()

#     print(' '.join(format(ord(x), 'b').zfill(8) for x in binary))