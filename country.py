from __future__ import annotations

import numpy

import matplotlib

import warnings

from dataclasses import dataclass

from typing import TYPE_CHECKING, List, Optional

from plotting_utilities import plot_country, plot_path

if TYPE_CHECKING:
    from pathlib import Path

    from matplotlib.figure import Figure


def travel_time(
    distance,
    different_regions,
    locations_in_dest_region,
    speed=4.75,
):
    """
    Computes the time taken to travel between two locations, seperated by 'distance' meters, travelling at 'speed' meters per second. 
    Taking into account delays due to interregional border control by the factor (1+('different_regions'*'locations_in_dest_region')/10).
    """
    #Function represents the equation 't = (D/3600S)(1+RN/10)'.
    #Note: 'speed' has a default value of 4.75 m/s.
    #Where D is 'distance' [m, float], S is 'speed' [m/s, float], R is 'different_regions' [N/A, bool] and N is 'locations_in_dest_region' [N/A, int].
    
    #If 'distance' or 'speed' are integer values, convert them into floats
    if type(distance) is int:
        distance = float(distance)
    if type(speed) is int:
        speed = float(speed)

    #Check input types
    if type(distance) is not float:
        raise TypeError("'distance' should be a float or integer value.")
    if type(speed) is not float:
        raise TypeError("'speed' should be a float or integer value.")
    if type(different_regions) is not bool:
        raise TypeError("'different_regions' should he a boolean value.")
    if type(locations_in_dest_region) is not int:
        raise TypeError("'locations_in_dest_region' should be an integer value.")

    #Check input values
    if distance<0:
        raise ValueError("'distance' should be a positive value.")
    if distance==0 and different_regions is True:
        raise ValueError("If 'different regions' is True, then distance cannot be zero and visa versa.")
    if distance==0 and different_regions is False and locations_in_dest_region !=1:
        raise ValueError("If 'distance' is zero and 'different_regions' is false, then 'locations_in_dest_region' must be one.")
    if distance!=0 and different_regions is False and locations_in_dest_region ==1:
        raise ValueError("If 'locations_in_dest_region' is one and 'different_regions' is false, then 'distance' must be zero.")
    if distance==0 and different_regions is True and locations_in_dest_region ==1:
        raise ValueError("If 'distance' is zero and 'locations_in_dest_region' is one, then 'locations_in_dest_region' must be one.")    
    if speed<=0:
        raise ValueError("'speed' should be a positive, non-zero value for a finite time to be calculated.")
    if locations_in_dest_region<1:
        raise ValueError("'locations_in_dest_region' should be a positive value, greater than or equal to 1.")
    
    #Implementation of travel time function
    one_hour_distance = 3600*speed
    optimal_time = distance/(one_hour_distance)
    time=optimal_time*(1+(different_regions*locations_in_dest_region)/10)
    
    #Check the final value of 'time' is greater than or equal to zero and therefore a valid travel time
    if time<0:
        raise ValueError("'time' has returned as a negative value")
    
    return time

def capitalisation_of_strings(string):
        """Reformats a string, capitalising the first letter of each word only."""
        cap_string = ""
        string = string.lower()
        string = string.strip()
        list_of_words_plus_whitespace = string.split(" ")
        list_of_words =[list_of_words_plus_whitespace[i] for i in range(len(list_of_words_plus_whitespace)) if list_of_words_plus_whitespace[i] != ""]
        list_of_stripped_words = [list_of_words[i].strip() for i in range(len(list_of_words))]
        words_first_letter = [list_of_stripped_words[i][0] for i in range(len(list_of_stripped_words))]
        words_without_first_letter = [list_of_stripped_words[i][1:] for i in range(len(list_of_stripped_words))]
        for j in range(len(words_first_letter)):
            words_first_letter[j] = words_first_letter[j].upper()
        cap_words= [words_first_letter[i] + words_without_first_letter[i] for i in range(len(words_first_letter))]
        for k in range(len(cap_words)-1):
            cap_string = cap_string + cap_words[k]+" "
        cap_string = cap_string+ cap_words[len(cap_words)-1]
            
        return(cap_string)

