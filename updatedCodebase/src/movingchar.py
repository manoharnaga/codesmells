import time
import os
import src.global_variable as gv
import src.building as b
from src.building import gameBoard as Game_Map
from src.initialise import  townhall, hut_list, canon_list, wall_list, Universal_array,  townhall_list
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


class Character:

    def __init__(self):
        self.movement_speed = 1

    def move(self, direction, array, pseudo_array):
        old_x = self.x_coor
        old_y = self.y_coor

        def change_postion():
            array[old_x][old_y] = " "
            pseudo_array[old_x][old_y] = " "
            array[self.x_coor][self.y_coor] = "K"
            pseudo_array[self.x_coor][self.y_coor] = "K"
        
        def change_postion2():
            array[old_x][old_y] = Fore.BLUE + "N" + Style.RESET_ALL
            pseudo_array[old_x][old_y] = "N"
            array[self.x_coor][self.y_coor] = "K"
            pseudo_array[self.x_coor][self.y_coor] = "K"

        if self.type == "king":
            if direction == "w" and self.x_coor > 0:
                if(array[self.x_coor-1][self.y_coor] == " "):
                    if pseudo_array[self.x_coor][self.y_coor+1] == 'N' or pseudo_array[self.x_coor][self.y_coor-1] == 'N':
                        self.x_coor -= 1
                        change_postion2()
                    else :
                        self.x_coor -= 1
                        change_postion()
                self.last_move = "w"
            elif direction == "s" and self.x_coor < gv.m-1:
                if(array[self.x_coor+1][self.y_coor] == " "):
                    if pseudo_array[self.x_coor][self.y_coor+1] == 'N' or pseudo_array[self.x_coor][self.y_coor-1] == 'N':
                        self.x_coor += 1
                        change_postion2()
                    else:
                        self.x_coor += 1
                        change_postion()
                self.last_move = "s"
            elif direction == "a" and self.y_coor > 0:
                if(array[self.x_coor][self.y_coor-1] == " "):
                    self.y_coor -= 1
                    change_postion()
                self.last_move = "a"
            elif direction == "d" and self.y_coor < gv.n-1:
                if(array[self.x_coor][self.y_coor+1] == " "):
                    self.y_coor += 1
                    change_postion()
                self.last_move = "d"

    def health_bar(self, array, pseudo_array):
        health = self.health
        health_value = int(health/10)

        if(health <= 0):
            self.destroy(array, pseudo_array)

        healthBar = ""
        for i in range(health_value):
            if i <= 2:
                healthBar += Back.RED + "  "
            elif i <= 5:
                healthBar += Back.YELLOW + "  "
            elif i <= 10:
                healthBar += Back.GREEN + "  "
        print(healthBar)

    def destroy(self, array, pseudo_array):
        self.health = 0
        if self.x_coor != 1000:
            array[self.x_coor][self.y_coor] = " "
            pseudo_array[self.x_coor][self.y_coor] = " "
        self.x_coor = 1000
        self.y_coor = 1000
        self.attack_power = 0

    def damage(self, array, pseudo_array):
        self.health -= gv.canon_damage
        if(self.health <= 0):
            self.destroy(array, pseudo_array)        

    def attack_buildings(self,code, array, pseudo_array):
        if code[0] == 'T':
            townhall.damage(self.attack_power, array, pseudo_array)
        elif code[0] == 'H':
            code = code[1:len(code):1]
            hut_list[int(code)].damage(self.attack_power, array, pseudo_array)
        elif code[0] == 'C':
            code = code[1:len(code):1]
            canon_list[int(code)].damage(self.attack_power, array, pseudo_array)
        elif code[0] == 'W':
            code = code[1:len(code):1]
            wall_list[int(code)].damage(self.attack_power, array, pseudo_array)

    def attack(self, array, pseudo_array):
        curr_X = self.x_coor
        curr_Y = self.y_coor

        dict = { 
            "w" : (-1, 0),
            "s" : (1, 0),
            "a" : (0, -1),
            "d" : (0, 1)
        }

        if self.last_move in dict.keys():
            if(pseudo_array[curr_X+dict[self.last_move][0]][curr_Y + dict[self.last_move][1]] != ' '):
                code = pseudo_array[curr_X+dict[self.last_move][0]][curr_Y + dict[self.last_move][1]]
                self.attack_buildings(code, array, pseudo_array)

    def leviathan(self, array, pseudo_array, Universal_array):
        for i in range(4):
            for j in Universal_array[i]:
                if((self.x_coor - j.X_coor)**2 + (self.y_coor - j.Y_coor)**2 <= 25):
                    j.damage(self.attack_power, array, pseudo_array)

