__author__ = 'Marc'
# --------------------------- #
# Intro to CS Final Project   #
# Gaming Social Network       #
# --------------------------- #
#
# For students who have subscribed to the course,
# please read the submission instructions in the Instructor Notes below.
# -----------------------------------------------------------------------------

# Background
# ==========
# You and your friend have decided to start a company that hosts a gaming
# social network site. Your friend will handle the website creation (they know
# what they are doing, having taken our web development class). However, it is
# up to you to create a data structure that manages the game-network information
# and to define several procedures that operate on the network.
#
# In a website, the data is stored in a database. In our case, however, all the
# information comes in a big string of text. Each pair of sentences in the text
# is formatted as follows:
#
# <user> is connected to <user1>, ..., <userM>.<user> likes to play <game1>, ..., <gameN>.
#
# For example:
#
# John is connected to Bryant, Debra, Walter.John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.
#
# Note that each sentence will be separated from the next by only a period. There will
# not be whitespace or new lines between sentences.
#
# Your friend records the information in that string based on user activity on
# the website and gives it to you to manage. You can think of every pair of
# sentences as defining a user's profile.
#
# Consider the data structures that we have used in class - lists, dictionaries,
# and combinations of the two (e.g. lists of dictionaries). Pick one that
# will allow you to manage the data above and implement the procedures below.
#
# You may assume that <user> is a unique identifier for a user. For example, there
# can be at most one 'John' in the network. Furthermore, connections are not
# symmetric - if 'Bob' is connected to 'Alice', it does not mean that 'Alice' is
# connected to 'Bob'.
#
# Project Description
# ====================
# Your task is to complete the procedures according to the specifications below
# as well as to implement a Make-Your-Own procedure (MYOP). You are encouraged
# to define any additional helper procedures that can assist you in accomplishing
# a task. You are encouraged to test your code by using print statements and the
# Test Run button.
# -----------------------------------------------------------------------------

# network =     {
#                   userA:   {
#                               connections:    []
#                               games:      []
#                           }
#                   userB:   {
#                               connections:    []
#                               games:      []
#                           }
#               }

# Example string input. Use it to test your code.
example_input="John is connected to Bryant, Debra, Walter.\
John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
Bryant is connected to Olive, Ollie, Freda, Mercedes.\
Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
Mercedes is connected to Walter, Robin, Bryant.\
Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
Olive is connected to John, Ollie.\
Olive likes to play The Legend of Corgi, Starfleet Commander.\
Debra is connected to Walter, Levi, Jennie, Robin.\
Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.\
Walter is connected to John, Levi, Bryant.\
Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.\
Levi is connected to Ollie, John, Walter.\
Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.\
Ollie is connected to Mercedes, Freda, Bryant.\
Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.\
Jennie is connected to Levi, John, Freda, Robin.\
Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.\
Robin is connected to Ollie.\
Robin likes to play Call of Arms, Dwarves and Swords.\
Freda is connected to Olive, John, Debra.\
Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."

# -----------------------------------------------------------------------------
# parse_sentence(network, string_input):
#   Determine whether or not this is a game or connection sentence.
#   Return the result from the appropriate method
#
# Arguments:
#   network: the network object
#   string_input: block of text containing the network information
#
#   Match games on          " likes to play "
#   Match connections on    " is connected to "
#
#   if string_input is blank then return network
#
# Return:
#   network
def parse_sentence(network, string_input):
    if string_input is None or len(string_input) == 0:
        return network

    re_games = " likes to play "
    re_connections = " is connected to "
    if re_games in string_input:
        return parse_games_sentence(network, string_input)
    elif re_connections in string_input:
        return parse_friends_sentence(network, string_input)
    else:
        return network

# -----------------------------------------------------------------------------
# parse_games_sentence(network, string_input)
#   Parse out the user and the games
#   Add the user with the list of games
#
# Arguments:
#   network: the network object
#   string_input: block of text containing the network information
#
#   if string_input is blank then return network
#
# Return:
#   network
def parse_games_sentence(network, string_input):
    re_games = " likes to play "
    start_index = string_input.index(re_games)
    user = string_input[:start_index]
    games_string = string_input[start_index + len(re_games):]
    games = [game.strip() for game in games_string.split(",")]
    if user not in network:
        network = add_new_user(network, user, games)
    else:
        for game in games:
            add_game(network, user, game)
    return network

# -----------------------------------------------------------------------------
# parse_friends_sentence(network, string_input)
#   Parse out the user and the connections
#   Add each connection
#
# Arguments:
#   network: the network object
#   string_input: block of text containing the network information
#
#   if string_input is blank then return network
#
# Return:
#   network
def parse_friends_sentence(network, string_input):
    re_connections = " is connected to "
    start_index = string_input.index(re_connections)
    user = string_input[:start_index]
    friends_string = string_input[start_index + len(re_connections):]
    friends = [friend.strip() for friend in friends_string.split(",")]
    if user not in network:
        network = add_new_user(network, user, [])

    for friend in friends:
        temp = add_connection(network, user, friend)
        if temp is not None and type(temp) is dict:
            network = temp
    return network

