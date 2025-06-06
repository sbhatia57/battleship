import random
class ship:
    def __init__(self, length, type):
        self.length = length
        self.coordinates = []
        self.hitCoordinates = [0 for _ in range(self.length)]  # Initialize hit coordinates to 0
        self.type = type  # e.g., 'carrier', 'battleship', etc.
    
    def place(self, start_x, start_y, direction, boardsize, grid):
        # Continue generating starting coordinates and changing direction of a ship until a valid location is found
        horizontal_directions = ['horizontal', 'vertical']
        while True:
            if direction == 'horizontal':
                if start_x + self.length > boardsize:
                    start_x = random.randint(0, boardsize - 1)
                    direction = horizontal_directions[random.randint(0, 1)]
                else:
                    found_ship = False
                    for i in range(self.length):
                        if grid[start_y][start_x + i] == 'S':
                            start_x = random.randint(0, boardsize - 1)
                            direction = horizontal_directions[random.randint(0, 1)]
                            found_ship = True
                            break
                    if found_ship:
                        continue
                    else:
                        break
            elif direction == 'vertical':
                if start_y + self.length > boardsize:
                    start_y = random.randint(0, boardsize - 1)
                    direction = horizontal_directions[random.randint(0, 1)]
                else:
                    found_ship = False
                    for i in range(self.length):
                        if grid[start_y + i][start_x] == 'S':
                            start_y = random.randint(0, boardsize - 1)
                            direction = horizontal_directions[random.randint(0, 1)]
                            found_ship = True
                            break
                    if found_ship:
                        continue
                    else:
                        break
        if direction == 'horizontal':
            self.coordinates = [(start_x + i, start_y) for i in range(self.length)]
            for x, y in self.coordinates:
                grid[y][x] = 'S'
        elif direction == 'vertical':
            self.coordinates = [(start_x, start_y + i) for i in range(self.length)]
            for x, y in self.coordinates:
                grid[y][x] = 'S'
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
    
    def __repr__(self):
        return f"Ship(length={self.length}, coordinates={self.coordinates})"
    
    def hit(self, x, y):
        # Check if the coordinates hit the ship
        if (x, y) in self.coordinates:
            index = self.coordinates.index((x, y))
            self.hitCoordinates[index] = 1
    
    def is_sunk(self):
        # Check if all parts of the ship have been hit
        return all(hit == 1 for hit in self.hitCoordinates)
    
class board:
    def __init__(self, size):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.carrier = ship(5, 'carrier')
        self.battleship = ship(4, 'battleship')
        self.cruiser = ship(3, 'cruiser')
        self.submarine = ship(3, 'submarine')
        self.destroyer = ship(2, 'destroyer')
        self.place_ships()
    
    # printing board for debugging purposes
    def __repr__(self):
        board_str = '  ' + ' '.join(str(i) for i in range(self.size)) + '\n'
        for i, row in enumerate(self.grid):
            board_str += str(i) + ' ' + ' '.join(row) + '\n'
        return board_str
    
    def place_ships(self):
        # Example placements, can be randomized or user-defined
        horizontal_directions = ['horizontal', 'vertical']
        self.carrier.place(random.randint(0, self.size - 1), random.randint(0, self.size - 1), horizontal_directions[random.randint(0, 1)], self.size, self.grid)
        self.battleship.place(random.randint(0, self.size - 1), random.randint(0, self.size - 1), horizontal_directions[random.randint(0, 1)], self.size, self.grid)
        self.cruiser.place(random.randint(0, self.size - 1), random.randint(0, self.size - 1), horizontal_directions[random.randint(0, 1)], self.size, self.grid)
        self.submarine.place(random.randint(0, self.size - 1), random.randint(0, self.size - 1), horizontal_directions[random.randint(0, 1)], self.size, self.grid)
        self.destroyer.place(random.randint(0, self.size - 1), random.randint(0, self.size - 1), horizontal_directions[random.randint(0, 1)], self.size, self.grid)

