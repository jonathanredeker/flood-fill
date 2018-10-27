import json

class Map:
    """A 3D map to test our program on"""
    def __init__(self):
        """
        0 - Free-space
        1 - Obstacle
        2 - Goal
        """
        self.collision_map = [[[2,0,0,0,0],
                               [0,0,0,0,0],
                               [0,0,1,0,0],
                               [0,0,0,0,0]],
                              [[0,0,0,0,0],
                               [0,0,1,0,0],
                               [0,1,0,1,0],
                               [0,0,1,0,0]],
                              [[0,0,0,0,0],
                               [0,0,0,0,0],
                               [0,0,0,0,0],
                               [0,0,0,0,0]]]

        self.length = len(self.collision_map[0][0])
        self.width = len(self.collision_map[0])
        self.height = len(self.collision_map)

    def get_element(self, position):
        """Returns the element from a coordinate on the collision_map"""
        return self.collision_map[position[2]][position[1]][position[0]]

class Node():
    """These Nodes will spread throughout the map and collect the coordinates
       for our path"""
    def __init__(self, parent, position):
        self.path = []
        self.parent = parent
        self.position = position

        # If the Node has a parent, then it will inherit all coordinates from
        # the parent's path.
        if self.parent != None:
            for coordinate in parent.path:
                self.path.append(coordinate)

        # Append the Node's position to the path
        self.path.append(self.position)

