# Compression-MLX

(En cours de développement !)

Outil de compression de fichier texte. Le fichier doit être constitué de mots en anglais, avec ou sans ponctuation, avec une grammaire correcte et sans fautes d'orthographe.

Pour compresser le fichier, on associe à chaque mot anglais un indice, qui est plus petit lorsque le mot est plus fréquemment utilisé. On trouve l'indice maximale des mots dans le fichier, et on trouve le nombre de bits nécessaire pour représenter cet indice.

Ce nombre de bits suffit à représenter chaque indice du texte, donc on écrit simplement l'indice de chaque mot sur ce nombre de bits. Il s'agit du fichier compressé.

La compression est plus efficace si le texte utilise des mots courants, et est beaucoup moins efficace si un mot rare est utilisé. Je travaille sur une solution à cela.
