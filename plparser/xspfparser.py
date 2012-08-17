from common import Playlist, Track
from xml.dom import minidom

playlist = list()

def parse(data):
    dom = minidom.parseString(data)
    
    tracks = dom.getElementsByTagName('trackList')[0].getElementsByTagName('track')
    for track in tracks:
        t = Track()
        for item in track.childNodes:
            key = item.nodeName
            try:
                value = item.childNodes[0].nodeValue
                if key == "creator":
                    t.Artist = value
                if key == "title":
                    t.Title = value
                if key == "location":
                    t.File = value
                if key == "duration":
                    t.Duration = int(value)
                if key == "album":
                    t.Album = value
                playlist.append(t)
            except:
                pass
    return Playlist(Tracks=playlist)