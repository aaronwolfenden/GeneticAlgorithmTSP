import random
import math
import csv
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    """ Problem Solver """

    def __init__(self):
        self.population = population
        self.new_population = Population(self.population.population_size)
        self.parent_one = DNA()
        self.parent_two = DNA()
        self.mutation_chance = 0.1
        self.generations = 20
        self.best_fitness = 0
        self.starting_fitness = 0
        self.starting_length = 0
        self.starting_best = 0

    def evolve_population(self):
        """ Main Loop For Evolving The Population """
        self.starting_best = self.population.random_best
        # self.starting_fitness = self.population.best_fitness
        # self.starting_length = self.population.best_solution_length
        for i in range(self.generations):
            #print("\n\t== Generation ==" + str(i) + " ===\n")
            self.new_population = Population(population.population_size)
            self.crossover()
            self.new_population.set_best_solution()
            self.population.best = self.new_population.get_best_solution()
            print("\n\t\t=== Generation " + str(i) + " Stats ===")
            print("\t\tSize Of Population: " + str(len(self.new_population.population)))
            print("\t\tGeneration Best Fitness: " + str(self.new_population.get_best_fitness()))
            print("\t\tGeneration Best Length: " + str(self.new_population.get_best_solution_length()))
            print("\t\t===========================\n")
            self.population = self.new_population
            self.best_solution = self.population.get_best_solution()

        print("\t\t=== Start Solution === ")
        print("\t\tGeneration Best Fitness: " + str(self.starting_best.get_fitness()))
        print("\t\tSolution Length: " + str(self.starting_best.get_tour_distance()))
        print("\t\t===========================\n")

        print("\t\t=== GA Solution === ")
        print("\t\tBest Fitness: " + str(self.population.best_fitness))
        print("\t\tSolution Length: " + str(self.population.best_solution_length))
        print("\t\t===========================\n")


    def parent_selection(self):
        """ The Function That Selects The Two Parent Paths Using Probability Based On Fitness
            As The Smaller The Fitness Function The Better 1/fitness Is Used Using Roulette
            Wheel Probability """

        sum_of_fitness = 0

        for dna in population.population:
            sum_of_fitness += dna.dna_fitness

        parent_one_choice = random.uniform(0, sum_of_fitness)
        current_probability = 0

        for dna in population.population:
            current_probability += dna.dna_fitness
            if current_probability >= parent_one_choice:
                self.parent_one = dna
            #    for node in self.parent_one.route_taken:
            #       print(node.name)
                break

        parent_two_choice = random.uniform(0, sum_of_fitness)
        current_probability = 0

        for dna in population.population:
            current_probability += parent_two_choice
            if current_probability >= parent_two_choice:
                self.parent_two = dna
            #   for node in self.parent_two.route_taken:
            #      print(node.name)
                break

    def crossover(self):
        """ Crosses Over The DNA's To Create A New Child
            The Crossover Method That Is Used Is An Ordered Crossover. As A Regular
            Single Point Crossover Could Result In Duplicated Cities Or Unused Cities Making
            The Solution Incorrect / Invalid

            A Crossover Start And End Point Is Used To Define Which Genes Are Being Passed Over From
            Each Parent """

        # print("=== Parent One ===")
        # for node in self.parent_one.route_taken:
        #     print(node.name)
        # print("=== ========== ===")
        # print("=== Parent Two ===")
        # for node in self.parent_two.route_taken:
        #     print(node.name)
        # print("=== ========== ===")
        for pop in range(self.population.population_size):
            self.parent_selection()
            start_point = random.randint(1, graph.get_tour_length() - 1) # The Crossover points are chosen at random
            end_point = random.randint(start_point, graph.get_tour_length() - 1)

            child_dna = DNA()
            temp_storage = []

            # print("Crossover Points Are: " + str(start_point) + " And " + str(end_point))

            for i in range(graph.get_tour_length()): # Adding The Chosen DNA from Parent A
                if start_point <= i <= end_point:
                    temp_storage.append(self.parent_one.route_taken[i])

            count = 0

            while count < graph.get_tour_length():  # While The Tour Is Not Fulfilled
                if count == start_point:
                    child_dna.route_taken.extend(temp_storage)  # Add The List Of Parent 1 DNA
                    for node in temp_storage:  # Moves The Data Pointer For Each Node Added From P1
                        count += 1
                    continue
                for i in range(0, graph.get_tour_length()):  # For Each Node In A Tour
                    if self.parent_two.route_taken[i] not in child_dna.route_taken and self.parent_two.route_taken[i] \
                            not in temp_storage:  # If Parent Two's Node Is Not Used In The Child's Route or In Parent
                        #  One
                        if count < start_point:  # If The Current Position In Child's DNA Is Before The Crossover Point
                            child_dna.route_taken.append(self.parent_two.route_taken[i])  # Add Parent Two's First Valid
                            # Node
                            count += 1  # Move Onto Next Data Value
                            break
                        else:
                            child_dna.route_taken.append(self.parent_two.route_taken[i])
                            count += 1
                            break
            child_dna.route_taken.append(child_dna.route_taken[0]) # Adds The Return Node To The Tour
            count += 1

            # print("== Child DNA! ==")
            # for node in child_dna.route_taken:
            #     print(node.name)
            self.mutation(child_dna)  # Attempts To Mutate Solution Based On Probability
            self.new_population.population.append(child_dna)  # The New Child DNA Is Added To The New Population


    def mutation(self, dna):
        """ Swaps 2 Cities Around To Keep Variation It Also Makes Sure That
         Duplicate Or Missing Values Don't Occur"""

        if random.uniform(0, 1) < self.mutation_chance:
            temp_dna = DNA()
            node_one = random.randint(1, graph.get_tour_length() - 1)
            node_two = random.randint(1, graph.get_tour_length() - 1)
            while node_two == node_one:
                node_two = random.randint(1, graph.get_tour_length() - 1)
            # print(dna.route_taken[node_one].name)
            # print(dna.route_taken[node_two].name)
            temp_dna = dna.route_taken[node_one]
            dna.route_taken[node_one] = dna.route_taken[node_two]
            dna.route_taken[node_two] = temp_dna
            # print(dna.route_taken[node_one].name)
            # print(dna.route_taken[node_two].name)
            # print("== After Mutation! ==")
            # for node in dna.route_taken:
            #     print(node.name)
        return dna

    def display_solution(self):
        """ Used To Display The Results In Matplotlib,
        Displays Both Best Fitness From Start Of Algorithm And
        Genetic Algorithm Best Result """
        x_nodes = []
        y_nodes = []
        plt.subplot(1, 2, 1)
        for node in graph.get_nodes():
            plt.scatter(node.x, node.y, c="#000000")
        for node in ga.starting_best.route_taken:
            x_nodes.append(node.x)
            y_nodes.append(node.y)
        plt.plot(x_nodes, y_nodes)
        plt.title("Original Randomly Generated Solution")

        x_nodes = []
        y_nodes = []
        plt.subplot(1, 2, 2)
        for node in graph.get_nodes():
            plt.scatter(node.x, node.y, c="#000000")
        for node in ga.get_solution_best():
            x_nodes.append(node.x)
            y_nodes.append(node.y)
        plt.plot(x_nodes, y_nodes)
        plt.title("Genetic Algorithm Solution")

        plt.savefig("solution_comparison")
        plt.tight_layout()

    def set_solution_best_solution(self):
        if self.best_fitness < self.population.get_best_fitness():
            self.best_fitness = self.population.get_best_fitness()
            self.best_solution = self.population.get_best_solution()


    def get_solution_best(self):
        return self.best_solution



