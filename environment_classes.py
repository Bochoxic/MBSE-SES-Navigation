# import of the needed libraries
import pygame
import pymunk
from variables_and_functions import *
import random

class fish:
    """
    This class define the state
    and behaviour of the fish
    """
    
    # Initialization of the class with the different variables of the fish itself and the variables that will be used
    def __init__(self, true_fish_type, position, space, direction, collision_type, center, area):
        
        # Create the pymunk body. Pymunk is the librarie used to process the physics of the simulation, in this case the collisions.
        # Assigning a pymunk body to each fish we can know when they collide with other bodies, like the circle of detection of the buoy. 
        self.body = pymunk.Body()
    
        # Configuration of the different attributes of the class fish    
        x, y = position
        self.historic_position = [position]
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 3) # Define the shape of the pymunk body as a circle of radius 3
        self.shape.elasticity = 1 # Define elasticity of the pymunk body
        self.shape.density = 1 # Define density of the pymunk body
        self.shape.collision_type = collision_type # Define the collision type of the pymunk body
        self.detect = 0
        self.direction = direction 
        self.center_environment = center
        self.area_environment = area
        self.predicted_zone = 0
        self.true_zone = 0
        self.prev_predicted_zone = 0
        self.true_fish_type = true_fish_type
        self.predicted_fish_type = 'None'
        
        # Definition of depht, velocity and vision angle depending the type of fish. Also the values for the orientation, repulsion
        # and attraction radius are defined here. The meaning of these radius are explained in the report

        if self.true_fish_type == "tuna":
            self.depht = 10
            self.velocity = 50
            self.alpha = 150
            self.r_attraction = 200
            self.r_orientation = 25
            self.r_repulsion = 2
           
        if self.true_fish_type == "salmon":
            self.depht = 20
            self.velocity = 80
            self.alpha = 90
            self.r_attraction = 200
            self.r_orientation = 25
            self.r_repulsion = 2
        
        if self.true_fish_type == "clown":
            self.depht = 30
            self.velocity = 70
            self.alpha = 90
            self.r_attraction = 200
            self.r_orientation = 25
            self.r_repulsion = 2
        
        # Calculus of velocity as a multiplication of the vector direction by the velocity
        self.body.velocity = tuple(np.multiply(self.velocity, direction))
        # Add the body to the simulartion space
        space.add(self.body, self.shape)

    # Function that simulate the Image Recognition module. In this case the accuracy is of a 90%
    def predict_fish_type(self):

        random_n = random.uniform(0,1)

        if self.true_fish_type == "tuna":
            if random_n < 0.9:
                return "tuna"
            else:
                
                if random_n < 0.97:
                    return "salmon"
                else: 
                    return "clown"

        if self.true_fish_type == "salmon":
            if random_n < 0.9:
                return "salmon"
            else:
                
                if random_n < 0.97:
                    return "tuna"
                else: 
                    return "clown"
        
        if self.true_fish_type == "clown":
            if random_n < 0.9:
                return "clown"
            else:
                
                if random_n < 0.95:
                    return "salmon"
                else: 
                    return "tuna"

    
    # Functions that provide information about the fish. This functions will trigger when a collision is detected between the fish and the body of one of
    # the buoys. The functions check if the fishes are swimming on the right depth that they are supossed to swim in and, after that, they make a call to 
    # the function collision_detection, which evaluate what is happening on the environment in the moment and process the detection.

    def collision(self,arbiter,space,data):
        if(self.depht>20):
            if(self.true_fish_type!="clown"): print("ERRO1")
            return self.collision_detection()
        else:   
            return False

    def collision2(self,arbiter,space,data):
        if(self.depht>10 and self.depht<=20):
            if(self.true_fish_type!="salmon"): print("ERRO2")
            return self.collision_detection()
        else:   
            return False

    def collision3(self,arbiter,space,data):
        if(self.depht<=10):
            if(self.true_fish_type!="tuna"): print("ERRO3")
            return self.collision_detection()
        else:   
            return False

    # This function is the collision handler and the one in charge to process the information when a detection is made. Basically, the aim
    # of the function is to guess where a fish that has been detected is going. This way it can be processed the changes between the different zones
    # of the pattern. To perform this, it has to be known which buoy has detected the fish and the orientation that the fish has. 

    def collision_detection(self):

        global previous_delta

        self.detect = 1
        # If the pattern is the circle pattern        
        if(type_pattern == 1):
            # Code for detection in circle pattern
            # The bigger circle has a radius of 1/3 of environment size
            # The smaller circle radius has a radius of 1/2 of environment sizes
            side = math.sqrt(area_pattern)
            dist = distance_between_points(center, self.body.position)

            # Detection if it's entering or leaving the zone calculating the distance to the center and the angle depending on the direction of the fish 
            fish_location_center = np.subtract(center, self.body.position)
            angle = angle_of_vectors(fish_location_center[0], fish_location_center[1], self.direction[0], self.direction[1])
            # Define the boundaries of the different circles of buoys
            boundary3 = side/6+(side/3-side/6)/2
            boundary2 = side/3+(side/2-side/3)/2
            # Process the information and determine where the detection was made. This way the results are the previous zone and the new zone 
            if(dist < boundary3):
                #print("**ZONE3**")
                if(angle < 90):
                    #print("Entering ")
                    self.predicted_zone = 3
                    self.prev_predicted_zone = 2

                if angle > 90:
                    self.predicted_zone = 2
                    self.prev_predicted_zone = 3
                    #print("Leaving")
            elif(dist < boundary2):
                #print("**ZONE2**")
                if(angle < 90):
                    #print("Entering ")
                    self.predicted_zone = 2
                    self.prev_predicted_zone = 1

                if angle > 90:
                    #print("Leaving")
                    self.predicted_zone = 1
                    self.prev_predicted_zone = 2
            """
            else:
                print("**ZONE1**")
                if angle<90: 
                    self.predicted_zone=1
                    self.prev_predicted_zone=0
                if angle>90: 
                    print("Leaving")"""

            # Do the image recognition
            self.predicted_fish_type = self.predict_fish_type()

            # Update the delta matrix. Normally it adds 1 to the zone the fish is moving to (representing that there is a positive variation, an entrance) and
            # substract 1 to the previous zone (negative variation, a leaving). In the case of the clown fishes, it is the opposite. This difference is made
            # because the endagered specie is meant to be protected, so a zone with clown fishes wants to be represented as a zone with less fishes on it
            # to indicate the fisherman that is not a zone to go.
     
            if fish_dict[self.predicted_fish_type] == 2 :
                delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1]-3
                delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1]+3
            else:
                delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1]+1
                delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1]-1
            
        # If the pattern is the cross pattern
        if(type_pattern == 2):
           
            #The algorithm for detection in the cross pattern is:
            #   1st-detect in wich boundary the fish was detected, using the fish locations relatively to the
            #        center
            #   2nd- after detecting the boundary we will find angle of the vector representing the boundary
            #        and the direction of the fish

            if (abs(center[0]-self.body.position[0]) < 265 and (abs(center[1]-self.body.position[1]) < 265)): #to ignore the square buoyes

                fish_location_center = np.subtract(self.body.position, center)
                diagonal_1_2 = (1, -1)
                diagonal_2_3 = (1, 1)
                diagonal_3_4 = (-1, 1)
                diagonal_4_1 = (-1, -1)
                
                if(fish_location_center[0]>0 and fish_location_center[1]<0): #boundary zone 1 - zone 2
                    
                    angle = angle_of_vectors_0_360(diagonal_1_2, self.direction)
                    # print("LOCATION:", angle, self.body.position)
                    if(angle > 180):
                        #print("2->1")
                        self.prev_predicted_zone = 2
                        self.predicted_zone = 1
                    else:
                        #print("1->2")
                        self.prev_predicted_zone = 1
                        self.predicted_zone = 2
                elif(fish_location_center[0]>0 and fish_location_center[1]>0): #boundary zone 2 - zone 3
                    
                    angle=angle_of_vectors_0_360(diagonal_2_3, self.direction)
                    # print("LOCATION:", angle, self.body.position)
                    if(angle > 180):
                        #print("3->2")
                        self.prev_predicted_zone = 3
                        self.predicted_zone = 2
                    else:
                        #print("2->3")
                        self.prev_predicted_zone = 2
                        self.predicted_zone = 3

                
                elif(fish_location_center[0]<0 and fish_location_center[1]>0): #boundary zone 3 - zone 4
                    angle=angle_of_vectors_0_360(diagonal_3_4, self.direction)
                    # print("LOCATION:", angle, self.body.position)
                    if(angle > 180):
                        #print("4->3")
                        self.prev_predicted_zone = 4
                        self.predicted_zone = 3
                    else:
                        #print("3->4")
                        self.prev_predicted_zone = 3
                        self.predicted_zone = 4
                
                elif(fish_location_center[0]<0 and fish_location_center[1]<0): #boundary zone 1 - zone 4
                    angle=angle_of_vectors_0_360(diagonal_4_1, self.direction)
                    # print("LOCATION:", angle, self.body.position)
                    if(angle > 180):
                        #print("1->4")
                        self.prev_predicted_zone = 1
                        self.predicted_zone = 4
                    else:
                        #print("4->1")
                        self.prev_predicted_zone = 4
                        self.predicted_zone = 1
                        
            # Do the image recognition
            self.predicted_fish_type = self.predict_fish_type()

            # Update the delta matrix. The logic behind it is the same for all the patterns and can be seen in the comments made on lines 189-192.
            if fish_dict[self.predicted_fish_type] == 2 :
                delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1]-3
                delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1]+3
            else:
                delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1]+1
                delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1]-1

        # If the pattern is the jail pattern       
        if(type_pattern == 3):

            # Code for detection in jail pattern
            # We will consider just for the size we are using (600,600)
            # Our buoys center are between 12,5 and 587,5 in both axis
            
            #The algorithm for detection in the jail pattern is:
            #   1st- separate the between 12,5 and 587,5 in 5 parts
            #   2nd- after knowing the boundaries of each zone we wil calculate
            #    in wich row and column the fish was found, allowing us to know the zone
            row = 0
            column = 0
            zones_size = (587.5-12.5)*0.2

            for index_column in range(5):
                if(self.body.position[0]<12.5+(index_column+1)*zones_size):
                    column=index_column+1
                    break
            for index_rows in range(5):
                if(self.body.position[1]<12.5+(index_rows+1)*zones_size):
                    row=index_rows+1
                    break

            
            # Now we need to translate row and column to the number of the zone
            zone_detected = column+5*(row-1)

            #Once it is found where the detection has been done, to detect if the boundary that detected was horizontal or vertical we will find 
            #from where it is closer.
            horizontal_boundary_down = 12.5+row*zones_size
            horizontal_boundary_up = 12.5+(row-1)*zones_size
            vertical_boundary_right = 12.5+column*zones_size
            vertical_boundary_left = 12.5+(column-1)*zones_size

            lower_distance = 1000
            boundaries = [horizontal_boundary_down, horizontal_boundary_up, vertical_boundary_left, vertical_boundary_right]
            measures = [self.body.position[1], self.body.position[1], self.body.position[0], self.body.position[0]]
            closer_boundary = 0
            i=0
            for measure,boundary in zip(measures, boundaries):
                distance=abs(measure-boundary)
                i=i+1
                if(distance<lower_distance):
                    lower_distance = distance
                    closer_boundary = i

            # Now, depending on the closer boundary, the previous zone is calculated
            if(closer_boundary == 1): #horizontal boundary down
                if(self.direction[1]>0): 
                    if(zone_detected < 21):
                        self.predicted_zone = zone_detected + 5 #zone same column,next row
                        self.prev_predicted_zone = zone_detected
                else:
                    if(zone_detected < 21):
                        self.predicted_zone = zone_detected
                        self.prev_predicted_zone = zone_detected+5
            if(closer_boundary==2): #horizontal boundary up
                if(self.direction[1]>0):
                    if zone_detected > 5: 
                        self.predicted_zone = zone_detected
                        self.prev_predicted_zone = zone_detected-5
                else:
                    if zone_detected > 5: 
                        self.predicted_zone = zone_detected-5 #zone same column,lower row
                        self.prev_predicted_zone = zone_detected
            if(closer_boundary==3): #vertical boundary left
                if ((zone_detected+4)%5 !=0):
                    if(self.direction[0]>0): 
                        self.predicted_zone = zone_detected
                        self.prev_predicted_zone = zone_detected-1
                    else:
                        self.predicted_zone = zone_detected-1 #zone same row, left column
                        self.prev_predicted_zone = zone_detected
            if(closer_boundary==4): #vertical boundary right
                if(zone_detected%5 != 0):
                    if(self.direction[0]>0): 
                        self.predicted_zone = zone_detected+1 #zone same row, next column
                        self.prev_predicted_zone = zone_detected

                    else:
                        self.predicted_zone = zone_detected
                        self.prev_predicted_zone = zone_detected+1
            predicted_zone = self.predicted_zone
            prev_predicted_zone = self.prev_predicted_zone

            if (predicted_zone > 25 or predicted_zone < 1 or prev_predicted_zone > 25 or prev_predicted_zone < 1):
                print("Zone detected: ",zone_detected,"New zone: ",predicted_zone,"Previous zone:",prev_predicted_zone)
                print("----------------------------------------")
            else:
                # Do the image recognition 
                self.predicted_fish_type = self.predict_fish_type()
                
                # Update the delta matrix. The logic behind it is the same for all the patterns and can be seen in the comments made on lines 189-192
                if fish_dict[self.predicted_fish_type] == 2 :
                    delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1]-3
                    delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1]+3
                else:
                    delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.predicted_zone-1]+1
                    delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1] = delta[fish_dict[self.predicted_fish_type]][self.prev_predicted_zone-1]-1

        return True

    
    # Function that handles when one of the fishes has stopped being on the collision radius with the detection radius of a buoy
    def separation(self, arbiter, space, data):
        self.detect = 0
        #print("**SEPARAÇAO**")
        return True


    
    #Function that draw a the fishes in pygame. The color is different between the different types of fish
    
    def draw(self, display):
        if self.true_fish_type == "tuna":
            pygame.draw.circle(display, (0, 0, 255), self.body.position, 3) # Tunas are drawn blue
        elif self.true_fish_type == "salmon":
            pygame.draw.circle(display, (250, 128, 114), self.body.position, 3) # Salmons are drawn in a color similar to rose (salmon color)
        elif self.true_fish_type == "clown":
            pygame.draw.circle(display, (255, 255, 1), self.body.position, 3) # Clown fishes are drawn yellow

    
    # Function that returns the new velocity of the fish. Fishes type position is a matrix of vectors where is saved the position of all the same fishes type.
        
    def new_velocity(self, fishes_type_position):
        
    
        # Creates the vector fishes_distance, where we will save all the distance of all the different fishes of the same specie 
        # with the fish we want to calculate the new velocity. Creates the vector fishes_angles, that will contain the distance 
        # between all the different fishes of the same specie and the fish we want to calculate the new velocity
        fishes_distance = np.zeros(len(fishes_type_position))
        fishes_angles = np.zeros(len(fishes_type_position))

        # Calcules the values of fishes distance and the fishes angles
        for i in range(len(fishes_type_position)):
            v = fishes_type_position[i] - self.body._get_position() # Distance vector between two fishes
            fishes_angles[i] = math.degrees(math.atan2(v[1],v[0]) - math.atan2(self.direction[1],self.direction[0]))
            fishes_distance[i] = np.linalg.norm(v)
        
        # Divide the fishes in different groups depending on the distance to the fish we are calculating the velocity for. This groups are a repulsion group, 
        # an orientation group and a attraction group. Also, it checks if the fishes are in the radius of vision of the fish (alpha). The logic behind this division
        # can be seen in the report and it comes from a paper that studies the movement of different animals and bring a general mathematical model.
        fishes_repulsion = np.transpose(np.asarray(np.where((fishes_distance < self.r_repulsion) & (fishes_angles < self.alpha) & (fishes_angles > -self.alpha))))
        fishes_orientation = np.transpose(np.asarray(np.where((fishes_distance > self.r_repulsion) & (fishes_distance < self.r_orientation) & (fishes_angles < self.alpha) & (fishes_angles > -self.alpha))))
        fishes_attraction = np.transpose(np.asarray(np.where((fishes_distance > self.r_orientation) & (fishes_distance < self.r_attraction) & (fishes_angles < self.alpha) & (fishes_angles > -self.alpha))))
        
        
        # First case of movement, there is fishes in the repulsion circle, so the fish goes away.
        if len(fishes_repulsion) > 1:
            # Variable 'a' will be the vector distance between all repulsion fishes
            a = np.zeros((len(fishes_repulsion),2))
            for i in range(len(fishes_repulsion)):
                # Calculate the 'a' distance vector
                a[i,:] = np.asarray(fishes_type_position[fishes_repulsion[i],:])-np.asarray(self.body._get_position())
                # This if is to not get an error due to divede by 0
                if np.array_equal(a[i,:], np.array((0,0))) != True:
                    a[i,:] = a[i,:]/np.linalg.norm(a[i,:])
            # Calculate the new direction
            new_direction = -(np.sum(a, axis = 0)/np.linalg.norm(np.sum(a, axis = 0))) # Goes in the opposite direction
            self.direction = new_direction
            # Calculate the new velocity
            new_velocity = self.velocity*new_direction
            return new_velocity 
        
        # Second case, there is no fishes in the repulsion circle but there is fishes on the orientation circle and not in the attraction circle
        elif len(fishes_orientation) > 0 and len(fishes_attraction) == 0:
            # Calculate the distance vector between all the orientation fishes
            a = np.zeros((len(fishes_orientation)+1,2))
            a[0,:] = np.asarray(self.body._get_velocity())
            a[0,:] = a[0,:]/np.linalg.norm(a[0,:])
            for i in range(len(fishes_orientation)):
                a[i+1,:] = np.asarray(fishes_type_position[fishes_orientation[i],:]) - np.asarray(self.body._get_position())
                a[i+1,:] = a[i,:]/np.linalg.norm(a[i,:])
            # Calculates the new direction
            new_direction = np.sum(a, axis = 0)/np.linalg.norm(np.sum(a, axis = 0)) # Same direction
            self.direction = new_direction
            # Calculates the new velocity
            new_velocity = self.velocity*new_direction
            return new_velocity
        
        # Third case, there is fishes in the orientation circle and also in the attraction one. In this case the fish changes direction being attracted by
        # the fishes in both groups.
        elif len(fishes_orientation) > 0 and len(fishes_attraction) > 0:
            a = np.zeros((len(fishes_orientation)+1,2))
            a[0,:] = np.asarray(self.body._get_velocity())
            a[0,:] = a[0,:]/np.linalg.norm(a[0,:])
            for i in range(len(fishes_orientation)):
                a[i+1,:] = np.asarray(fishes_type_position[fishes_orientation[i],:]) - np.asarray(self.body._get_position())
                a[i+1,:] = a[i,:]/np.linalg.norm(a[i,:])
            # Calculates the direction that the fishes in the orientation circle are attracting the fish to 
            new_a_direction = np.sum(a, axis = 0)/np.linalg.norm(np.sum(a, axis = 0))
            
            a = np.zeros((len(fishes_attraction),2))
            for i in range(len(fishes_attraction)):
                a[i,:] = np.asarray(fishes_type_position[fishes_attraction[i],:]) - np.asarray(self.body._get_position())
                if np.array_equal(a[i,:], np.array((0,0))) != True:
                    a[i,:] = a[i,:]/np.linalg.norm(a[i,:])
            # Calculates the direction that the fishes in the attraction circle are attracting the fish to 
            new_b_direction = -(np.sum(a, axis = 0)/np.linalg.norm(np.sum(a, axis = 0)))   
            # Calculate the new direction of the fish based on the other two directions previously calculated
            new_direction = (1/2)*(new_a_direction+new_b_direction)
            self.direction = new_direction
            # Calculates velocity
            new_velocity = self.velocity*new_direction
            return new_velocity
        
        # Fourth case, there is fishes just in the attraction circle. 
        elif len(fishes_attraction) > 0:
            a = np.zeros((len(fishes_attraction),2))
            for i in range(len(fishes_attraction)):
                # Calculate distances
                a[i,:] = np.asarray(fishes_type_position[fishes_attraction[i],:]) - np.asarray(self.body._get_position())
                if np.array_equal(a[i,:], np.array((0,0))) != True:
                    a[i,:] = a[i,:]/np.linalg.norm(a[i,:])
            # Calculate the new direction
            new_direction = (np.sum(a, axis = 0)/np.linalg.norm(np.sum(a, axis = 0)))
            self.direction = new_direction
            # Calculate the new velocity
            new_velocity = self.velocity*new_direction
            return new_velocity
        else:
            # Keeps the same velocity
            new_velocity = self.body._get_velocity()
            return new_velocity
    

    # Updates the velocity of the fish
    def update_velocity(self, new_velocity):
        if isinstance(new_velocity, pymunk.vec2d.Vec2d) == True:
            self.body.velocity = new_velocity
        else:
            self.body.velocity = new_velocity.tolist()               

    # Gets the true zone of the fish. The true zone is used to build the staticstics dataframe
    def update_zone(self, pattern):

        # Calculus of the zone if the pattern is the circle pattern
        if pattern == 1:

            side = math.sqrt(self.area_environment)
            dist = distance_between_points(self.center_environment, self.body.position)
            boundary3 = side/6
            boundary2 = side/3
            
            if dist < boundary3:
                self.true_zone = 3
                
            
            elif dist < boundary2:
                self.true_zone = 2
                
            
            else:
                self.true_zone = 1

            return

        
        # Calculus of the zone if the pattern is the cross pattern        
        elif pattern == 2:

            # V1 --> y = x
            # V2 --> y = 600-x

            upper_v1 = 0
            upper_v2 = 0
            x = self.body.position[0]
            y = self.body.position[1]

            if y < x:
                upper_v1 = 1

            if y+x < 600:
                upper_v2 = 1

            if upper_v1 == 1 and upper_v2 == 1:
                self.true_zone = 1
            elif upper_v1 == 1 and upper_v2 == 0:
                self.true_zone = 2
            elif upper_v1 == 0 and upper_v2 == 0:
                self.true_zone = 3
            else: 
                self.true_zone = 4

            # print("Upper_V1: ", upper_v1, "Upper V2: ", upper_v2, "Zone :", self.true_zone)
            return

        # Calculus of the zone if the pattern is the jail pattern
        elif pattern == 3:
            
            buoys_space_x = (600)/5
            buoys_space_y = (600)/5
            column = math.floor(self.body.position[0] / buoys_space_x) + 1
            row = math.floor(self.body.position[1] / buoys_space_y) + 1
            
            self.true_zone = column + ((row-1)*5)
            #print("Column: ",column," Row: ", row, " Zone: ", self.true_zone)
            return
    
        return


