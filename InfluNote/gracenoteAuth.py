#Read the USER_ID from a file.
def get_gracenote_userID():
  with open("InfluNote/gracenote_user_id.key") as f:
    userID = f.read()[:-1] #Remove the newline character.
  return userID


def get_gracenote_clientID():
  with open("InfluNote/gracenote_client_id.key") as f:
    clientID = f.read()[:-1] #Remove the newline character.
  return clientID

