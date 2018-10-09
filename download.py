import youtube_dl
import os
import sys
import time
import re
import urllib.request
import urllib.parse


def getlink(x):
    query_string = urllib.parse.urlencode({"search_query": x + " topic"})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    contains = 1
    i = 0
    while contains:
        html_content2 = urllib.request.urlopen("http://www.youtube.com/watch?v=" + search_results[i])
        search_results2 = re.findall(r'Auto-generated by YouTube\.', html_content2.read().decode())
        if len(search_results2) > 0:
            contains = 0
        else:
            i += 1
    return search_results[i]
for i in sys.argv:
    if i == "-h" or i == "--help" or len(sys.argv) != 3:
        print("\n\nUsage:\npython youtube.py [directory name] [song file]\n\n\n[directory]\tWill be created if not in existence\n[song file]\tShould consist of one song name per line\n\t\tBegin additional information about song with semicolon\n\t\tBegin song id with semicolon and backslash")
        exit()
failedFiles = []
successfullFiles = []
savedir = sys.argv[1]
try:
    with open(sys.argv[2]) as songfile:
        songs = songfile.read().splitlines()
except:
    raise Exception("Error reading file: " + sys.argv[2])
for i, e in enumerate(songs):
    songs[i] = e.split(";")
if not os.path.exists(savedir):
    os.makedirs(savedir)
directory = os.getcwd()
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for i in songs:
        timestart = time.time()
        try:
            if (len(i) > 1 and i[1].strip()[0] == "\\"):
                link = i[1].strip()[1:]
            else:
                link = getlink(" ".join(i))
            ydl.download(["https://youtube.com/watch?v=" + link])
            found = False
            for fil in os.listdir(directory):
                if link in fil:
                    found = True
                    newname = "/" + savedir + "/" + i[0] + ".mp3"
                    os.rename(directory + "/" + fil, directory + newname)
            if found:
                successfullFiles.append([i[0], str(round(time.time() - timestart, 3)) + "s"])
            else:
                failedFiles.append([i[0]])
        except Exception:
            failedFiles.append([i[0]])
if len(failedFiles) > 0:
    print("\n\n\n\n\n\nFailed Downloads:\n")
    for i in failedFiles:
        print(i[0])
if len(successfullFiles) > 0:
    print("\n\n\n\n\n\nSuccessful Downloads:\n")
    col_width = max(len(word) for row in successfullFiles for word in row) + 2
    for row in successfullFiles:
        print(" ".join(word.ljust(col_width) for word in row))
    print("\n\n\n\n\n")
