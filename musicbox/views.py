from django.shortcuts import render

from urllib.request import urlopen
import xml.dom.minidom
import os
from django.http import HttpRequest


def parse_from_api(url, file_name):
    s = urlopen(url)
    contents = s.read()
    file = open("%s/%s.xml" % (os.path.dirname(os.path.abspath(__file__)) ,file_name), 'wb')
    file.write(contents)
    file.close()
    doc = xml.dom.minidom.parse("%s/%s.xml" % (os.path.dirname(os.path.abspath(__file__)), file_name))
    content = doc.toxml()

    os.remove("%s/%s.xml" % (os.path.dirname(os.path.abspath(__file__)), file_name))

def database():
    try:
        pass
    except:
        print("Creating database")
        #create database

        #seed database
        doc = xml.dom.minidom.parse("%s/artists.xml" % os.path.dirname(os.path.abspath(__file__)))
        content = doc.toxml()

        doc = xml.dom.minidom.parse("%s/Users.xml" % os.path.dirname(os.path.abspath(__file__)))
        content = doc.toxml()

        #add xml with top current tracks
        get_top_tracks_url = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=79004d202567282ea27ce27e9c26a498"
        parse_from_api(get_top_tracks_url, "toptracks")

        #add xml with top portugal tracks
        get_pt_top_tracks_url = "http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=portugal&api_key=79004d202567282ea27ce27e9c26a498"
        parse_from_api(get_pt_top_tracks_url, "toptrack_portugal")


def home(request):
    database()
    assert isinstance(request, HttpRequest)
    pass


def search_query(request):
    pass
def artists(request):
    pass

def albums(request):
    pass

def albuminfo(request):
    assert isinstance(request, HttpRequest)
    pass

def artist_page(request):
    pass
def charts(request):
    pass

def login(request):
    return render(request, 'logIn.html')

def register(request):
    return render(request, 'register.html')

def profile(request):
    pass