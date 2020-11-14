from argparse import ArgumentParser
import numpy as np
import random
import time

def get_command_line_arguments():
    """
    Get command line arguments required to perform simulation.
    
    :return: parameters 
    :rtype: ArgumentParser
    """
    # Create an ArgumentParser object to parse command-line 
    # strings into Python objects.
    parameters=ArgumentParser()

    # Define how each of the command-line arguments should be parsed
    # and added to the parameters object.
    parameters.add_argument("-r","--birth-hares",type=float,default=0.08,
                        help="Birth rate of hares")
    parameters.add_argument("-a","--death-hares",type=float,default=0.04,
                        help="Rate at which pumas eat hares")
    parameters.add_argument("-k","--diffusion-hares",type=float,default=0.2,
                        help="Diffusion rate of hares")
    parameters.add_argument("-b","--birth-pumas",type=float,default=0.02,
                        help="Birth rate of pumas")
    parameters.add_argument("-m","--death-pumas",type=float,default=0.06,
                        help="Rate at which pumas starve")
    parameters.add_argument("-l","--diffusion-pumas",type=float,default=0.2,
                        help="Diffusion rate of pumas")
    parameters.add_argument("-dt","--delta-t",type=float,default=0.4,
                        help="Time step size")
    parameters.add_argument("-t","--time_step",type=int,default=10,
                        help="Number of time steps at which to output files")
    parameters.add_argument("-d","--duration",type=int,default=500,
                        help="Time to run the simulation (in timesteps)")
    parameters.add_argument("-f","--landscape-file",type=str,required=True,
                        help="Input landscape file")
    parameters.add_argument("-hs","--hare-seed",type=int,default=1,
                        help="Random seed for initialising hare densities")
    parameters.add_argument("-ps","--puma-seed",type=int,default=1,
                        help="Random seed for initialising puma densities")

    return parameters

def create_args_dictionary(command_line_args):
    """
    Creates a dictionary relating the names of the command-line
    arguments with variables containing their values.

    :param command_line_args: command_line_args
    :type command_line_args: ArgumentParser
    :return: dictionary of command-line arguments and their values
    :rtype: dict
    """
    # Convert argument strings to objects and assign them as attributes 
    # of the Namespace object args.
    args = command_line_args.parse_args()

    # Assign each of the attributes of the Namespace object args,
    # to a separate variable 
    birth_rate_hares = args.birth_hares
    death_rate_hares = args.death_hares
    diffusion_rate_hares = args.diffusion_hares
    birth_rate_pumas = args.birth_pumas
    death_rate_pumas = args.death_pumas
    diffusion_rate_pumas = args.diffusion_pumas
    time_step_size = args.delta_t
    time_step_number = args.time_step
    duration = args.duration
    landscape_file = args.landscape_file
    hseed = args.hare_seed
    pseed = args.puma_seed

    return {
        'birth_rate_hares'  : birth_rate_hares,
        'death_rate_hares'  : death_rate_hares,
        'diffusion_rate_hares'  : diffusion_rate_hares,
        'birth_rate_pumas'  : birth_rate_pumas,
        'death_rate_pumas'  : death_rate_pumas,
        'diffusion_rate_pumas'  : diffusion_rate_pumas,
        'time_step_size' : time_step_size,
        'time_step_number'  : time_step_number,
        'duration'  : duration,
        'landscape_file' : landscape_file,
        'hseed' : hseed,
        'pseed' : pseed,
    }

def create_simulation_landscape(simulation_args):
    """
    Creates a landscape represented by a numpy array, via reading in a
    landscape file and generates variables to represent the dimensions
    of the landscape.

    :param simulation_args: simulation_args
    :type simulation_args: dict
    :return: grid_dimensions, landscape
    :rtype: tuple
    """
    with open(simulation_args['landscape_file'],"r") as file_object:
        # Read in the width and height from the landscape file, which is given
        # by the first line of the file
        width, height =[int(i) for i in file_object.readline().split(" ")]

        print("Width: {} Height: {}".format(width, height))

        # Create a grid of zeroes to represent the landscape, adding a
        # "halo" around the edges by adding two to the width and height
        # to represent water around the land.
        width_including_halo = width + 2
        height_including_halo = height + 2
        landscape = np.zeros((height_including_halo, width_including_halo), 
                            int)

        # Read in the lines of the landscape file starting from the second row
        # as the first row contains a hole row of water squares, as does the 
        # final row, as shown below.
        row = 1
        for line in file_object.readlines():
            values = line.split(" ")
            # Pad the start and end of each row with zero
            # to encircle the "land" squares with the "halo" 
            # or water squares mentioned previously.
            landscape[row] = [0] + [int(i) for i in values] + [0]
            row += 1
            # The result will have the form:
            #    0 0 0 0 0 0 0 0 0 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 1 1 1 1 1 1 1 1 0
            #    0 0 0 0 0 0 0 0 0 0

    grid_dimensions = [width, height, width_including_halo, 
                    height_including_halo]

    return grid_dimensions, landscape

