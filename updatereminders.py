from bs4 import BeautifulSoup
import requests
from rfeed import *
import datetime

#set up beautifulsoup for download page
downloadpage = requests.get("https://dolphin-emu.org/download/")
downloadpagesoup = BeautifulSoup(downloadpage.content, 'html.parser')

# find the download link on the page
downloadpagetag = downloadpagesoup.body.find('td', "version always-ltr")
print(downloadpagetag)
print(str(downloadpagetag)[40:])
for letternum in range(len(str(downloadpagetag)[40:])):
    if str(downloadpagetag)[40:][letternum] == '"':
        downloadlink = str("https://dolphin-emu.org" + (str(downloadpagetag)[40:int(40+letternum)]))
        break

#set up beautifulsoup for commitpage
commitpage = requests.get(downloadlink)
commitpagesoup = BeautifulSoup(commitpage.content, 'html.parser')

# find the commit link
commitpagetag = commitpagesoup.body.find('dd', "commithash")
print()
for letternum in range(len(str(commitpagetag)[32:])):
    if str(commitpagetag)[32:][letternum] == '"':
        commitlink = str(commitpagetag)[32:int(32+letternum)]
        break

global line1
line1 = str("@licaon-kter The current version of Dolphin Emulator on Fdroid is outdated.")
global line2
line2 = str("The commit link is: " + commitlink)
global line3
line3 = str("The direct download link is: " + downloadlink)
print(datetime.datetime(datetime.datetime.now().date().year, datetime.datetime.now().date().month,
                        datetime.datetime.now().date().day, datetime.datetime.now().time().hour,
                        datetime.datetime.now().time().minute))
item1 = Item(
    title = "NEW UPDATE TO DOLPHIN EMULATOR",
    link = "https://gitlab.com/fdroid/fdroiddata/-/issues/2043",
    description = '<p>'+ line1 +'</p><p>'+line2+'</p><p>'+line3+'</p>',
    pubDate = datetime.datetime(datetime.datetime.now().date().year, datetime.datetime.now().date().month,
                        datetime.datetime.now().date().day, datetime.datetime.now().time().hour,
                        datetime.datetime.now().time().minute)
)

feed = Feed(
        title = "Fdroid Update Reminders",
        link = "https://www.cyberciti.biz/atom/updated.xml",
        description = "Reminders to update different Fdroid packages",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = [item1])

print(feed.rss())

with open('Fdroid_Alerter.xml', 'w') as rssfile:
    rssfile.write(feed.rss())


