from common import Playlist, Track

def parse(file):
    playlist = list()
    
    lines = file.split('\n')
    lines.pop(0)
    
    i = 1
    while i != lines.count(''):
        lines.remove('')
        i = i + 1
    
    info = None
    fileref = None
    
    for line in lines:
        if len(line.split(u'#EXTINF:') ) == 2:
            info = line.split(u'#EXTINF:')[1]
        else:
            fileref = line
        
        if info != None and fileref != None:
            info = info.split(',')
            length = int(info [0])
            name = info[1]
            playlist.append( Track(Name=name, Duration=length, File=fileref) )
            info = None
            fileref = None
    
    return Playlist(Tracks=playlist)