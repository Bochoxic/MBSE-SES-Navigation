import pygame
import pymunk
import numpy as np
import math
import pandas as pd

''' This scripts contains all the functions and variables that the simulation uses that are not 
    part of any of the classes. Here, it can be found functions to measure distance between points,
    calculate angles, create matrixes, dataframes, etc... '''


# Function that compute the euclidean distance between 2 points with 2 coordinates (x,y)
def distance(v1, v2):
    return (math.sqrt(math.pow((v1[0]-v2[0]), 2) + math.pow((v1[1]-v2[1]), 2)))

# Function that compute the euclidean distance between 2 points with 2 coordinates (x,y)
def distance_between_points(v1, v2):
    return (math.sqrt(math.pow((v1[0]-v2[0]), 2) + math.pow((v1[1]-v2[1]), 2)))

# Function that compute de angle between two vectors with two components each one.
# and return an angle between 0 and 360.
def angle_of_vectors_0_360(v1, v2):

    dot = v1[0]*v2[0] + v1[1]*v2[1]      # dot product
    det = v1[0]*v2[1] - v1[1]*v2[0]      # determinant

    angle = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    angle=angle*180/math.pi
    if angle<0: 
        angle=angle+360
    return angle

# # Function that compute de angle between two vectors with two components each one.
# and return an angle between 0 and 180. 
# The main difference between this function and the previous one is the range of values that 
# are returned. This difference serves the purpose of making the detection of the zone changing
# easier depending of the pattern.
def angle_of_vectors(a, b, c, d):
    
     dotProduct = a*c + b*d
         # for three dimensional simply add dotProduct = a*c + b*d  + e*f 
     modOfVector1 = math.sqrt( a*a + b*b) * math.sqrt(c*c + d*d)
         # for three dimensional simply add modOfVector = math.sqrt( a*a + b*b + e*e)*math.sqrt(c*c + d*d +f*f) 
     angle = dotProduct/modOfVector1
     angleInDegree = math.degrees(math.acos(angle))
     return angleInDegree

# Function that initialize a matrix full of zeros that has different dimensions depending on the pattern chosen for the
# buoys arrangement. This function is called various times to create the different Delta variables that we have. 
# As explained in other scripts (and later on this one also) this Deltas are the difference of fishes detected between zones. 
def variation_matrix(pattern):

    if pattern == 1:
        return np.zeros((3,3))
    elif pattern == 2:
        return np.zeros((3,4))
    elif pattern == 3:
        return np.zeros((3,25))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function that returns the position of the next buoy to arrange from the position of one of the buoys and the distance that they should have between them 
# in the pattern
def buoys_coordinates(actual_buoy, deltax, deltay):
    list_actual_buoy = list(actual_buoy)
    list_actual_buoy[0] = list_actual_buoy[0]+deltax
    list_actual_buoy[1] = list_actual_buoy[1]+deltay
    actual_buoy = tuple(list_actual_buoy)
    return actual_buoy

# Function that verifies if one buoy is the buoy that it is thought it is 
def check_equal_buoy(Buoys_set, actual_buoy):
    for elem in Buoys_set:
        list_elem = list(elem.location)
        list_actual_buoy = list(actual_buoy)
        if distance(list_elem, list_actual_buoy) < 1: return False
    return True

# This function contains all the lines that are neccesary to initialize and configure the simulation    
def initilize_pymunk_pygame():
    ### Initialize pygame ###
    pygame.init()
    space = pymunk.space
    # Set up the drawing window
    display = pygame.display.set_mode((x_size, y_size))
    font50 = pygame.font.SysFont(None, 50)


    ### Initialize the clock ###
    clock = pygame.time.Clock()
    space = pymunk.Space()
    FPS = 10
    #pygame.time.delay(10000)
    run = True
    return space, display, clock

