# -*- coding: utf-8 -*-
"""
Created on Nov 12 16:53:28 2024


Program that splits .swc files with multiple somas 
into separate .swc files in O(n) time
and generates an equivalent OBJ file (lines) using navis (https://navis-org.github.io/navis/)

@author: Kakolla, jmbouteiller
"""


import neurom
from convert_SWC_to_OBJ_line import convert_to_obj
from convert_SWC_to_OBJ_navis import convert_to_obj_navis

# morphology = neurom.load_morphology('retinal_cells/output1.swc')


file = open("retinal_cells.swc")

# enums for readability
id = 0
type = 1
x = 2
y = 3
z = 4
radius = 5
parent = 6

class Cell:
    next = None
    prev = None

    def __init__(self, id, type, pos, radius, parent):
        self.id = id
        self.type = type
        self.pos = pos
        self.radius = radius
        self.parent = parent


parents = []

children_map = {} # store list of child ids
all_cells = {}
line = []

# parsing
for l in file:
    line = l.split()
    
    if (line[id] == '#'): # skip comment lines
        continue
    for m in range(len(line)):
        line[m] = float(line[m]) # convert all strings to floats
    
    c = Cell(int(line[id]), int(line[type]), [line[x], line[y], line[z]], line[radius], int(line[parent]))
    all_cells[c.id] = c # make id point to the cell

    if (c.parent != -1):
        if c.parent not in children_map:
            children_map[c.parent]= [] # initialize an empty list if it wasn't there
        children_map[c.parent].append(c.id) # add a new child to the list of children 


    else:
        # if this cell is a parent (soma)
        parents.append(c)
        children_map[c.id] = [] # initialize soma's children as empty for now


# branching out from individual parent somas
parent_count = 0
for elem in parents:
    output = open(f"retinal_cells/output{parent_count+1}.swc", "w")
    output.write("# sample, type, x, y, z, radius, parent\n")
    print(elem.id)

    # write soma cell info first
    soma_info = f"{elem.id} {elem.type} {' '.join(map(str, elem.pos))} {elem.radius} -1\n"
    output.write(soma_info)

    stack = [elem] # stack to stimulate Depth First Search to handle bifurcating / expanding children
    num_neurites = 0
    while (stack):
        curr_cell = stack.pop()

        # catch if the cell is a soma that has no children
        if curr_cell.id not in children_map or not children_map[curr_cell.id]:
            continue

        
        # iterate over each child of the current child
        for child_id in children_map[curr_cell.id]:
            child_cell = all_cells[child_id]

            # write child cell information
            child_info = f"{child_cell.id} {child_cell.type} {' '.join(map(str, child_cell.pos))} {child_cell.radius} {curr_cell.id}\n"
            output.write(child_info)  # Write to file

            # add the child cell to the stack to continue traversal
            stack.append(child_cell)
            num_neurites += 1
        
    print(" Number of Neurites: " + str(num_neurites))

    # check if the swc file is just 1 point (can't make an obj)
    if (num_neurites > 1):
        # convert to obj (line only)
        #convert_to_obj(f"./retinal_cells/output{parent_count+1}.swc", f"./retinal_cells_obj/output{parent_count+1}.obj")
        # convert to obj (mesh)
        convert_to_obj_navis(f"./retinal_cells/output{parent_count+1}.swc", f"./retinal_cells_obj/output{parent_count+1}.obj")

    parent_count += 1
    output.close()
