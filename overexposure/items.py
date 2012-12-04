# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
import urllib

SPOTIFY_ALBUM_STUB =  'http://open.spotify.com/album/'
SPOTIFY_SONG_STUB =  'http://open.spotify.com/track/'

class Album(Item):
    # define the fields for your item here like:
    artist = Field()
    title = Field()
    score = Field()
    source = Field()
    spotify_link = Field()
    review_date = Field()

    def get_spotify_link(self):
        query_title = urllib.quote(self['title'].replace(' ','+'))
        stub = u'http://ws.spotify.com/search/1/album?q='
        return stub + query_title

class Song(Item):
    # define the fields for your item here like:
    artist = Field()
    title = Field()
    source = Field()
    spotify_link = Field()
    review_date = Field()

    def get_spotify_link(self):
        query_title = urllib.quote(self['title'].replace(' ','+'))
        stub = u'http://ws.spotify.com/search/1/track?q='
        return stub + query_title
