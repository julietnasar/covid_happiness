# script to add sentimentAnalysis stats to the end of a pipe delim
# file where the input lines are located in the last column 

from sentimentAnalysis import SentimentAnalyzer
import sys

# create sentiment analyzer object
analyzer = SentimentAnalyzer(sys.argv[1], sys.argv[2])  # input positive_words filepath as argv[1]
                                                        # and negative_words filepath as argv[2]

filepath = sys.argv[3]   # input filepath to add on analysis as argv[3] 

f = open(filepath, "r")  # open input file for reading


# fencepost loop: read in first line
line = f.readline() 
first = True   # bool value to tell us if this is the first iteration so we can print headings

# go through lines
while(line):
    # if this is the first line, it is full of headings
    # add stats heading and print
    if(first):
        print(line + "pos_rate|neg_rate")
        first = False
    # if data rows
    else:
        # get yelp review (last col)
        review = line.split("|")[-1]
        # get sentiment analysis stats
        tup = analyzer.get_sentimentRates(review)
        # print pipe delimeted
        print(line.strip() + "|" + str(tup[0]) + "|" + str(tup[1]))
    # get next line
    line = f.readline()
# close file when done
f.close()
    