def get_width(grid_dimensions):
    """
    Returns the width of the landscape.
    
    :param grid_dimensions: grid_dimensions
    :type grid_dimensions: list of type int
    :return: width
    :rtype: int
    """
    return grid_dimensions[0]

def get_height(grid_dimensions):
    """
    Returns the height of the landscape.

    :param grid_dimensions: grid_dimensions
    :type grid_dimensions: list of type int
    :return: height
    :rtype: int
    """
    return grid_dimensions[1]

def get_width_including_halo(grid_dimensions):
    """
    Returns the width of the landscape including 
    the water or "halo" squares.

    :param grid_dimensions: grid_dimensions
    :type grid_dimensions: list of type int
    :return: width including halo
    :rtype: int
    """
    return grid_dimensions[2]

def get_height_including_halo(grid_dimensions):
    """
    Returns the height of the landscape including 
    the water or "halo" squares.

    :param grid_dimensions: grid_dimensions
    :type grid_dimensions: list of type int
    :return: height including halo
    :rtype: int
    """
    return grid_dimensions[3]

def calculate_number_land_only_squares(landscape):
    """
    Determines the number of squares in the simulation landscape whihc are not
    water or "halo" squares.

    :param landscape: landscape
    :type landscape: ndarray
    :return the number of squares in the landscape which are not water or 
    "halo" squares
    :rtype: int
    """
    return np.count_nonzero(landscape)
    
def create_land_neighbours_grid(grid_dimensions, landscape):
    """
    Creates a grid represented by a numpy array which corresponds to the
    simulation landscape, storing the number of land neighbours of each square
    of the landscape.

    :param grid_dimensions: grid_dimensions
    :type grid_dimensions: list of type int
    :param landscape: landscape
    :type landscape: ndarray
    :return a grid representing the number of land neighbours
    :rtype: ndarray
    """

    # Get the individual grid dimensions required.
    width = get_width(grid_dimensions)
    height = get_height(grid_dimensions)
    width_including_halo = get_width_including_halo(grid_dimensions)
    height_including_halo = get_height_including_halo(grid_dimensions)

    # Determine how many squares in the landscape are not water or "halo" 
    # squares and print the result
    number_land_only_squares = calculate_number_land_only_squares(landscape)
    print("Number of land-only squares: {}".format(number_land_only_squares))

    # Pre-calculate number of land neighbours of each land square.
    land_neighbours = np.zeros((height_including_halo, width_including_halo), 
                                int)

    # Loop through each row and column of the landscape, determining how 
    # many land neighbours each square of the landscape has. 
    # In other words how many of the squares immediately above, below, left 
    # and right of each square are land and not water.
    for x in range(1, height + 1):
        for y in range(1, width + 1):
            land_neighbours[x, y] = landscape[x-1, y] \
                + landscape[x+1, y] \
                + landscape[x, y-1] \
                + landscape[x, y+1]

    return land_neighbours

