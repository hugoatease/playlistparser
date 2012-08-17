from common import Playlist, Track
from xml.dom import minidom

def parse(data):
    
    dom = minidom.parseString(data)
    
    tracks = dom.getElementsByTagName('dict')[0].getElementsByTagName('dict')[0].getElementsByTagName('dict')
    playlist = list()
    
    for track in tracks:
        t = Track()
        items = track.getElementsByTagName('key')
        for item in items:
            key = item.childNodes[0].nodeValue
            value = item.nextSibling.childNodes[0].nodeValue
            if key == 'Artist':
                t.Artist = value
            if key == 'Name':
                t.Title = value
            if key == 'Location':
                t.File = value
            if key == 'Total Time':
                t.Duration = int(value)
            if key == 'Album':
                t.Album = value
            playlist.append(t)
    
    return Playlist(Tracks=playlist)