from game import Game
from player import Player

class Lobby():

    def __init__(self):
        self.games = {}
        self.players = {}
    
    def new_game(self, name, player_id):
        player = self.players.pop(player_id)
        new_game = Game(name, player)  
        game_id = new_game.id
        self.games[game_id] = new_game
        return new_game
    
    def join_game(self, player_id, game_id):
        player = self.players.pop(player_id)
        game = self.games[game_id]
        if len(self.players) > 1:
            return "FULL"
        if player_id in game.players:
            return "EXISTS"
        game.players[player.id] = player
        return "OK"
        
    def new_player(self, id, name):
        player = Player(id, name)
        self.players[player.id] = player
        return player