import sys

# a sentiment analyzer object that's main functionality
# is it take in a file of pos words & a file of neg words
# and creates an internal list of words with proper tags
# user can create a sentimentAnalyzer object with their own files
# and run methods to get statistics on english language input lines
class SentimentAnalyzer(object):

    def __init__(self, pos_words_filepath, neg_words_filepath):

        # create dict and add pos and neg words to it with tags 'POS' & 'NEG'
        # upon initialization the Sentiment object automatically loads words from:
        # http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
        self.__words = dict()
        self.__addToDict(neg_words_filepath, 'NEG', self.__words)
        self.__addToDict(pos_words_filepath, 'POS', self.__words)
        
    # filename - file path with words to add
    # tag - data for dict is the tag for the words
    # d - dictionary to add to
    def __addToDict(self, filename, tag, d):

        # open file
        f = open(filename)

        # read in lines
        w = f.readline()
        while(w):
            # in our files ; are comments so we do
            # not want lines starting with ;
            if(w[0] != ';'):
                # add word to words arr with correct tag
                self.__words[w.strip().upper()] = tag
            # try to read in next line, if error then break
            try: w = f.readline()
            except: break

        f.close()

    # prints stored words and their tags separated by \t
    def printWords(self):
        for key in self.__words:
            print(key, "\t", self.__words[key])

    
    # returns tuple  = (pos_rate, neg_rate)
    # takes in single line and returns sentiment statistics
    def get_sentimentRates(self, line):

        # split up the line into words (by space)
        lineSplit = line.split(' ')

        # initialize stats vars
        countPos = 0
        countNeg = 0
        countTot = 0

        # go through each word
        for w in lineSplit:
            w = w.upper() # everything in the dicts is upper
            
            try:
                tag = self.__words[w.strip()] # get emotive tag for that word (if exists in words)
                if tag == 'POS':              # if its POS
                    countPos += 1             # add to positive word count
                if tag == 'NEG':              # if its NEG
                    countNeg += 1             # add to neg word count
                countTot += 1                 # ALWAYS increase the total words count
            except:
                countTot += 1

        # calculate statistics & return        
        pos_rate = countPos/countTot
        neg_rate = countNeg/countTot
        return (pos_rate, neg_rate)
