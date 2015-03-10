"""
The function that used to be part of my Sentence_Probability class. 
I got rid of it when I realized that I could implement the same thing in a much easier manner.
I'm still to sentimental to get rid of it, but it was making me mad sitting 
at the bottom of the working file. 
WONT WORK!!!
"""

    def calc_cumulative_prob(self,coordinates):
        """
        coordinates are the coordinates of the parts of speech in the list_pos list.
        I don't want to crowd this function up with a bunch of stuff - it has to run quick!
        """
        length = len(coordinates)
        if length > self.total_prob.shape[2]:
            print("You need to make sure that the number of coordinates is equal to or less than the depth of non cumulative array")
        else:
            prob = 1
            for i in xrange(length-1):
                if coordinates[i] == None or coordinates[i+1] == None:
                    continue
                else:
                    posB = int(coordinates[i])
                    posA = int(coordinates[i+1])
                    prob *= self.total_prob[posB,posA,i]
            return prob

    def calc_cumu_prob(self,sentence,**kwargs):
        """
        This function calculates the cumulative probability of a sentence that you supply it. 
        The sentence should be a list whose elements are a tuple -- (word, p_o_s)
        This is the one I want to use outside of the class. The one above is to used in the calc_cumulative_prob method.

        **kwargs:
            - position: The position in the sentence about which you want it to calculate the probability. 
            If position is in the middle of the sentence, then it will calculate probability using the 
            3 previous words (if available) and the 3 after the word (if available). If position is the last word,
            it will use 3 previous entries to calculate probability. 
        """
        first_chunk = 3
        second_chunk = 3
        if len(sentence) == 1 and isinstance(sentence[0],list):
            sentence = sentence[0]
        if len(sentence) == 1 and isinstance(sentence[0],tuple):
            print("One word sentence: Returning 0.0")
            return 0.0
        elif len(sentence) != 1: 
            sentence = sentence 
        length = len(sentence)

        # print(sentence[0])
        try:
            position = int(kwargs['position'])
            coord = [None for i in xrange(length)]
            coord2 = tuple([list_pos.index(word[1]) for word in sentence])
            # print(coord2)
            if position > length-1:
                print("Position argument provided is bigger than length of sentence. Defaulting to last position.")
                position = len(sentence)-1
            else:
                pass

            if length <= first_chunk+second_chunk: #sentence isn't long enough for this positional business to matter.
                coord = coord2
            elif position < first_chunk:
                coord[0:position+first_chunk+1] = coord2[0:position+first_chunk+1]
            elif position > length - second_chunk:
                coord[position-second_chunk:length] = coord2[position-second_chunk:length]
            else:
                coord[position-first_chunk:position+second_chunk+1] = coord2[position-first_chunk:position+second_chunk+1]
        
        except (KeyError,ValueError):
            coord = tuple([list_pos.index(word[1]) for word in sentence])

        try:
            if len(sentence) != len(self.cumu_prob.shape):
                raise ValueError("The sentence doesn't have the right length")
            else:
                prob = self.cumu_prob[coord]
                return prob

        except AttributeError:
            # this means the cumu_prob variable doesn't exist -- it hasn't been loaded in or the method 
            # above hasn't been called. Cumulative probabilty thing is deprecated as of now. 
            # print(coord)
            if len(sentence) > self.up_to_all_probs:
                # raise ValueError("The sentence doesn't have the right length")
                coord = coord[0:self.up_to_all_probs]
                prob = self.calc_cumulative_prob(coord)
                return prob
            else:
                prob = self.calc_cumulative_prob(coord)
                return prob

    def total_cumulative_prob(self, up_to_cumu=3, write_to_file=False):
        """
        assumes the all_probs method has already been called. (fix)
        max_val = initial up_to
        """
        up_to_cumu = int(up_to_cumu)
        dimension = [len(list_pos) for i in xrange(up_to_cumu)]
        master = np.zeros(len(list_pos)**up_to_cumu,dtype=float)
        coord = [0 for i in xrange(up_to_cumu)]
        for j in xrange(0,len(list_pos)**up_to_cumu):
            if j % 50000 == 0:
                print("Only {} iterations to go!".format(len(list_pos)**up_to_cumu - j))
            val = j 
            for power in range(up_to_cumu)[::-1]:
                coord[power] = val/(len(list_pos)**power)
                val = val%(len(list_pos)**power)
            master[j] = self.calc_cumulative_prob(coord[::-1])
        self.cumu_prob = master.reshape(dimension)
        if write_to_file:
            with InOut(self.text_dir):
                with open("prob{}.py".format(self.filename.strip('.txt')), 'a') as writer:
                    writer.write("var_cumu = {}\n".format(str(master.reshape(dimension))))

            return self.cumu_prob
        else:
            return self.cumu_prob