# -----------------------------------------------------------------------------
# create_data_structure(string_input):
#   Parses a block of text (such as the one above) and stores relevant
#   information into a data structure. You are free to choose and design any
#   data structure you would like to use to manage the information.
#
# Arguments:
#   string_input: block of text containing the network information
#
#   You may assume that for all the test cases we will use, you will be given the
#   connections and games liked for all users listed on the right-hand side of an
#   'is connected to' statement. For example, we will not use the string
#   "A is connected to B.A likes to play X, Y, Z.C is connected to A.C likes to play X."
#   as a test case for create_data_structure because the string does not
#   list B's connections or liked games.
#
#   The procedure should be able to handle an empty string (the string '') as input, in
#   which case it should return a network with no users.
#
# Return:
#   The newly created network data structure
def create_data_structure(string_input, separator="."):
    lines = string_input.split(".")
    network = {}
    for line in lines:
        network = parse_sentence(network, line)
    return network

# ----------------------------------------------------------------------------- #
# Note that the first argument to all procedures below is 'network' This is the #
# data structure that you created with your create_data_structure procedure,    #
# though it may be modified as you add new users or new connections. Each       #
# procedure below will then modify or extract information from 'network'        #
# ----------------------------------------------------------------------------- #

# -----------------------------------------------------------------------------
# get_connections(network, user):
#   Returns a list of all the connections that user has
#
# Arguments:
#   network: the gamer network data structure
#   user:    a string containing the name of the user
#
# Return:
#   A list of all connections the user has.
#   - If the user has no connections, return an empty list.
#   - If the user is not in network, return None.
def get_connections(network, user):
    if user in network:
        return network[user]["connections"]
    else:
        return None

# -----------------------------------------------------------------------------
# get_games_liked(network, user):
#   Returns a list of all the games a user likes
#
# Arguments:
#   network: the gamer network data structure
#   user:    a string containing the name of the user
#
# Return:
#   A list of all games the user likes.
#   - If the user likes no games, return an empty list.
#   - If the user is not in network, return None.
def get_games_liked(network,user):
    if user in network:
        return network[user]["games"]
    else:
        return None

# -----------------------------------------------------------------------------
# add_connection(network, user_A, user_B):
#   Adds a connection from user_A to user_B. Make sure to check that both users
#   exist in network.
#
# Arguments:
#   network: the gamer network data structure
#   user_A:  a string with the name of the user the connection is from
#   user_B:  a string with the name of the user the connection is to
#
# Return:
#   The updated network with the new connection added.
#   - If a connection already exists from user_A to user_B, return network unchanged.
#   - If user_A or user_B is not in network, return False.
def add_connection(network, user_A, user_B):
    found = True
    if user_A not in network:
        network = add_new_user(network, user_A, [])
        found = False
    if user_B not in network:
        network = add_new_user(network, user_B, [])
        found = False

    if user_B not in get_connections(network, user_A):
        network[user_A]["connections"].append(user_B)
	return network if found else False

# -----------------------------------------------------------------------------
# add_game(network, user_A, game):
#   Adds a game for user_A
#
# Arguments:
#   network: the gamer network data structure
#   user_A:  a string with the name of the user the connection is from
#   game:  a string with the game to add
#
# Return:
#   The updated network with the new game added.
#   - If user_A is not in network, return False.
def add_game(network, user_A, game):
    found = True
    if user_A not in network:
        network = add_new_user(network, user_A, [])
        found = False
    network[user_A]["games"].append(game)
    return network if found else False

# -----------------------------------------------------------------------------
# add_new_user(network, user, games):
#   Creates a new user profile and adds that user to the network, along with
#   any game preferences specified in games. Assume that the user has no
#   connections to begin with.
#
# Arguments:
#   network: the gamer network data structure
#   user:    a string containing the name of the user to be added to the network
#   games:   a list of strings containing the user's favorite games, e.g.:
#		     ['Ninja Hamsters', 'Super Mushroom Man', 'Dinosaur Diner']
#
# Return:
#   The updated network with the new user and game preferences added. The new user
#   should have no connections.
#   - If the user already exists in network, return network *UNCHANGED* (do not change
#     the user's game preferences)
def add_new_user(network, user, games):
    if user in network:
        return network
    network[user] = {"connections": [], "games": games}
    return network

# -----------------------------------------------------------------------------
# get_secondary_connections(network, user):
#   Finds all the secondary connections (i.e. connections of connections) of a
#   given user.
#
# Arguments:
#   network: the gamer network data structure
#   user:    a string containing the name of the user
#
# Return:
#   A list containing the secondary connections (connections of connections).
#   - If the user is not in the network, return None.
#   - If a user has no primary connections to begin with, return an empty list.
#
# NOTE:
#   It is OK if a user's list of secondary connections includes the user
#   himself/herself. It is also OK if the list contains a user's primary
#   connection that is a secondary connection as well.
def get_secondary_connections(network, user):
    if user not in network:
        return None

    secondary = []
    for friend in network[user]["connections"]:
        secondary.extend(get_connections(network, friend))
    return list(set(secondary))

