import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import src.global_variable as gv

# make a class for gameboard in green color
class GameBoard:
    def __init__(self):
        self.array=[[' ' for i in range(gv.n)] for j in range(gv.m)]
        self.pseudo_array = [[' ' for i in range(gv.n)] for j in range(gv.m)]

        # add a 'X' to the boundary of the gameboard
        for i in range(gv.m):
            self.array[i][0] = Back.BLUE+ 'X' + Style.RESET_ALL
            self.array[i][gv.n-1] = Back.BLUE + 'X' + Style.RESET_ALL
            self.pseudo_array[i][0]= 'X'
            self.pseudo_array[i][gv.n-1]   = 'X'

        for j in range(gv.n):
            self.array[0][j] = Back.BLUE + 'X' + Style.RESET_ALL
            self.array[gv.m-1][j] = Back.BLUE + 'X' + Style.RESET_ALL
            self.pseudo_array[0][j] = 'X'
            self.pseudo_array[gv.m-1][j] = 'X'    

    def print_board(self):
        printVal = ""
        for i in range(gv.m):
            for j in range(gv.n):
                printVal += self.array[i][j]
            printVal += "\n"
        print('\033[H'+ printVal)

    def print_pseudo_array(self):
        for i in range(gv.m):
            for j in range(gv.n):
                print(self.pseudo_array[i][j], end="")
            print()

    def game_lost(self, king, barbarians, barbarian_count):
        king_death = -1
        barbarians_death = -1
        if king.health <= 0:
            print(Fore.RED + "King is dead!")
            king_death = 0
        for i in barbarians:
            if barbarian_count == 15:
                if i.health > 0:
                    barbarians_death = 0
                    break
        
        if(king_death == 0 and barbarians_death == -1 and barbarian_count == 15):
            return True
        else:
            return False

    def game_won(self, Universal_array):
        for i in range(3):
            for j in Universal_array[i]:
                if(j.health > 0):
                    return False
        return True

    def game_points(self, Universal_array): 
        game_points = 0
        multiplier = [20,10,5,1]
        for i in range(4):
            for j in Universal_array[i]:
                if j.health <= 0:
                    game_points += multiplier[i]

        print(Fore.BLUE + "SCORE: ", game_points)
            