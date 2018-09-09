class Player():

    def __init__(self, id, name):

        self.id = id
        self.name = name
        self.board = ""
        self.bomb_coords = []
    
    def is_dead(self):

        board = self.board
        rows = len(board)
        cols = len(board[0])
        is_dead = True
        for row in range(rows):
            for col in range(cols):
                if board[row][col]:
                    is_dead = False
        
        return is_dead