class Wall():
    ''' 
    Class that defines an object Wall that will serve as a boundary so the fishes don't go out of the screen
    '''
    def __init__(self, p1, p2, radius, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, radius)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

def initialize_tunas(n_tunas, space):
    
    #Function that initialize the tunas
    
    tunas = []
    tunas_position = np.zeros((n_tunas, 2))
    tunas_handlers=[]
    tunas_handlers2=[]
    tunas_handlers3=[]
    
    for i in range(n_tunas):
        direction = np.random.randn(2) 
        # direction = [0, 1]
        direction = direction/ np.linalg.norm(direction)
        p_x = np.random.randint(0, x_size)
        p_y = np.random.randint(0, y_size)
        position = [p_x, p_y]
        # position = [10,10]
        tunas.append(fish("tuna", position, space, direction, i+4, center, area_pattern))
        print(tunas[i].shape.collision_type)
        tunas_handlers.append(space.add_collision_handler(1, tunas[i].shape.collision_type))
        tunas_handlers2.append(space.add_collision_handler(2, tunas[i].shape.collision_type))
        tunas_handlers3.append(space.add_collision_handler(3, tunas[i].shape.collision_type))

    for i,handler in enumerate(tunas_handlers):
        handler.begin = tunas[i].collision
        handler.separate = tunas[i].separation
    for i,handler in enumerate(tunas_handlers2):
        handler.begin = tunas[i].collision2
        handler.separate = tunas[i].separation
    for i,handler in enumerate(tunas_handlers3):
        handler.begin = tunas[i].collision3
        handler.separate = tunas[i].separation

    tunas_total_handlers=[tunas_handlers,tunas_handlers2,tunas_handlers3]

    return tunas, tunas_position, tunas_total_handlers

