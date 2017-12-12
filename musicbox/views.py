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
        client = ApiClient(endpoint=endpoint)
        accessor = GraphDBApi(client)
        repo_name = "musicbox"

        return(repo_name, accessor)

def home(request):
    assert isinstance(request, HttpRequest)

    db_info = database()

    top_artist = """    PREFIX artist:<http://www.artists.com/artist#>
                   PREFIX foaf: <http://xmlns.com/foaf/spec/>
                   PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> 
                   SELECT ?name ?listeners ?imgLarge{
                        ?s artist:artist ?artist.
                        ?artist foaf:name ?name.
                        ?artist artist:listeners ?listeners.
                        ?artist artist:imgLarge ?imgLarge
                    }
                    ORDER BY DESC(xsd:nonNegativeInteger(?listeners))
                    LIMIT 12
                   """

    payload_query = {"query": top_artist}
    res = db_info[1].sparql_select(body=payload_query,
                                 repo_name=db_info[0])
    res = json.loads(res)
    top_artists_result = dict()
    top_artists_list = []
    count = 0
    for e in res['results']['bindings']:
        top_artists_result['name'] = e['name']['value']
        top_artists_result['image'] = e['imgLarge']['value']
        top_artists_result['listeners'] = e['listeners']['value']
        count +=1
        top_artists_result['count'] = count
        top_artists_list.append(top_artists_result)
        top_artists_result = dict()

    return render(request, 'index.html', {'artists':top_artists_list})



def search_query(request):
    assert isinstance(request, HttpRequest)
    db_info = database()
    search = dict(request.POST)
    term = search.get('search_term')[0]

    search_artist = """     PREFIX artist:<http://www.artists.com/artist#>
                            PREFIX foaf: <http://xmlns.com/foaf/spec/> 
                            SELECT ?name ?img_Large
                            WHERE{
                                ?s artist:artist ?artist.
                                ?artist foaf:name ?name.
                                OPTIONAL{?artist artist:imgLarge ?img_Large}
                                FILTER REGEX(?name, "%s", "i")
                            }
                   """ %term

    search_album = """  PREFIX artist:<http://www.artists.com/artist#>
                        PREFIX foaf: <http://xmlns.com/foaf/spec/> 
                        SELECT ?name ?img_Large
                        WHERE{
                            ?s artist:album ?album.
                            ?album foaf:name_album ?name.
                            OPTIONAL{?album artist:imgLarge_album ?img_Large}
                            FILTER REGEX(?name, "%s", "i")
                        } """ % term

    payload_query = {"query": search_artist}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    artists_result = dict()
    artists_list = []

    for e in res['results']['bindings']:
        artists_result['Name'] = e['name']['value']
        artists_result['Image'] = e['img_Large']['value']
        artists_list.append(artists_result)
        artists_result = dict()

    payload_query = {"query": search_album}
    ress = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    ress = json.loads(ress)
    albums_result = dict()
    albums_list = []

    for e in ress['results']['bindings']:
        albums_result['Name'] = e['name']['value']
        albums_result['Image'] = e['img_Large']['value']
        albums_list.append(albums_result)
        albums_result = dict()

    if not albums_list and not artists_list:
        return render(request, 'searchNFound.html')
    elif not albums_list and artists_list:
        return render(request, 'search.html', {'artists': artists_list})
    elif not artists_list and albums_list:
        return render(request, 'search.html', {'albums': albums_list})
    else:
        return render(request, 'search.html', {'albums': albums_list, 'artists': artists_list})


def artists(request):
    assert isinstance(request, HttpRequest)
    list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
    lst = dict()
    flist = []
    for l in list:
        lst['ll'] = l[0]
        flist.append(lst)
        lst = dict()

    if request.GET.get('name') == None:
        letter = 'A'
    else:
        letter = request.GET.get('name')

    db_info=database()

    artists = """       PREFIX artist:<http://www.artists.com/artist#>
                        PREFIX foaf: <http://xmlns.com/foaf/spec/> 
                        SELECT ?name ?img_Large
                        WHERE{
                            ?s artist:artist ?artist.
                            ?artist foaf:name ?name.
                            OPTIONAL{?artist artist:imgLarge ?img_Large}
                            FILTER REGEX(?name, "^%s", "i")
                        }
            """ % letter

    payload_query = {"query": artists}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    artists_result = dict()
    artists_list = []

    for e in res['results']['bindings']:
        artists_result['name'] = e['name']['value']
        artists_result['image'] = e['img_Large']['value']
        artists_list.append(artists_result)
        artists_result = dict()

    return render(request, 'artists.html', {'artists': artists_list, 'flist': flist})

