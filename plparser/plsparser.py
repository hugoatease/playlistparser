from common import Playlist, Track

Keys = ['File', 'Title', 'Length']
genKeys = dict()

def iniParse(data):
    result = dict()
    lines = data.split('\n')
    for line in lines:
        parts = line.split('=')
        if len(parts) == 2:
            result[parts[0]] = parts[1].replace('\r','')
    return result

def mkKeys(cursor):
    global genKeys
    cKeys = list()
    for key in Keys:
        cKeys.append(key + str(cursor))
        genKeys[key + str(cursor)] = key
    return cKeys

def getKeyName(genKey):
    global genKeys
    return genKeys[genKey]

def parse(data):
    playlist = list()
    data = iniParse(data)
    
    finish = False
    cursor = 1
    while finish != True:
        keys = mkKeys(cursor)
        result = dict()
        for key in keys:
            try:
                result[ getKeyName(key) ] = data[key]
            except KeyError:
                pass
        if len(result) > 0:
            try:
                playlist.append( Track(Name=result['Title'], Duration=int(result['Length']), File=result['File']) )
            except KeyError:
                pass
            cursor = cursor + 1
        else:
            finish = True
    
    return Playlist(Tracks=playlist)