def initialize_salmons(n_salmons, n_tunas, space):
    #Function that initialize the salmons
    salmons = []
    salmons_position = np.zeros((n_salmons, 2))
    salmons_handlers=[]
    salmons_handlers2=[]
    salmons_handlers3=[]

    for i in range(n_salmons):
        #direction= np.random.randn(2) 
        direction = [0.5, 0.5]
        direction = direction/ np.linalg.norm(direction)
        p_x = np.random.randint(0, x_size)
        p_y = np.random.randint(0, y_size)
        position = [p_x, p_y]
        salmons.append(fish("salmon", position, space, direction, i+n_tunas+4, center, area_pattern))
        print(salmons[i].shape.collision_type)
        salmons_handlers.append(space.add_collision_handler(1, salmons[i].shape.collision_type))
        salmons_handlers2.append(space.add_collision_handler(2, salmons[i].shape.collision_type))
        salmons_handlers3.append(space.add_collision_handler(3, salmons[i].shape.collision_type))

    for i,handler in enumerate(salmons_handlers):
        handler.begin = salmons[i].collision
        handler.separate = salmons[i].separation
    for i,handler in enumerate(salmons_handlers2):
        handler.begin = salmons[i].collision2
        handler.separate = salmons[i].separation
    for i,handler in enumerate(salmons_handlers3):
        handler.begin = salmons[i].collision3
        handler.separate = salmons[i].separation

    salmons_total_handlers=[salmons_handlers,salmons_handlers2,salmons_handlers3]
    
    return salmons, salmons_position, salmons_total_handlers

