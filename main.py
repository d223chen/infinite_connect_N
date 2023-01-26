from collections import defaultdict

class Game:
    board = dict() # (x,y) to piece at coordinate
    heights = defaultdict(lambda : 0) # x to height
    
    def __init__(self, N: int, height : int, width : int) -> None:
        self.N = N
        self.height = height
        self.width = width
        
    def number_matching_in_direction(self, piece: str, x : int, y: int, delta_x : int, delta_y: int) -> int:
        number_matching_in_direction = 0
        i = 1
        while (x + i * delta_x, y + i * delta_y) in self.board.keys() and self.board[(x + i * delta_x, y + i * delta_y)] == piece:
            number_matching_in_direction += 1
            i += 1
        
        return number_matching_in_direction
        
    def check_if_direction_forms_line(self, piece : str, x : int, y: int, delta_x : int, delta_y : int) -> bool:
        number_matching_in_direction = self.number_matching_in_direction(piece, x, y, delta_x, delta_y)
        number_matching_in_opposite_direction = self.number_matching_in_direction(piece, x, y, -delta_x, -delta_y)
        
        return number_matching_in_direction + number_matching_in_opposite_direction + 1 >= self.N
        
    def check_if_winner(self, piece : str, x : int, y : int) -> bool:
        horizonal_line = self.check_if_direction_forms_line(piece, x, y, 1, 0)
        vertical_line = self.check_if_direction_forms_line(piece,x, y, 0, 1)
        main_diagonal = self.check_if_direction_forms_line(piece,x, y, 1, -1) # top left to bottom right
        other_diagonal = self.check_if_direction_forms_line(piece,x, y,1, 1) # bottom left to top right
        
        return horizonal_line or vertical_line or main_diagonal or other_diagonal

    def play(self, piece: str, x: int) -> bool:
        assert(x >= 0)
        assert(x < self.width)
        assert(self.heights[x] < self.height)
        
        y = self.heights[x]
        self.board[(x,y)] = piece
        self.heights[x] += 1
        
        return self.check_if_winner(piece, x, y)
        
        
    def render(self) -> None:
        print()
        for y in reversed(range(self.height)):
            cur_line = "*"
            for x in range(self.width):
                if (x,y) in self.board.keys():
                    cur_line += self.board[(x,y)]
                else:
                    cur_line += " "
            cur_line += "*"
            print(cur_line)
            
        print("*" + "".join([str(i) for i in range(self.width)]) + "*")

def main() -> None:
    N = input("Enter N (number of pieces to be connected in a line to win, usually N = 4): ")
    width = input("Enter width of the board: ")
    height = input("Enter height of the board: ")
    
    game = Game(int(N), int(height), int(width))
    players = ['X', 'O']
    turn = 0
    while True:
        cur_player = players[turn % len(players)]
        game.render()
        x = input(f"Turn {turn}: {cur_player} to play. Choose x coordinate of piece: ")
        winner = game.play(cur_player, int(x))
        if winner:
            print(f"Player {cur_player} wins! ")
            print("Final state of the board: ")
            game.render()
            return
        
        turn += 1
    

if __name__ == "__main__":
    main()