class Player:

    def __init__(self, x, y, name):
        # Atual posicao no grid
        self.name = name
        self.x = x
        self.y = y

        self.direction = "Up"

        self.reward_amount = 20

        self.score = 0

    def move(self, direction, grid):

        if direction == "Up":
            self.direction = "Up"
            if grid.is_valid_position(self.x, self.y - 1):
                grid.clear_position(self.x, self.y)
                self.y -= 1
        if direction == "Down":
            self.direction = "Down"
            if grid.is_valid_position(self.x, self.y + 1):
                grid.clear_position(self.x, self.y)
                self.y += 1
        if direction == "Left":
            self.direction = "Left"
            if grid.is_valid_position(self.x-1, self.y):
                grid.clear_position(self.x, self.y)
                self.x -= 1
        if direction == "Right":
            self.direction = "Right"
            if grid.is_valid_position(self.x+1, self.y):
                grid.clear_position(self.x, self.y)
                self.x += 1