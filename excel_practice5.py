# README: this version of the main working script will accept .csv files instead of .xlsx files.
# this version will also accept "Inconclusive" results (previous versions did not)

import csv
import openpyxl
import pandas as pd
import datetime
import sqlite3

import sqlite_practice
from sqlite_practice import total_mean
from sqlite_practice import total_stdv

# open readout sheet
readout_book = openpyxl.Workbook()
sheet = readout_book.active


# import .csv file with results
with open(r'J:\Python\other\1691246219__.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    interpretation = []
    for row in reader:
        interpretation.append(row[5])
interpretation = interpretation[12:]
print(interpretation)


# count result types from .csv
positive_count = interpretation.count('Positive')
negative_count = interpretation.count('Negative')
inconclusive_count = interpretation.count('Inconclusive')
notemplate_count = interpretation.count('No Template')
print("")
print("Positive count = " + str(positive_count) + "\nNegative count = " + str(negative_count) + "\nInconclusive count = " + str(inconclusive_count)+ "\nNo Template count = " + str(notemplate_count))
print("")

sheet["d1"] = "Positive count = " + str(positive_count) + ", Negative count = " + str(negative_count) + ", Inconclusive count = " + str(inconclusive_count)+ ", No Template count = " + str(notemplate_count)
# sheet["c1"] = positive_count
# sheet["c2"] = negative_count
# sheet["c3"] = notemplate_count

positive_count = int(positive_count)
negative_count = int(negative_count)
notemplate_count = int(notemplate_count)

# Determine total number of positive and negative samples
total_count = positive_count + negative_count + inconclusive_count
sheet["d2"] = "Total actual sample count = " + str(total_count)

# Determine percentage of each result type in batch
if positive_count == 0:
    positive_percent = 0
else:
    positive_percent = (positive_count / total_count) * 100
if negative_count == 0:
    negative_percent = 0
else:
    negative_percent = (negative_count / total_count) * 100
if inconclusive_count == 0:
    inconclusive_percent = 0
else:
    inconclusive_percent = (inconclusive_count / total_count) * 100
sheet['d5'] = "Inconclusive percent = " + str(inconclusive_percent) + "%"
sheet["d4"] = "Positive percent = " + str(positive_percent) + "%"
sheet["d3"] = "Negative percent = " + str(negative_percent) + "%"

# Insert date/time stamp to readout file
sheet["a1"] = datetime.datetime.now().strftime("%d/%m/%Y")
sheet["a2"] = datetime.datetime.now().strftime("%H:%M:%S")

# connect to database
conn = sqlite3.connect('test.db')
print("Opened database successfully.")
c = conn.cursor()


# Save date/ timestamp and positive percent to database

timestamp = str(datetime.datetime.now().strftime("%d/%m/%Y") + " , " + datetime.datetime.now().strftime("%H:%M:%S"))
positive_percent = positive_percent
print(timestamp, positive_percent)
c.execute("INSERT INTO results VALUES ('{}', '{}')".format(timestamp, positive_percent))
conn.commit()
conn.close()
print("Closed database successfully.")

# Insert total positive mean from calculator for comparison
total_positive_average = total_mean
total_stdev = total_stdv
print("Total mean positive % = " + str(total_positive_average))
print("Total stdev = " + str(total_stdev))

sheet["d6"] = "Total mean positive % = " + str(total_positive_average)
sheet["d7"] = "Total stdev = " + str(total_stdev)

if positive_percent > total_positive_average + total_stdev:
    sheet["d8"] = "Positive sample % falls greater than one standard deviation from total mean (pos %)."

elif positive_percent < total_positive_average - total_stdev:
    sheet["d8"] = "Positive sample % falls lower than one standard deviation from total mean."

else:
    sheet["d8"] = "Positive sample % falls within one standard deviation of total mean."


readout_book.save("J:/Python/Python results/sample_readout2.xlsx")
