list_pos = ["CC", "CD", "DT", "EX", "IN", "JJ", "JJR", "JJS", "MD",
            "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR",
            "RBS", "RP", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
import time
up_to = 4
coord = [0 for i in xrange(up_to)]
for j in xrange(0,len(list_pos)**up_to):
    val = j 
    for power in range(up_to)[::-1]:
        coord[power] = val/(len(list_pos)**power)
        val = val%(len(list_pos)**power)
    print(coord)
