import random
from support_funcs import transpose, invert

class game_board(object):

    def __init__(self, width = 4, height = 4, win_condition = 2048, spawn_four_chance = 0.1):
        
        # Gameplay variables
        self.width = width
        self.height = height
        self.win_condition = win_condition
        self.spawn_four_chance = max(0, spawn_four_chance)

        # Score variables
        self.current_score = 0
        self.highscore = 0

        # Set up the game state
        self.reset_game()

    def reset_game(self):

        # Update highscore if needed
        self.highscore = max(self.current_score, self.highscore)

        # Reset score and board state
        self.score = 0
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # Add two tiles to start
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        # Get the new tile value, with the chance that it is 4 instead of 2
        new_tile_value = 2 if random.randrange(100) < int((1 - self.spawn_four_chance) * 100) else 4

        # Get a random location that is empty
        (x, y) = random.choice([(x, y) for x in range(self.width) for y in range(self.height) if self.grid[x][y] == 0])

        # Enter the value of the new tile into the empty slot
        self.grid[x][y] = new_tile_value

    def move(self, direction):
        def move_left(row):

            length = len(row)

            # Method to shift the values in the row to the leftmost position
            def shift():
                # Create an row with all of the non-zero elements
                new_row = [i for i in row if i != 0]
                # Append the difference in zeros to the end of the new row
                new_row += [0 for _ in range(length - len(new_row))]
                return new_row

            # Method to merge adjacent similar values
            def merge():
                found_pair = False
                new_row = [0] * length

                for i in range(length):
                    next_val = 0
                    if found_pair:
                        next_val = 2 * row[i]
                        self.score += next_val
                        found_pair = False
                    elif i + 1 < length and row[i] == row[i + 1]:
                        found_pair = True
                    else:
                        next_val = row[i]
                    new_row[i] = next_val

                return new_row

            # Shift the row, merge everything, then shift again
            return shift(merge(shift(row)))

        # Get the possible moves and operations to do each move
        moves = {}
        moves["LEFT"] = lambda grid: [move_left(row) for row in grid]
        moves["RIGHT"] = lambda grid: invert(moves["LEFT"](invert(grid)))
        moves["UP"] = lambda grid: transpose(moves["LEFT"](transpose(grid)))
        moves["DOWN"] = lambda grid: transpose(moves["RIGHT"](transpose(grid)))

        # Attempt to perform the movement
        if direction in moves and self.can_move(direction):
            # Move the tiles
            self.grid = moves[direction](self.grid)
            # Add a new tile
            self.add_new_tile()
            # Indicate that a move has been made
            return True
        else:
            # Indicate that the move cannot be made
            return False

    def can_move(self, direction):

        def can_move_left(row):
            prev_num = -1
            for i in row:
                # The move is possible if either there is an empty space or there is 
                # two adjacent tiles with the same value, meaning a merge is possible
                if i == 0 or i == prev_num:
                    return True
                else:
                    prev_num = i
            return False

        # Get the possible checks and operations to do each check
        check = {}
        check["LEFT"] = lambda grid: any(can_move_left(row) for row in grid)
        check["RIGHT"] = lambda grid: check["LEFT"](invert(grid))
        check["UP"] = lambda grid: check["LEFT"](transpose(grid))
        check["DOWN"] = lambda grid: check["RIGHT"](transpose(grid))

        return check[direction](self.grid) if direction in check else False

    def has_won(self):
        return any(any(i >= self.win_condition for i in row) for row in self.grid)

    def has_lost(self):
        directions = ["LEFT", "RIGHT", "UP", "DOWN"]
        return not any(self.move)