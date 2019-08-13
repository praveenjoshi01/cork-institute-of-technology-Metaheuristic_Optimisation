#-----------------------------------------------------------------------------
#Author: Aditya Nair.
#Student_number: R00170651
#-----------------------------------------------------------------------------
# --------------------------------------------------------
#           PYTHON PROGRAM
# Here is where we are going to define our set of...
# - Imports
# - Global Variables
# - Functions
# ...to achieve the functionality required.
# When executing > python 'this_file'.py in a terminal,
# the Python interpreter will load our program,
# but it will execute nothing yet.
# --------------------------------------------------------
import random
import time
filename = "./uf20-01.cnf"

#---------------------------------------------------------------------------
#Funtion to get CNF problem from file:
#--------------------------------------------------------------------------
def get_cnf(filename):
    clauses = []
    temp = []
    with open(filename,"r") as f:
        cnf_data = f.readlines()
    for lines in cnf_data:
        if lines.startswith("p"):
            variable_count = lines.split()[2]
            clause_count = lines.split()[3]
            # print(variable_count,clause_count)
        if not lines.startswith("c") and not lines.startswith("p") and not lines.startswith("0") and not lines.startswith("%"):
            for word in lines.split():
                if word != '0':
                    temp.append(int(word))
                else:
                    clauses.append(temp)
                    temp = []
    # return number of variables, no. of clauses and clauses
    return int(variable_count),int(clause_count),clauses

#---------------------------------------------------------------------------
#Funtion for checking satisfiability of the clauses :
#--------------------------------------------------------------------------
def check_clause(single_clause_list,variable_values):
    boolean_result = 0
    for variable in single_clause_list:
        if variable > 0:
            if variable_values[variable-1] == 1:
                boolean_result = 1
                break
        else:
            if variable_values[abs(variable)-1] == 0:
                boolean_result = 1
                break
    #return boolean result
    return boolean_result


#---------------------------------------------------------------------------
#Funtion for checking satisfiability of the SAT problem i.e CNF formula F: :
#---------------------------------------------------------------------------
def check_formula(all_clauses_list,variable_values):
    clause_boolean_values = []
    for clause in all_clauses_list:
        boolean_result = check_clause(clause,variable_values)
        clause_boolean_values.append(boolean_result)
    if 0 in clause_boolean_values:
        result = 0
    else:
        result = 1
    # print(result)
    # print(clause_boolean_values)
    # return booleean result for the formula and list of boolean values for each clause
    return result,clause_boolean_values

#-------------------------------------------------------------------------------
#Function for flipping variable values:
#-------------------------------------------------------------------------------
def flip(variable):
    flipped_value = 0
    if variable == 0:
        flipped_value = 1
    return flipped_value


#---------------------------------------------------------------------------------------------------------------------
#Function for selecting variable which minimizes the unsatisfied clauses. This is the implementation of just the GSAT
#---------------------------------------------------------------------------------------------------------------------
def select_variable(all_clause_list,variable_values):
    min_cost_variables = []
    cost_per_variables = []
    for value in range(len(variable_values)):
        temp = variable_values.copy()
        # print(temp)
        flipped_value = flip(variable_values[value])
        # print(flipped_value)
        temp[value] = flipped_value
        # print(temp)
        clause_boolean_values = check_formula(all_clause_list,temp)[1]
        # print(clause_boolean_values)
        cost_per_variables.append(clause_boolean_values.count(0))
        # print(cost_per_variables)
    Min = min(cost_per_variables)
    # print(Min)
    # min_cost_variables = cost_per_variables.index(Min)
    # print(min_cost_variables)
    for cost in range(len(cost_per_variables)):
        if cost_per_variables[cost] == Min:
            min_cost_variables.append(cost)
    choice =  random.randint(0,(len(min_cost_variables)-1))
    random_min_cost_variable = min_cost_variables[choice]
    # print(random_min_cost_variable)
    return random_min_cost_variable


#---------------------------------------------------------------------------------------------------------------------
#Function for selecting variable in a random unsatisfied clause(Random walk):
#---------------------------------------------------------------------------------------------------------------------
def random_walk_selection(all_clause_list,variable_values):
    clauses_list = all_clause_list.copy()
    print("Clauses_list", clauses_list)
    clause_values = check_formula(clauses_list, variable_values)[1]
    print("Clauses_values", clause_values)
    unsatisfied_clauses = []
    for values in range(len(clause_values)):
        if clause_values[values] == 0:
            unsatisfied_clauses.append(values)
    print("Unsatisfied clause :", unsatisfied_clauses )
    if len(unsatisfied_clauses) != 0:
        random_unsatisfied_clause_index = unsatisfied_clauses[random.randint(0,len(unsatisfied_clauses)-1)]
        random_unsatisfied_clause = clauses_list[random_unsatisfied_clause_index]
        print("random_unsatisfied_clause", random_unsatisfied_clause)
        random_target_variable_index =  random.randint(0,len(random_unsatisfied_clause)-1)
        random_target_variable = abs(random_unsatisfied_clause[random_target_variable_index]) - 1
        print("random_target_variable", random_target_variable)
    else:
        random_target_variable = random.randint(0, len(variable_values)- 1)
        print("random_target_variable", random_target_variable)
    return random_target_variable






#---------------------------------------------------------------------------
#Funtion for GSAT with Tabu and Novelty+ :
#--------------------------------------------------------------------------
def gsat(maxTries,maxFlips,choice):
    solutions = []
    tl = 5
    walk_probability = 0.3
    variable_count,clause_count,clauses = get_cnf(filename)
    boolean_values = [1] * variable_count
    # val = [0,1,1,1,0,0,0,1,1,1,1,0,0,1,1,0,1,1,1,1]
    for tries in range(maxTries):
        tabu_variables = []
        variable_flip_age = [0] * variable_count
        for values in range(len(boolean_values)):
            boolean_values[values] = random.randint(0,1)
        variable_values = boolean_values.copy()
        for flips in range(maxFlips):
            # clause_list = clauses.copy()
            result = check_formula(clauses.copy(),variable_values.copy())[0]
            # check result
            if result == 1:
                print('Solution found:Appending now')
                solutions.append(variable_values.copy())
                # break
            # print(tabu_variables)
            # min_cost_variable = select_variable(clauses,variable_values)
            # to select varibable for flipping for GSAT with tabu:
            if choice == 1:
                probability =  random.uniform(0 ,1)
                if probability <= walk_probability:
                    target_variable = random_walk_selection(clauses.copy(), variable_values.copy())
                else:
                    target_variable = select_variable(clauses.copy(), variable_values.copy())
                # update_tabu = tabu_variables.copy()
                # min_cost_variable,tabu_variables = select_variable_tabu(clauses.copy(),variable_values.copy(),tl,update_tabu)
                variable_values[target_variable] = flip(variable_values[target_variable])

        if len(solutions) != 0:
            break
    if len(solutions) == 0:
        print("No solution found")
    else:
        for solution in solutions:
            if check_formula(clauses,solution)[0] == 1:
                print(solution)
        # print("solutions found: \n")
        # for solution in solutions:
        #     print("\n",solution)




# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    completion_time_tabu = []
    completion_time_novelty = []
    print("choose either GSAT with tabu Search or novelty plus:")
    print("1.GSAT with Tabu Search")
    choice = int(input("choice one of the above options:"))
    # for i in range(100):
    if choice == 1:
        start_time = time.clock()
        gsat(10,1000,1)
        end_time = time.clock() - start_time
        print("--- %s seconds ---" % (end_time))