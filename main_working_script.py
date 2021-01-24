# README: this version will recursively search and run through all .csv files in target directory
# this version of the main working script will accept .csv files instead of .xlsx files.
# this version will accept "Inconclusive" results (previous versions did not)

import csv
import openpyxl
import datetime
import sqlite3
import os


file_names = []
target = 'J:\PCR Analysis\Raw Results Files form Biomark1\Data Analysis Export Files'
for root, dirs, files in os.walk(target):
    for file in files:
        if file.endswith('.csv'):
            file_names.append(os.path.join(root,file))
print("Number of files : " + str(len(file_names)))
print(file_names)

index = 0
for i in file_names:
    with open(file_names[index], 'r') as csv_file:
        reader = csv.reader(csv_file)
        path_object = file_names[index]
        file_name = path_object[75:]
        file_name = file_name.replace('\\','-')
        # print(file_name)
        index += 1
        interpretation = []
        for i in reader:
            interpretation.append(i)

        interpretation = interpretation[13:]
        row_5 = []
        for row in interpretation:
            row_5.append(row[5])

        interpretation = row_5
        # print(interpretation)

        # open readout sheet
        readout_book = openpyxl.Workbook()
        sheet = readout_book.active

        # count result types from .csv
        positive_count = interpretation.count('Positive') + interpretation.count('POSITIVE')
        negative_count = interpretation.count('Negative') + interpretation.count('NEGATIVE')
        inconclusive_count = interpretation.count('Inconclusive') + interpretation.count('INCONCLUSIVE')
        notemplate_count = interpretation.count('No Template') + interpretation.count('NO TEMPLATE')
        # print("")
        # print("Positive count = " + str(positive_count) + "\nNegative count = " + str(negative_count) + "\nInconclusive count = " + str(inconclusive_count) + "\nNo Template count = " + str(notemplate_count))
        # print("")

        sheet["c1"] = "Positive count = " + str(positive_count) + ", Negative count = " + str(negative_count) + ", Inconclusive count = " + str(inconclusive_count) + ", No Template count = " + str(notemplate_count)
        # sheet["c1"] = positive_count
        # sheet["c2"] = negative_count
        # sheet["c3"] = notemplate_count

        positive_count = int(positive_count)
        negative_count = int(negative_count)
        notemplate_count = int(notemplate_count)

        # Determine total number of positive and negative samples
        total_count = positive_count + negative_count + inconclusive_count
        sheet["c2"] = "Total actual specimen count = " + str(total_count)

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
        sheet["c3"] = "Negative percent = " + str(negative_percent) + " %"
        sheet['c4'] = "Inconclusive percent = " + str(inconclusive_percent) + " %"
        sheet["c5"] = "Positive percent = " + str(positive_percent) + " %"

        # Insert date/time stamp to readout file
        sheet["a1"] = "Date : " + datetime.datetime.now().strftime("%d/%m/%Y")
        sheet["a2"] = "Time : " + datetime.datetime.now().strftime("%H:%M:%S")

        # connect to database
        conn = sqlite3.connect('database.db')
        # print("Opened database successfully.")
        c = conn.cursor()

        # Save date/ timestamp and positive percent to database, close database

        timestamp = str(datetime.datetime.now().strftime("%d/%m/%Y") + " , " + datetime.datetime.now().strftime("%H:%M:%S"))
        positive_percent = positive_percent
        # print(timestamp, positive_percent)
        c.execute("INSERT INTO results VALUES ('{}', '{}')".format(timestamp, positive_percent))
        conn.commit()
        conn.close()
        # print("Closed database successfully.")

        # Connect to calculator
        import sqlite_practice
        from sqlite_practice import total_mean
        from sqlite_practice import total_stdv

        # Insert total positive mean from calculator for comparison
        total_positive_average = total_mean
        total_stdev = total_stdv
        # print("Total mean positive % = " + str(total_positive_average))
        # print("Total stdev = " + str(total_stdev))

        sheet["c6"] = "Total mean positive % = " + str(total_positive_average)
        sheet["c7"] = "Total stdev = " + str(total_stdev)

        if positive_percent > total_positive_average + total_stdev:
            sheet["c8"] = "Positive sample % falls greater than one standard deviation from total mean (pos %)."

        elif positive_percent < total_positive_average - total_stdev:
            sheet["c8"] = "Positive sample % falls lower than one standard deviation from total mean."

        else:
            sheet["c8"] = "Positive sample % falls within one standard deviation of total mean."

        book_destination = 'J:\\Python\\Python results\\' + file_name
        readout_book.save(book_destination)
        print("Readout book" + file_name + "saved successfully.")