# Function that get the information of different attributes of the fish in the simulation, builds a dataframe out of it and return it .
# The information that the dataframe contains is the actual type of the fish (True type), the type of fish that the system has labeled the fish as
# (Predicted Type), the zone where the fish are (True Zone), the zone that the system thinks the fish is in (Predicted Zone) and the depth (Depth).
# This dataframe gets updated every iteration, so, in the first of the columns (Time), it also has information of the time when the information was taken.
# The information gathered on this dataframe can be used to get statistics about the accuracy of detection.
def get_dataframe(fishes,df,iter):

    # Create all the lists necessary to build the dataset
    # type = []
    depth =[]
    # velocity = []
    predicted_zone = []
    true_zone = []
    predicted_type = []
    true_type = []

    # Get attributes from all the fish
    for fish in fishes:

        depth.append(fish.depht)
        # velocity.append(fish.velocity)
        predicted_zone.append(fish.predicted_zone)
        true_zone.append(fish.true_zone)
        predicted_type.append(fish.predicted_fish_type)
        true_type.append(fish.true_fish_type)

    # Build dataframe and append it to the existing dataframe 
    d = {'Time': iter,'True_type': true_type,'Predicted_type': predicted_type, 'True_zone':true_zone,'Predicted_zone':predicted_zone, 'Depth': depth}
    df_new = pd.DataFrame(d)
    frame=[df,df_new]
    df=pd.concat(frame,ignore_index=True)
    return df

# Function that get the information from the Delta matrix and build a dataframe from it. As said later on this same script, this delta matrix 
# represents variation on the number of fishes in each zone based on the detections made during the time the program is running. This dataframe has 
# the information of the Delta matrix on each iteration of the simultion. The structure of it will contain the time when the information was taken (Time), 
# the type of fish that is changing zone (Type) and as many columns as zones there are in the pattern, indicating what is the variation of the amount on 
# each moment (Zone1, Zone2, Zone3,...) 
# This will be one of the results of the system. This information is the one that the Dashboard will make use to build the dataset.
def get_delta_dataframe(delta,delta_df,iter):

    # Build all the necessary dataframes and lists to build the dataframe. 
    data = {}
    data['Time'] = [iter,iter,iter]
    data['Type'] = ['Tuna', 'Salmon', 'Clown']

    # For each zone in the pattern, gets the variation that have been in that zone for the different types of fish and save it. 
    for i in range(len(delta[0])):
        type = 'Zone' + str(i+1)
        data[type] = delta[:,i]

    df = pd.DataFrame(data)
    frame=[delta_df,df]
    delta_df=pd.concat(frame)
    
    return delta_df


# Function that calculates the variation on the delta matrix between the different iterations of it (once it is finished), build a dataframe with it and returns it. 
# The reason of having this function and also the past one is because this format is easier to process and analyse for the software that it is used to show the
# dashboard. 
def compute_relative_delta(delta):

    # Get dimensions of Delta
    n_rows = delta.shape[0]
    n_columns = delta.shape[1]
    data = {}

    l = []
    
    # Copy the column Time of delta
    for i in range(0,n_rows-3):
        l.append(delta.iat[i,0])
    data['Time'] = l
    # print("Time: ",data['Time'])

    print("Time Lenght: ", len(data['Time']))

    l = []

    # Copy the column Type of delta
    for i in range(0,n_rows-3):
        l.append(delta.iat[i,1])
    data['Type'] = l

    l = []

    # Get the difference of the values of delta between the different iterations
    for j in range(2,n_columns):
        for i in range(3,n_rows):
            l.append(delta.iat[i,j] - delta.iat[i-3,j])
        column = 'Zone' + str(j-1)
        data[column] = l
        print("Length Type: ",len(data[column]))
        l = []

    relative_delta = pd.DataFrame(data)
    
    return relative_delta
        

# General variables about the model that will be used in the other scripts

x_size = 600 # size of the window in the horizontal axis
y_size = 600 # size of the window in the horizontal axis
center = (x_size/2, y_size/2) # center of the window
area_pattern = (x_size-25)*(y_size-25) # cropped total area that will be used to make calculations

type_pattern = 2 # Variable that changes the pattern selected. The values correspond to: 1 = Circle Pattern, 2 = Cross Pattern, 3 = Jail Pattern
 
fish_dict = {'tuna': 0, 'salmon': 1, 'clown': 2} # Dictionary about the types of fish

FPS = 10 # Limit our fps

# Number of fishes
n_tunas = 60
n_salmons = 60
n_clowns = 10


delta = variation_matrix(pattern=type_pattern) # Create the delta matrix. This matrix contains the variation on the number of fishes 
                                               # that have been detected entering or leaving each zone since the begining of the simulation

n_iterations = 200 # Number of iterations where the program is going to stop and save the .csv files

