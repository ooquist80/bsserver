from connection_factory import ConnectionFactory
from lobby import Lobby
from player import Player
from game import Game
import time
import pickle
import threading

def s_create_game(data):
    name = data[0]
    player_name = data[1]
    game = create_game(name, player_name)
    return ("OK", game.id)
    
def create_game(name, player_id):
    game = lobby.new_game(name, player_id)
    print("Game " + str(game.id) + " " + game.name + " created by " + player_id)
    return game

def s_create_player(data):
    player_id = data[0]
    name = data[1]
    create_player(player_id, name)
    return "OK"

def create_player(id, name):
    player = lobby.new_player(id, name)
    print("Player " + player.name + " created id: " + str(player.id))

def s_join_game(data):
    game_id = int(data[0])
    player_id = data[1]
    status = join_game(game_id, player_id)
    if status == "OK":
        return ("OK", game_id)
    elif status == "FULL":
        return ("ERROR", "Game is full")
    elif status == "EXISTS":
        return ("ERROR", "Player with same id already exists")

def join_game(game_id, player_id):
    status = lobby.join_game(player_id, game_id)
    if status == "OK":
        print(player_id + " joined " + str(game_id) + ".")
    elif status == "FULL":
        print(player_id + " tried to join " + str(game_id) + " but it was full.")
    elif status == "EXISTS":
        print(player_id + " tried jo join but a player with same id exists")
    return status

def s_get_games():
    game_list = get_games()
    if game_list:
        return ("OK", game_list)
    else:
        return ("EMPTY", "No games running :(")

def get_games():
    games = lobby.games
    game_list = []
    
    for game in games.values():
        player_names = []
        for player in game.players.values():
            player_names.append(player.name)
        player_1_name = player_names[0]
        if len(player_names) < 2:
            player_2_name = "?"
        else:
            player_2_name = player_names[1]
        gamestring = str(game.id) + " " + game.name + " (" + player_1_name + " vs " + player_2_name + ")"
        game_list.append(gamestring)
    return game_list

def s_get_game_status(data):
    game_id = int(data[0])
    status = get_game_status(game_id)
    return ("OK", status)

def get_game_status(game_id):
    print("Getting status for Id: " + str(game_id) )
    game = lobby.games[game_id]
    status = game.get_status()
    return status

def s_wait_for_game_status(data):
    game_id = int(data[0])
    status = data[1]
    wait_for_game_status(game_id, status)
    return ("OK")

def wait_for_game_status(game_id, status):
    game = lobby.games[game_id]
    while True:
        time.sleep(1)
        current_status = game.get_status()
        if current_status == status:
            break

def s_wait_for_turn(data):
    game_id = int(data[0])
    player_id = data[1]
    wait_for_turn(game_id, player_id)
    return ("OK")

def wait_for_turn(game_id, player_id):
    game = lobby.games[game_id]
    while True:
        time.sleep(1)
        if game.active_player.id == player_id:
            break

def s_submit_board(data):
    game_id = int(data[0])
    player_id = data[1]
    board = data[2]
    if submit_board(game_id, player_id, board):
        return ("OK")
    else:
        return ("ERROR")

def submit_board(game_id, player_id, board):
    """Stores the board in game object"""
    game = lobby.games[game_id]
    player = game.players[player_id]
    player.board = board
    return True

def s_get_active_player(data):
    game_id = int(data[0])
    player_id = get_active_player(game_id)
    if player_id:
        return ("OK", player_id)
    else:
        return ("ERROR")

def get_active_player(game_id):
    """Returns id of the active player"""
    game = lobby.games[game_id]
    player_id = game.active_player.id
    if player_id:
        return player_id
    else:
        return False

def s_drop_bomb(data):
    game_id = int(data[0])
    player_id = data[1]
    row = data[2]
    col = data[3]
    result = drop_bomb(game_id, player_id, row, col)
    if result == "HIT":
        return ("OK", result)
    if result == "MISS":
        return("OK", result)

def drop_bomb(game_id, player_id, row, col):
    """Bomb the other player and return result"""
    game = lobby.games[game_id]
    player = game.players[player_id]
    opponent = game.get_opponent(player)
    board = opponent.board
    player.bomb_coords.append((row, col))
    game.switch_active_player()
    if board[row][col]:
        board[row][col] = ""
        return "HIT"
    else:
        return "MISS"

def s_get_round_data(data):
    game_id = int(data[0])
    player_id = data[1]
    round_data = get_round_data(game_id, player_id)
    return ("OK", round_data)

def get_round_data(game_id, player_id):
    """Retrieve opponents last bomb position and game status."""
    game = lobby.games[game_id]
    player = game.players[player_id]
    opponent = game.get_opponent(player)
    last_bomb_coords = ()
    if opponent.bomb_coords:
        last_bomb_coords = opponent.bomb_coords[-1]
    status = game.get_status()
    return (last_bomb_coords, status)

def s_get_game_info(data):
    game_id = int(data[0])
    game_info = get_game_info(game_id)
    return ("OK", game_info)

def get_game_info(game_id):
    """Retrieves general information about the game"""
    game = lobby.games[game_id]
    game_name = game.name
    players = []
    for player_id, player in game.players.items():
        players.append((player_id, player.name))
    return (game_name, players)


lobby = Lobby()

commands = {'s_create_game' : s_create_game, 's_get_games' : s_get_games, 's_create_player' : s_create_player,
            's_join_game' : s_join_game, "s_get_game_status" : s_get_game_status, "s_submit_board" : s_submit_board,
            's_get_active_player' : s_get_active_player, 's_drop_bomb' : s_drop_bomb, 's_get_round_data' : s_get_round_data,
            's_get_game_info' : s_get_game_info, 's_wait_for_game_status' : s_wait_for_game_status, 's_wait_for_turn' : s_wait_for_turn }

server = ConnectionFactory("BattleShip Server", "0.0.0.0", 8888, commands)

server.start()
server.connections
while True:
    time.sleep(1)