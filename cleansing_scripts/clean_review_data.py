import gzip
import pprint
import re
import json
import sys

################ UTILITY FUNCTIONS

# prints fields from line
def print_piped(fields, line):

  max = len(fields)-1
  
  # go through all the fields we want
  for i in range(len(fields)):

    f = fields[i]
    #print(f)
    # try getting the data
    try:
      data = line
      
      # if date we want to split into Month|Day|Year|fulldate
      
      for f2 in f:

        # we don't want | in our data since later on we will
        # be creating a pipe delimeted file
        data = re.sub(r'|', r'', data[f2])
        
        if(f2 == 'date'):
          year,month,day = re.findall(r'([0-9]{4})-([0-9]{2})-([0-9]{2})', data)[0]
          data = month + "|" + day + "|" + year + "|" + month + "/" + day + "/" + year
      
    # if no field, put 'NA'
    except:
      data = 'NA'

    data = re.sub(r'\s{2,}',r' ', str(data)) 
    
    if(i == max):
      print(data)
    else:
      print(data,end="|")

# print headers for pipe delim file    
def print_piped_headers(fields):

  max = len(fields) -1
  
  # header will be the 'last' field in the list
  # but really the only field in the list
  for i in range(len(fields)):
    f = fields[i]   # get fields
    header = f[-1]  

    # we reformated for date field so add in
    # breakdown headers
    if(header == 'date'):
      header = 'month|day|year|fulldate'

    # if last header don't print trailing |
    if(i == max):
      print(header)
    else:
      print(header, end="|")

  

##################

# fields we want to get:
fields = [
  ['review_id'],
  ['user_id'],
  ['business_id'],
  ['stars'],
  ['date'],
  ['useful'],
  ['funny'],
  ['cool'],
  ['text']
]
          
################ 

filepath = sys.argv[1]
#"../raw_data/yelp_review_data.json.gz"
f = gzip.open(filepath)

# print headers
print_piped_headers(fields)

# read in the lines and print out in pipe delimited fashion
l = f.readline()
while l:
  temp_dict = json.loads(l)
  print_piped(fields, temp_dict)
  l = f.readline()

f.close()




