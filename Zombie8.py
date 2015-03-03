"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._human_list = []
        self._zombie_list = []
        poc_grid.Grid.clear(self)

        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
        pass
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie
        #return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append([row,col])
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        #print entity_type
        height = self.get_grid_height()
        width = self.get_grid_width()
        
        visited = poc_grid.Grid(height, width)

        distance_field = [[height*width for dummy_col in range(width)] for dummy_row in range(height)]
      
        boundary = list(self._human_list) if entity_type == HUMAN else list(self._zombie_list) 


        
#       For cells in the bondary queue, 
#		initialize visited to be FULL and 
#		distance_field to be zero
        for cel in boundary:
            row, col = cel[0], cel[1]
            visited.set_full(row, col)
            distance_field[row][col] = 0
        
        #BFS loop
        while len(boundary)!=0: 
            current_cell  = boundary.pop(0)
#            print current_cell
            cell_row, cell_col = current_cell[0], current_cell[1]
    
            for neighbor in self.four_neighbors(cell_row, cell_col):
                neigh_row, neigh_col =neighbor[0],neighbor[1]  
                if visited.is_empty(neigh_row, neigh_col)==True:
                    #print "not in visited"
                    visited.set_full(neigh_row, neigh_col)
                    boundary.append(neighbor)
#                    print "boundary:, "
#                    print boundary
                    
                    #in addition, update the neighbor's distance
                    #to be the minimum of its own distance
                    #nd the distance to current_cell plus one
                    current_distance = distance_field[cell_row][cell_col]
                    neighbor_distance = distance_field[neigh_row][neigh_col]
                    distance = min([(current_distance+1), neighbor_distance])

                    distance_field[neigh_row][neigh_col] = distance
   
#                    cur_distance =min([current_distance, neighbor_distance+1])
#                    distance_field[cell_row][cell_col] = cur_distance
                    
                               
        return  distance_field
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
      
        for cell in  self._human_list:
            cell_row, cell_col = cell[0], cell[1]
            #neighbors = [neighbor for neighbor in self.eight_neighbors(cell_row, cell_col)]
            #print neighbors
            cell_to_move = [cell, zombie_distance[cell_row][cell_col]]
            
            for neighbor in  self.eight_neighbors(cell_row, cell_col):
                neigh_row, neigh_col =neighbor[0],neighbor[1]
                if self.is_empty(neigh_row, neigh_col)!=EMPTY:
                    if zombie_distance[neigh_row][neigh_col] >cell_to_move[1]:
                        cell_to_move = [neighbor, zombie_distance[neigh_row][neigh_col]]
            cell_location = self._human_list.index(cell)
            self._human_list[cell_location] = cell_to_move[0]
            
 
            
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for cell in  self._zombie_list:
            cell_row, cell_col = cell[0], cell[1]
            

            cell_to_move = [cell, human_distance[cell_row][cell_col]]
            
            for neighbor in  self.eight_neighbors(cell_row, cell_col):
                neigh_row, neigh_col =neighbor[0],neighbor[1]
                if self.is_empty(neigh_row, neigh_col)!=EMPTY:
                    if human_distance[neigh_row][neigh_col] < cell_to_move[1]:
                        cell_to_move = [neighbor, human_distance[neigh_row][neigh_col]]
            cell_location = self._zombie_list.index(cell)
            self._zombie_list[cell_location] = cell_to_move[0]
    
    
def run_test():
    """
    Function to test zombie class
    """
    grid_height =4
    grid_width = 4
    zombies = Zombie(grid_height, grid_width)
    #zombies.add_zombie(1,1)
    #zombies.add_zombie(3,3)
    zombies.add_zombie(0,0)

    print zombies.num_zombies()
    for zombie in zombies.zombies():
        print zombie
    print type(zombies)
    
    
    zombies.add_human(3,3)
    zombies.add_human(2,2)
    
    print zombies.num_humans()
    for human in zombies.humans():
        print human
        
   
        
    zombie_distance_field =  zombies.compute_distance_field(ZOMBIE)    
    print "zombie_distance_field"
    for row in zombie_distance_field:
        print row
        
    human_distance_field =  zombies.compute_distance_field(HUMAN)        
    print "human_distance_field"
    for row in human_distance_field:
        print row
    
    zombies.move_humans(zombie_distance_field) 
    zombies.move_zombies(human_distance_field) 
    
run_test()    

# Start up gui for simulation - You will need to write some code above
# before this will work without errors
z = [(4,4), (2,2)]
x = [(0,0), (5,5)]
poc_zombie_gui.run_gui(Zombie(30, 40, None, x,z))