class player:
    def __init__(self, name):
        self.name = name
        self.board = board(10)  # Default board size of 10x10
        self.playerGrid = [[' ' for _ in range(10)] for _ in range(10)]
        self.hitsToWin = 17  # Total hits needed to win (5+4+3+3+2)
        self.hits = 0
        self.misses = 0
        self.missiles = 60  # Number of missiles available
    
    def __repr__(self):
        return f"Player(name={self.name}, board=\n{self.board})"
    
    def printVisualBoard(self):
        # Print the player's board with hits and misses
        alphabet= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        board_str = '  ' + ' '.join(alphabet[i] for i in range(self.board.size)) + '\n'
        for i, row in enumerate(self.playerGrid):
            board_str += str(i) + ' ' + ' '.join(row) + '\n'
        print(board_str)

    def game_loop(self):
        print("Welcome to Battleship!")

        while True:

            print("You have missed {} times.".format(self.misses))
            print("You have made {} hits.".format(self.hits))
            print("You have {} missiles to left to use.".format(self.missiles))
            print("You need to make {} hits to win.".format(self.hitsToWin))
            
            # Print the board
            self.printVisualBoard()
            input("Where would you like to fire? (Press Enter to continue)")
            # Get user input for coordinates
            while True:
                try:
                    coordinates = input("Enter coordinates (e.g., A5): ").upper()
                    if len(coordinates) != 2 or coordinates[0] not in 'ABCDEFGHIJ' or not coordinates[1].isdigit():
                        raise ValueError("Invalid input format. Please use the format A5.")
                    x = ord(coordinates[0]) - ord('A')  # Convert letter to index
                    y = int(coordinates[1])  # Convert number to index
                    if x < 0 or x >= self.board.size or y < 0 or y >= self.board.size:
                        raise ValueError("Coordinates out of bounds. Please enter valid coordinates.")
                    break
                except ValueError as e:
                    print(e)
            # Check if the coordinates have already been fired upon
            if self.playerGrid[y][x] == 'X' or self.playerGrid[y][x] == 'O':
                print("You have already fired at these coordinates. Please try again.")
                continue

            # Decrement the number of missiles
            self.missiles -= 1

            # Check if the shot hits a ship
            if self.board.grid[y][x] == 'S':
                print("Hit!")
                # Determine which ship was hit based on the coordinates
                for ship in [self.board.carrier, self.board.battleship, self.board.cruiser, self.board.submarine, self.board.destroyer]:
                    if (x, y) in ship.coordinates:
                        ship.hit(x, y)
                        if ship.is_sunk():
                            print(f"You have sunk the {ship.type}!")
                self.playerGrid[y][x] = 'X'
                self.hitsToWin -= 1
                self.hits += 1
            else:
                print("Miss!")
                self.playerGrid[y][x] = 'O'
                self.misses += 1

            if self.hitsToWin == 0:
                print("Congratulations! You have sunk all the ships!")
                # Check if the player wants to play again
                play_again = input("Do you want to play again? (yes/no): ").strip().lower()
                if play_again == 'yes':
                    self.hitsToWin = 17  # Reset hits to win
                    self.hits = 0
                    self.misses = 0
                    self.missiles = 60  # Reset missiles
                    self.playerGrid = [[' ' for _ in range(10)] for _ in range(10)]
                    self.board = board(10)  # Reset the board
                    print(self.board)
                else:
                    print("Thanks for playing!")
                    break
            
             # Check if the missile is available
            elif self.missiles <= 0:
                print("You have no missiles left!")
                print("Game Over!")
                # Check if the player wants to play again
                # Check if the player wants to play again
                play_again = input("Do you want to play again? (yes/no): ").strip().lower()
                if play_again == 'yes':
                    self.hitsToWin = 17  # Reset hits to win
                    self.hits = 0
                    self.misses = 0
                    self.missiles = 60  # Reset missiles
                    self.playerGrid = [[' ' for _ in range(10)] for _ in range(10)]
                    self.board = board(10)  # Reset the board
                else:
                    print("Thanks for playing!")
                    break

player1 = player("Player 1")
player1.game_loop()