def cond_prob(tagged_text, magic_range, index1, index2, p1, p2):
    """
    tokenized_sentence_list is the list of sentences whose words have been tokenized and p.o.s. tagged.
    index1 is the index of A (in P(A|B))
    index2 is the index of B 
    p1 is the position of A in the sentence
    p2 is the position of B in the sentence 
    """
    magic_range = list(magic_range)
    special_index = index1  # A
    special_index2 = index2  # B
    tokenized_sentence_list = tagged_text
    # foo = imp.load_source('tokentesttext', '{}/tokentesttext.py'.format(text_dir))
    # tokenized_sentence_list = foo.var1

    def make_matrix(index_to_start):
        for index1, sentence in enumerate(tokenized_sentence_list):
            if index1 <= index_to_start:
                pass
            else:
                if len(sentence) >= magic_range[0] and len(sentence) <= magic_range[1]:
                    sentence_matrix = []
                    freq_given_special = np.zeros(len(list_pos))
                    for index_sen, word in enumerate(sentence):
                        row = np.zeros(len(list_pos))
                        # Below I'm constructing a vector that will allow me to
                        # calculate P(B|A)
                        # At position p1 and the part of speech is the one
                        # we're testing.
                        if index_sen == p1 and word in list_pos[special_index]:
                            for index, p_o_s in enumerate(list_pos):
                                if sentence[p2] in p_o_s:
                                    freq_given_special[index] += 1
                                    break
                        for index, pos in enumerate(list_pos):
                            if word in pos:
                                row[index] = int(1)
                                sentence_matrix.append(row)
                                break
                            else:
                                pass
                        # this is to ensure that the row gets appended no
                        # matter what
                        if list(row) == list(np.zeros(len(list_pos))):
                            sentence_matrix.append(row)
                    while len(sentence_matrix) < magic_range[1]:
                        sentence_matrix.append(np.zeros(len(list_pos)))
                    return (sentence_matrix, freq_given_special, index1)
                else:
                    pass
    A = np.zeros(
        magic_range[1] * len(list_pos)).reshape((magic_range[1], len(list_pos)))
    B = np.zeros(len(list_pos))
    t = 1
    factor = float(3.0 / 4.0)
    while t < int(float(len(tokenized_sentence_list)) * factor):
        stuff = make_matrix(t)
        matrix = stuff[0]
        freq_B_A = stuff[1]
        t = stuff[2]
        B = np.add(B, freq_B_A)
        A = np.add(A, matrix)
    # calculating P(A|B)
    # print(B)
    row2 = A[p2]
    # print(row2)
    numerator = ((row2[special_index2]) / np.sum(row2)) * \
        (B[special_index2] / np.sum(B))
    denominator = 0
    for i in xrange(0, len(B)):
        denominator += ((row2[i]) / np.sum(A[p2])) * (B[i] / np.sum(B))

    return numerator / denominator


    def independent(self):
        """
        This function returns a dictionary of the most probable pairs at each position in the sentence.
        """
        dic = {}
        try:
            test = self.total_prob
        except NameError:
            self.all_probs()
        for h in xrange(self.up_to):
            position = self.total_prob[h]
            maxB = []
            max_index = []
            for B in position:
                maxB.append(max(B))
                max_index.append(B.index(max(B)))
            dic[str(h)] = (max(maxB), list_pos[maxB.index(max(maxB))],
                           list_pos[max_index[maxB.index(max(maxB))]])  # (maxprob,A,B)
            # print(h, dic[str(h)], list_pos[dic[str(h)][1]],
            #       list_pos[dic[str(h)][2]])
        return dic

    def naive_dependent(self):
        """
        This function returns a dictionary of the most probable pairs,
        using the A from the previous step as the new B. 
        """
        try:
            test = self.total_prob
        except NameError:
            self.all_probs()
        dic = {}
        new_B = 0
        for h in xrange(self.up_to):
            if h == 0:
                position = self.total_prob[h]
                maxB = []
                max_index = []
                for A in position:
                    maxB.append(max(A))
                    max_index.append(A.index(max(A)))
                new_B = maxB.index(max(maxB))
                dic[str(h)] = (max(maxB), list_pos[maxB.index(max(maxB))],
                               list_pos[max_index[maxB.index(max(maxB))]])  # (maxprob,A,B)
                # print(h, dic[str(h)], list_pos[dic[str(h)][1]],
                #       list_pos[dic[str(h)][2]])
            else:
                position = self.total_prob[h]
                special = [position[i][new_B] for i in xrange(0, len(position))]
                old_B = new_B
                new_B = special.index(max(special))
                dic[str(h)] = (max(special), list_pos[new_B], list_pos[old_B])  # maxprob, A, B
                # print(h, dic[str(h)], list_pos[dic[str(h)][1]],
                #       list_pos[dic[str(h)][2]])
        return dic

    def smart_dependent(self):
        """
        This function generates the sentence with the highest probability. 
        """
        try:
            test = self.total_prob
        except NameError:
            self.all_probs()

        def calc_prob(A,B):
            prob = float(self.total_prob[0][A][B])
            new_B = A
            size = len(self.total_prob[0])
            dic = {'0': (prob, list_pos[A],list_pos[B])}
            for h in xrange(1,self.up_to):
                special = [self.total_prob[h][i][new_B] for i in xrange(size)]
                old_B = new_B
                new_B = special.index(max(special))
                dic[str(h)] = (max(special),list_pos[new_B],list_pos[old_B])
                prob *= max(special)
            return {'prob':prob,'dict':dic}

        current_A = 0
        current_B = 0
        current_prob = calc_prob(current_A,current_B)['prob']
        for A in xrange(len(list_pos)):
            for B in xrange(len(list_pos)):
                test_prob = calc_prob(A,B)['prob']
                # print(test_prob)
                if test_prob > current_prob:
                    current_prob = test_prob
                    current_A = A
                    current_B = B
                else:
                    pass
        return {"total prob": current_prob, 'dict': calc_prob(current_A,current_B)['dict']}