def albums(request):
    assert isinstance(request, HttpRequest)
    list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
    lst = dict()
    flist = []
    for l in list:
        lst['ll'] = l[0]
        flist.append(lst)
        lst = dict()

    if request.GET.get('name') == None:
        letter = 'A'
    else:
        letter = request.GET.get('name')

    db_info=database()

    albums = """    PREFIX artist:<http://www.artists.com/artist#>
                    PREFIX foaf: <http://xmlns.com/foaf/spec/> 
                    SELECT ?name ?img_Large
                    WHERE{
                        ?s artist:album ?album.
                        ?album foaf:name_album ?name.
                        OPTIONAL{?album artist:imgLarge_album ?img_Large}
                        FILTER REGEX(?name, "^%s", "i")
                    }       
            """ %letter

    payload_query = {"query": albums}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    albums_result = dict()
    albums_list = []

    for e in res['results']['bindings']:
        albums_result['name'] = e['name']['value']
        albums_result['image'] = e['img_Large']['value']
        albums_list.append(albums_result)
        albums_result = dict()

    return render(request, 'albums.html', {'albums': albums_list, 'flist': flist})

def albuminfo(request):
    assert isinstance(request, HttpRequest)
    db_info=database()

    if request.POST:
        if 'faveBtn' in request.POST:
            name_album = request.POST['faveBtn']
            ##complete query
        elif 'delBtn' in request.POST:
            album_delete = request.POST['delBtn']
            ##complete query
        else:
            pass

    album_name = request.GET['name']

    tracks = """    PREFIX artist:<http://www.artists.com/artist#>
                    PREFIX foaf: <http://xmlns.com/foaf/spec/> 
                    SELECT  ?track_name ?duration
                    WHERE{
                        ?s      artist:album     ?album.
                        ?album  foaf:name_album  "%s".
                        ?album  artist:tracks    ?tracks .
                        ?tracks foaf:track_name  ?track_name.
                        ?tracks artist:track_duration ?duration.
                    } 
             """ % album_name

    payload_query = {"query": tracks}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    tracks_result = dict()
    tracks_list = []

    for e in res['results']['bindings']:
        tracks_result['name'] = e['track_name']['value']
        tracks_result['duration'] = e['duration']['value']
        tracks_list.append(tracks_result)
        tracks_result = dict()

    tags = """      PREFIX artist:<http://www.artists.com/artist#>
                    PREFIX foaf: <http://xmlns.com/foaf/spec/> 
                    SELECT  ?name
                    WHERE{
                        ?s      artist:album     ?album.
                        ?album  foaf:name_album  "%s".
                        ?album  artist:tag       ?tag .
                        ?tag    foaf:tag_name    ?name.
                    } 
                 """ % album_name

    payload_query = {"query": tags}
    ress = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    ress = json.loads(ress)
    tags_result = ""

    for e in ress['results']['bindings']:
        tags_result = e['name']['value']

    wiki = """      PREFIX artist:<http://www.artists.com/artist#>
                    PREFIX foaf: <http://xmlns.com/foaf/spec/> 
                    SELECT ?wiki
                    WHERE{
                        ?s artist:album ?album .
                        ?album foaf:name_album "%s".
                        OPTIONAL{?album artist:wiki ?wiki}
                    }
            """ % album_name

    payload_query = {"query": wiki}
    ress = db_info[1].sparql_select(body=payload_query,
                                    repo_name=db_info[0])
    ress = json.loads(ress)
    wiki_result = ""

    for e in ress['results']['bindings']:
        wiki_result = e['wiki']['value']


    photo = """     PREFIX artist:<http://www.artists.com/artist#>
                    PREFIX foaf: <http://xmlns.com/foaf/spec/> 
                    SELECT ?image
                    WHERE{
                        ?s     artist:album ?album .
                        ?album foaf:name_album "%s".
                        ?album artist:imgExtraLarge_album ?image.
                    }                
            """ % album_name

    payload_query = {"query": photo}
    ress = db_info[1].sparql_select(body=payload_query,
                                    repo_name=db_info[0])
    ress = json.loads(ress)
    photo_result = ""

    for e in ress['results']['bindings']:
        photo_result = e['image']['value']

    artist = """    PREFIX artist:<http://www.artists.com/artist#>
                    PREFIX foaf: <http://xmlns.com/foaf/spec/> 
                    SELECT ?name
                    WHERE{
                        ?s     artist:album ?album .
                        ?album foaf:name_album "%s".
                        ?album artist:artist_name ?name.
                    }
             """ % album_name

    payload_query = {"query": artist}
    ress = db_info[1].sparql_select(body=payload_query,
                                    repo_name=db_info[0])
    ress = json.loads(ress)
    artist_result = ""

    for e in ress['results']['bindings']:
        artist_result = e['name']['value']

    return render(request, 'albuminfo.html', {'tracks': tracks_list, 'tags':tags_result, 'wiki':wiki_result, 'photo':photo_result, 'artist':artist_result, 'album_name':album_name })

