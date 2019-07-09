"""
firstly you have to put authentication data in to api_tokon.json file.

Entity library use function api_request() for get api data.
In this function you have pass some variable like this :
    api_request( path = u want data , args = arguments disc which need for get with formate)
    path = 'season/2018/competitions';
    args = {'per_page':10 ,'paged':20}; where paged is which page u wana get data

"""
class Entity:
  def __init__(self):
    self.api_url_for_get = 'https://rest.entitysport.com/soccer/'

  def CallAPI(self ,method, url,data):
    import requests
    r = requests.get(url = url, params = data)
    return r;
    
  def api_request(self ,path,args):
    import json, time, os
    return_error = {}
    return_error["status"] = 'error'
    ts = time.time() #current timestamp
    if(os.path.exists("api_token.json")):
      with open(os.getcwd()+"/api_token.json" , "r+") as jsnfile:
        settings = json.load(jsnfile)
    else:
      return_error["response"] = 'api_token.json file missing.'
      return return_error;

    #settings = json.loads(jsnfile)
    api_token = settings['api_token']
    token_expires = settings['token_expires']

    if(not api_token or not token_expires or token_expires < ts):

        api_access_key = settings["api_access_key"]
        api_secret_key = settings["api_secret_key"]

        # either access token has not been generated or expired
        if(not api_access_key or  not api_secret_key):
            return_error["response"] = 'Api access / secret keys missing.';
            return return_error;

        ret = self.api_token(api_access_key,api_secret_key)
        if(ret.status_code==200):
            data = ret.json()
            resk = data["response"]
            settings["api_token"] = api_token = resk["token"]
            settings["token_expires"] = resk["expires"]
            with open(os.getcwd()+"/api_token.json", 'w') as f:
              json.dump(settings, f, indent=4)
        else:
            return ret ;
            
    api_url = self.api_url_for_get+path
    args["token"] = api_token
    response = self.CallAPI('GET',api_url,args)
    
    return response.json();

  def api_token(self ,api_access_key,api_secret_key):
    args = {}
    api_url = self.api_url_for_get+'auth'

    args["access_key"] = api_access_key
    args["secret_key"] = api_secret_key
    
    return self.CallAPI('GET',api_url,args)

"""
for get data for all season call get_seasons_data()
for get data for perticular season call get_seasons_data(sid,args)...sid eg- 2018,18-19,etc.

for get data for all competitions call get_competitions_data(cid=0,args)
here args use for filter data you get. Like paged,per_page,status with those variables.
status status code 1 = upcoming, 2 = result, 3 = live.

get perticular competition info with stats ,squads , matches call get_competitions_data(cid,args)
this  get_competition_squad(cid) ,get_competition_matches(cid), get_competition_statstic(cid)

for get data for all metches call get_matches_data(mid=0,args={})
here args use for filter data you get. Like paged,per_page,status with those variables.
status status code 1 = upcoming, 2 = result, 3 = live.

get perticular metches info with stats  , fantacy call get_matches_stats(mid,args) get_matches_fantasy(mid,args)

for get data for all teams call get_teams_data(tid=0,args)
for get data for all teams maches call get_teams_maches(tid,args)

for get data for all players call get_players_data(pid=0,args)
for get data for plater profile call get_players_data(pid,args)

If you do not send the id than u get all data other perticular id info.

"""

class Entity_soccer(Entity) :

  def get_seasons_data(self ,sid=0,args={}):     
    if(sid):
        path = 'season/'+str(sid)+'/competitions'
    else:
        path = 'seasons'
        
    return self.api_request(path,args)
  #If you do not send the id than u get all data other perticular id info.

  #for get data for all competitions call get_competitions_data(cid=0,args)
  #here args use for filter data you get. Like paged,per_page,status with those variables.
  #status status code 1 = upcoming, 2 = result, 3 = live.
  def get_all_cometition(self ,cid=0,args={}):     
    if(cid):
        path = 'competition/'+str(cid)+'/info'
    else:
        path = 'competitions'
        
    return self.api_request(path,args)
  
  def get_competition_squad(self, cid,args={}):
    path = 'competition/'+str(cid)+'/squad'

    return self.api_request(path,args)
  #get perticular competition info with stats ,squads , matches call get_competitions_data(cid,args)
  #this  get_competition_squad(cid) ,get_competition_matches(cid), get_competition_statstic(cid)
  def get_competition_matches(self, cid,args={}):
    path = 'competition/'+str(cid)+'/matches'

    return self.api_request(path,args)
  
  def get_competition_statstic(self, cid,args={}):
    path = 'competition/'+str(cid)+'/statsv2'

    return self.api_request(path,args)

  """
  for get data for all metches call get_matches_data(mid=0,args={})
    here args use for filter data you get. Like paged,per_page,status with those variables.
    status status code 1 = upcoming, 2 = result, 3 = live.
  """
  def get_matches_data(self ,mid=0,args={}):     
    if(mid):
        path = 'matches/'+str(mid)+'/info'
    else:
        path = 'matches'
        
    return self.api_request(path,args)
  
  #get perticular metches info with stats  , fantacy call get_matches_stats(mid,args)
  def get_matches_stats(self, mid,args={}):
    path = 'matches/'+str(mid)+'/statsv2'

    return self.api_request(path,args)

  def get_matches_fantasy(self, mid,args={}):
    path = 'matches/'+str(mid)+'/fantasy'

    return self.api_request(path,args)

  #for get data for all teams call get_teams_data(tid=0,args)
  def get_teams_data(self ,tid=0,args={}):     
    if(tid):
        path = 'team/'+str(tid)+'/info'
    else:
        path = 'teams'
        
    return self.api_request(path,args)

  def get_teams_maches(self, tid,args={}):
    path = 'team/'+str(tid)+'/matches'

    return self.api_request(path,args)

  def get_players_data(self ,pid=0,args={}):     
    if(pid):
        path = 'player/'+str(pid)+'/profile'
    else:
        path = 'players'
        
    return self.api_request(path,args)


"""
for example in your codignator project
inlude file index.py

and than class Entity_soccer()
        entity = Entity_soccer()
        result = entity.get_all_cometition()
        this result is your output 
"""
