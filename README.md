# Pathfinding-Visualizer
<img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/dijstra_demo.gif"  width="550" height="550"> <br>
This project was my final assignment for the Data Structure course at university. The program was made using Python, 
mainly utilizing the Pygame library. Initially, the base of this project was inspired by a YouTube video by max on tech. 
The link for the video and the code source will be provided at the end. <br>

## Technologies
- Language: Python 3.11
- Library used: Pygame, tkinter
- Data Structures: Graph, Stack, Queue

## Algorithms
The algorithms that can be displayed using this Pathfinding Visualizer program are as follows:
1. Breadth-First-Search
2. Dijkstra
3. Depth-First-Search

## Features <br>
Below, I will describe each feature of the Pathfinding Visualizer along with the explanation and the data structure used. <br>
* Main Menu <br>
  The main menu is quite simple, constructed with 3 buttons that lead the user to the Dijkstra page, the DFS page, and to Quit the program. <br>
  <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/main.gif"  width="300" height="300"> <br>
* Set Start Node<br>
  Users can set the starting node by pressing the [S] button using the computer mouse and choosing the desired grid. <br>
  Instead of using the mouse, users can perform the same action using the "S" keyboard input. <br>
  <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/start.gif"  width="300" height="300"> <br>
* Set End Node (Target)<br>
  Users can set the target node by pressing the [E] button using the computer mouse and choosing the desired grid. <br>
  Instead of using the mouse, users can perform the same action using the "E" keyboard input.<br>
  <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/end.gif"  width="300" height="300"> <br>
* Add/ Remove Wall(s)<br>
  Users have the option to create or remove walls to block certain grids, preventing exploration.
  * Adding wall(s) <br>
    Users can add wall(s) by pressing the [W] button using the computer mouse and choosing the desired grid. <br>
    Instead of using the mouse, users can perform the same action using the "W" keyboard input.<br>
    <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/add wall.gif"  width="300" height="300"> <br>
  * Removing wall(s) <br>
    Users can set the starting node by pressing the [W] button twice using the computer mouse and choosing the wall(s) to remove. <br>
    Instead of using the mouse, users can perform the same action using the "W" keyboard input. <br>
    The [W] button will turn red, indicating the action performed is "removing walls" and not "adding walls"<br>
    <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/remove wall.gif"  width="300" height="300"> <br>
* Clear the Grid<br>
  Users have the option to reset the start node, end node, walls, weights, and neighbors by pressing the "C" keyboard input. <br>
  <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/clear.gif"  width="300" height="300"> <br>
* Set Weight for Each Node<br>
  Users can add weight to a node to make the exploration process longer on that certain node. The point of this is to represent
  the dynamic of all the possible paths. It will create a traffic jam situation in certain areas.<br><br>
  <b>Here's how users can add weight:</b>
  1. Click on the type field below the weight button/ press the "Tab" keyboard input
  2. Type the desired weight, ranging from 1-99. (1 is the default weight of each node)
  3. Click the [weight] button above the type field/ press the "B" keyboard input
  4. Choose all the node(s) to apply that weight <br><br>
  Comparison between running with and without weight(s):
  * Without weight(s)<br>
  <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/run no weight.gif"  width="300" height="300"> <br>
  * With weight(s)<br>
  <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/run with weight.gif"  width="300" height="300"> <br>
* Set Neighbours<br>
  Users have the option to set the freedom to which neighbor(s) a node can explore. <br><br>

  To turn on/off each node neighbor, users can click on the dark green node on the right-bottom. The light green node represents
  the current node and the dark green nodes represent the allowed neighbor(s) to explore. If the node is turned red, it means
  that each node cannot explore there from their current location.
  <br><br>

  There will be differences in the path taken if the neighbors are modified. The example can be seen below:
  * The diagonal neighbors turned on<br>
  <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/run all neighbours.gif"  width="300" height="300"> <br>
  * The diagonal neighbors turned off <br>
  <img src="https://github.com/GaTheLy/Pathfinding-Visualizer/blob/main/assets/run no weight.gif"  width="300" height="300"> <br>


