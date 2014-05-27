from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from InfluNote.settings import BASE_DIR

from gracenoteAuth import get_gracenote_userID, get_gracenote_clientID

import json
import InfluNote.pygn as gn
import pylast

#Create a global connection to LastFM to query for similar songs.
def getLastFMConnection():
  return pylast.LastFMNetwork(api_key="3c3e40bc576fb5b6ae1122df2fcfb60b",
                              api_secret="b94bfdbcfc1c34bbdcd9e8288c637f56",
                              username="caseyfalk",
                              password_hash="1b031162f2b3a35c9c8b06a842b7442d")
lastFM = getLastFMConnection()

def get_base_query():
  return {
          "userID":get_gracenote_userID(),
          "clientID":get_gracenote_clientID()
         }


def content_page(request, content="home"):
  return render(request, "global_page.html", {"content":content})


def get_cumulative_data(song, artist, depth): 
  global lastFM

  print "HERE"
  #Get the user's query.
  query = get_base_query() 
  if song: query["track"] = song
  if artist: query["artist"] = artist

  #Load the initial song info.
  try:
    metadata = gn.search(**query)
    orig_track = lastFM.get_track(metadata["track_title"], metadata["album_artist_name"])
    similar_tracks = orig_track.get_similar()
  except Exception as e:
    print e
    raise Exception("Could not find song...")

  data = []
  adjacency = []
  options = []
  
  for i in xrange(depth):
    for track in similar_tracks:
      pass
      #Add missing data if applicable.
      #Add any edges.
      #Add any options.

  return {"data": data, "adjacency":adjacency, "options":options}


def get_song(query):
  return query


@require_http_methods(["GET"])
def search_song(request):
  try:
    #Get the song and artist information.
    query = request.GET["query"]
    song = get_song(query)
    artist = ""

    depth = int(request.GET["depth"])
  except Exception as e:
    print e
    return HttpResponse("I can't figure out your query...")  

  #Get a similarity matrix of similar songs.
  try:
    response = get_cumulative_data(song, artist, depth)  
    print adjacency_matrix
    json_response = json.dumps(response)
  except Exception as e:
    print e
    return HttpResponse("I can't get the related songs...")  

  return HttpResponse(json_response, content_type="application/json")
  
