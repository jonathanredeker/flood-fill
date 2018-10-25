# Flood Fill
A Flood Fill pathfinding algorithm for 2D and 3D spaces.

## flood_fill.py

### To-do
- [x] Solve bug that allows the Node to traverse between two diagonally adjacent obstacles:
```
P - Player
O - Obstacle

[P][O]    [ ][O]
[O][ ] => [O][P]
```
- [ ] Allow the algorithm to check a non-rectangular/uneven map

## :rocket: flood_fill_3d.py
Let's visit another dimension! How about 3D space?

### To-do
- [ ] :bug: Solve bug in method Pathfinder.check_for_obstacle() that allows the Node to make illegal moves
- [x] Create 3D model to aid debugging
- [ ] Export Map.collision_map and Pathfinder.path to be imported by 3d_model.py
- [ ] Find a way to make Pathfinder.node_look() less bloated and more efficient
