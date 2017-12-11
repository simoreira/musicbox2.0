from django.shortcuts import render

from urllib.request import urlopen
import xml.dom.minidom
import os
from django.http import HttpRequest
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

def database():
        endpoint = "http://localhost:7200"
        repo_name = "musicbox"
        client = ApiClient(endpoint=endpoint)
        accessor = GraphDBApi(client)

        query = """
                PREFIX foaf:<http://xmlns.com/foaf/spec/>
                PREFIX artist:<http://www.artists.com/>
                SELECT ?namealbum
                WHERE{
                    ?b artist:album ?a.
                    ?a foaf:name_album ?namealbum.
                }
                """

        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                     repo_name=repo_name)
        res = json.loads(res)
        for e in res['results']['bindings']:
            print(e['namealbum']['value'])

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


def profile(request):
    pass
