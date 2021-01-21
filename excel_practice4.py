# module imports
import openpyxl
import datetime
import sqlite3
import sqlite_practice
from sqlite_practice import total_mean
from sqlite_practice import total_stdv

# import .xlsx workbook and sheet
import_book = openpyxl.load_workbook("J:/PCR Analysis/Raw Results Files form Biomark1/Data Analysis Export Files/2021/January/4/20210104145858_26_0.xlsx")
import_sheet = import_book.active

readout_book = openpyxl.Workbook()
sheet = readout_book.active

# import_sheet values as list of tuples
results = []
for i in import_sheet.values:
    results.append(i)

# place result values in list of strings
column_f = []
for row in results:
    column_f.append(row[5])
print(column_f)


# count result types from sheet
positive_count = column_f.count('Positive')
negative_count = column_f.count('Negative')
notemplate_count = column_f.count('No Template')
print("")
print("Positive count = " + str(positive_count) + ", Negative count = " + str(negative_count) + ", No Template count = " + str(notemplate_count))
print("")

sheet["d1"] = "Positive count = " + str(positive_count) + ", Negative count = " + str(negative_count) + ", No Template count = " + str(notemplate_count)
# sheet["c1"] = positive_count
# sheet["c2"] = negative_count
# sheet["c3"] = notemplate_count

positive_count = int(positive_count)
negative_count = int(negative_count)
notemplate_count = int(notemplate_count)

# Determine total number of positive and negative samples
total_count = positive_count + negative_count
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

sheet["d5"] = "Total mean positive % = " + str(total_positive_average)
sheet["d6"] = "Total stdev = " + str(total_stdev)

if positive_percent > total_positive_average + total_stdev:
    sheet["d7"] = "Positive sample % falls greater than one standard deviation from total mean"

elif positive_percent < total_positive_average - total_stdev:
    sheet["d7"] = "Positive samples fall lower than one standard deviation from total mean"

else:
    sheet["d7"] = "Number of positive samples falls within one standard deviation of YTD positive percent average."


readout_book.save("J:/Python/Python results/sample_readout2.xlsx")
