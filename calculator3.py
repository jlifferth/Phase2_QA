import statistics


list_2 = [(4.972375690607735, 181), (7.027027027027027, 185), (22.0, 100), (7.894736842105263, 38), (50.0, 6), (0.0, 0), (17.72151898734177, 158), (11.11111111111111, 9), (9.090909090909092, 22), (33.33333333333333, 3), (12.5, 16), (2.941176470588235, 68), (40.0, 5), (42.857142857142854, 7), (42.857142857142854, 7), (42.857142857142854, 7), (25.0, 4), (7.142857142857142, 28), (9.523809523809524, 21), (32.18390804597701, 87), (5.555555555555555, 18), (4.972375690607735, 181), (7.027027027027027, 185), (22.0, 100), (7.894736842105263, 38), (50.0, 6), (0.0, 0), (17.72151898734177, 158), (11.11111111111111, 9), (9.090909090909092, 22), (33.33333333333333, 3), (12.5, 16), (2.941176470588235, 68), (40.0, 5), (42.857142857142854, 7), (42.857142857142854, 7), (42.857142857142854, 7), (25.0, 4), (7.142857142857142, 28), (9.523809523809524, 21), (32.18390804597701, 87), (5.555555555555555, 18)]
print(len(list_2))

# create unique list to remove duplicate values
unique_list_2 = []
for i in list_2:
    if i not in unique_list_2:
        unique_list_2.append(i)
print(len(unique_list_2))

# list 3 will multiply each pos % value by each total specimen count
list_3 = []
for i in unique_list_2:
    list_3.append(i[0] * i[1])
print(list_3)

# population_sample_count will sum all sample sizes from all runs
population_sample_count = []
for i in unique_list_2:
    population_sample_count.append(i[1])
print(population_sample_count)
population_sample_count = sum(population_sample_count)
print(population_sample_count)

raw_mean = statistics.mean(list_3)
print(raw_mean)

total_mean = raw_mean / population_sample_count
print(total_mean)
