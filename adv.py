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
opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}


def traversal(room):
    # scaffold the stuff
    # DFT but with a dict like Social
    stack = Stack()
    stack.push([room])
    visited = {} # dict like social.

    current_path = []
    
    def get_neighbors(node_id):
        rooms = []

        for direction in node_id.get_exits():
            path = node_id.get_room_in_direction(direction)
            
            if direction not in visited:
                visited[node_id.id][direction] = path.id
                if path:
                    current_path.append(direction)
                    rooms.append(path)
            else:
                current_path.append(opposites[direction])
        return rooms
    

    # spec mentions keeping track of rooms
    # using a dict format of room.id: [connections]

    # this means rooms are nodes, and directions are edges.
    while stack.size() > 0:
        player_path = stack.pop()
        player_room = player_path[-1]

        if player_room.id not in visited:
            visited[player_room.id] = {}

        for next_room in get_neighbors(player_room):
            stack.push([*player_path, next_room])
                
    return current_path


traversal_path = traversal(player.current_room)



# Recursion
# def traversal(room, visited=None):

#     if not visited:
#         visited = set()

#     current_path = []

#     visited.add(room.id)

#     # this is going to act as "get neighbors," basically
#     for direction in room.get_exits():
#         new_room = room.get_room_in_direction(direction)
#         print(new_room)

#         if new_room.id not in visited:
#             # recurse
#             new_path = traversal(new_room, visited)
#             print(new_path)
            
#             # if traversal returns something
#             if new_path:
#                 # create an array with the the direction string
#                 # and concat it with the new path array and
#                 # creates an array out of the strings in the opposites dict
#                 # at that direction
#                 make_path = [direction] + new_path + [opposites[direction]]
#             else:
#                 # if new path doesn't return anything, create an array out
#                 # of the direction strings
#                 # and whatever's in opposites at that direction
#                 make_path = [direction, opposites[direction]]
#             current_path = current_path + make_path
#     return current_path





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
    print(player.current_room.id)

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
