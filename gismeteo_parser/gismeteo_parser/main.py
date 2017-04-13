from scrapy.cmdline import execute

def main():
    execute(['scrapy', 'crawl', 'gismeteo_parser'])


if __name__ == '__main__':
    main()
