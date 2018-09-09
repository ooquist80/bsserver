class Game():
    
    id = 0

    def __init__(self, name, player):
        
        # Unique id for each game starting from 1
        Game.id += 1
        self.id = Game.id
        
        self.name = name
        self.players = {player.id : player}

        self.active_player = player

    def get_opponent(self, other_player):
        """Returns the other player of the game"""
        for player in self.players.values():
            if player.id != other_player.id:
                return player

    def switch_active_player(self):
        """Switches the active player."""
        opponent = self.get_opponent(self.active_player)
        self.active_player = opponent

    def get_status(self):
        """Returns the status of the game""" 
        
        # Populating, Preparing, Running, Finished
        
        status = "populating"
        # Check for 2 players
        if len(self.players) > 1:
            status = "preparing"
        # Check if both players have boards
        have_boards = True
        for player in self.players.values():
            if not player.board:
                have_boards = False
        # If both have boards check if the player is alive
        if have_boards:
            status = "running"
            for player in self.players.values():
                if player.is_dead():
                    status = "finished"
        return status