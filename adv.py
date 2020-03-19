from room import Room
from player import Player
from world import World

from util import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# basic Idea behind my solution:
# use room.get_exits() and
# room.get_room_in_direction()
# to find all available untraversed rooms.

# I know we're going to need an opposites dict to move backwards, though I'm not super sure why. Late night brain is unhelpful.

# using DFT to traverse all nodes, with an extra path variable to pass letters to if thei rooms exit it marked with a question mark somehow

def traversal(room, visited=None):
    opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    # # scaffold the stuff
    # # DFT but with a dict like Social
    # stack = Stack()
    # stack.push([room])
    # visited = {} # dict like social.

    # current_path = []
    
    # def get_neighbors(node_id):
    #     rooms = []

    #     for direction in node_id.get_exits():
    #         if node_id.get_room_in_direction(direction):
    #             current_path.append(direction)
    #             rooms.append(node_id.get_room_in_direction(direction))
    #         else:
    #             current_path.append(opposites[direction])

    #         # path = node_id.get_room_in_direction(direction)

    #         # if path:
    #         #     # print(f"{current_path}")
    #         #     
    #         # # if deadend
    #         # else:
    #         #     print('hit else')
    #         #     current_path.append(opposites[direction])
    #         #     print(current_path)
    #     return rooms
    

    # # spec mentions keeping track of rooms
    # # using a dict formate of room.id: [connections]

    # # this means rooms are nodes, and directions are edges.
    # while stack.size() > 0:
    #     player_path = stack.pop()
    #     player_room = player_path[-1]

    #     if player_room.id not in visited:
    #         visited[player_room.id] = player_path

    #         for next_room in get_neighbors(player_room):
    #             stack.push([*player_path, next_room])
                
    # return current_path


traversal_path = traversal(player.current_room)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



# #######
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