def calculate_number_hares(grid_dimensions, landscape, simulation_args):
    """
    Creates a grid to represent the population density of hares within
    the simulation landscape, assigning a number of hares to each square of
    the landscape with a value between 0 and 5.0.

    :param grid_dimensions: grid_dimensions
    :type grid_dimensions: list of type int
    :param landscape: landscape
    :type landscape: ndarray
    :param simulation_args: simulation_args
    :type simulation_args: dict
    :return: grid representing the number of hares in the landscape
    :rtype: ndarray
    """
    # Get the individual grid dimensions required.
    width = get_width(grid_dimensions)
    height = get_height(grid_dimensions)

    # Create a copy of the simulation landscape to represent
    # the hare population density.
    number_of_hares = landscape.astype(float).copy()

    # Use the hseed simulation argument to produce a random number which will
    # represent the initial number of hares in the landscape.
    random.seed(simulation_args['hseed'])

    # Loop through the grid representing the hare population density.
    for x in range(1, height + 1):
        for y in range(1, width + 1):
            # Check if the value for initial number of hares in the landscape
            # is equal to zero.
            if simulation_args['hseed'] == 0:
                # If the initial number of hares in the landscape is zero,
                # then set the number of hares in the current square to zero.
                number_of_hares[x, y] = 0
            else:
                # If the value for initial number of hares in the landscape is
                # non-zero then check that the current square of the landscape
                # is also non-zero and hence a land square rather than a water
                # square.
                if landscape[x, y]:
                    # If the current square of the landscape is non-zero and 
                    # hence a land square, then set the number of hares in the
                    # current landscape square to a random number between 0
                    # and 5.0.
                    number_of_hares[x, y] = random.uniform(0,5.0)
                else:
                    # If the current square of the landscape is zero and hence
                    # a water square then set the number of hares in the 
                    # current landscape square to zero, since hares and pumas
                    # in the simulation are assumed to be unable to swim.
                    number_of_hares[x, y] = 0

    return number_of_hares

def calculate_number_pumas(grid_dimensions, landscape, simulation_args):
    """
    Creates a grid to represent the population density of pumas within
    the simulation landscape, assigning a number of pumas to each square of
    the landscape with a value between 0 and 5.0.
    
    :param grid_dimensions: grid_dimensions
    :type grid_dimensions: list of type int
    :param landscape: landscape
    :type landscape: ndarray
    :param simulation_args: simulation_args
    :type simulation_args: dict
    :return grid representing the number of pumas in the landscape
    :rtype: ndarray
    """
    # Get the individual grid dimensions required.
    width = get_width(grid_dimensions)
    height = get_height(grid_dimensions)

    # Create a copy of the simulation landscape to represent 
    # the puma population density.
    number_of_pumas = landscape.astype(float).copy()

    # Use the hseed simulation argument to produce a random number which will
    # represent the initial number of pumas in the landscape.
    random.seed(simulation_args['pseed'])

    # Loop through the grid representing the hare population density.
    for x in range(1, height + 1):
        for y in range(1, width + 1):
            # Check if the value for initial number of pumas in the landscape
            # is equal to zero.
            if simulation_args['pseed'] == 0:
                # If the initial number of pumas in the landscape is zero,
                # then set the number of pumas in the current square to zero.
                number_of_pumas[x, y] = 0
            else:
                # If the value for initial number of pumas in the landscape is
                # non-zero then check that the current square of the landscape
                # is also non-zero and hence a land square rather than a water
                # square.
                if landscape[x,y]:
                    # If the current square of the landscape is non-zero and 
                    # hence a land square, then set the number of pumas in the
                    # current landscape square to a random number between 0
                    # and 5.0.
                    number_of_pumas[x, y] = random.uniform(0,5.0)
                else:
                    # If the current square of the landscape is zero and hence
                    # a water square then set the number of pumas in the 
                    # current landscape square to zero, since hares and pumas
                    # in the simulation are assumed to be unable to swim.
                    number_of_pumas[x, y] = 0
    
    return number_of_pumas

def create_grid_copies(grid_dimensions, number_of_hares, number_of_pumas):
    """
    Creates copies of the landscape grids representing the population 
    densities of hares and pumas for use in successive iterations of the
    simulation.
    
    :param grid_dimensions: grid_dimensions
    :type grid_dimensions: list of type int
    :param number_of_hares: number_of_hares
    :type number_of_hares: ndarray
    :param number_of_pumas: number_of_pumas
    :type number_of_pumas: ndarrays
    :return: a copy of the population densities of hares and columns and grids
    to represent the columns which hold hares and pumas.
    :rtype: tuple
    """

    # Get the individual grid dimensions required.
    width = get_width(grid_dimensions)
    height = get_height(grid_dimensions)

    # Create copies of the grids representing hare and puma population 
    # densities, for use in calculating the new populations.
    number_of_new_hares = number_of_hares.copy()
    number_of_new_pumas = number_of_pumas.copy()

    # Create grids of zeroes with identical dimensions to the landscape, to 
    # represent the columns which hold hares and pumas.
    hare_columns = np.zeros((height, width), int)
    puma_columns = np.zeros((height, width), int)

    return (number_of_new_hares, number_of_new_pumas, 
        hare_columns, puma_columns)

