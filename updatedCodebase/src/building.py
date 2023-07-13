import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import src.global_variable as gv
import src.scenery 

gameBoard = src.scenery.GameBoard()

class Building:
    
    def __init__(self):
        self.id = 0 
        self.X_coor = int(gv.m/2)
        self.Y_coor = int(gv.n/2)
        self.len = 1
        self.width = 1
        self.attack_power = 0
        self.color = Fore.GREEN

    def give_color(self):
        for i in range(self.X_coor, self.X_coor+self.len):
            for j in range(self.Y_coor, self.Y_coor+self.width):
                gameBoard.array[i][j] = self.color + self.char + Style.RESET_ALL 
                gameBoard.pseudo_array[i][j] = self.char + str(self.id)

    def damage(self, damage, array, pseudo_array):
        self.health -= damage
        if self.health <= 0:
            for i in range(self.X_coor, self.X_coor+self.len):
                for j in range(self.Y_coor, self.Y_coor+self.width):
                    gameBoard.array[i][j] = ' '
                    gameBoard.pseudo_array[i][j] = ' ' 
                    self.attack_power = 0
            self.X_coor = 1000
            self.Y_coor = 1000
        else :
            if self.health < 0.2*self.max_health:
                self.color = Fore.RED
            elif self.health < 0.5*self.max_health:
                self.color = Fore.YELLOW
            self.give_color()
    
class Townhall(Building):
    def __init__(self,townhall_id):
        super().__init__()
        self.len = 4
        self.width = 3
        self.max_health = gv.max_health_townhall
        self.health = self.max_health
        self.char = 'T'
        self.id = townhall_id
        self.give_color()

class Huts(Building):
    def __init__(self, X_coor, Y_coor, hut_id):
        super().__init__()
        self.X_coor = X_coor
        self.Y_coor = Y_coor
        self.max_health = gv.max_health_huts
        self.health = self.max_health
        self.id = hut_id
        self.char = 'H' 
        self.give_color()
    
class Canon(Building):
    def __init__(self, X_coor, Y_coor, canon_id):
        super().__init__()
        self.X_coor = X_coor
        self.Y_coor = Y_coor
        self.max_health = gv.max_health_canon
        self.health = self.max_health
        self.id = canon_id
        self.attack_power = gv.canon_damage
        self.char = 'C'
        self.give_color()

    def attack(self, array, pseudo_array, king, barbarians):
        color_change = 1
        if(((self.X_coor-king.x_coor)**2 + (self.Y_coor - king.y_coor)**2 <= 36) and (king.x_coor != 1000 and king.y_coor != 1000) and king.health > 0):
                color_change = 0
                gameBoard.array[self.X_coor][self.Y_coor] = Back.RED + self.char + Style.RESET_ALL
                king.health -= self.attack_power
                if(king.health <=0):
                    king.destroy(gameBoard.array, gameBoard.pseudo_array)
        else:
            for i in barbarians:
                if(i.x_coor > 0 and i.y_coor > 0 and i.health > 0):
                    if((self.X_coor-i.x_coor)**2 + (self.Y_coor - i.y_coor)**2 <= 25):
                        gameBoard.array[self.X_coor][self.Y_coor] = Back.RED + self.char + Style.RESET_ALL
                        i.health -= self.attack_power
                        color_change = 0
                        if i.health <= 0:
                            i.destroy(gameBoard.array, gameBoard.pseudo_array)
                        break
        if color_change and self.X_coor != 1000 :
            gameBoard.array[self.X_coor][self.Y_coor] = Fore.GREEN + self.char + Style.RESET_ALL
        
class Wall(Building):
    def __init__(self, X_coor, Y_coor, wall_id):
        super().__init__()
        self.max_health = gv.max_health_wall
        self.health = self.max_health
        self.X_coor = X_coor
        self.Y_coor = Y_coor
        self.id = wall_id
        self.char = 'W'
        self.give_color()

gameBoard.print_board()
