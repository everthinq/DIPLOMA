import scrapy
from ..items import gismeteo_parserItem


class gismeteo_parser(scrapy.Spider):
    name = 'gismeteo_parser' # name of spider must be the same as filename
    start_urls = ['http://m.gismeteo.com/citysearch/districts/123/'] # reserved variable for urls list


    def parse(self, response): # overrided parse method for recursive requests
        urls = response.xpath('//li[@class = "catalog__item"]/a/@href').extract() #list of urls

        district = response.xpath('/html/body/div[1]/div[1]/span/span/text()').extract()

        for i in xrange(0, len(urls)):
            next_page = response.urljoin(urls[i])

            if 'weather' in next_page:
                next_page += 'detailday/'
                yield scrapy.Request(next_page, callback = self.parse_item, meta = {'district': district[0]})

            yield scrapy.Request(next_page, callback = self.parse)


    def parse_item(self, response): # parse items from e.g. http://m.gismeteo.com/weather/14490/detailday/
        url = str(response)[5:-1]

        date = response.xpath('//*[@id="time__select"]/option[1]/text()').extract()

        country     = response.xpath('/html/body/div[1]/div[2]/a/text()').extract()
        district    = response.meta['district']
        city        = response.xpath('/html/body/div[1]/div[2]/a/span/text()').extract()

        temperatureList = response.xpath('//td[@class = "weather__temp"]/span/text()').extract()

        night_feels         = response.xpath('/html/body/div[1]/div[5]/div[1]/p[1]/text()').extract()
        night_wind          = response.xpath('/html/body/div[1]/div[5]/div[1]/p[2]/text()').extract()
        night_pressure      = response.xpath('/html/body/div[1]/div[5]/div[1]/p[3]/text()').extract()
        night_humidity      = response.xpath('/html/body/div[1]/div[5]/div[1]/p[4]/text()').extract()
        night_geoConditions = response.xpath('/html/body/div[1]/div[5]/div[1]/p[5]/text()').extract()

        morning_feels         = response.xpath('/html/body/div[1]/div[5]/div[2]/p[1]/text()').extract()
        morning_wind          = response.xpath('/html/body/div[1]/div[5]/div[2]/p[2]/text()').extract()
        morning_pressure      = response.xpath('/html/body/div[1]/div[5]/div[2]/p[3]/text()').extract()
        morning_humidity      = response.xpath('/html/body/div[1]/div[5]/div[2]/p[4]/text()').extract()
        morning_geoConditions = response.xpath('/html/body/div[1]/div[5]/div[2]/p[5]/text()').extract()

        day_feels         = response.xpath('/html/body/div[1]/div[5]/div[3]/p[1]/text()').extract()
        day_wind          = response.xpath('/html/body/div[1]/div[5]/div[3]/p[2]/text()').extract()
        day_pressure      = response.xpath('/html/body/div[1]/div[5]/div[3]/p[3]/text()').extract()
        day_humidity      = response.xpath('/html/body/div[1]/div[5]/div[3]/p[4]/text()').extract()
        day_geoConditions = response.xpath('/html/body/div[1]/div[5]/div[3]/p[5]/text()').extract()

        evening_feels         = response.xpath('/html/body/div[1]/div[5]/div[4]/p[1]/text()').extract()
        evening_wind          = response.xpath('/html/body/div[1]/div[5]/div[4]/p[2]/text()').extract()
        evening_pressure      = response.xpath('/html/body/div[1]/div[5]/div[4]/p[3]/text()').extract()
        evening_humidity      = response.xpath('/html/body/div[1]/div[5]/div[4]/p[4]/text()').extract()
        evening_geoConditions = response.xpath('/html/body/div[1]/div[5]/div[4]/p[5]/text()').extract()

        if ',' in night_wind[0]:
            night_wind[0]   = night_wind[0].replace(',', ';')

        if ',' in morning_wind[0]:
            morning_wind[0] = morning_wind[0].replace(',', ';')

        if ',' in day_wind[0]:
            day_wind[0]     = day_wind[0].replace(',', ';')

        if ',' in evening_wind[0]:
            evening_wind[0] = evening_wind[0].replace(',', ';')

        if ' (today)' in date[0]:
            date[0] = date[0].replace(' (today)', '')

        date = date[0]

        country     = country[0]
        district    = district[3:]
        city        = city[0][3:]

        night_temp      = 'Temp: ' + temperatureList[0]
        morning_temp    = 'Temp: ' + temperatureList[1]
        day_temp        = 'Temp: ' + temperatureList[2]
        evening_temp    = 'Temp: ' + temperatureList[3]

        item = gismeteo_parserItem()
        item['URL'] = url

        item['DATE'] = date

        item['COUNTRY']     = country
        item['DISTRICT']    = district
        item['CITY']        = city

        item['NIGHT_TEMP']          = night_temp
        item['NIGHT_FEELS']         = night_feels[0]
        item['NIGHT_WIND']          = night_wind[0]
        item['NIGHT_PRESSURE']      = night_pressure[0]
        item['NIGHT_HUMIDITY']      = night_humidity[0]
        item['NIGHT_geoCONDITIONS'] = night_geoConditions[0]

        item['MORNING_TEMP']          = morning_temp
        item['MORNING_FEELS']         = morning_feels[0]
        item['MORNING_WIND']          = morning_wind[0]
        item['MORNING_PRESSURE']      = morning_pressure[0]
        item['MORNING_HUMIDITY']      = morning_humidity[0]
        item['MORNING_geoCONDITIONS'] = morning_geoConditions[0]

        item['DAY_TEMP']          = day_temp
        item['DAY_FEELS']         = day_feels[0]
        item['DAY_WIND']          = day_wind[0]
        item['DAY_PRESSURE']      = day_pressure[0]
        item['DAY_HUMIDITY']      = day_humidity[0]
        item['DAY_geoCONDITIONS'] = day_geoConditions[0]

        item['EVENING_TEMP']          = evening_temp
        item['EVENING_FEELS']         = evening_feels[0]
        item['EVENING_WIND']          = evening_wind[0]
        item['EVENING_PRESSURE']      = evening_pressure[0]
        item['EVENING_HUMIDITY']      = evening_humidity[0]
        item['EVENING_geoCONDITIONS'] = evening_geoConditions[0]

        return item