class Population:
    """ Defines A Group Of DNA """

    def __init__(self, population_size):
        self.population_size = population_size
        self.population = []
        self.best_fitness = 0.0
        self.best_solution = DNA()
        self.best_solution_length = 0
        self.random_best = DNA()

    def generate_random_dna(self, population_size):
        """ Generates A Random Population When The Program
         Is Started """
        self.population = [DNA() for i in range(population_size)]
        first_pass = True
        for element in self.population:
            #print("--- Element ---")
            element.initialise_dna()
            element.calculate_next_move()
            #element.print_route()
            element.calculate_fitness()
        for element in self.population:
            if first_pass:
                self.random_best = element
                first_pass = False
            if element.get_fitness() > self.random_best.get_fitness():
                self.random_best = element


    def get_population_size(self):
        return self.population_size

    def set_best_solution(self):
        for solution in self.population:
            solution.calculate_fitness()
            if solution.get_fitness() > self.best_fitness:
                self.best_fitness = solution.get_fitness()
                self.best_solution = solution.route_taken
                self.best_solution_length = solution.get_tour_distance()

    def get_best_solution(self):
        self.set_best_solution()
        return self.best_solution

    def get_best_fitness(self):
        self.set_best_solution()
        return self.best_fitness

    def get_best_solution_length(self):
        self.set_best_solution()
        return self.best_solution_length



