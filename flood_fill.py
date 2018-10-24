class Map:
    """Just a basic map to test our program on"""
    def __init__(self):
        """
        0 - Free-space
        1 - Obstacle
        2 - Goal
        """
        self.collision_map = [[2,1,0,0,0],
                              [0,1,1,0,0],
                              [0,0,1,0,0],
                              [1,0,0,0,0]]
        self.width = len(self.collision_map[0])
        self.height = len(self.collision_map)

    def get_element(self, position):
        return self.collision_map[position[1]][position[0]]

    def _print(self, path):
        """Print maps for demonstration"""
        map = "\n\n\n"
        for i in range(len(self.collision_map)):
            map += "\t"
            for j in range(len(self.collision_map[i])):
                map += str(self.collision_map[i][j]) + "  "
            map += "\n\n"
        for point in path:
            a = point[1]
            b = point[0]
            self.collision_map[a][b] = "@"
        for i in range(len(self.collision_map)):
            for j in range(len(self.collision_map[i])):
                if self.collision_map[i][j] == 0:
                    self.collision_map[i][j] = " "
                elif self.collision_map[i][j] == 1:
                    self.collision_map[i][j] = "."
        map += "\n\n\n"
        for i in range(len(self.collision_map)):
            map += "\t"
            for j in range(len(self.collision_map[i])):
                map += str(self.collision_map[i][j]) + "  "
            map += "\n\n"

        print map

class Node():
    """These Nodes will spread throughout the map"""
    def __init__(self, parent, position):
        self.path = []
        self.parent = parent
        self.position = position

        # If the Node's parent is not equal to None, then it will
        # inherit all coordinates from the parent's path.
        if self.parent != None:
            for coordinate in parent.path:
                self.path.append(coordinate)

        # Append the Node's position to the path
        self.path.append(self.position)

class Pathfinder():
    """This is our pathfinding class that will search for and return the requested path."""
    def __init__(self, map, start):
        self.path = []
        self.checked_steps = []
        self.queued_nodes = []
        self.closed_nodes = []
        self.map = map
        self.start = start
        self.solved = False

    def search(self):
        self.queue_node(None, self.start)
        self.check_step(self.start)

        while self.queued_nodes != [] and self.solved == False:

            self.current_node = self.queued_nodes[0]

            for direction in range(8):

                step = self.move_node(direction)

                if self.step_is_real(step):

                    if self.step_is_checked(step) == False:

                        if self.step_is_obstacle(self.current_node.position, step, direction) == False:

                            # Queue new node
                            self.queue_node(self.current_node, step)

                            if self.step_is_goal(step):
                                # Return path self.current_node.path
                                self.solved = True
                                self.current_node.path.append(step)
                                return self.current_node.path

            self.close_node()

        # We could not reach the goal, therefore return an empty path
        return []

    def move_node(self, direction):
        step = self.current_node.position
        # Node searches clock-wise
        if direction == 0:
            # [x, y - 1]
            return [step[0], step[1] - 1]
        elif direction == 1:
            # [x + 1, y - 1]
            return [step[0] + 1, step[1] - 1]
        elif direction == 2:
            # [x + 1, y]
            return [step[0] + 1, step[1]]
        elif direction == 3:
            # [x + 1, y + 1]
            return [step[0] + 1, step[1] + 1]
        elif direction == 4:
            # [x, y + 1]
            return [step[0], step[1] + 1]
        elif direction == 5:
            # [x - 1, y + 1]
            return [step[0] - 1, step[1] + 1]
        elif direction == 6:
            # [x - 1, y]
            return [step[0] - 1, step[1]]
        elif direction == 7:
            # [x - 1, y - 1]
            return [step[0] - 1, step[1] - 1]

    def queue_node(self, node, position):
        """Append an instance of the Node class to our open_nodes list"""
        self.queued_nodes.append(Node(node, position))

    def close_node(self):
        """Pop the current Node and append it to closed_nodes"""
        self.closed_nodes.append(self.queued_nodes.pop(0))

    def step_is_real(self, step):
        """Check if the step is out-of-bounds"""
        if step[1] < 0 or step[1] > self.map.height - 1:
            return False
        elif step[0] < 0 or step[0] > self.map.width - 1:
            return False
        else:
            return True

    def check_step(self, step):
        self.checked_steps.append(step)

    def step_is_checked(self, step):
        """Check if step is in checked_steps. If not, add it to the list."""
        if step in self.checked_steps:
            return True
        else:
            self.check_step(step)
            return False

    def step_is_obstacle(self, position, step, direction):
        """Check if the step an obstacle"""
        if self.map.get_element(step) == 1:
            return True
        else:
            """Checks for diagonal obstacles between Node's position and the requested step"""
            if direction % 2:
                obstacle_x, obstacle_y = [position[0], step[1]], [step[0], position[1]]
                if self.map.get_element(obstacle_x) == 1 and self.map.get_element(obstacle_y) == 1:
                    return True
            return False

    def step_is_goal(self, step):
        if self.map.get_element(step) == 2:
            return True
        else:
            return False

map = Map()
pathfinder = Pathfinder(map, [4,3])
path = pathfinder.search()

# Print demonstration
map._print(path)
print path
if len(path):
    print "Total steps to goal:", str(len(path) - 1), "\n"
else:
    print "Total steps to goal: 0"