def initialize_clowns(n_clowns, n_tunas, n_salmons, space):
    #Function that initialize the clown fishes
    clowns = []
    clowns_position = np.zeros((n_clowns, 2))
    clowns_handlers=[]
    clowns_handlers2=[]
    clowns_handlers3=[]
    for i in range(n_clowns):
        #direction= np.random.randn(2) 
        direction = [0.5, 0.5]
        direction = direction/ np.linalg.norm(direction)
        p_x = np.random.randint(0, x_size)
        p_y = np.random.randint(0, y_size)
        position = [p_x, p_y]
        clowns.append(fish("clown", position, space, direction, i+n_tunas+n_salmons+4, center, area_pattern))
        print(clowns[i].shape.collision_type)
        clowns_handlers.append(space.add_collision_handler(1, clowns[i].shape.collision_type))
        clowns_handlers2.append(space.add_collision_handler(2, clowns[i].shape.collision_type))
        clowns_handlers3.append(space.add_collision_handler(3, clowns[i].shape.collision_type))

    for i,handler in enumerate(clowns_handlers):
        handler.begin = clowns[i].collision
        handler.separate = clowns[i].separation
    for i,handler in enumerate(clowns_handlers2):
        handler.begin = clowns[i].collision2
        handler.separate = clowns[i].separation
    for i,handler in enumerate(clowns_handlers3):
        handler.begin = clowns[i].collision3
        handler.separate = clowns[i].separation


    clowns_total_handlers=[clowns_handlers,clowns_handlers2,clowns_handlers3]
    return clowns, clowns_position, clowns_total_handlers

# Fuction that creates the boundaries of the lake
def initialize_lake(space):
    thickness_wall = 20
    walls = [Wall((0, 0), (0, y_size), thickness_wall, space),
    Wall((0, 0), (x_size, 0), thickness_wall, space),
    Wall((x_size, 0), (x_size, y_size), thickness_wall, space),
    Wall((0, y_size), (x_size, y_size), thickness_wall, space)]

# Function that calculates the velocity and updates it for all the fishes in fish_array
def velocity_computation(fish_array, fish_array_position):

    for i in range(len(fish_array)):
            # fish_array[i].draw(display)
            fish_array_position[i] = np.asarray(fish_array[i].body._get_position())
        
    for i in range(len(fish_array)):
        new_velocity = fish_array[i].new_velocity(fish_array_position)
        fish_array[i].update_velocity(new_velocity)
        fish_array[i].update_zone(pattern = type_pattern)

# Function that draws all the fish at once
def draw_fish(display,fish_array):
    for i in range(len(fish_array)):
            fish_array[i].draw(display)