def artist_page(request):
    assert isinstance(request, HttpRequest)
    db_info = database()

    if request.POST:
        if 'faveBtn' in request.POST:
            name_artist = request.POST['faveBtn']

        elif 'delBtn' in request.POST:
            artist_delete = request.POST['delBtn']
        else:
            pass

    artist_name = request.GET['name']

    image = """     PREFIX artist:<http://www.artists.com/artist#>
                    PREFIX foaf: <http://xmlns.com/foaf/spec/>
                    SELECT ?image
                    WHERE{
                        ?s      artist:artist    ?artist .
                        ?artist foaf:name       "%s".
                        ?artist  artist:imgExtraLarge ?image.
                    } 
            """ % artist_name

    payload_query = {"query": image}
    res = db_info[1].sparql_select(body=payload_query,
                                    repo_name=db_info[0])
    res = json.loads(res)
    image_result = ""

    for e in res['results']['bindings']:
        image_result = e['image']['value']

    bio = """       PREFIX artist:<http://www.artists.com/artist#>
                    PREFIX foaf: <http://xmlns.com/foaf/spec/>
                    SELECT ?text
                    WHERE{
                        ?s artist:artist   ?artist.
                        ?artist foaf:name "%s".
                        ?artist     artist:bio      ?bio.
                        ?bio        foaf:bioSummary ?text.
                    }
          """ % artist_name

    payload_query = {"query": bio}
    res = db_info[1].sparql_select(body=payload_query,
                                    repo_name=db_info[0])
    res = json.loads(res)
    bio_result = ""

    for e in res['results']['bindings']:
        bio_result = e['text']['value']

    top_albums = """    PREFIX artist:<http://www.artists.com/artist#>
                        PREFIX foaf: <http://xmlns.com/foaf/spec/>
                        SELECT ?name ?img_Large
                        WHERE{
                            ?s      artist:artist ?artist.
                            ?artist foaf:name     "%s".
                            ?artist artist:album   ?album.
                            ?album  foaf:name_album ?name.
                            ?album artist:imgLarge_album ?img_Large.
                            ?album  artist:album_listeners ?listeners.
                        }
                        ORDER BY DESC(?listeners)
                        LIMIT 3
                 """ % artist_name

    payload_query = {"query": top_albums}
    res = db_info[1].sparql_select(body=payload_query,
                                    repo_name=db_info[0])
    res = json.loads(res)
    top_albums_result = dict()
    top_albums_list = []

    for e in res['results']['bindings']:
        top_albums_result['name'] = e['name']['value']
        top_albums_result['image'] = e['img_Large']['value']
        top_albums_list.append(top_albums_result)
        top_albums_result =dict()

    all_albums = """    PREFIX artist:<http://www.artists.com/artist#>
                        PREFIX foaf: <http://xmlns.com/foaf/spec/>
                        SELECT ?name ?img_Large
                        WHERE{
                             ?s artist:artist ?artist.
                             ?artist foaf:name "%s".
                             ?artist artist:album ?album.
                             ?album  foaf:name_album ?name.
                             ?album artist:imgLarge_album ?img_Large
                        }
                 """ % artist_name

    payload_query = {"query": all_albums}
    res = db_info[1].sparql_select(body=payload_query,
                                    repo_name=db_info[0])
    res = json.loads(res)
    all_albums_result = dict()
    all_albums_list = []

    for e in res['results']['bindings']:
        all_albums_result['name'] = e['name']['value']
        all_albums_result['image'] = e['img_Large']['value']
        all_albums_list.append(all_albums_result)
        all_albums_result = dict()

    return render(request, 'artist_page.html', {'image':image_result, 'bio': bio_result, 'album': top_albums_list, 'lista':all_albums_list, 'name':artist_name})