def calculate_averages(number_of_hares, number_of_pumas, 
                    number_land_only_squares):
    """
    Calculates the average number of hares and pumas in the landscape.
    
    :param number_of_hares: number_of_hares
    :type number_of_hares: ndarray
    :param number_of_pumas: number_of_pumas
    :type number_of_pumas: ndarray
    :param number_land_only_squares: number_land_only_squares
    :type number_land_only_squares: int
    :return: average number of hares and pumas
    :rtype: tuple
    """
    # Calculate the average number of hares and pumas per square of the 
    # landscape.
    # If the number of squares which are land and not water doesn't equal zero
    # then the average is calculated, however if all the squares are water 
    # squares, then the average number of hares and pumas is simply set to zero
    # since hares and pumas are assumed to be unable to swim in this 
    # simulation.
    if number_land_only_squares != 0:
        average_number_of_hares = (np.sum(number_of_hares) / 
                                    number_land_only_squares)
        average_number_of_pumas = (np.sum(number_of_pumas) / 
                                    number_land_only_squares)
    else:
        average_number_of_hares = 0
        average_number_of_pumas = 0

    return (average_number_of_hares, average_number_of_pumas)

def initialise_averages_file(number_of_hares, number_of_pumas, 
                            number_land_only_squares):
    """
    Print the average number of hares and pumas at the initial timestep and
    store them in the averages.csv file, initialising it.
    
    :param number_of_hares: number_of_hares
    :type number_of_hares: ndarray
    :param number_of_pumas: number_of_pumas
    :type number_of_pumas: ndarray
    :param number_land_only_squares: number_land_only_squares
    :type number_land_only_squares: int
    """
    average_number_of_hares, average_number_of_pumas = \
        calculate_averages(number_of_hares, 
                        number_of_pumas, 
                        number_land_only_squares)

    # Print the first line of averages for the hares and pumas at the initial
    # time step.
    print("Averages. Timestep: {} Time (s): {} Hares: {} Pumas: {}"\
        .format(0,0, average_number_of_hares, average_number_of_pumas))
    
    # Write a file header to the averages.csv file, representing the data 
    # which will be written to it.
    with open("averages.csv", "w") as file_object:
        file_header = "Timestep,Time,Hares,Pumas\n"
        file_object.write(file_header)

def calculate_total_number_time_steps(simulation_args):
    """
    Calculates the total number of time steps.
    
    :param simulation_args: simulation_args
    :type simulation_args: dict
    :return: total time per time step
    :rtype: int
    """
    return int(simulation_args['duration'] / simulation_args['time_step_size'])

def display_averages(i, simulation_args, average_number_of_hares, 
                average_number_of_pumas):
    """
    Displays the average number of hares and pumas at the present timestep.

    :param i: i
    :type i: int
    :param simulation_args: simulation_args
    :type simulation_args: dict
    :param average_number_of_hares: average_number_of_hares
    :type average_number_of_hares:  int
    :param average_number_of_pumas: average_number_of_pumas
    :type average_number_of_pumas:  int
    """
    print(("Averages. Timestep: {} Time (s): {} Hares: {} Pumas: {}") \
            .format(i, i*simulation_args['time_step_size'], 
                average_number_of_hares, average_number_of_pumas))

def append_averages_to_file(i, simulation_args, average_number_of_hares, 
                        average_number_of_pumas):
    """
    Appends the average number of hares and pumas and the corresponding
    timestep and time in seconds to the averages.csv file.
    
    :param i: i
    :type i: int
    :param simulation_args: simulation_args
    :type simulation_args: dict
    :param average_number_of_hares: average_number_of_hares
    :type average_number_of_hares:  int
    :param average_number_of_pumas: average_number_of_pumas
    :type average_number_of_pumas:  int
    """
    with open("averages.csv".format(i),"a") as file_object:
            file_object.write("{},{},{},{}\n".format(i, 
                                        i*simulation_args['time_step_size'], 
                                        average_number_of_hares, 
                                        average_number_of_pumas))

