from src.building import Townhall, Wall, Huts, Canon
import src.global_variable as gv

Universal_array = []
count = 0

townhall_list = [] 
hut_list = [] 
canon_list = []
wall_list = []

#TownHall
townhall = Townhall(0)
townhall_list.append(townhall)

#Huts
hut_coordinates = [(6, 13), (14, 23), (8, 25), (14, 43), (6, 38)]
for i in range(0, len(hut_coordinates)):
    hut_list.append(Huts(hut_coordinates[i][0],hut_coordinates[i][1], i))

#Canon
canon_coordinates = [(6, 25), (12, 45)]
for i in range(0, len(canon_coordinates)):
    canon_list.append(Canon(canon_coordinates[i][0], canon_coordinates[i][1], i))

#Wall
for i in [int(gv.m/5), int(4*gv.m/5)]:
    for j in range(int(gv.n/5), int(4*gv.n/5)+1):
        wall_list.append(Wall(i, j, count))
        count += 1

for j in [int(gv.n/5), int(4*gv.n/5)]:
    for i in range(int(gv.m/5)+1, int(4*gv.m/5)):
        wall_list.append(Wall(i, j, count))
        count += 1

Universal_array.extend([townhall_list, hut_list, canon_list, wall_list])

