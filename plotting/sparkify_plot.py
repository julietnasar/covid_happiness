import pyspark
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys

# maps data with key = date, data = covid stats
def mapByDate(line):

    arr = line.split('|')
    key = datetime.datetime(int(arr[6]), int(arr[4]), int(arr[5]))

    data = arr[12:]
    l = len(data)
    
    # map data as list of lists so we can add each date's fields up later
    for i in range(len(data)):
        data[i] = [data[i]] 
    return (key, data)  # (date, [pos_rate, neg_rate, new_tests, num_hospitalized, deaths, total_tests])

# reduces by common date
def reduceByDate(x, y):

    assert len(x) == len(y)
    ans = x
    for i in range(len(x)):
        
        # only the first two fields positive_rate & neg_rate will change per review
        # the covid stats will be the same so no need to store them in a large list
        if(i < 2):
            ans[i] += y[i]

    return ans

# get the averages for each pos & neg rate per each date
# other fields are left alone
# returns (key, [avg_pos_rate, avg_neg_rate, ...])
def mapAvg(tup):
    ans = []
    key, data = tup[0], tup[1]
    # go through data
    for i in range(len(data)):
        # first two are floats of pos & neg rate
        if(i < 2):
            # get averages
            sum = 0.0
            for j in range(len(data[i])):
                sum += float(data[i][j])
            avg = sum/len(data[i])
            ans += [avg]
        # otherwise just add normally
        else:
            ans += [int(data[i][0])]
    return key, ans


sc = pyspark.SparkContext()

lines = sc.textFile(sys.argv[1])
lines_filtered = lines.filter(lambda x: 'N/A' not in x and len(x.split('|')) == 18) # filter out lines with NA values and more than 18 fields (can happen when reviews have '|')

pairs = lines_filtered.map(mapByDate)   # date, covid_stats_arr

pairs_byDate = pairs.reduceByKey(reduceByDate) # date, [[arr of pos rates], [arr of neg rates], rest of covid stats]
pairs_avgByDate = pairs_byDate.map(mapAvg)     # date, [avg_pos_rate, avg_neg_rate, rest of covid stats]

finalPairs_avg = pairs_avgByDate.sortByKey()   # sort by date asc

# get each field in their own RDD
dates_a = finalPairs_avg.map(lambda x: x[0])
negativity_a = finalPairs_avg.map(lambda x: x[1][1])
positivity_a = finalPairs_avg.map(lambda x: x[1][0])
deaths_a = finalPairs_avg.map(lambda x: x[1][4])

##############################################################

# plots three graphs with same x, diff y's on same figure
def plot(x, y1, y2, y3, x_lab, y1_lab, y2_lab, y3_lab, saveAs):    

    # three subplots
    fig, axis = plt.subplots(3)

    # first subplot
    # green for pos rate
    axis[0].plot(x, y1, color = 'green')
    axis[0].set_title(y1_lab)

    # second subplot
    axis[1].plot(x, y2)
    axis[1].set_title(y2_lab)

    # third subplot
    # red for neg rate
    axis[2].plot(x, y3, color = 'red')
    axis[2].set_title(y3_lab)
    
    fig.tight_layout()
    # set dimensions
    fig.set_size_inches(9,7)

    # save
    fig.savefig(saveAs)

    # show the plot
    plt.show()
    # clear plot
    plt.clf()

# inputting values
# plot
# x = date
# y1 = positivity rate
# y2 = deaths
# y3 = negativity rate
x = dates_a.collect()
plot(x, positivity_a.collect(), deaths_a.collect(), negativity_a.collect(), 'DATE', 'POSITIVITY INDEX', 'DEATHS', 'NEGATIVITY INDEX', 'comparison.pdf')