class king(Character):
    def __init__(self, x_coor, y_coor, array, pseudo_array):
        self.type = "king"
        self.x_coor = x_coor
        self.y_coor = y_coor
        array[self.x_coor][self.y_coor] = "K"
        pseudo_array[self.x_coor][self.y_coor] = "K"
        self.health = gv.max_health_king
        self.last_move = " "
        self.attack_power = gv.attack_power_king
        self.movement_speed = 1

class Nuke(Character):
    def __init__(self, x_coor, y_coor, array, pseudo_array):
        self.type = "Rocket"
        self.x_coor = x_coor
        self.y_coor = y_coor
        self.color = Fore.BLUE
        array[self.x_coor][self.y_coor] = self.color + "N" + Style.RESET_ALL
        pseudo_array[self.x_coor][self.y_coor] = "N"
        self.last_move = " "
        self.attack_power = gv.attack_power_nuke

    def move(self, array, pseudo_array, Universal_array):
        if(self.y_coor == int(gv.n)-1):
            self.x_coor = 1000
            self.y_coor = 1000
            gv.Nuke_isdestroyed = True
            print("TownHall aldready destroyed")
            return
        elif((self.x_coor == Universal_array[0][0].X_coor and self.y_coor == Universal_array[0][0].Y_coor) ):
            self.x_coor = 1000
            self.y_coor = 1000
            Universal_array[0][0].damage(self.attack_power, array, pseudo_array)
            gv.Nuke_isdestroyed = True

            file = "bomb_explosion_sms.mp3"
            os.system("mpg123 " + file)
            time.sleep(0.24)
            print("Destroyed the townhall")
            return
        else:
            self.y_coor += 1
            if(pseudo_array[self.x_coor][self.y_coor] == ' '):
                pseudo_array[self.x_coor][self.y_coor] = "N"
                array[self.x_coor][self.y_coor] = self.color + "N" + Style.RESET_ALL