class DNA:
    """ Defines Each Individual Array Element """

    def __init__(self):
        self.route_taken = []
        self.dna_fitness = 0
        self.tour_distance = 0

    def initialise_dna(self):
        """ Function To Initialise The DNA On A Random Node """
        random_start = random.randint(0, graph.get_tour_length() - 1)
        self.route_taken.append(graph.nodes[random_start])

    def calculate_next_move(self):
        """ Calculates The Next Move Based On Possible Moves"""
        for i in range(graph.get_tour_length()):
            if len(self.check_possible_moves()) > 0:
                move_taken = random.randint(0, len(self.check_possible_moves()) - 1)
                self.route_taken.append(self.check_possible_moves()[move_taken])
                if not self.check_possible_moves():
                    self.route_taken.append(self.route_taken[0])
            else:
                break

    def check_possible_moves(self):
        """ Looks At Possible Moves
         For Node Not In Route Taken """
        possible_moves = []
        for node in graph.get_nodes():
            if node not in self.route_taken:
                possible_moves.append(node)
        return possible_moves

    def calculate_fitness(self):
        """ Calculates The Fitness Of The Tour Based On The Cost Of The Tour Defined By Length
            Higher Fitness = Better """
        previous_flag = 0
        current_flag = 1
        while current_flag < graph.get_tour_length():
            previous_node = self.route_taken[previous_flag]
            current_node = self.route_taken[current_flag]
            self.tour_distance += current_node.get_distance_to_node(previous_node.get_x(), previous_node.get_y())
            self.dna_fitness = 1 / self.tour_distance * 10000
            previous_flag += 1
            current_flag += 1

    def get_fitness(self):
        return self.dna_fitness

    def print_route(self):
        for node in self.route_taken:
            print(node.name)

    def get_tour_distance(self):
        return self.tour_distance


class Graph:
    """ Used To Manage Nodes Into A Singular Class """
    def __init__(self):
        self.nodes = []
        self.edges = {}
        self.length = 0

    def create_new_node(self):
        """ Used To Create Nodes And Increment Tour Length """
        self.nodes.append(Node(10, 20, name="Manchester"))
        self.length += 1
        self.nodes.append(Node(90, 30, name="Chester"))
        self.length += 1
        self.nodes.append(Node(50, 40, name="Birmingham"))
        self.length += 1
        self.nodes.append(Node(40, 40, name="London"))
        self.length += 1
        self.nodes.append(Node(50, 50, name="Newcastle"))
        self.length += 1
        self.nodes.append(Node(90, 100, name="Hull"))
        self.length += 1
        # self.nodes.append(Node(20, 10, name="Brussels"))
        # self.length += 1
        # self.nodes.append(Node(30, 40, name="Ireland"))
        # self.length += 1
        # self.nodes.append(Node(60, 20, name="Swansea"))
        # self.length += 1
        # self.nodes.append(Node(90, 10, name="Hull"))
        # self.length += 1

        # with open('tsp_problem.csv', newline='') as csvfile:
        #     node_reader = csv.reader(csvfile, delimiter=',')
        #     x_locations = []
        #     y_locations = []
        #     names = []
        #     for row in node_reader:
        #         x = row[0]
        #         y = row[1]
        #         name = row[2]
        #
        #         x_locations.append(x)
        #         y_locations.append(y)
        #         names.append(name)
        #
        # print(x_locations)
        # print(y_locations)
        # print(names)



    def print_all_nodes(self):
        """ Used To Print Out All Node Information """
        for node in self.nodes:
            print("Node Name: " + node.name)
            print("Edges: ")
            for edge in node.edges:
                print(edge.name)

    def get_nodes(self):
        return self.nodes

    def get_tour_length(self):
        return self.length


class Node:
    """ Contains All Information Relating To The Nodes
    x - Used For Distance / Display Purposes
    y - Used For Distance / Display Purposes
    name - String For Readability"""
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def print_name(self):
        print(self.name)

    def get_name(self):
        return str(self.name)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_distance_to_node(self, previous_node_x, previous_node_y):
        """ The Distance Between Two Nodes Is Calculated Here And Is Used For Both The Length Of A Tour And
        Through That, The Fitness Of The Solution Created """
        distance = math.sqrt((self.x - previous_node_x)**2 + (self.y - previous_node_y)**2)
        return distance





graph = Graph()
graph.create_new_node()
print("\n")

population = Population(50)
population.generate_random_dna(population.get_population_size())

ga = GeneticAlgorithm()
ga.evolve_population()
ga.display_solution()
plt.show()