# -----------------------------------------------------------------------------
# connections_in_common(network, user_A, user_B):
#   Finds the number of people that user_A and user_B have in common.
#
# Arguments:
#   network: the gamer network data structure
#   user_A:  a string containing the name of user_A
#   user_B:  a string containing the name of user_B
#
# Return:
#   The number of connections in common (as an integer).
#   - If user_A or user_B is not in network, return False.
def connections_in_common(network, user_A, user_B):
    if user_A not in network or user_B not in network:
        return False
    user_A_conn = get_connections(network, user_A)
    user_B_conn = get_connections(network, user_B)
    matches = 0
    for friend in user_A_conn:
        if friend in user_B_conn:
            matches += 1
    return matches

# -----------------------------------------------------------------------------
# path_to_friend(network, user_A, user_B):
#   Finds a connections path from user_A to user_B. It has to be an existing
#   path but it DOES NOT have to be the shortest path.
#
# Arguments:
#   network: The network you created with create_data_structure.
#   user_A:  String holding the starting username ("Abe")
#   user_B:  String holding the ending username ("Zed")
#
# Return:
#   A list showing the path from user_A to user_B.
#   - If such a path does not exist, return None.
#   - If user_A or user_B is not in network, return None.
#
# Sample output:
#   >>> print path_to_friend(network, "Abe", "Zed")
#   >>> ['Abe', 'Gel', 'Sam', 'Zed']
#   This implies that Abe is connected with Gel, who is connected with Sam,
#   who is connected with Zed.
#
# NOTE:
#   You must solve this problem using recursion!
#
# Hints:
# - Be careful how you handle connection loops, for example, A is connected to B.
#   B is connected to C. C is connected to B. Make sure your code terminates in
#   that case.
# - If you are comfortable with default parameters, you might consider using one
#   in this procedure to keep track of nodes already visited in your search. You
#   may safely add default parameters since all calls used in the grading script
#   will only include the arguments network, user_A, and user_B.
def path_to_friend(network, user_A, user_B, path=None):
    if user_A == user_B:
        if path is not None:
            path = path + [user_A]
        return path

    if path is None:
        path = []

    path = path + [user_A]

    if not network.has_key(user_A):
        return None
    for connection in get_connections(network, user_A):
        if connection not in path:
            new_path = path_to_friend(network, connection, user_B, path)
            if new_path: return new_path
    return None

# Make-Your-Own-Procedure (MYOP)
# -----------------------------------------------------------------------------
# find_shortest_path_to_friend(network, user_A, user_B, path=None):
#   Find the shortest path between user_A and user_B
#
# Arguments:
#   network: the gamer network data structure
#   user_A:  a string containing the name of user_A
#   user_B:  a string containing the name of user_B
#
# Return:
#   The shortest path (a list of users) between user_A and user_B
#   - If such a path does not exist, return None.
#   - If user_A or user_B is not in network, return None.
def find_shortest_path_to_friend(network, user_A, user_B, path=None):
    #if A and B are the same then done
    if user_A == user_B:
        # if path is not None then then add the final step to the path
        # if path is None then this is the first iteration and return None
        if path is not None:
            path = path + [user_A]
        return path

    if path is None:
        path = []
    #add this step to the path
    path = path + [user_A]
    #if user_A doesn't exist then return None...shouldn't ever happen but just in case
    if not network.has_key(user_A):
        return None
    shortest = None
    #iterate over each connection
    for connection in get_connections(network, user_A):
        #current connection is not in path so analyze this possible path
        if connection not in path:
            new_path = find_shortest_path_to_friend(network, connection, user_B, path)
            if new_path:
                #if this current path is shortest then set shortest variable
                if not shortest or len(new_path) < len(shortest):
                    shortest = new_path
    return shortest
'''
network = create_data_structure(example_input)
print network
# ['Bryant', 'Debra', 'Walter']
print sorted(get_connections(network,"John"))
#['Dinosaur Diner', 'The Legend of Corgi', 'The Movie: The Game']
print sorted(get_games_liked(network,"John"))
#['Bryant', 'Freda', 'Jennie', 'John', 'Levi', 'Mercedes', 'Olive', 'Ollie', 'Robin', 'Walter']
print sorted(get_secondary_connections(network,"John"))
'''
network = create_data_structure('')
network = add_new_user(network,'A',[])
network = add_new_user(network,'B',[])
network = add_new_user(network,'C',[])
network = add_new_user(network,'D',[])
network = add_new_user(network,'E',[])
network = add_connection(network,'A','C')
network = add_connection(network,'B','C')
network = add_connection(network,'C','E')
network = add_connection(network,'A','E')
network = add_connection(network,'E','D')
network = add_connection(network,'D','B')
network = add_connection(network,'C','B')
print path_to_friend(network,'A','B')
print find_shortest_path_to_friend(network,'A','B')
'''
network = create_data_structure('')
network = add_new_user(network,'A',[])
network = add_new_user(network,'B',[])
network = add_new_user(network,'C',[])
network = add_connection(network,'A','B')
network = add_connection(network,'B','C')
network = add_connection(network,'C','B')
network = add_connection(network,'B','A')
print path_to_friend(network,'Z','Z')
'''