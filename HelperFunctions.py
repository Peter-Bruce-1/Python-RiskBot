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

    """Parses Godots output into something slgihtly more helpful?"""
    

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
    """Return a list of Tiles that _from can attack"""

    _attack_candidates = [Tile.GET_Tile(x) for x in _graph[_from.id] if Tile.GET_Tile(x).team_id != _from.team_id]

    return _attack_candidates

#return a list of all the tiles 'from' can fortify to...
def GET_fortifyCandidates(_Tiles,_graph,_from):
    _return = [Tile.GET_Tile(x) for x in _graph[_from.id] if Tile.GET_Tile(x).team_id == _from.team_id]
    return _return
