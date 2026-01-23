import sys
import random


class Tile:

    CACHE_GET_Tile = {}
    def __init__(self,_string):
        
        self.id = int(_string.split(":")[0])
        self.team_id = int(_string.split(":")[1].split(".")[0])
        self.n_troops = int(_string.split(":")[1].split(".")[1])

        Tile.CACHE_GET_Tile[self.id] = self

    def GET_Tile(_id):

        if _id in Tile.CACHE_GET_Tile:
            return Tile.CACHE_GET_Tile[_id]
        return None
        

        

def parseTileData(_godot_output):

    #parse godots output into something a bit more useful
    

    _Tiles = []

    for _tile_data in _godot_output.split(","):
        if _tile_data == "":
            continue
        _Tiles.append(Tile(_tile_data))
        
    return _Tiles
    
def parseGraphString(_string):

    _graph = {}
    for _tile_data in _string.split("|"):
        
        _graph[int(_tile_data.split(":")[0])] = [int(x) for x in _tile_data.split(":")[1].split(",")]
        
    
    return _graph




def GET_attackCandidates(_Tiles,_graph,_from):

    _attack_candidates = [Tile.GET_Tile(x) for x in _graph[_from.id] if Tile.GET_Tile(x).team_id != _from.team_id]

    return _attack_candidates

#return a list of all the tiles 'from' can fortify to...
def GET_fortifyCandidates(_Tiles,_graph,_from):
    _return = [Tile.GET_Tile(x) for x in _graph[_from.id] if Tile.GET_Tile(x).team_id == _from.team_id]
    return _return


def placeCapitalLogic(_tile_data):

    print("called placeCapitalLogic")
    _Tiles = parseTileData(_tile_data)

    _my_Tiles = [x for x in _Tiles if x.team_id == 0]

    if len(_my_Tiles) > 0:
        _random = random.choice(_my_Tiles)
        print("Capital Placement,{}".format(_random.id))
        return
    
    print("Capital Placement,-1")
    return

def tradeLogic(_tile_data):
    print("Force Trade In,-1")
    return

def deployLogic(_tile_data,_graph_string):

    print("called deployLogic")
    
    _Tiles = parseTileData(_tile_data)
    _parsed_graph = parseGraphString(_graph_string)
    

    _my_Tiles = [x for x in _Tiles if x.team_id == 0]
    

    _good_candidates = [x for x in _my_Tiles if len(GET_attackCandidates(_Tiles,_parsed_graph,x)) > 0]
    

    if len(_good_candidates) > 0:
        _random_Tile = random.choice(_good_candidates)
    else:
        _random_Tile = random.choice(_my_Tiles)

    print("Deploy,{0},1".format(_random_Tile.id))
    return

    
   
    

def attackLogic(_tile_data,_graph_string):

    print("called attackLogic")
    
    _parsed_graph = parseGraphString(_graph_string)
    _Tiles = parseTileData(_tile_data)


    _attack_start_candidates = [x for x in _Tiles if x.team_id == 0 and x.n_troops > 1 and len(GET_attackCandidates(_Tiles,_parsed_graph,x)) > 0]

    if len(_attack_start_candidates) <= 0:
        print("Attack,-1")
        return

    #select a random tile...
    _random_Tile = random.choice(_attack_start_candidates)
    #get all the tiles it can attack...
    _attack_target_candidates = [Tile.GET_Tile(x) for x in _parsed_graph[_random_Tile.id] if Tile.GET_Tile(x).team_id != 0]

    if len(_attack_target_candidates) <= 0:
        print(-1)
        return

    _attack_target = random.choice(_attack_target_candidates)
    _n_troops = _random_Tile.n_troops - 1

    print("Attack,{0},{1},{2}".format(_random_Tile.id,_attack_target.id,_n_troops))
    return

    



    
    print(-1)
    return

def fortifyLogic(_game_state,_graph_string):

    print("called fortifyLogic")

    _Tiles = parseTileData(_game_state)
    
    _parsed_graph = parseGraphString(_graph_string)
    

    #ok rank the tiles by order of n troops
    _good_start_candidates = [x for x in _Tiles if x.team_id == 0 and x.n_troops > 1 and len(GET_attackCandidates(_Tiles,_parsed_graph,x)) == 0]
    
    

    if len(_good_start_candidates) > 0:
        
        _good_start_candidates.sort(key=lambda x: x.n_troops,reverse = True)
        
        

        for _good_start_candidate in _good_start_candidates:
           
            _fortify_target_candidates = GET_fortifyCandidates(_Tiles,_parsed_graph,_good_start_candidate)
            

            for _target in _fortify_target_candidates:
                if len(GET_attackCandidates(_Tiles,_parsed_graph,_target)) > 0:
                    #fortify to that tile
                    print("Fortify,{0},{1},{2}".format(_good_start_candidate.id,_target.id,_good_start_candidate.n_troops - 1))
                    return

        
        #work out which tiles it can fortify to...
    print("Fortify",-1)
    return

    

def captureLogic(_game_state,_graph_string):
    print("called captureLogic")
    print("Capture,1")#capture with 1 troops...
    return




if __name__ == "__main__":
    
    
    _turn_state = sys.argv[1]
    _n_cards = sys.argv[2]
    _n_deployable_troops = sys.argv[3]
    _tile_data = sys.argv[4]
    _graph = sys.argv[5]
    
    if _turn_state == "Force Trade In":
        tradeLogic(_tile_data)

    elif _turn_state == "Capital Placement":
        placeCapitalLogic(_tile_data)
        
    elif _turn_state == "Deploy":
        deployLogic(_tile_data,_graph)
        
    elif _turn_state == "Attack":
        attackLogic(_tile_data,_graph)

    elif _turn_state == "Fortify":
        fortifyLogic(_tile_data,_graph)

    elif _turn_state == "Capture":
        captureLogic(_tile_data,_graph)
    
    else:
        print("Unknown turn state")
