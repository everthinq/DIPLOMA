import csvWriter

import sqlite3
import re

# selecting cities for city combobox
def cities_select():
    filename = 'gismeteo.db'

    con = sqlite3.connect(filename)

    with con:
        cities_array = []
        cur = con.cursor()

        cur.execute('SELECT DISTINCT city FROM db ORDER BY city')
        data = cur.fetchall()

        for each in data:
            try:
                cities_array.append(str(each[0]))
            except:
                pass

    return cities_array


# selecting dates for start_date combobox and end_date combobox
def dates_select():
    filename = 'gismeteo.db'

    con = sqlite3.connect(filename)

    with con:
        dates_array = []
        cur = con.cursor()

        cur.execute('SELECT DISTINCT date FROM db ORDER BY date')
        data = cur.fetchall()

        for each in data:
            try:
                dates_array.append(str(each[0]))
            except:
                pass

    return dates_array


def rows_select(city, dayPart, start_date, end_date):
    filename = 'gismeteo.db'
    con = sqlite3.connect(filename)

    try:
        weather_array = []
        query = 'SELECT DISTINCT date, '        + \
                    dayPart + '_temp, '         + \
                    dayPart + '_feels, '        + \
                    dayPart + '_wind, '         + \
                    dayPart + '_pressure, '     + \
                    dayPart + '_humidity, '     + \
                    dayPart + '_geoconditions ' + \
                    'FROM db WHERE city = "' + city + '"' + \
                    ' AND date BETWEEN "' + start_date + '" AND "' + end_date + '"'

        data = con.execute(query)
        data = data.fetchall()
    except:
        print 'SQL selecting error'

    for each in data:
        date = each[0]
        temp = each[1][6:]
        feels = each[2][7:]

        if each[3][6:] == 'calm':
            wind = '0'
        else:
            wind = re.findall(r'\d+', each[3])[0]

        pressure = each[4][10:13]
        humidity = each[5][10:12]
        geocond = each[6][24:25]

        weather_array.append(date       + ',' +
                             temp       + ',' +
                             feels      + ',' +
                             wind       + ',' +
                             pressure   + ',' +
                             humidity   + ',' +
                             geocond)

    con.close()

    return weather_array
