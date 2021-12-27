from bs4 import BeautifulSoup
import requests
from rfeed import *
import datetime
from google_play_scraper import app
import yaml

print('checkpoint 1!  Program started!')
# find current google play store version of dolphin emulator
googleplaydolphindata = app(
    'org.dolphinemu.dolphinemu'
)
current_android_version = googleplaydolphindata["version"]
with open('old_android_version_file') as versionfile:
    old_android_version = versionfile.readlines()
if old_android_version[0] != current_android_version:
    #set up beautifulsoup for dolphin emulator download page
    downloadpage = requests.get("https://dolphin-emu.org/download/")
    downloadpagesoup = BeautifulSoup(downloadpage.content, 'html.parser')
    print('checkpoint 2 got past old vs new version check!')

    #find the version of dolphin emulator on f-droid
    dolphinmetadatafdroid = requests.get("https://gitlab.com/fdroid/fdroiddata/-/raw/master/metadata/org.dolphinemu.dolphinemu.yml")
    fdroidversion = yaml.load(dolphinmetadatafdroid.text, Loader=yaml.CLoader)["CurrentVersion"]
    if str(fdroidversion) != str(current_android_version):

        # find the download link on the page (using current android version!)
        try:
            downloadpagetag = str(downloadpagesoup.body.find('a', string=current_android_version))
            for letternum in range(len(str(downloadpagetag)[9:])):
                if str(downloadpagetag)[9:][letternum] == '"':
                    partdownloadlink = str(downloadpagetag)[9:int(9+letternum)]
                    fulldownloadlink = str("https://dolphin-emu.org" + partdownloadlink)
                    break

            #set up beautifulsoup for commitpage
            commitpage = requests.get(fulldownloadlink)
            commitpagesoup = BeautifulSoup(commitpage.content, 'html.parser')

            # find the commit link
            commitpagetag = commitpagesoup.body.find('dd', "commithash")
            for letternum in range(len(str(commitpagetag)[32:])):
                if str(commitpagetag)[32:][letternum] == '"':
                    commitlink = str(commitpagetag)[32:int(32+letternum)]
                    break

            global line1
            line1 = str("@licaon-kter The current version of Dolphin Emulator on Fdroid is outdated.")
            global line2
            line2 = str("The commit link is: " + commitlink)
            global line3
            line3 = str("The direct download link is: " + fulldownloadlink)
            item1 = Item(
                title = "NEW UPDATE TO DOLPHIN EMULATOR",
                link = "https://gitlab.com/fdroid/fdroiddata/-/issues/2043",
                description = '<p>'+ line1 +'</p><p>'+line2+'</p><p>'+line3+'</p><p>The current F-Droid version of dolphin is: '
                + str(fdroidversion) + '</p><p>The current F-Droid version of dolphin is: '
                + str(current_android_version) + '</p><p>Link to F-Droid Dolphin Emulator page: https://f-droid.org/en/packages/org.dolphinemu.dolphinemu/</p>',
                pubDate = datetime.datetime(datetime.datetime.now().date().year, datetime.datetime.now().date().month,
                                    datetime.datetime.now().date().day, datetime.datetime.now().time().hour,
                                    datetime.datetime.now().time().minute)
            )

            feed = Feed(
                    title = "Fdroid Update Reminders",
                    link = "https://raw.githubusercontent.com/exaCORE42/FdroidAlerter/master/Fdroid_Alerter.xml?token=AUKAXQEZBLHG46XVVM5465LBY7DDE",
                    description = "Reminders to update different Fdroid packages",
                    language = "en-US",
                    lastBuildDate = datetime.datetime.now(),
                    items = [item1])


            with open('Fdroid_Alerter.xml', 'w') as rssfile:
                rssfile.write(feed.rss())
            with open('old_android_version_file', 'w') as oldversionfile:
                oldversionfile.write(str(current_android_version))
        except:
            item1 = Item(
                title="NEW UPDATE TO DOLPHIN EMULATOR",
                link="https://gitlab.com/fdroid/fdroiddata/-/issues/2043",
                description='SOMETHING WENT WRONG IN THE CODE, BUT THERE IS STILL A NEW VERSION!  PLEASE CHECK IT OUT!!'
                            'OLD VERSION: ' + str(old_android_version[0]) + 'NEW VERSION: ' + str(current_android_version)
                + 'https://dolphin-emu.org/download/ https://play.google.com/store/apps/details?id=org.dolphinemu.dolphinemu&hl=en_US&gl=US',
                pubDate=datetime.datetime(datetime.datetime.now().date().year, datetime.datetime.now().date().month,
                                          datetime.datetime.now().date().day, datetime.datetime.now().time().hour,
                                          datetime.datetime.now().time().minute)
            )
            feed = Feed(
                title="Fdroid Update Reminders",
                link="https://raw.githubusercontent.com/exaCORE42/FdroidAlerter/master/Fdroid_Alerter.xml?token=AUKAXQEZBLHG46XVVM5465LBY7DDE",
                description="Reminders to update different Fdroid packages",
                language="en-US",
                lastBuildDate=datetime.datetime.now(),
                items=[item1])

            with open('Fdroid_Alerter.xml', 'w') as rssfile:
                rssfile.write(feed.rss())