def rounding_correction(x):
    """Rounding function to round the input to two decimal places correctly and overwrite the 'numpy.round' methods 'even-rounding' preference."""
    decimal_factor = 100 #10**2 To round to 2 decimal places.
    if type(x) is float:    
        if x > 0:
            return float(numpy.floor(x*decimal_factor+0.5))/decimal_factor 
        else:
            return float(numpy.ceil(x*decimal_factor-0.5))/decimal_factor
    else:
        raise TypeError("The input to 'rounding correction' should be a float value.")

@dataclass
class Location:
    """Class for creating location objects with attributes containing name, region, depot status and location data."""
    name : str
    region : str
    r : float
    theta : float
    depot : bool
    def __repr__(self):
        """
        Do not edit this function.
        You are NOT required to document or test this function.

        Not all methods of printing variable values delegate to the
        __str__ method. This implementation ensures that they do,
        so you don't have to worry about Locations not being formatted
        correctly due to these internal Python caveats.
        """
        return self.__str__()
    
    def __init__(self,name:str,region:str,r,theta,depot:bool):
        """Initialisation of a 'Location' object, with attributes 
        'name' [N/A, str], 
        'region' [N/A, str], 
        'r' [m, float], 
        'theta' [rad, float] 
        'depot' [N/A, bool]"""

        #Handling 'r' and 'theta' inputs

        if isinstance(r, float) is True or isinstance(r, int) is True:
            if r<0:
                raise ValueError("'r' should have a value greater than or equal to zero.")
            else:
                self.r = float(r)
        else:
            raise TypeError("'r' should be inputted as an integer or floating point number.")


        if isinstance(theta, float) is True or isinstance(theta, int) is True:
            if theta<-numpy.pi or theta>numpy.pi:
                raise ValueError("'theta' should have a value between, or equal to, negative pi and positive pi.")
            else:
                self.theta = float(theta)
        else:
            raise TypeError("'theta' should be inputted as an integer or floating point number.")
        
        
        #Handling and setting 'depot' input

        if type(depot) is not bool:
            raise TypeError("'depot' should be a boolean value.")
        else:
            self.depot = depot
        
        #Handling and setting 'name' and 'region' inputs

        if type(name) is not str:
            raise TypeError("'name' should be a string.")
        
        if type(region) is not str:
            raise TypeError("'region' should be a string.")
        
        #if name or region are not already in the correct form
        temp_name = capitalisation_of_strings(name)
        if name != temp_name:
            self.name = temp_name
            warnings.warn("Location names should have the first character of each word capitalised, no excess whitespace and no additional and only one whitespace character between each word. The input has been reformatted to fit this regime.")
        else:
            self.name = name
        

        temp_region = capitalisation_of_strings(region)
        if region != temp_region:
            self.region = temp_region
            warnings.warn("Region names should have the first character of each word capitalised, no excess whitespace and no additional and only one whitespace character between each word. The input has been reformatted to fit this regime.")
        else:
            self.region = region

    #Equity operator between two 'Location' objects.
    def __eq__(self, other):
        """Overloading the comparison operator '==' to compare the 'name' and 'region' attributes of two 'Location' objects."""
        if type(other) is not Location:
            raise TypeError("The other location parameter should be a 'Location' object.")
        else:
            self_list = [self.name, self.region]
            other_list = [other.name, other.region]
            if self_list == other_list:
                return True
            else:
                return False
            
    def __hash__(self) -> str:
        return hash(self.name + self.region)

    #Method to return an objects attributes 'r' and 'theta'.
    def __getattributes_r_theta__(self):
        """Returns an objects attributes 'r' and 'theta' as a tuple '(r,theta)'."""
        tuple_r_theta = (self.r,self.theta)
        return tuple_r_theta

    #Helper function to create the 'settlement' property, as well as maintain consitency between the 'depot' attribute and the 'settlement' property.
    def _get_settlement(self):
        """Given the bool value of the 'depot' attribute, returns the desired value of the 'settlement' property."""
        if self.depot is False:
            return True
        elif self.depot is True:
            return False
        else: 
            raise TypeError("'depot' should be a boolean value to create the settlement property.")
    
    #The 'settlement' property. Always the boolean negation of the depot attribute.
    settlement = property(fget = _get_settlement, fset = None, fdel = None, doc = "A boolean property representing whether the Location object is a settlement or not.")
        
    

    def __str__(self):
        """Alters the output of the 'print' function when called on a 'Location' object to display its attributes in a user friendly format."""
        if self.depot is True:
            location_type_string = " [depot] "
        elif self.depot is False:
            location_type_string = " [settlement] "
        else:
            raise TypeError("'depot' should be a boolean value.")
        theta_in_pi = self.theta/numpy.pi #'theta' in units of pi
        if numpy.floor(theta_in_pi *100)%2 == 0 and str(int(numpy.floor(theta_in_pi *1000)))[-1] == "5":
            theta_rounded = rounding_correction(theta_in_pi)
        else:
            theta_rounded= numpy.round(theta_in_pi,2)
        location_string = self.name + location_type_string + "in " + self.region + " @ (" +str(self.r) +"m, "+str(theta_rounded)+"pi)"
        return location_string


    def distance_to(self, other):
        """Calculates the distance between two location objects using their polar co-ordinates '(r,theta)'.
        The calculated distance is in the units of the polar radial co-ordinates 'r' of the objects passed into the method, meters."""
        
        if type(other) is not Location:
            raise TypeError("The other location parameter should be a 'Location' object.")
        else:
            #Calculating the distance using the formula: d = sqrt(r1^2 + r2^2 - 2r1r2 cos(theta1-theta2)).
            other_attributes = other.__getattributes_r_theta__()
            other_r = other_attributes[0]
            other_theta = other_attributes[1]
            calculated_distance = numpy.sqrt(self.r**2 + other_r**2 - 2*self.r*other_r * numpy.cos(self.theta - other_theta))
            calculated_distance = float(calculated_distance)
        
        return calculated_distance


