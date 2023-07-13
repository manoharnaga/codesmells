from telnetlib import GA
from colorama import Fore, Back, Style
import os
import json

from numpy import save
from src.input import Get, input_to
import src.movingchar as mc
import src.building as b
from src.building import gameBoard as Game_Map
import src.global_variable as gv
from src.initialise import Universal_array, townhall, hut_list, canon_list, wall_list
import time


if __name__ == "__main__":

    king = mc.king(2, 2, Game_Map.array, Game_Map.pseudo_array)
    barbarians = []
    barbarian_count = 0
    universal_iterator = 0
    replay = []
    timeout = 0.24

    while True:
        # Getting input from user
        input_time = time.time()

        os.system("clear")
        universal_iterator = universal_iterator + 1
        universal_iterator = universal_iterator % 100
        Game_Map.print_board()
        if king.health>0:
           king.health_bar(Game_Map.array, Game_Map.pseudo_array)
           print(king.health)
        
        # Nuke
        if(gv.Nuke == True and gv.Nuke_count == 0):
            print(Fore.LIGHTMAGENTA_EX+ "Nuke is launched" + Style.RESET_ALL)
            Nuke = mc.Nuke(int(gv.m/2), 3, Game_Map.array, Game_Map.pseudo_array)
            gv.Nuke_count += 1
        
        elif gv.Nuke == True and gv.Nuke_count == 1 and gv.Nuke_isdestroyed == False:
            Nuke.move(Game_Map.array, Game_Map.pseudo_array, Universal_array)
            print("Nuke is approaching the townhall")
        elif gv.Nuke_isdestroyed == True:
            print("Destruction Done\n")
            gv.Nuke_count += 1
            for i in range(gv.m):
                for j in range(gv.n):
                    if(Game_Map.pseudo_array[i][j] == "N"):
                        Game_Map.array[i][j] = " "
                        Game_Map.pseudo_array[i][j] = " "


        # spells-variables
        gv.Rage_step += 1
        if(gv.Rage_step == 25):
            gv.Rage_spell = False
            gv.Rage_step = 0
            if king.health > 0:
                king.attack_power = gv.attack_power_king
            for i in barbarians:
                if i.health > 0:
                    i.attack_power = gv.attack_power_barbarians
            timeout = 0.24


        # Health Bar
        for i in barbarians:
            i.health_bar(Game_Map.array, Game_Map.pseudo_array)

         # check game_ending:
        game_lost = Game_Map.game_lost(king, barbarians,barbarian_count)
        game_won = Game_Map.game_won(Universal_array)
        game_points = Game_Map.game_points(Universal_array)

        if(game_won == True or game_lost ==  True):
            if game_won:
                print(Fore.RED + "YOU WON, nice dude") 
            else :
                print(Fore.RED + "YOU LOST, koi baat nahi , sab ke liye nhi bna ye game")
            input_file = input("Save Game as: ")
            with open ("replays/" + input_file + ".json" ,'w')as outfile:
                json.dump(replay,outfile)
            break

        input_ = input_to(Get(), timeout)
        if(input_ == None):
            input_ = 'k'
        replay.append(input_)
        
        # Barbarian spawning
        barb_spawn = [(18,55), (2,17), (17,45)]
        if ((input_ == "1" or input_ == "2" or input_  == "3") and barbarian_count < 15):
            index = int(input_) - 1
            barbarians.append(mc.barbarians(barb_spawn[index][0],barb_spawn[index][1], Game_Map.array, Game_Map.pseudo_array, barbarian_count))
            barbarian_count += 1

        # quit game
        elif input_ == "q":
            input_file = input("Save Game as: ")
            with open ("replays/" + input_file + ".json" ,'w')as outfile:
                json.dump(replay,outfile)
                break
        
        # spells and nuke
        elif input_ == "h":
            if king.health > 0:
                king.health += 0.5*king.health
                king.health = min(king.health, 100)
            for i in barbarians:
                i.health += 0.5*i.health 
                i.health = min(i.health, gv.max_health_barbarians)
        elif input_ == "r":
            gv.Rage_spell = True
            gv.Rage_step = 0
            if king.health > 0:
                king.attack_power = int(1.5*king.attack_power) 
            for i in barbarians:
                if i.health > 0:
                    i.attack_power = int(1.5*i.attack_power)
            timeout /= 2
        elif input_ == 'n':
            gv.Nuke = True 


        # King Controls and attack
        if king.health>0:
            if input_ == "w" or input_ == "s" or input_ == "a" or input_ == "d":
                king.move(input_, Game_Map.array, Game_Map.pseudo_array)
            elif input_ == "-":
                king.damage(Game_Map.array, Game_Map.pseudo_array)
            elif input_ == " ":
                king.attack(Game_Map.array, Game_Map.pseudo_array)
            elif input_ == "l":
                king.leviathan(Game_Map.array, Game_Map.pseudo_array, Universal_array)

        # Barbarian Movement and attack
        for i in barbarians:
            i.bar_move(Game_Map.array, Game_Map.pseudo_array)
            i.attack(Game_Map.array, Game_Map.pseudo_array)
            if(i.health<=0):
                i.destroy(Game_Map.array, Game_Map.pseudo_array)

        # Canon attack
        for i in canon_list:
            if(universal_iterator%3 == 2):
                i.attack(Game_Map.array, Game_Map.pseudo_array, king, barbarians)
            if(universal_iterator%3 == 1):
                if(i.X_coor >0 and i.X_coor < gv.n and i.Y_coor > 0 and i.Y_coor < gv.m):
                    Game_Map.array[i.X_coor][i.Y_coor] = Fore.GREEN + 'C' + Style.RESET_ALL
            
