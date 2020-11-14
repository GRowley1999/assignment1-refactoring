from argparse import ArgumentParser
import numpy as np
import random
import time
import simulation_functions as sf


def sim():
    # Get command line arguments from the terminal.
    command_line_args = sf.get_command_line_arguments()

    # Store the command line arguments in a dictionary.
    simulation_args = sf.create_args_dictionary(command_line_args)

    # Create the simulation landscape as a numpy array and store the 
    # dimensions of the landscape in a list.
    grid_dimensions, landscape = \
        sf.create_simulation_landscape(simulation_args)

    # Get the individual dimensions of the landscape required for the 
    # simulation.
    width = sf.get_width(grid_dimensions)
    height = sf.get_height(grid_dimensions)

    # Calculate the number of squares in the landscape which are land squares
    # rather than water or "halo" squares.
    number_land_only_squares = \
        sf.calculate_number_land_only_squares(landscape)

    # Calculate the number of land neighbours of each square in the landscape.
    land_neighbours = \
        sf.create_land_neighbours_grid(grid_dimensions, landscape)
    
    # Create a numpy array representing the population density of hares in
    # the simulation landscape.
    number_of_hares = sf.calculate_number_hares(grid_dimensions, landscape, 
                        simulation_args)
    
    # Create a numpy array representing the population density of pumas in
    # the simulation landscape.
    number_of_pumas = sf.calculate_number_pumas(grid_dimensions, landscape, 
                        simulation_args)
    
    # Print the initial average number of hares and pumas and store them in
    # the averages.csv file.
    sf.initialise_averages_file(number_of_hares, number_of_pumas, 
                            number_land_only_squares)

    # Calculate the total number of time steps over which the simulation will 
    # be executed.
    total_times = sf.calculate_total_number_time_steps(simulation_args)

    # Initialise copies of the population densities of hares and pumas in the 
    # landscape.
    number_of_new_hares, number_of_new_pumas, hare_columns, puma_columns = \
        sf.create_grid_copies(grid_dimensions, number_of_hares, 
                            number_of_pumas)

    # Loop through all of the time steps.
    for i in range(1, total_times):
        # Check if the modulus of i and the current time step is zero.
        if not i % simulation_args['time_step_number']:
            # Calculate the maximum number of hares and pumas.
            max_number_hares = np.max(number_of_hares)
            max_number_pumas = np.max(number_of_pumas)

            # Calcualte the average numbers of hares and pumas in the 
            # landscape at the current time step.
            average_number_of_hares, average_number_of_pumas = \
                sf.calculate_averages(number_of_hares, 
                            number_of_pumas, 
                            number_land_only_squares)

            # Display the average number of hares and pumas at the present 
            # timestep.
            sf.display_averages(i, simulation_args, average_number_of_hares, 
                            average_number_of_pumas)

            # Append the average number of hares and pumas and the 
            # corresponding timestep and time in seconds to the averages.csv 
            # file.
            sf.append_averages_to_file(i, simulation_args, 
                                    average_number_of_hares, 
                                    average_number_of_pumas)

            # Generate columns of hare and puma population values to be 
            # written to map files.
            hare_columns, puma_columns = \
                sf.generate_hare_and_puma_columns(width, height, 
                                    max_number_hares, number_of_hares, 
                                    max_number_pumas, number_of_pumas, 
                                    landscape, hare_columns, puma_columns)

            # Write the columns of hare and puma population data to map files.
            sf.write_columns_to_map_files(i, width, height, landscape, 
                                        hare_columns, puma_columns)

        # Calculate the number of new hares and pumas.
        number_of_new_hares, number_of_new_pumas = \
            sf.calculate_the_number_of_new_hares_and_pumas(width, height, 
                                            landscape, number_of_new_hares, 
                                            number_of_hares, 
                                            number_of_new_pumas, 
                                            number_of_hares, simulation_args, 
                                            land_neighbours)
                                            
        # Switch the old population densities of hares and pumas with the new 
        # population densities of hares and pumas for the next iteration of
        # the simulation.
        sf.swap_array_for_next_iteration(number_of_hares, number_of_pumas, 
                                    number_of_new_hares, number_of_new_pumas)

if __name__ == "__main__":
    sim()
