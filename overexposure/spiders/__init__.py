from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from overexposure.items import Album, Song, SPOTIFY_ALBUM_STUB, SPOTIFY_SONG_STUB
import urllib2
from xml.dom import minidom
import xlwt

class PitchforkSpider(BaseSpider):
    name = u'pitchfork'
    allowed_domains = ['pitchfork.com']
    start_urls = ['http://pitchfork.com/reviews/best/albums/%s' % page for page in xrange(1, 30)]
    albums = []
    headers = ['artist', 'title', 'score', 'source', 'spotify_link', 'review_date']

    def parse(self, response):
     	hxs = HtmlXPathSelector(response)
        reviews = hxs.select('//div[@id="main"]//div[@class="info"]')
        #with open(filename, 'wb') as f: 
        for review in reviews:
            album = Album()
            title = review.select('a//h2//text()').extract()[0]
            artist = review.select('a//h1//text()').extract()[0]
            score = review.select('span[contains(concat(" ", @class, " "), "score")]//text()').extract()[0].strip(' ')
            review_date = review.select('h4//text()').extract()[0].split(';')[-1]
            album['title'] = title
            album['artist'] = artist
            album['source'] = self.name
            album['score'] = score
            album['review_date'] = review_date
            print album
            search_link = album.get_spotify_link()
            print search_link
            spot_response = urllib2.urlopen(search_link)
            spot_parse = minidom.parse(spot_response)
            spot_tag = spot_parse.getElementsByTagName('album')
            spot_uid = spot_tag and spot_tag[0] and spot_tag[0].getAttribute('href').split(':')[-1] or 'None'
            album['spotify_link'] = SPOTIFY_ALBUM_STUB + spot_uid
            #import pdb; pdb.set_trace()
            #f.write(album['spotify_link']+'\n')
            self.albums.append(album)
       	self.excelify(self.albums, self.headers)

    def excelify(self, objs, headers):
        filename = self.name + '.xls'
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('Sheet 1')
        for i, header in enumerate(headers):
	    row = 0
            sheet.write(row, i, header)
	    row += 1
            for obj in objs:
                sheet.write(row, i, obj[header])
                row += 1
        wbk.save(filename)

class StereogumSpider(BaseSpider):
    name = u'stereogum'
    allowed_domains = ['stereogum.com']
    start_urls = ['http://stereogum.com/music/gum-mix/page/%s/' % page for page in xrange(1, 30)]
    songs = []
    headers = ['artist', 'title', 'source', 'spotify_link']

    def parse(self, response):
     	hxs = HtmlXPathSelector(response)
        songs_html = hxs.select('//ul[@class="playlist"]//li')
        #with open(filename, 'wb') as f: 
        for song_html in songs_html:
            song = Song()
            title_attr = song_html.select('a[@title]//text()').extract()[-1].split('-')
            print title_attr
            title = title_attr[1].replace('"','').strip()
            artist = title_attr[0]
            #score = review.select('span[contains(concat(" ", @class, " "), "score")]//text()').extract()[0].strip(' ')
            #review_date = review.select('h4//text()').extract()[0].split(';')[-1]
            song['title'] = title
            song['artist'] = artist
            song['source'] = self.name
            #album['score'] = score
            #album['review_date'] = review_date
            #print album
            search_link = song.get_spotify_link()
            print search_link, '!!!!!!!!!!!!!'
            spot_response = urllib2.urlopen(search_link)
            spot_parse = minidom.parse(spot_response)
            spot_tag = spot_parse.getElementsByTagName('track')
            spot_uid = spot_tag and spot_tag[0] and spot_tag[0].getAttribute('href').split(':')[-1] or 'None'
            song['spotify_link'] = SPOTIFY_SONG_STUB + spot_uid
            #import pdb; pdb.set_trace()
            #f.write(album['spotify_link']+'\n')
            self.songs.append(song)
       	self.excelify(self.songs, self.headers)

    def excelify(self, objs, headers):
        filename = self.name + '.xls'
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('Sheet 1')
        for i, header in enumerate(headers):
	    row = 0
            sheet.write(row, i, header)
	    row += 1
            for obj in objs:
                sheet.write(row, i, obj[header])
                row += 1
        wbk.save(filename)