def generate_hare_and_puma_columns(width, height, max_number_hares, 
            number_of_hares, max_number_pumas, number_of_pumas, landscape, 
            hare_columns, puma_columns):
    """
    Generates columns of hare and puma population values to be written to
    map files.
    
    :param width: width
    :type width: int
    :param height: height
    :type height: int
    :param max_number_hares: max_number_hares
    :type max_number_hares: int
    :param number_of_hares: number_of_hares
    :type number_of_hares: ndarray
    :param max_number_pumas: max_number_pumas
    :type max_number_pumas:  int
    :param number_of_pumas: number_of_pumas
    :type number_of_pumas: ndarray
    :return: hare_columns and puma_columns
    :rtype: tuple
    """
    # Loop through the landscape.
    for x in range(1, height + 1):
            for y in range(1, width + 1):
                # Check if the current landscape square is non-zero and 
                # hence a land square rather than a water square
                if landscape[x,y]:
                    # If the current landscape square is a land square then
                    # check that the maximum number of hares is non-zero.
                    if max_number_hares != 0:
                        # If the maximum number of hares is non-zero then
                        # calculate the value of hare_column
                        hare_column = (number_of_hares[x, y] / 
                        max_number_hares) * 255
                    else:
                        # If the maximum number of hares is zero then
                        # hare_column is set to zero.
                        hare_column = 0

                    # If the current landscape square is a land square then
                    # check that the maximum number of pumas is non-zero.
                    if max_number_pumas != 0:
                        # If the maximum number of pumas is non-zero then
                        # calculate the value of puma_column
                        puma_column = (number_of_pumas[x, y] / 
                                            max_number_pumas) * 255
                    else:
                        # If the maximum number of pumas is zero then
                        # puma_column is set to zero.
                        puma_column = 0

                    # Set the values of hare_columns and puma_columns at the 
                    # current value of [x, y] to the value calculated for
                    # hare_column and puma_column in the current iteration.
                    hare_columns[x-1, y-1] = hare_column
                    puma_columns[x-1, y-1]= puma_column

    return hare_columns, puma_columns

def write_columns_to_map_files(i, width, height, landscape, hare_columns, 
                            puma_columns):
    """
    Writes columns of hare and puma population data to map files which
    visualise density of hares and pumas and water-only squares.
    
    :param i: i
    :type i: int
    :param width: width
    :type width: int
    :param height: height
    :type height: int
    :param landscape: landscape
    :type landscape: ndarray
    :param hare_columns: hare_columns
    :type hare_columns: ndarray
    :param puma_columns: puma_columns
    :type puma_columns: ndarray
    """
    # Open a file of the form map_{<4 figure form of the current time step>} 
    # in write mode.
    with open("map_{:04d}.ppm".format(i), "w") as file_object:
            # Write a file header to the map file, containing the width and 
            # height of the simulation landscape.
            file_header="P3\n{} {}\n{}\n".format(width, height, 255)
            file_object.write(file_header)

            # Loop through the simulation landscape.
            for x in range(0, height):
                for y in range(0, width):
                    # Check if the current square of the simulation landscape
                    # is nonzero and hence a land square rather than a water
                    # square.
                    if landscape[x+1, y+1]:
                        # If the current landscape square is a land square then
                        # write the values of the corresponding hare and puma
                        # columns to the map file along with a zero to signify
                        # that it is a land square containing hare and puma
                        # columns values.
                        file_object.write("{} {} {}\n"\
                            .format(hare_columns[x, y], puma_columns[x, y], 0))
                    else:
                        # If the current landscape square is a water square
                        # then write zeros, in place of the corresponding hare
                        # and puma columns, along with the number 255, to 
                        # signify that it is a water square not containing 
                        # hare and puma columns values.
                        file_object.write("{} {} {}\n".format(0, 0, 255))

