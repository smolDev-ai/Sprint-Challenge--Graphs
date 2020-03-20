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
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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

traversal_path = []

def traversal(graph, traversal_path):
    opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    
    # check will see if we have any questionmarks left in the visted rooms
    def check(graph):
        for key in graph:
            if '?' in graph[key].values():
                return True
        return False

    # Find_move takes the current room and figures out what the directions available are
    def find_move(visited_rooms, current):
        room_exits = visited_rooms[current.id]
        for direction in room_exits:
            if room_exits[direction] == '?' and current.get_room_in_direction(direction).id not in visited_rooms:
                return direction
        return None

    # find next room takes the current room and finds if any rooms connected
    # have a questionmark if they do we will add that direction to our path
    def find_next_room(stack, traversal_path, visited_rooms, current):
        while True:
            next_move = stack.pop()
            traversal_path.append(next_move)
            next_room = current.get_room_in_direction(next_move)
            # Removing values here creates a NoneType error
            if '?' in visited_rooms[next_room.id].values():
                return next_room.id
            current = next_room


    # Create our stack
    stack = Stack()
    # Add our starting room
    room_id = 0
    # Create a visited dict
    visited_rooms = {0: {}}
    # our current room
    player_room = world.rooms[room_id]
    # For loop that adds direction key and questionmark as a value to our starting room
    for direction in player_room.get_exits():
        visited_rooms[player_room.id][direction] = '?'
    # While loop that will check if we have visited the max number of rooms 
    # and that there are no questionmarks
    while len(visited_rooms) < len(world.rooms) and check(visited_rooms):
        # Update the current room
        player_room = world.rooms[room_id]
        # If current room has not been visited yet
        if player_room not in visited_rooms:
            # Add to visited
            visited_rooms[player_room.id] = {}
            # Get the direction key and ? as a value 
            for direction in player_room.get_exits():
                visited_rooms[player_room.id][direction] = '?'
        # Run find move to decide where to go next
        next_move = find_move(visited_rooms, player_room)
        # If next move == None we path to the next room with questionmarks in 
        # it still
        if not next_move:
            room_id = find_next_room(stack, traversal_path, visited_rooms, player_room)
        else:
            # If we have our next move then we will add that move to traversal
            traversal_path.append(next_move)
            # Update next room
            next_room = player_room.get_room_in_direction(next_move)
            # Add to visited rooms
            visited_rooms[room_id][next_move] = next_room.id
            # If the next room is not in visited
            if next_room.id not in visited_rooms:
                # Add to visited
                visited_rooms[next_room.id] = {}
                # Get exits and add direction as key and questionmark as value
                for direction in next_room.get_exits():
                    visited_rooms[next_room.id][direction] = '?'
            # Traverse back 
            visited_rooms[next_room.id][opposites[next_move]] = player_room.id
            stack.push(opposites[next_move])
            room_id = next_room.id


traversal(world, traversal_path)





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
