import numpy as np
import time as time
import pickle

def move_up(config):
    return config[0:4] + config[7] + config[4:7] + config[8:12] + config[15] + config[12:15]

def move_front(config):
    x1 = (int(config[10]) + 2) % 3
    x2 = (int(config[14]) + 1) % 3
    x6 = (int(config[15]) + 2) % 3
    x7 = (int(config[9]) + 1) % 3
    return config[0] + config[2] + config [6] + config[3:6] + config[7] + config [1] + config[8] + str(x1) + str(x2) + config[11:14] + str(x6) + str(x7)

def move_right(config):
    x2 = (int(config[11]) + 2) % 3
    x3 = (int(config[13]) + 1) % 3
    x5 = (int(config[14]) + 2) % 3
    x6 = (int(config[10]) + 1) % 3
    return config[0:2] + config[3] + config[5] + config[4] + config[6] + config[2] + config[7:10] + str(x2) + str(x3) + config[12] + str(x5) + str(x6) + config[15]

# def basic_moves(node):
#     return {'U1' : move_up(node), 'U2': move_up(move_up(node)), 'U3': move_up(move_up(move_up(node))), 'F1':move_front(node), 'F2' : move_front(move_front(node)), 'F3' : move_front(move_front(move_front(node))), 'R1' : move_right(node), 'R2' : move_right(move_right(node)), 'R3' : move_right(move_right(move_right(node)))}

def basic_moves(node):
    return {'U1' : move_up(node), 'U2': move_up(move_up(node)), 'U3': move_up(move_up(move_up(node))), 'F1':move_front(node), 'F2' : move_front(move_front(node)), 'F3' : move_front(move_front(move_front(node)))}

def record(unexplored, visited, equivalence, diameter_count):
    node = unexplored.pop(0)
    diameter = visited[node][2]
    diameter_count[int(diameter)] = diameter_count[int(diameter)] + 1
    next_configs = basic_moves(node)
    for edge in next_configs:
        if visited.get(next_configs[edge]) == None:
            visited[next_configs[edge]] = (node, edge, diameter+1)
            unexplored.append(next_configs[edge])
        else:
            equivalence.append((next_configs[edge],(node, edge, diameter+1)))
    return diameter, diameter_count


def init_dict():
    return {'0123456700000000' : ("", "", 0)}, ['0123456700000000']

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, 0)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


# MAIN RUN

print("2-Generator group G=<U,F>")
print("")

# explored = {}
visited, unexplored = init_dict()
# unexplored = ['0123456700000000', '0123745600000000', '0263457102100021', '0123745600000000', '0263457102100021']
equivalence = []
timings = []
diameter_count = np.zeros(20,  np.int32)

n=0
start = time.time()
# goal = 3674160 # G=<U,F,R>
goal = 29160 # G=<U,F>
checkpoint = goal/10

# while n < goal:
while len(unexplored) > 0:
    diameter, diameter_count = record(unexplored, visited, equivalence, diameter_count)

    if n % checkpoint == 0:
        print (str((n//checkpoint)*10) + "% complete")
        runtime = round(time.time() - start,2)
        timings.append(runtime)
        print ("Runtime: " + str(runtime) + " sec(s)" )
    n += 1

runtime = time.time() - start
timings.append(runtime)
print ("Diameter: " + str(diameter))
print (diameter_count)
print (sum(diameter_count))
print ("Number of Configs: " + str(n))
print ("Remaining no. of Configs: " + str(goal - n))
print ("Nodes visited: " + str(len(visited)))
print ("Total explored: " + str(len(visited) - len(unexplored)))
# print (equivalence[0:10])
print ("Timings:")
print (timings)
print ("Runtime: " + str(runtime))

# save_obj(explored, "explored")
save_obj(diameter_count, "diameter_count")
save_obj(timings, "timings")
save_obj(equivalence, "equivalence")
save_obj(visited, "visited")




# TESTS

# config = "0124763501210200"
# if move_up(config) == "0124576301210200":
#     print ("UP Correct")
# else:
#     print ("UP WRONG !!!!")
#
# config = "0123456700000000"
# if move_front(config) == "0263457102100021":
#     print("FRONT Correct")
# else:
#     print("FRONT WRONG !!!!")
#
# config = "0263457102100021"
# if move_right(config) == "0235476102210121":
#     print("RIGHT Correct")
# else:
#     print("RIGHT WRONG !!!!")