def swap_array_for_next_iteration(number_of_hares, number_of_pumas, 
            number_of_new_hares, number_of_new_pumas):
    """
    Switches the old population densities of hares and pumas with the new 
    population densities of hares and pumas, in preparation for calculating
    the new population at the next timestep of the simulation.
    
    :param number_of_hares: number_of_hares
    :type number_of_hares: ndarray
    :param number_of_pumas: number_of_pumas
    :type number_of_pumas: ndarray
    :param number_of_new_hares: number_of_new_hares
    :type number_of_new_hares: ndarray
    :param number_of_new_pumas: number_of_new_pumas
    :type number_of_new_pumas: ndarray
    """
    tmp = number_of_hares
    number_of_hares = number_of_new_hares
    number_of_new_hares = tmp
    tmp = number_of_pumas
    number_of_pumas = number_of_new_pumas
    number_of_new_pumas = tmp

def calculate_the_number_of_new_hares_and_pumas(width, height, landscape, 
            number_of_new_hares, number_of_hares, number_of_new_pumas, 
            number_of_pumas, simulation_args, land_neighbours):
    """
    Calculates the number of new hares and pumas using the numerical 
    approximations of the partial differential equations used to model the 
    behaviour of pumas and hares within a landscape.
    
    :param width: width
    :type width: int
    :param height: height
    :type height: int
    :param landscape: landscape
    :type landscape: ndarray
    :param number_of_new_hares: number_of_new_hares
    :type number_of_new_hares: ndarray
    :param number_of_hares: number_of_hares
    :type number_of_hares: ndarray
    :param number_of_new_pumas: number_of_new_pumas
    :type number_of_new_pumas: ndarray
    :param number_of_pumas: number_of_pumas
    :type number_of_pumas: ndarray
    :param simulation_args: simulation_args
    :type simulation_args: dict
    :param land_neighbours: land_neighbours
    :type land_neighbours: ndarray
    :return: the number of new hares and pumas
    :rtype: tuple
    """
    # Loop through the simulation landscape.
    for x in range(1, height + 1):
        for y in range(1, width + 1):
            # Check that the current landscape square is non-zero, hence a
            # land square and not a water square.
            if landscape[x,y]:
                # If the current landscape square is a land square, then
                # calculate the new number of hares and pumas in the landscape, 
                # using the numerical approximations of the partial 
                # differential equations used to model the behaviour of pumas 
                # and hares within a landscape.
                number_of_new_hares[x, y] = (number_of_hares[x, y] + 
                        simulation_args['time_step_size'] * 
                        (simulation_args['birth_rate_hares'] * 
                        number_of_hares[x, y]) - 
                        (simulation_args['death_rate_hares'] * 
                        number_of_hares[x, y] * 
                        number_of_pumas[x, y]) + 
                        simulation_args['diffusion_rate_hares'] *
                        ((number_of_hares[x-1, y] +
                        number_of_hares[x+1, y] + 
                        number_of_hares[x, y-1] 
                        + number_of_hares[x, y+1]) - 
                        (land_neighbours[x, y] * 
                        number_of_hares[x, y])))

                # Check if the number of new hares calculated is less than 
                # zero.
                if number_of_new_hares[x, y] < 0:
                    # If the number of new hares is less than zero then set
                    # the number of new hares in the current landscape square
                    # to zero.
                    number_of_new_hares[x, y] = 0

                number_of_new_pumas[x, y] = (number_of_pumas[x, y] + 
                            simulation_args['time_step_size'] * 
                            ((simulation_args['birth_rate_pumas'] * 
                            number_of_hares[x, y] * number_of_pumas[x, y]) - 
                            (simulation_args['death_rate_pumas'] * 
                            number_of_pumas[x, y]) + 
                            simulation_args['diffusion_rate_pumas'] * 
                            ((number_of_pumas[x-1, y] 
                            + number_of_pumas[x+1, y] + 
                            number_of_pumas[x, y-1] 
                            + number_of_pumas[x, y+1]) - 
                            (land_neighbours[x, y] * 
                            number_of_pumas[x,y]))))
                
                # Check if the number of new pumas calculated is less than 
                # zero.
                if number_of_new_pumas[x, y] < 0:
                    # If the number of new pumas is less than zero then set
                    # the number of new pumas in the current landscape square
                    # to zero.
                    number_of_new_pumas[x, y] = 0

    return number_of_new_hares, number_of_new_pumas