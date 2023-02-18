from pickle import FALSE, TRUE
import math
import random
import pygame
import pymunk
from variables_and_functions import *


class Buoy:
    """Class responsible to represent each buoy"""
    deepness_detection = {50:34, 100:69.4, 150:103.4, 200:139} #key is the deepness and the item is the diameter of detection

    #initialization method of each buoy
    #Parameters:
                #location-location of the center of the buoy
                #space- space to represent the environment and allow to add the bodies to the environment using pymunk

    def __init__(self, location, space):
        self.location = location
        self.body = pymunk.Body()
        self.body.position = location
        self.shape = pymunk.Circle(self.body, 20)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = 1
        space.add(self.body, self.shape)
        self.shape.sensor = True

        self.body2 = pymunk.Body()
        self.body2.position = location
        self.shape2 = pymunk.Circle(self.body2, 14)
        self.shape2.elasticity = 1
        self.shape2.density = 1
        self.shape2.collision_type = 2
        space.add(self.body2, self.shape2)
        self.shape2.sensor = True

        self.body3 = pymunk.Body()
        self.body3.position = location
        self.shape3 = pymunk.Circle(self.body3, 7)
        self.shape3.elasticity = 1
        self.shape3.density = 1
        self.shape3.collision_type = 3
        space.add(self.body3, self.shape3)
        self.shape3.sensor = True

        #Shapes tagged as sensors (Shape.sensor == true) never generate collisions that get processed, 
        # so collisions between sensors shapes and other shapes will never call the post_solve() callback. 
        # They still generate begin(), and separate() callbacks, and the pre_solve() callback is also called 
        # every frame even though there is no collision response.
        
        self.detect = 0