@dataclass
class Country:
    """A class for creating country objects, containing multiple locations where each location is an instance of the 'Location' class.
    Has the attribute '_all_locations', a tuple containing the 'Location' objects."""
    _all_locations : tuple

    def __init__(self, list_of_locations):
        """Initialisation of a 'Country' object with the attribute '_all_locations' containing a tuple of 'Location' objects."""
        if type(list_of_locations) is not list:
            raise TypeError("The input parameter should be a list of 'Location' objects.")
        else:
            for i in range(len(list_of_locations)):
                if isinstance(list_of_locations[i], Location) is False:
                    raise TypeError("The inputted list should have 'Location' objects as its elements.")
                else:
                    index_list = [index for index in range(len(list_of_locations)) if index != i]
                    for j in index_list:
                        if list_of_locations[i] == list_of_locations[j]:
                            raise ValueError("There exists duplicate 'Location' objects in the inputted list.")
            self._all_locations = tuple(list_of_locations)


    #Settlements property.
    def _get_settlements(self):
        """Given a country object with attribute '_all_locations' containing a list of 'Location' objects, returns the list of 'Location' objects with a 'True' 'settlement' property."""
        list_of_settlements = []
        for location in self._all_locations:
            if type(location.settlement) is not bool:
                raise TypeError("The 'settlement' property of the 'Location' objects in the '_all_locations' attribute should be boolean values.")
            elif location.settlement is True:
                list_of_settlements.append(location)
        return list_of_settlements
    settlements = property(fget=_get_settlements, fset=None ,fdel=None, doc="A list property containing the 'Location' objects with a 'True' 'settlement' property.")

    #n_settlements property.
    def _get_n_settlements(self):
        """Given a country object with attribute '_all_locations' containing a list of 'Location' objects, returns the length of the list of 'Location' objects with a 'True' 'settlement' property."""
        len_settlements_list = len(self.settlements)
        return len_settlements_list
    n_settlements = property(fget=_get_n_settlements,fset = None,fdel = None, doc = "An integer property containing the number or 'Location' objects with a 'True' 'settlement' property.")


    #Depots property.
    def _get_depots(self):
        """Given a country object with attribute '_all_locations' containing a list of 'Location' objects, returns the list of 'Location' objects with a 'True' 'depot' property."""
        list_of_depots = []
        for location in self._all_locations:
            if type(location.depot) is not bool:
                raise TypeError("The 'depot' attribute of the 'Location' objects in the '_all_locations' attribute should be boolean values.")
            elif location.depot is True:
                list_of_depots.append(location)
        return list_of_depots
    depots = property(fget=_get_depots, fset=None ,fdel=None, doc="A list property containing the 'Location' objects with a 'True' 'depot' property.")

    #n_depots property.
    def _get_n_depots(self):
        """Given a country object with attribute '_all_locations' containing a list of 'Location' objects, returns the length of the list of 'Location' objects with a 'True' 'depot' property."""
        len_depots_list = len(self.depots)
        return len_depots_list
    n_depots = property(fget=_get_n_depots,fset = None,fdel = None, doc = "An integer property containing the number or 'Location' objects with a 'True' 'depot' property.")



    def travel_time(self, start_location, end_location):
        """Calculates the travel time between two locations represented by 'Location' objects, within a 'Country' object, using the 'travel_time' function. Returns the travel time in hours."""
        #Raise value errors if one, or both, of arguments are not elements of the 'Country' objects '_all_locations' attribute or 'Location' objects at all.
        if isinstance(start_location, Location) is False or isinstance(end_location, Location) is False:
            raise TypeError("Arguments of the 'travel_time' method should be 'Location' objects.")
        elif start_location not in self._all_locations:
            raise ValueError("Arguments of the 'travel_time' method should be 'Location' objects in the 'Country' objects '_all_locations' attribute.")
        elif end_location not in self._all_locations:
            raise ValueError("Arguments of the 'travel_time' method should be 'Location' objects in the 'Country' objects '_all_locations' attribute.")
        
        #Gather attributes of the 'Country' and 'Locations' classes to pass into the 'travel_time' function.
        distance = start_location.distance_to(end_location)
        if start_location.region == end_location.region:
            different_region = False
        else:
            different_region = True

        locations_in_dest_region = 0
        for location in self._all_locations:
            if location.region == end_location.region:
                locations_in_dest_region +=1

        time = travel_time(distance,different_region,locations_in_dest_region)
        return time

    def fastest_trip_from(
        self,
        current_location,
        potential_locations = None,
    ):
        """Calculates the minimum travel time needed to reach anpther location given an initial location 'Location' object as the first argument and a list of potential destination 'Location' objects as the second argument.
        In the event of tie breaks in travel time, the location with the lower alphabetical name will be chosen and in the event of further ties, the location with the lower alphabetical region will be chosen."""
        #Setting the defualt argument for the 'potential_locations' argument.
        if potential_locations is None:
            potential_locations = self.settlements
        elif potential_locations == []:
            return (None, None)

        #Dealing with integer elements of the argument 'potential_locations'.
        i = 0
        time_list = []
        for location in potential_locations:
            if isinstance(location, Location) is True and location not in self.settlements:
                raise ValueError("An element of 'potential_locations' is not an element of the 'Country' objects 'settlements' property.")
            elif isinstance(location, int) is True:
                if location in range(len(self.settlements)):
                    location = self.settlements[location]
                else:
                    raise ValueError("An integer element of 'potential_locations' is an out of bounds index for the 'Country' objects 'settlements' property.")
            i +=1
            #Calculating the travel time between each 'potential_location' and 'current_location'.
            time_list.append(self.travel_time(current_location, location))
        
        #Dealing with potential tie-breaks in travel time, name and region by alphabetical order.
        min_time = min(time_list)
        duplicates = [item for item in potential_locations if self.travel_time(current_location, item) == min_time]
        duplicate_time_num = len(duplicates)
        if duplicate_time_num != 1:
            names = [item.name for item in duplicates]
            min_name = min(names)
            duplicate_names = [item for item in duplicates if item.name == min_name]
            duplicate_name_num = len(duplicate_names)
            if duplicate_name_num != 1:
                regions = [item.region for item in potential_locations if item.name in names and self.travel_time(current_location,item) == min_time]
                min_region = min(regions)
                min_location = [location for location in potential_locations if location.name == min_name and location.region == min_region]
            else:
                min_location = [location for location in potential_locations if location.name == min_name and self.travel_time(current_location, location) == min_time]
        else:
            min_location = duplicates
        min_location = min_location[0]
        fastest_trip_tuple = (min_location, self.travel_time(current_location, min_location))
        return fastest_trip_tuple
        

        


    def nn_tour(self, starting_depot):
        """Computes the neares neighbor algorithm for the settlements in the 'settlements' property of the 'Country' object, starting from a depot 'Location' object passed as the argument.
        Returns a tuple where the first element is the list of locations, in order, of the tour, with start and end locations being the argument depot location. The second element is the total time of the tour, calculated by the 'travel_time' method of the 'Country' class."""
        tour = [starting_depot]
        if len(self.settlements) == 0:
            tour = 0
            tour_time = 0
        else:
            tour_time = 0
            unvisited = [[location, True] for location in self.settlements]
            unvisited_loc = [location[0] for location in unvisited]
            current_location = starting_depot
            for location in unvisited:
                next_stop = self.fastest_trip_from(current_location, unvisited_loc)    
                tour.append(next_stop[0])
                tour_time = tour_time + next_stop[1]
                current_location = next_stop[0]
                #Removing the visited settlement from the list of unvisited settlements.
                location[1] = False
                unvisited = [locations for locations in unvisited if locations[1] is True]
                unvisited_loc = [location[0] for location in unvisited]
        #Finishing the tour.
        tour_time = tour_time + self.travel_time(tour[-1], starting_depot)
        tour.append(starting_depot)
        return tour, tour_time

    def best_depot_site(self, display):
        raise NotImplementedError

    def plot_country(
        self,
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """

        Plots the locations that make up the Country instance on a
        scale diagram, either displaying or saving the figure that is
        generated.

        Use the optional arguments to change the way the plot displays
        the information.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        distinguish_regions : bool, default: True
            If True, locations in different regions will use different
            marker colours.
        distinguish_depots bool, default: True
            If True, depot locations will be marked with crosses
            rather than circles.  Their labels will also be in
            CAPITALS, and underneath their markers, if not toggled
            off.
        location_names : bool, default: True
            If True, all locations will be annotated with their names.
        polar_projection : bool, default: True
            If True, the plot will display as a polar
            projection. Disable this if you would prefer the plot to
            be displayed in Cartesian (x,y) space.
        save_to : Path, str
            Providing a file name or path will result in the diagram
            being saved to that location. NOTE: This will suppress the
            display of the figure via matplotlib.
        """
        return plot_country(
            self,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )

    def plot_path(
        self,
        path: List[Location],
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """
        Plots the path provided on top of a diagram of the country,
        in order to visualise the path.

        Use the optional arguments to change the way the plot displays
        the information. Refer to the plot_country method for an
        explanation of the optional arguments.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        path : list
            A list of Locations in the country, where consecutive
            pairs are taken to mean journeys from the earlier location to
            the following one.
        distinguish_regions : bool, default: True,
        distinguish_depots : bool, default: True,
        location_names : bool, default: True,
        polar_projection : bool, default: True,
        save_to : Path, str

        See Also
        --------
        self.plot_path for a detailed description of the parameters
        """
        return plot_path(
            self,
            path,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )