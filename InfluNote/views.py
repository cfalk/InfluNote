from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from InfluNote.settings import BASE_DIR

#from gracenoteAuth import get_gracenote_userID, get_gracenote_clientID

import json
import InfluNote.pygn as gn
import InfluNote.pylast as pylast

#Create a global connection to LastFM to query for similar songs.
def getLastFMConnection():
  return pylast.LastFMNetwork(api_key="3c3e40bc576fb5b6ae1122df2fcfb60b",
                              api_secret="b94bfdbcfc1c34bbdcd9e8288c637f56",
                              username="caseyfalk",
                              password_hash="1b031162f2b3a35c9c8b06a842b7442d")
lastFM = getLastFMConnection()


#def get_base_query():
#  return {
#          "userID":get_gracenote_userID(),
#          "clientID":get_gracenote_clientID()
#         }


def content_page(request, content="home"):
  return render(request, "global_page.html", {"content":content})


def get_track_data(track):
  return [track.get_name(), track.get_artist().get_name()]


def get_id(track):
  return "{} %% {}".format(track.title, track.get_artist().get_name())


def get_cumulative_data(song, artist, depth): 
  #Variable Setup.
  sim_limit = 2

  #Load the initial song info.
  try:
    orig_track = lastFM.get_track(artist, song)
    overall_tracks = [orig_track]
    track_list = [get_id(orig_track)]

    new_tracks = [sim[0] for sim in orig_track.get_similar()[:sim_limit]]
    track_adjacency = []
    for i in xrange(depth):
      tracks_to_calculate = new_tracks
      new_tracks = []

      for track in tracks_to_calculate:
        print "track: {}".format(track.title)
        track_id = get_id(track)
        if track_id not in track_list:
          track_list.append(track_id)
          overall_tracks.append(track) 
          #If we haven't reached a network terminal, then get similar tracks.
          if i!= depth-1:
            similar_tracks = [sim[0] for sim in track.get_similar()[:sim_limit]]
            track_adjacency.append(similar_tracks)
            new_tracks += similar_tracks

  except Exception as e:
    print e
    raise Exception("Could not load song network...")

  #Get the track information to display for each unique track.
  fields = ["title", "artist"]
  data = [fields] + [get_track_data(track) for track in overall_tracks]
  
  #Get the unique options for each field.
  options = {field:[] for field in fields}
  for row in data[1:]:
    for (value, field) in zip(row, fields):
      if value not in options[field]:
        options[field].append(value)
 
  #Get a numbered adjacency matrix corresponding to the order of the data.
  adjacency = []
  for similar_tracks in track_adjacency:
    connections = [track_list.index(get_id(track)) for track in similar_tracks]
    adjacency.append(connections)

  return {"data": data, "adjacency":adjacency, "options":options}


@require_http_methods(["GET"])
def search_song(request):
  try:
    #Get the song and artist information.
    song = request.GET["track"]
    artist = request.GET["artist"]
    depth = int(request.GET["depth"])

  except Exception as e:
    print e
    return HttpResponse("ERROR: I can't figure out your query...")  

  #Get a similarity matrix of similar songs.
  try:
    response = get_cumulative_data(song, artist, depth)  
    json_response = json.dumps(response)
    print json_response
  except Exception as e:
    print e
    return HttpResponse("ERROR: {}".format(e))  

  return HttpResponse(json_response, content_type="application/json")
  