class Buoys_group:
    """Class responsible to represent each arrangement/pattern of buoys"""
    Buoys_set = []
    #initialization method of each pattern of buoys
    #Parameters:
                #pattern- it's a number and represents the system pattern which will be used(The values correspond to: 1 = Circle Pattern, 2 = Cross Pattern, 3 = Jail Pattern)
                #center-  center of the arrangement of buoys.
                #area_covered- area covered by the arrangement
    def __init__(self, pattern, center, area_covered):
        self.pattern = pattern
        self.area = area_covered
        self.center = center
        
  
    #This method builds the square border which every patterns contains.
    #Parameters:
                #self- object representative of the whole pattern
                #space- space to represent the environment space and allow to add the bodies to the environment using pymunk
    def square_structure(self, space):
        #first we define the size of each square side
        side_size=math.sqrt(self.area)
        buoys_between_vertices = 5 #this will be changed with the real simulations
        #then we define the vertices location
        vertices_location = [(self.center[0]-side_size/2, self.center[1]-side_size/2), (self.center[0]-side_size/2, self.center[1]+side_size/2),
        (self.center[0]+side_size/2, self.center[1]+side_size/2), (self.center[0]+side_size/2, self.center[1]-side_size/2)]
        print("LOCAL:", vertices_location)
        print(self.center)
        for i in range(4):
            self.Buoys_set.append(Buoy(vertices_location[i], space))

        #now we will have to append the full square
        for index in range(4):  
            vertice_init = vertices_location[index]
            if(index!=3): vertice_end = vertices_location[index+1]
            else : vertice_end = vertices_location[0]

            if (vertice_init[0] == vertice_end[0]): side ="vertical"
            else: side = "horizontal"
            if(side == "vertical"):
                buoy_space = (vertice_end[1]-vertice_init[1])/buoys_between_vertices
                if(buoy_space < 0):direction = -1
                else: direction = 1
                #print(index, direction)
                actual_buoy = buoys_coordinates(vertice_init, 0, buoy_space)
                while(direction*actual_buoy[1] < vertice_end[1]*direction):
                    #print(index)
                    #in the same vertical side, all the boyes will have the same x.
                    #we only need to change y
                    self.Buoys_set.append(Buoy(actual_buoy,space))
                    actual_buoy=buoys_coordinates(actual_buoy,0,buoy_space)
                    
            else:
                buoy_space = (vertice_end[0]-vertice_init[0])/buoys_between_vertices
                if(buoy_space < 0):direction = -1
                else: direction = 1
                #print(index,direction)
                actual_buoy = buoys_coordinates(vertice_init, buoy_space, 0)
                while(direction*actual_buoy[0] < direction*vertice_end[0]):
                    #in the same vertical side, all the boyes will have the same x.
                    #we only need to change y
                    self.Buoys_set.append(Buoy(actual_buoy, space))
                    actual_buoy = buoys_coordinates(actual_buoy, buoy_space, 0)
  
    #This method builds the cross pattern.
    #Parameters:
                #self- object representative of the whole pattern
                #space- space to represent the environment space and allow to add the bodies to the environment using pymunk
    def pattern_cross(self, space):
        
        #first 4 postions in buoys_set are the vertices
        vertices_position = []
        for index in range(4):
            vertices_position.append(self.Buoys_set[index].location)
        number_between_vertices = 15 # number of spaces between vertices .it has to be higher than 2
                                #20 full cross
                                #15 70% 
                                #11 54 %
        for index in range(2):
            vertice_init = vertices_position[index]
            vertice_end = vertices_position[index+2]
            buoys_space = distance(vertice_init, vertice_end)/number_between_vertices
            buoys_space_x_y = buoys_space/math.sqrt(2)
            if(vertice_init[0] < vertice_end[0]):
                buoys_space_x = buoys_space_x_y
                direction_x = 1
            else: 
                buoys_space_x = -buoys_space_x_y
                direction_x = -1

            if(vertice_init[1]<vertice_end[1]): 
                buoys_space_y = buoys_space_x_y
                direction_y = 1
            else: 
                buoys_space_y = -buoys_space_x_y
                direction_y = -1

            actual_buoy = buoys_coordinates(vertice_init, buoys_space_x, buoys_space_y)
            while(direction_x*actual_buoy[0] < direction_x*vertice_end[0] or direction_y*actual_buoy[1] < direction_y*actual_buoy[1]):
                if check_equal_buoy(self.Buoys_set, actual_buoy) : self.Buoys_set.append(Buoy(actual_buoy,space))
                actual_buoy=buoys_coordinates(actual_buoy, buoys_space_x, buoys_space_y)
      
    #This method builds the Jail/Chessboard pattern.
    #Parameters:
                #self- object representative of the whole pattern
                #space- space to represent the environment space and allow to add the bodies to the environment using pymunk
    def jail_pattern(self, space):
        
        characteristic_variable=5 #if characteristic_variable is 5 the pattern will be 5x5
        # ATTENTION: it's important to change the variable buoys_between_vertices in square pattern for the same value as
        #characterstic_variable
        number_spaces_per_boundary=2 #to change the number of buoys per boundary just change this variable
                                    #3 full jail
                                    #2 70%
        #first 4 postions in buoys_set are the vertices
        vertices_position = []
        for index in range(4):
            vertices_position.append(self.Buoys_set[index].location)
        print("Vertices:", vertices_position)
        vertice_init_hor = vertices_position[0] #left top corner
        vertice_end_hor = vertices_position[3] #right top corner
        buoys_zone_side = distance(vertice_init_hor, vertice_end_hor)/(characteristic_variable)
        
        for  number_spaces_hor in range(1,characteristic_variable):
            vertice_init=buoys_coordinates(vertice_init_hor,number_spaces_hor*buoys_zone_side,0)
            vertice_end=buoys_coordinates(vertice_init,0,buoys_zone_side)
            buoys_space=distance(vertice_init, vertice_end)/(number_spaces_per_boundary)
            for j in range(1,characteristic_variable+1):
                for number_spaces_between_buoys in range(1,number_spaces_per_boundary+1):
                    actual_buoy=buoys_coordinates(vertice_init,0,number_spaces_between_buoys*buoys_space)
                    if(j==characteristic_variable and number_spaces_between_buoys==number_spaces_per_boundary ): break
                    self.Buoys_set.append(Buoy(actual_buoy,space))
                    
                vertice_init=actual_buoy
                vertice_end=buoys_coordinates(vertice_init,0,buoys_zone_side)

        #after this is just missing to add the horizontal lines

        vertice_init_vert=vertice_init_hor #left top corner
        vertice_end_vert= vertices_position[1] #left down corner

        for number_spaces_vert in range(1,characteristic_variable):
            vertice_init=buoys_coordinates(vertice_init_vert,0,number_spaces_vert*buoys_zone_side)
            vertice_end=buoys_coordinates(vertice_init,buoys_zone_side,0)
            buoys_space=distance(vertice_init, vertice_end)/(number_spaces_per_boundary)
            for j in range(1,characteristic_variable+1):
                for number_spaces_between_buoys in range(1,number_spaces_per_boundary):
                    actual_buoy=buoys_coordinates(vertice_init,number_spaces_between_buoys*buoys_space,0)
                    self.Buoys_set.append(Buoy(actual_buoy,space))
                vertice_init=vertice_end
                vertice_end=buoys_coordinates(vertice_init,buoys_zone_side,0)
    #This method builds the Circle pattern.
    #Parameters:
                #self- object representative of the whole pattern
                #space- space to represent the environment space and allow to add the bodies to the environment using pymunk
    def circles_pattern(self, space):

        #first 4 positions will be the most important points of the buoys
        #the circle center is the center of the group of buoys
        radius2 = math.sqrt(self.area)/3
        radius1 = radius2/2
        #print(radius1,radius2,math.sqrt(self.area)/2)
        #first we will add the 4 most important buoys of the smallest circle
        #points_change = [[1,0],[0,1],[-1,0],[0,-1]]
        n_buoys_per_circle_inner=11
        n_buoys_per_circle_outter=20
                                #16 28 full circles
                                #11 20 70% 
                                #8 14 50 %
        angle=2*math.pi/n_buoys_per_circle_inner
        for i in range(n_buoys_per_circle_inner):
            actual_buoy=buoys_coordinates(self.center,radius1*math.cos(angle*i),radius1*math.sin(angle*i))
            self.Buoys_set.append(Buoy(actual_buoy, space))


        angle=2*math.pi/n_buoys_per_circle_outter

        for i in range(n_buoys_per_circle_outter):
            actual_buoy=buoys_coordinates(self.center,radius2*math.cos(angle*i),radius2*math.sin(angle*i))
            self.Buoys_set.append(Buoy(actual_buoy, space))
        
    #This method is responsible to draw the arrangement of buoys in the simulation window
    #Parameters:
                #self- object representative of the whole pattern
                #window- simulation window which allow us to draw the bodies using pygame
    def draw(self, window):
        #window.blit((buoy.image for buoy in self.Buoys_set), (buoy.location for buoy in self.Buoys_set))
        for buoy in self.Buoys_set:
            pygame.draw.circle(window, (0, 0, 128), buoy.location, buoy.shape.radius)
            pygame.draw.circle(window, (0, 128, 0), buoy.location, buoy.shape2.radius)
            pygame.draw.circle(window, (128, 0,0), buoy.location, buoy.shape3.radius)
            #pygame.draw.circle(window, (0, 0, 0), buoy.location, 5)
            # window.blit(buoy.image, buoy.location)