def charts(request):
    assert isinstance(request, HttpRequest)
    db_info = database()

    top_Portugal =  """     PREFIX foaf: <http://xmlns.com/foaf/spec/>
                            PREFIX topP: <http://www.topPortugal.com/tracks#>
                            PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> 
                            SELECT ?name_track ?name_artist ?img_Large
                            WHERE{
                                ?s      topP:track       ?track.
                                ?track  foaf:name        ?name_track.
                                ?track  topP:listeners   ?listeners.
                                ?track  topP:imgLarge    ?img_Large.
                                ?track  topP:artist      ?artist.
                                ?artist foaf:name_artist ?name_artist.
                            }
                            ORDER BY DESC(xsd:nonNegativeInteger(?listeners))
                            LIMIT 10
                    """

    payload_query = {"query": top_Portugal}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    top_Portugal_result = dict()
    top_Portugal_list = []
    count = 0

    for e in res['results']['bindings']:
        count +=1
        top_Portugal_result['name'] = e['name_track']['value']
        top_Portugal_result['artist'] = e['name_artist']['value']
        top_Portugal_result['image'] = e['img_Large']['value']
        top_Portugal_result['count'] = count
        top_Portugal_list.append(top_Portugal_result)
        top_Portugal_result = dict()

    top_World = """         PREFIX foaf: <http://xmlns.com/foaf/spec/>
                            PREFIX toptracks: <http://www.topTracks.com/tracks#>
                            PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> 
                            SELECT ?name_track ?name_artist ?img_Large
                            WHERE{
                                ?s      toptracks:track         ?track.
                                ?track  foaf:name               ?name_track.
                                ?track  toptracks:listeners     ?listeners.
                                ?track  toptracks:imgLarge      ?img_Large.
                                ?track  toptracks:artist        ?artist.
                                ?artist foaf:name_artist        ?name_artist.
                            }
                            ORDER BY DESC(xsd:nonNegativeInteger(?listeners))
                            LIMIT 10
                """

    payload_query = {"query": top_World}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    top_World_result = dict()
    top_World_list = []
    count2 = 0

    for e in res['results']['bindings']:
        count2 += 1
        top_World_result['name'] = e['name_track']['value']
        top_World_result['artist'] = e['name_artist']['value']
        top_World_result['image'] = e['img_Large']['value']
        top_World_result['count'] = count2
        top_World_list.append(top_World_result)
        top_World_result = dict()

    return render(request, 'charts.html', {'topPortugal': top_Portugal_list, 'topWorld':top_World_list})

def profile(request):
    assert isinstance(request, HttpRequest)
    if request.POST:
        # query
        print("POST FORM")

    db_info=database()

    person = """    PREFIX foaf: <http://xmlns.com/foaf/spec/>
                    PREFIX user: <http://www.users.com/users#>
                    SELECT ?name ?email
                    WHERE{
                        ?s    user:user ?user.
                        ?user foaf:name ?name.
                        ?user user:email ?email.
                    }
            """

    payload_query = {"query": person}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    person_name = ""
    person_email = ""

    for e in res['results']['bindings']:
        person_name = e['name']['value']
        person_email = e['email']['value']

    artist = """    PREFIX foaf: <http://xmlns.com/foaf/spec/>
                    PREFIX user: <http://www.users.com/users#>
                    PREFIX starred: <http://www.users.com/users#/starred#>
                    SELECT ?name_artist
                    WHERE{
                        ?s         user:user     ?user.
                        ?user      foaf:name     ?name.
                        ?user      user:starred  ?starred.
                        ?starred   user:favArt   ?favorite.
                        ?favorite  foaf:favArt   ?name_artist.
                    }
             """

    payload_query = {"query": artist}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    artist_list = []
    artist_result = dict()

    for e in res['results']['bindings']:
        if e['name_artist']['value'] == None:
            pass
        else:
            artist_result['artist'] = e['name_artist']['value']
            artist_list.append(artist_result)
            artist_result = dict()

    album = """     PREFIX foaf: <http://xmlns.com/foaf/spec/>
                    PREFIX user: <http://www.users.com/users#>
                    PREFIX starred: <http://www.users.com/users#/starred#>
                    SELECT ?name_album
                    WHERE{
                        ?s         user:user     ?user.
                        ?user      foaf:name     ?name.
                        ?user      user:starred  ?starred.
                        ?starred   user:favAlb   ?favorite.
                        ?favorite  foaf:favAlb   ?name_album.
                    }
           """

    payload_query = {"query": album}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    album_list = []
    album_result = dict()

    for e in res['results']['bindings']:
        if e['name_album']['value'] == None:
            pass
        else:
            album_result['album'] = e['name_album']['value']
            album_list.append(album_result)
            album_result = dict()

    return render(request, 'profile.html', {'name': person_name, 'email':person_name, 'artists':artist_list, 'albums':album_list})