class Pathfinder():
    """This is our pathfinding class that will search for and return the
       requested path"""
    def __init__(self, map):
        self.path = []
        self.checked_steps = []
        self.queued_nodes = []
        self.closed_nodes = []
        self.map = map
        self.solved = False

    def search(self, start):
        """The main loop that iterates through each possible step"""
        # Store our start as a part of the object
        self.start = start

        # Queue initial node and  add to checked steps list
        self.queue_node(None, self.start)
        self.check_step(self.start)

        # While our list of queued_nodes is not empty and hasn't reached
        # the goal
        while self.queued_nodes != [] and self.solved == False:

            # Set current_node to the first node in the queued_nodes list
            self.current_node = self.queued_nodes[0]

            # We want to check each of the 26 positions around the node
            for direction in range(26):

                # Node looks at a step in the given direction
                step = self.node_look(direction)

                # If the step is real (not out-of-bounds), else move on to next
                # node
                if self.step_is_real(step):

                    # If check if the step has already been analyzed, else move
                    # on to the next node
                    if self.step_is_checked(step) == False:

                        # If there are no collisions between Node position and
                        # then step, else move on to the next node
                        if self.check_for_collision(self.current_node.position,\
                        step, direction) == False:

                            # Queue new node, pass current node as the parent of
                            # the next node
                            self.queue_node(self.current_node, step)

                            # If our step is the goal
                            if self.step_is_goal(step):

                                # Return path self.current_node.path
                                self.solved = True
                                self.current_node.path.append(step)
                                return self.current_node.path

            # Close the node by popping it from the queued_nodes list and adding
            # it to the closed_nodes list
            self.close_node()

        # We could not reach the goal, therefore return an empty path
        return []

    def node_look(self, direction):
        """The Node looks in a certain direction and returns its coordinate.
           It searches each layer of its surrounding cube clock-wise,
           starting from 12-o-clock."""
        # Create a coordinate for the Node to check
        step = self.current_node.position
        # For z = -1, relative to the Node
        if direction == 0:
            # [x, y, z - 1]
            return [step[0], step[1], step[2] - 1]
        elif direction == 1:
            # [x, y - 1, z - 1]
            return [step[0], step[1] - 1, step[2] - 1]
        elif direction == 2:
            # [x + 1, y - 1, z - 1]
            return [step[0] + 1, step[1] - 1, step[2] - 1]
        elif direction == 3:
            # [x + 1, y, z - 1]
            return [step[0] + 1, step[1], step[2] - 1]
        elif direction == 4:
            # [x + 1, y + 1, z - 1]
            return [step[0] + 1, step[1] + 1, step[2] - 1]
        elif direction == 5:
            # [x, y + 1, z - 1]
            return [step[0], step[1] + 1, step[2] - 1]
        elif direction == 6:
            # [x - 1, y + 1, z - 1]
            return [step[0] - 1, step[1] + 1, step[2] - 1]
        elif direction == 7:
            # [x - 1, y, z - 1]
            return [step[0] - 1, step[1], step[2] - 1]
        elif direction == 8:
            # [x - 1, y - 1, z - 1]
            return [step[0] - 1, step[1] - 1, step[2] - 1]
        # For z = 0, relative to the Node
        elif direction == 9:
            # [x, y - 1, z]
            return [step[0], step[1] - 1, step[2]]
        elif direction == 10:
            # [x + 1, y - 1, z]
            return [step[0] + 1, step[1] - 1, step[2]]
        elif direction == 11:
            # [x + 1, y, z]
            return [step[0] + 1, step[1], step[2]]
        elif direction == 12:
            # [x + 1, y + 1, z]
            return [step[0] + 1, step[1] + 1, step[2]]
        elif direction == 13:
            # [x, y + 1, z]
            return [step[0], step[1] + 1, step[2]]
        elif direction == 14:
            # [x - 1, y + 1, z]
            return [step[0] - 1, step[1] + 1, step[2]]
        elif direction == 15:
            # [x - 1, y, z]
            return [step[0] - 1, step[1], step[2]]
        elif direction == 16:
            # [x - 1, y - 1, z]
            return [step[0] - 1, step[1] - 1, step[2]]
        # For z = 1, relative to the Node
        elif direction == 17:
            # [x, y, z + 1]
            return [step[0], step[1], step[2] + 1]
        elif direction == 18:
            # [x, y - 1, z + 1]
            return [step[0], step[1] - 1, step[2] + 1]
        elif direction == 19:
            # [x + 1, y - 1, z - 1]
            return [step[0] + 1, step[1] - 1, step[2] + 1]
        elif direction == 20:
            # [x + 1, y, z + 1]
            return [step[0] + 1, step[1], step[2] + 1]
        elif direction == 21:
            # [x + 1, y + 1, z + 1]
            return [step[0] + 1, step[1] + 1, step[2] + 1]
        elif direction == 22:
            # [x, y + 1, z + 1]
            return [step[0], step[1] + 1, step[2] + 1]
        elif direction == 23:
            # [x - 1, y + 1, z + 1]
            return [step[0] - 1, step[1] + 1, step[2] + 1]
        elif direction == 24:
            # [x - 1, y, z + 1]
            return [step[0] - 1, step[1], step[2] + 1]
        elif direction == 25:
            # [x - 1, y - 1, z + 1]
            return [step[0] - 1, step[1] - 1, step[2] + 1]

    def queue_node(self, node, position):
        """Append an instance of the Node class to our open_nodes list"""
        self.queued_nodes.append(Node(node, position))

    def close_node(self):
        """Pop the current Node and append it to closed_nodes"""
        self.closed_nodes.append(self.queued_nodes.pop(0))

    def step_is_real(self, step):
        """Check if the step is out-of-bounds"""
        if step[2] < 0 or step[2] > self.map.height - 1:
            return False
        elif step[1] < 0 or step[1] > self.map.width - 1:
            return False
        elif step[0] < 0 or step[0] > self.map.length - 1:
            return False
        else:
            return True

    def check_step(self, step):
        """Add the given step to our list of checked steps to prevent
           redundant checks"""
        self.checked_steps.append(step)

    def step_is_checked(self, step):
        """Check if step is in checked_steps. If not, add it to the list"""
        if step in self.checked_steps:
            return True
        else:
            self.check_step(step)
            return False

    def check_for_collision(self, position, step, direction):
        """Check if there is a collision between position and step"""
        if self.map.get_element(step) == 1:
            return True
        else:
            # We are checking to see if we illegally cross through a surface
            # created with the points of the obstacles between the Node's
            # position and its step.
            if (direction > 0 and direction < 9) or direction > 16:
                obstacle_p1 = [step[0], position[1], position[2]]
                obstacle_p2 = [position[0], step[1], position[2]]
                obstacle_p3 = [position[0], position[1], step[2]]
                obstacle_p4 = [step[0], step[1], position[2]]
                if (self.map.get_element(obstacle_p1) == 1 \
                and self.map.get_element(obstacle_p2) == 1 \
                and self.map.get_element(obstacle_p3) == 1) \
                or (self.map.get_element(obstacle_p3) == 1 \
                and self.map.get_element(obstacle_p4) == 1):
                    return True
            # We are checking to see if the Node is passing between two
            # obstacles diagonally on the Node's z-axis.
            elif (direction > 8 and direction < 17) and direction % 2 == 0:
                obstacle_p1, obstacle_p2 = [position[0], step[1], position[2]],\
                [step[0], position[1], position[2]]

                if self.map.get_element(obstacle_p1) == 1 and self.map.get_element(obstacle_p2) == 1:
                    return True

            return False

    def step_is_goal(self, step):
        """Checks if the map element at the given position is the goal value"""
        if self.map.get_element(step) == 2:
            return True
        else:
            return False

# Instantiate Map() and Pathfinder()
map = Map()
pathfinder = Pathfinder(map)

# Search starting from the coordinate [x, y, z]
path = pathfinder.search([2, 2, 1])

# Store the collision map and path as json
data = json.dumps({"map": map.collision_map, "path": path})

# Write the data to a json file for 3d_model.py to interpret
with open("flood_fill_3d.json", "w") as file:
    file.write(data)
    print "\n\tData saved to flood_fill_3d.json\n"

# - - - - - - - - - - - - - - Print Demonstration - - - - - - - - - - - - - - #

print "\t" + str(path)
if len(path):
    print "\tTotal steps to goal:", str(len(path) - 1), "\n"
else:
    print "\tTotal steps to goal: 0"
