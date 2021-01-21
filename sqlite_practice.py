import sqlite3
import datetime
import statistics

# This calculator takes values from the database and calculates the total mean
# and total standard deviation for all runs

# timestamp = str(datetime.datetime.now().strftime("%d/%m/%Y") + " , " + datetime.datetime.now().strftime("%H:%M:%S"))
# print(timestamp)
# positive = 25

conn = sqlite3.connect('test.db')
print("Opened database successfully")

c = conn.cursor()

# conn.execute('''CREATE TABLE results (
#             timestamp text,
#             positivepercent real
#             )''')
# print("Table created successfully")

# conn.execute('DROP TABLE results')
# print("Table dropped successfully")

# c.execute("INSERT INTO results VALUES ('{}', '{}')".format(timestamp, positive))
c.execute("SELECT * FROM results")
all_runs = c.fetchall()
print(all_runs)

c.execute("SELECT positivepercent FROM results")
result = c.fetchall()
print(result)
my_list = []
for row in result:
    my_list.append(row)

# create a list only including the 0th item from each tuple
my_list2 = [result[0] for result in my_list]
print(my_list2)

# # calculate total number of tests run, mean, standard deviation
print("Total number of tests run to date : " + str(len(my_list2)))

total_mean = statistics.mean(my_list2)
print("total mean = " + str(total_mean))
total_stdv = statistics.stdev(my_list2)
print("total stdev = " + str(total_stdv))

# print(sum(c.fetchall()))
#
# my_list = []
#
# for i in c.fetchall():
#     my_list.append(i)
# print(my_list)


conn.commit()
conn.close()
