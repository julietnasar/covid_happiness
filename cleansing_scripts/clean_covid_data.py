import re
import sys

# dictionary of months and corresponding numeric value (2 dig so if 1 dig has 0 in front)
numeric_months = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07',
                  'August':'08', 'September':'09', 'October':'10','November':'11', 'December':'12'}

# pattern to match per row of input file
table_pat = re.compile(r'<tr>.*?<td.*?Date.*?<span.*?>([^<]+)<.*?State.*?<span.*?>([^<]+)<.*?New tests.*?<span.*?>([^<]+)<.*?Cases.*?<span.*?>([^<]+)<.*?Negative PCR tests.*?<span.*?>([^<]+)<.*?Currently hospitalized.*?<span.*?>([^<]+).*?Deaths.*?<span.*?>([^<]+)', flags = re.DOTALL)

# get data from command line
f = open(sys.argv[1])
data = f.read()

if data:
    # print headers
    print('Month|Day|Year|Full Date|State or Territory|New tests|Negative PCR Tests|Currently Hospitalized|Deaths|Total test results')
    # find all matches
    table = re.findall(table_pat, data)

    # go through matches
    for row in table:
        # go through each individual match item
        for i in range(len(row)-1):

            # we hit the date field if i==0
            # and we want to reformat to numeric
            if(i == 0):

                # replace ',' with '' (there are commas such as: March 14, 2021)
                date = re.sub(r',', r'', row[i])
                # split based on ' ' & assign to proper vars
                month, day, year  = re.split(r' ', date)
                # convert month to numeric month based on our dict (above)
                month = numeric_months[month]

                # formatted date: month/day/year
                formatted_date = month + "/" + day + "/" + year

                # print each var sep by space & the formatted date
                print(month + "|" + day + "|" + year + "|" + formatted_date, end="|")
            # if not a date
            else:
                # print with commas taken out of the numbers
                # eg we want 400000 not 400,000 so it is easier to
                # convert to numeric
                print(re.sub(r',', r'', row[i]), end = "|")

        # fencepost, print last one without |        
        print(re.sub(r',', r'', row[len(row)-1]))
else:
    print("no data")
        

