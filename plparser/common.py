from xml.dom import minidom
from random import randrange

class Track:
    def __init__(self, Artist = None, Title = None, Album = None, Name = None, Duration = None, File = None):
        self.Artist = Artist
        self.Title = Title
        self.Album = Album
        self.Name = Name
        self.Duration = Duration
        self.File = File
        
        self.Inverted = False
    
    def defineArtist(self, Artist):
        self.Artist = Artist
        if self.Inverted:
            self.Title = self.Name.split(' - ' + Artist)[0]
        else:
            self.Title = self.Name.split(Artist + ' - ')[1]
        
    def nameParse(self, invert = False):
        if invert:
            self.Inverted = True
        invert = self.Inverted

        results = list()
        splitted = self.Name.split(' - ')
        if len(splitted) == 2:
            if not invert:
                self.Artist = splitted[0]
                self.Title = splitted[1]
            else:
                self.Artist = splitted[1]
                self.Title = splitted[0]
            return True
        elif len(splitted) < 2:
            return False
        else:
            probcursor = 1
            if invert:
                splitted.reverse()
            while probcursor != len(splitted):    
                artist = str()
                wordcursor = 1
                words = splitted[ 0:probcursor ]
                if invert:
                    words.reverse()
                for part in words:
                    artist = artist + part
                    if len(words) - wordcursor > 0:
                        artist = artist + ' - '
                    wordcursor = wordcursor + 1
                results.append( artist )
                probcursor = probcursor + 1
            return results
    def mustInvert(self, artist):
        if self.Name.lower().rfind(artist.lower()) > 0:
            self.Inverted = True
        else:
            self.Inverted = False
        return self.Inverted

class Playlist:
    def __init__(self, Tracks=None):
        self.Tracks = Tracks
        self.Inverted = False
    def nameParse(self, invert = False):
        for track in self.Tracks:
            track.nameParse(invert)
    def mustInvert(self, artist = None):
        if artist == None:
            self.randTracks = list()
            for i in range(0, 3, 1):
                self.randTracks.append(self.Tracks[ randrange(0, len(self.Tracks) - 1) ])
            return self.randTracks
        else:
            for track in self.randTracks:
                if track.mustInvert(artist):
                    for track in self.Tracks:
                        track.Inverted = True
                    self.Inverted = True
                    return True
        
            

def typeGuess(data):
    lines = data.split('\n')
    if '#EXTM3U' in lines[0]:
        try:
            lines.decode('utf-8')
            return '.m3u8'
        except:
            return '.m3u'
    if '[playlist]' in lines[0]:
        return '.pls'
    dom = minidom.parseString(data)
    try:
        for namespace in dom.getElementsByTagName('playlist')[0].attributes.items():
            try:
                if namespace[1] == 'http://xspf.org/ns/0/':
                    return '.xspf'
            except:
                pass
    except:
        pass
    try:
        dom.getElementsByTagName('plist')
        return '.xml'
    except:
        return None
    
    
def parse(filename=None, filedata=None):
    if filedata != None:
        file = filedata
        if filename == None:
            filename = typeGuess(filedata)
    else:
        f = open(filename, 'r')
        file = f.read()
        f.close()

    if '.m3u8' in filename:
        file = file.decode('utf-8')
    elif '.m3u' in filename or '.pls' in filename:
        try:
            file = file.decode('ISO-8859-2')
        except:
            u = UniversalDetector()
            u.feed(file)
            u.close()
            if u.result['confidence'] > 0.5:
                try:
                    data = data.decode(result['encoding'])
                    print 'File encoding automatically detected as ' + result['encoding'] +'. It might be wrong...'
                except:
                    print 'Unable to find file encoding. Using escaped ASCII instead of Unicode'
            else:
                print 'Unable to find file encoding. Using escaped ASCII instead of Unicode'
    
    if '.m3u' in filename or '.m3u8' in filename:
        import m3uparser
        return m3uparser.parse(file)
    if '.pls' in filename:
        import plsparser
        return plsparser.parse(file)
    if '.xspf' in filename:
        import xspfparser
        return xspfparser.parse(file)
    if '.xml' in filename:
        import xmlparser
        return xmlparser.parse(file)

if __name__ == '__main__':
    from sys import argv
    f = open(argv[1], 'r')
    print parse(filedata=f.read())
    f.close()