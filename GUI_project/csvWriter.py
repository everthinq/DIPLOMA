import csv
import os

def write_rows(weather_array, filename):
    if not os.path.isdir('./raw_data'):
        os.mkdir('raw_data')

    with open('./raw_data/' + filename + '.arff', 'w') as csvHandle:
        writer = csv.writer(csvHandle)
        writer.writerow(['@RELATION ' + filename])
        writer.writerow('')
        writer.writerow(['@ATTRIBUTE _date DATE \'yyyy-MM-dd\''])
        writer.writerow(['@ATTRIBUTE temp NUMERIC'])
        writer.writerow(['@ATTRIBUTE feels NUMERIC'])
        writer.writerow(['@ATTRIBUTE wind NUMERIC'])
        writer.writerow(['@ATTRIBUTE pressure NUMERIC'])
        writer.writerow(['@ATTRIBUTE humidity NUMERIC'])
        writer.writerow(['@ATTRIBUTE geoconditions NUMERIC'])
        writer.writerow('')
        writer.writerow(['@DATA'])

        for each in weather_array:
            each = each.split(',')
            writer.writerow(each)
