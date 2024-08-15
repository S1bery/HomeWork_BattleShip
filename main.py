class Ship:
    def __init__(self, coords): # Инициализация корабля.
        self.coords = coords
        self.is_destroyed = False

    def is_hit(self, coord): # Проверяет попадание.
        if coord in self.coords:
            self.coords.remove(coord)
            if not self.coords:
                self.is_destroyed = True
            return True
        return False

    def __str__(self): # Представление корабля в виде строки.
        return f"Корабль: {self.coords}"

class Board:
    def __init__(self, ships): # Инициализация игровой доски.
        self.size = 6
        self.board = [['O' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = ships
        self.shots = set()

        for ship in self.ships:
            for coord in ship.coords:
                self.board[coord[1] - 1][coord[0] - 1] = '■'

    def is_valid_coord(self, coord): # Проверка координат.
        if 1 <= coord[0] <= self.size and 1 <= coord[1] <= self.size:
            return True
        return False

    def is_free_cell(self, coord): # Проверка клетки на пустоту.
        if self.board[coord[1] - 1][coord[0] - 1] == 'O':
            return True
        return False

    def is_ship_destroyed(self): # Проверяет, уничтожены ли все корабли.
        for ship in self.ships:
            if not ship.is_destroyed:
                return False
        return True

    def make_shot(self, coord): #Производит выстрел по заданным координатам.
        if not self.is_valid_coord(coord):
            raise ValueError("Некорректные координаты.")

        if coord in self.shots:
            raise ValueError("Вы уже стреляли в эту клетку.")

        self.shots.add(coord)

        if self.is_free_cell(coord):
            self.board[coord[1] - 1][coord[0] - 1] = 'T'
            return False

        for ship in self.ships:
            if ship.is_hit(coord):
                if ship.is_destroyed:
                    self.board[coord[1] - 1][coord[0] - 1] = 'X'
                return True

    def print_board(self): # Печатать игровой доски.
        print(" | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i in range(self.size):
            print(f"{i + 1} | {' | '.join(self.board[i])} |")

def generate_ships(board): # Генерирует случайные корабли на доске.
    ships = []
    # 3-клеточный корабль
    ships.append(generate_ship(board, 3))
    # 2-клеточные корабли
    for _ in range(2):
        ships.append(generate_ship(board, 2))
    # 1-клеточные корабли
    for _ in range(4):
        ships.append(generate_ship(board, 1))

    return ships

def generate_ship(board, length): # Генерирует случайный корабль заданной длины.

    import random # Импорт random внутри функции
    while True:
        direction = random.choice(['horizontal', 'vertical'])
        if direction == 'horizontal':
            x = random.randint(1, board.size - length + 1)
            y = random.randint(1, board.size)
            coords = [(x + i, y) for i in range(length)]
        else:
            x = random.randint(1, board.size)
            y = random.randint(1, board.size - length + 1)
            coords = [(x, y + i) for i in range(length)]

        # Проверка, что корабль не пересекается с другими кораблями
        if all(board.is_free_cell(coord) for coord in coords):
            return Ship(coords)

def get_player_shot(): # Получает координаты выстрела от игрока.
    while True:
        try:
            x, y = map(int, input("Введите координаты выстрела (x y): ").split())
            if 1 <= x <= 6 and 1 <= y <= 6:
                return (x, y)
            else:
                print("Некорректные координаты. Повторите ввод.")
        except ValueError:
            print("Некорректный формат ввода. Повторите ввод.")

def play_game(): # Запуск игры.
    player_board = Board(generate_ships(Board([])))
    computer_board = Board(generate_ships(Board([])))

    player_turn = True

    while True:
        if player_turn:
            print("Ваша доска:")
            player_board.print_board()
            print("Доска противника:")
            computer_board.print_board()

            try:
                coord = get_player_shot()
                hit = computer_board.make_shot(coord)
                if hit:
                    print("Попадание!")
                else:
                    print("Промах.")
            except ValueError as e:
                print(e)

            if computer_board.is_ship_destroyed():
                print("Вы победили!")
                break

        else:
            print("Ход компьютера:")
            while True:
                try:
                    import random # Импорт рандома внутри цикла, чтобы не импортировать его перед вызовом функции
                    x = random.randint(1, 6)
                    y = random.randint(1, 6)
                    coord = (x, y)
                    hit = player_board.make_shot(coord)
                    break
                except ValueError:
                    pass

            if hit:
                print("Компьютер попал!")
            else:
                print("Компьютер промахнулся.")

            if player_board.is_ship_destroyed():
                print("Компьютер победил!")
                break

        player_turn = not player_turn

if __name__ == "__main__":
    play_game()