class barbarians(Character):
    def __init__(self, x_coor, y_coor, array, pseudo_array, barbarian_count):
        self.type = "barbarians"
        self.x_coor = x_coor
        self.y_coor = y_coor
        self.color = Back.GREEN
        array[self.x_coor][self.y_coor] = self.color + "B" + Style.RESET_ALL
        pseudo_array[self.x_coor][self.y_coor] = "B"
        self.health = gv.max_health_barbarians
        self.last_move = " "
        self.attack_power = gv.attack_power_barbarians
        self.barbarian_id = barbarian_count
        self.movement_speed = 1

    def bar_move(self, array, pseudo_array):
        old_x = self.x_coor
        old_y = self.y_coor

        def bar_position_change():
            array[old_x][old_y] = " "
            pseudo_array[old_x][old_y] = " "
            array[self.x_coor][self.y_coor] = self.color + "B" + Style.RESET_ALL
            pseudo_array[self.x_coor][self.y_coor] = "B"

        if(self.health > 0):
            # iterate over all the objects and find nearest object
            # Euclidean distance
            # iterate over Universal_array
            min_distance = 10000
            i_temp, j_temp = 0, 0
            for i in range(3):
                for j in range(len(Universal_array[i])):
                    x_diff = abs(self.x_coor - Universal_array[i][j].X_coor)**2
                    y_diff = abs(self.y_coor - Universal_array[i][j].Y_coor)**2
                    euclidean = x_diff + y_diff
                    if(min_distance >= euclidean):
                        min_distance = euclidean
                        i_temp = i
                        j_temp = j  

            x_diff = abs(self.x_coor - Universal_array[i_temp][j_temp].X_coor)**2
            y_diff = abs(self.y_coor - Universal_array[i_temp][j_temp].Y_coor)**2

            if((x_diff == 1 or y_diff == 1) or (x_diff == 1 or y_diff == 0) or (x_diff == 0 or y_diff == 0) or (x_diff == 0 or y_diff == 1)):
                self.attack(array, pseudo_array)

            if(self.x_coor > Universal_array[i_temp][j_temp].X_coor and self.y_coor == Universal_array[i_temp][j_temp].Y_coor and (pseudo_array[self.x_coor-1][self.y_coor] in [' ','B','K'])):
                if(pseudo_array[self.x_coor-1][self.y_coor] in ['B','K']):
                    if(pseudo_array[self.x_coor-1][self.y_coor-1] == ' '):
                        self.y_coor -= 1
                        self.x_coor -= 1
                        self.last_move = '#'
                    elif(pseudo_array[self.x_coor-1][self.y_coor+1] == ' '):
                        self.y_coor += 1
                        self.x_coor -= 1
                        self.last_move = '#'
                else :
                    self.x_coor -= 1
                    self.last_move = 'w'
                bar_position_change()
                
            elif(self.x_coor < Universal_array[i_temp][j_temp].X_coor and self.y_coor == Universal_array[i_temp][j_temp].Y_coor and (pseudo_array[self.x_coor+1][self.y_coor] in [' ','B','K'])):
                if(pseudo_array[self.x_coor+1][self.y_coor] in ['B','K']):
                    if(pseudo_array[self.x_coor+1][self.y_coor-1] == ' '):
                        self.x_coor += 1
                        self.y_coor -= 1
                        self.last_move = '#'
                    elif(pseudo_array[self.x_coor+1][self.y_coor+1] == ' '):
                        self.x_coor += 1
                        self.y_coor += 1
                        self.last_move = '#'
                else :
                    self.x_coor += 1
                    self.last_move = 's'
                bar_position_change()
            elif(self.x_coor == Universal_array[i_temp][j_temp].X_coor and self.y_coor > Universal_array[i_temp][j_temp].Y_coor and (pseudo_array[self.x_coor][self.y_coor-1] in [' ','B','K'])):
                if(pseudo_array[self.x_coor][self.y_coor-1] in ['B','K']):
                    if(pseudo_array[self.x_coor-1][self.y_coor-1] == ' '):
                        self.x_coor -= 1
                        self.y_coor -= 1
                        self.last_move = '#'
                    elif(pseudo_array[self.x_coor+1][self.y_coor-1] == ' '):
                        self.x_coor += 1
                        self.y_coor -= 1
                        self.last_move = '#'
                else :
                    self.y_coor -= 1
                    self.last_move = 'a'
                bar_position_change()
            elif(self.x_coor == Universal_array[i_temp][j_temp].X_coor and self.y_coor < Universal_array[i_temp][j_temp].Y_coor and (pseudo_array[self.x_coor][self.y_coor+1] in [' ','B','K'])):
                if(pseudo_array[self.x_coor][self.y_coor+1] in ['B','K']):
                    if(pseudo_array[self.x_coor-1][self.y_coor+1] == ' '):
                        self.x_coor -= 1
                        self.y_coor += 1
                        self.last_move = '#'
                    elif(pseudo_array[self.x_coor+1][self.y_coor+1] == ' '):
                        self.x_coor += 1
                        self.y_coor += 1
                        self.last_move = '#'
                else :
                    self.y_coor += 1
                    self.last_move = 'd'
                bar_position_change()
            elif(self.x_coor > Universal_array[i_temp][j_temp].X_coor and self.y_coor > Universal_array[i_temp][j_temp].Y_coor and (pseudo_array[self.x_coor-1][self.y_coor-1] in [' ','B','K'])):
                if(pseudo_array[self.x_coor-1][self.y_coor-1] in ['B','K']):
                    if(pseudo_array[self.x_coor-1][self.y_coor] == ' '):
                        self.x_coor -= 1
                        self.last_move = 'w'
                    elif(pseudo_array[self.x_coor][self.y_coor-1] == ' '):
                        self.y_coor -= 1
                        self.last_move = 'a'
                else :
                    self.x_coor -= 1
                    self.y_coor -= 1
                    self.last_move = '#'
                bar_position_change()
            elif(self.x_coor > Universal_array[i_temp][j_temp].X_coor and self.y_coor < Universal_array[i_temp][j_temp].Y_coor and (pseudo_array[self.x_coor-1][self.y_coor+1] in [' ','B','K'])):
                if(pseudo_array[self.x_coor-1][self.y_coor+1] in ['B','K']):
                    if(pseudo_array[self.x_coor-1][self.y_coor] == ' '):
                        self.x_coor -= 1
                        self.last_move = 'w'
                    elif(pseudo_array[self.x_coor][self.y_coor+1] == ' '):
                        self.y_coor += 1
                        self.last_move = 'd'
                else :
                    self.x_coor -= 1
                    self.y_coor += 1
                    self.last_move = '#'
                bar_position_change()
            elif(self.x_coor < Universal_array[i_temp][j_temp].X_coor and self.y_coor > Universal_array[i_temp][j_temp].Y_coor and (pseudo_array[self.x_coor+1][self.y_coor-1] in [' ','B','K'])):
                if(pseudo_array[self.x_coor+1][self.y_coor-1] in ['B','K']):
                    if(pseudo_array[self.x_coor+1][self.y_coor] == ' '):
                        self.x_coor += 1
                        self.last_move = 's'
                    elif(pseudo_array[self.x_coor][self.y_coor-1] == ' '):
                        self.y_coor -= 1
                        self.last_move = 'a'
                else :
                    self.x_coor += 1
                    self.y_coor -= 1
                    self.last_move = '#'
                bar_position_change()
            elif(self.x_coor < Universal_array[i_temp][j_temp].X_coor and self.y_coor < Universal_array[i_temp][j_temp].Y_coor and (pseudo_array[self.x_coor+1][self.y_coor+1] in [' ','B','K'])):
                if(pseudo_array[self.x_coor+1][self.y_coor+1] in ['B','K']):
                    if(pseudo_array[self.x_coor+1][self.y_coor] == ' '):
                        self.x_coor += 1
                        self.last_move = 's'
                    elif(pseudo_array[self.x_coor][self.y_coor+1] == ' '):
                        self.y_coor += 1
                        self.last_move = 'd'
                else :
                    self.x_coor += 1
                    self.y_coor += 1
                    self.last_move = '#'
                bar_position_change()

    def attack(self, array, pseudo_array):
        curr_X = self.x_coor
        curr_Y = self.y_coor

        if(self.health > 0):
            array_xcor = [-1, 0, 1, 0, -1, 1, -1, 1]
            array_ycor = [0, -1, 0, 1, -1, -1, 1, 1]
            for i in range(0, len(array_xcor)):
                code = pseudo_array[curr_X + array_xcor[i]][curr_Y + array_ycor[i]]
                if(code not in [' ','B', 'K'] ):
                    if code[0] == 'T':
                        townhall.damage(self.attack_power, array, pseudo_array)
                    elif code[0] == 'H':
                        code = code[1:len(code):1]
                        hut_list[int(code)].damage(self.attack_power, array, pseudo_array)
                    elif code[0] == 'C':
                        code = code[1:len(code):1]
                        canon_list[int(code)].damage(self.attack_power, array, pseudo_array)
                    elif code[0] == 'W':
                        code = code[1:len(code):1]
                        wall_list[int(code)].damage(self.attack_power,array, pseudo_array)
                    break

    def health_bar(self, array, pseudo_array):
        if self.health <= 0 and self.x_coor != 1000:
            old_X = self.x_coor
            old_Y = self.y_coor
            array[old_X][old_Y] = ' '
            pseudo_array[old_X][old_Y] = ' '
            self.x_coor = 1000
            self.y_coor = 1000
            self.attack_power = 0

        elif self.x_coor != 1000:
            if self.health < 0.2*gv.max_health_barbarians:
                self.color = Back.RED
            elif self.health < 0.5*gv.max_health_barbarians:
                self.color = Back.YELLOW

            array[self.x_coor][self.y_coor] = self.color + "B" + Style.RESET_ALL
            pseudo_array[self.x_coor][self.y_coor] = "B"
