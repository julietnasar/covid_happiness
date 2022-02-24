import sys

####### get dict of covid stats to add to file
covid_dict = {}

# get filepath of covid data
filepath = sys.argv[1]
f = open(filepath)


# fields indeces
formatted_date_index = 3
new_tests_index = 5
currently_hospitalized_index = 7
deaths_index = 8
total_tests_index = 9

# read first line
# fencepost
l = f.readline()

# read in rest of lines
while(l):
    # split line by |
    fields = l.split("|")
    
    # key is formatted date
    key = fields[formatted_date_index]
    # data is tuple of (new tests, currently_hospitalized, deaths, total_tests)
    data = (fields[new_tests_index], fields[currently_hospitalized_index], fields[deaths_index], fields[total_tests_index])

    # add to dict
    covid_dict[key] = data

    # get next line
    l = f.readline()

# close file
f.close()

######### READ IN REVIEW DATA, ADDING ON COVID STATS BY DATE

date_index = 7

# get review data from command line
filepath = sys.argv[2] 
f = open(filepath)

# get first line
l = f.readline()

# first line is headers so print headers + covid stats
print(l.split('|'),'new_tests', 'currently_hospitalized', 'deaths', 'total_tests',sep = '|')

# read in rest of lines
while(l):

    # split by |
    fields = l.split("|")
    
    try:
        # try and find covid stats for specific date
        covid_stats = covid_dict[fields[date_index]]

        # print the line split by |
        print(l.strip(), end = "|")

        # print the covid stats at the end
        for i in range(len(covid_stats)-1):
            print(covid_stats[i].strip(), end = "|")
        # print last stat without | at end
        print(covid_stats[len(covid_stats)-1].strip())
    # if date not found in covid dict, pass    
    except:
        pass
 
    l = f.readline()

f.close()
