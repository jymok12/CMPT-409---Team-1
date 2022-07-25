# Read Data
# 1. If the modified csv file or the minimum id txt file does not exist, then this will generate the modified csv file and the minimum id txt file
# 2. Each id in the modified csv file is subtracted by the minimum id
# 3. Read the modified csv file and the minimum id txt file
# 4. Get the id list and the id dictionary
# 5. Search the target id in the id list
# 6. Search the target id in the id dictionary


# Libraries
import math
import pandas as pd
import os

import matplotlib.pyplot as plt
import numpy as np

import pickle
from qiskit import IBMQ, Aer, assemble, transpile, execute
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.visualization import plot_histogram

from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library.phase_oracle import PhaseOracle
from qiskit.quantum_info import Statevector

# File Names
minimum_id_file_name = 'minimum_id.txt'
original_csv_file_name = 'high_diamond_ranked_10min.csv'
modified_csv_file_name = 'high_diamond_ranked_10min_updated.csv'


###########################################################################################
# Generate Files
# Generate the modified csv file and the minimum id file
def generate_modified_csv():
    original_csv = pd.read_csv(original_csv_file_name)
    minimum_id = original_csv['gameId'].min()
    original_csv['gameId'] = original_csv['gameId'] - minimum_id
    original_csv.to_csv(modified_csv_file_name, index=False)
    
    minimum_id_file = open(minimum_id_file_name, 'w')
    minimum_id_file.write(str(minimum_id))


# Check the modified csv file
# Returns
# True: both files exist, False: either file does not exist
def check_files():
    return os.path.exists(modified_csv_file_name) and os.path.exists(minimum_id_file_name)


###########################################################################################
# Read the modified csv file
def read_modified_csv():
    return pd.read_csv(modified_csv_file_name, index_col=0)


# Read the minimum id txt file
def read_minimum_id_txt():
    minimum_id_file = open(minimum_id_file_name, 'r')
    return int(minimum_id_file.readlines()[0])


###########################################################################################
# Create a List and a Dictionary
# Create a id list
def create_id_list(modified_csv):
    return modified_csv.index.to_list()


# Create a id dictionary
def create_id_dict(modified_csv):
    return modified_csv.to_dict()


###########################################################################################
# Search ID in the List
# Linear search in the list
# Returns
# True: target id exists, -1: target id does not exist
def linear_search_list(id_list, target_id):
    for i in range(len(id_list)):
        if id_list[i] == target_id:
            return True
    return False


# Linear search in the list (index version)
# Returns
# linear_target_index: the index of target, -1: target id does not exist
def linear_search_list_index(id_list, target_id):
    for i in range(len(id_list)):
        if id_list[i] == target_id:
            return i
    return -1


# Get the target info using target index
def get_target_info_list_index(modified_csv, target_index):
    return modified_csv.iloc[target_index]


###########################################################################################
# Search ID in the Dictionary
# Linear search in the dictionary
# Returns
# True: target id exists, -1: target id does not exist
def linear_search_dict(id_dict, target_id):
    for key in id_dict['blueWins']:
        if key == target_id:
            return True
    return False

###########################################################################################
#       sources: 
# https://qiskit.org/documentation/partners/qiskit_ibm_runtime/tutorials/grover_with_sampler.html
# https://qiskit.org/textbook/ch-algorithms/grover.html
# https://qiskit.org/documentation/tutorials/algorithms/07_grover_examples.html
# https://qiskit.org/documentation/stubs/qiskit.algorithms.Grover.html
# https://quantumcomputing.stackexchange.com/questions/15945/implementing-grovers-oracle-with-multiple-solutions-in-qiskit
# https://www.quantiki.org/wiki/grovers-search-algorithm
#
###########################################################################################
# Search ID in the List
# Grover's search in the list
# note: ID must exist in the list, otherwise bogus result
# Returns
# grover_target_index: the index of target
def grovers_search_list_index(id_list, target_id, known_index):
    # our search key is 228013878 or '1101100101110011011100110110' 
    # and known_index is 2
    
    size = len(id_list)
    
    # number of qbits required (14 in our case)
    n = math.ceil(math.log(size, 2))
    
    # grover iterations within circuit (78 in our case)
    # (pi*sqrt(N))/4     
    # https://www.quantiki.org/wiki/grovers-search-algorithm
    
    iters = int((math.pi*math.sqrt(size))/4)
    
    # circuit executions (1024 is default)
    shots = 1024
    
    # index taken from classical search!
    # format the target as a binary string, for checking validity
    target_binary = format(known_index, f"0{n}b") 
    
    # create a state vector with the phases flipped for the values we want to find
    # https://quantumcomputing.stackexchange.com/questions/15945/implementing-grovers-oracle-with-multiple-solutions-in-qiskit
    # need power of 2 # states, but id_list is not big enough, so just fill the rest with zeros
    
    oracle = Statevector([1 if state < size and id_list[state] == target_id else 0 for state in range(0, 2**n)])
    
    problem = AmplificationProblem(oracle, is_good_state=target_binary)
    
    grover = Grover(iterations=iters)
    grover_circuit = grover.construct_circuit(problem)
    grover_circuit.measure_all()
    
    # image of circuit
    # grover_circuit.draw(output='mpl')
    # show()
    
    # calculate result
    # result = execute(grover_circuit, backend=Aer.get_backend('aer_simulator'), shots=shots).result()
    # all_probabilities = result.get_counts()
    
    # load from file, don't recalc
    with open('grover_probabilities.pkl', 'rb') as f:
        all_probabilities = pickle.load(f)
    
    list_probs = [0 for _ in range(0, 2**n)]
    for idx_bin, prob in all_probabilities.items():
        # set probability of index (divide by number of shots, as that is the total count)
        list_probs[int(idx_bin, 2)] = prob/shots
    
    # graph of probabilities
    plt.bar(list(range(0, 2**n)), list_probs)
    plt.ylabel('Probability')
    plt.xlabel('Index')
    plt.show()
    
    answer_binary = max(all_probabilities, key=all_probabilities.get)
    answer = int(answer_binary, 2)

    # uncomment to save result because it takes a long time to compute
    #with open('grover_probabilities.pkl', 'wb') as f:
    #    pickle.dump(all_probabilities, f)
    
    return answer

    
    
###########################################################################################
# Main function
if __name__ == "__main__":
    # Generate files
    if (not check_files()):
        generate_modified_csv()

    # Read files
    modified_csv = read_modified_csv()
    minimum_id = read_minimum_id_txt()
    
    # Create a list and a dictionary
    id_list = create_id_list(modified_csv)
    id_dict = create_id_dict(modified_csv)

    # Search target
    target_id = 228013878
    
    # Search in the list
    # Check the target in the list
    output = linear_search_list(id_list, target_id)
    print(f"Linear search output: {output}")
    
    # Get the target index in the list
    linear_target_index = linear_search_list_index(id_list, target_id)
    print(f"Linear search target index: {linear_target_index}")
    
    #TEMPCOMMENT
    ## Get the target info though the target index (linear)
    #print("Row found by linear search")
    #print(get_target_info_list_index(modified_csv, linear_target_index))
    
    grover_target_index = grovers_search_list_index(id_list, target_id, linear_target_index)
    print(f"Grover's search target index: {grover_target_index}")
    
    # print the result and the known correct answer.
    print(f"Quantum index: {grover_target_index}")
    print(f"Correct index: {linear_target_index}")
    print('Success!' if grover_target_index == linear_target_index  else 'Failure!')
    
    
    #TEMPCOMMENT
    ## Get the target info though the target index (grover)
    #print("Row found by Grover's")
    #print(get_target_info_list_index(modified_csv, grover_target_index))
    
    #TEMPCOMMENT
    ## Search in the dictionary
    ## Check the target in the dictionary
    #output = linear_search_dict(id_dict, target_id)
    #print(output)
    
    #TEMPCOMMENT
    ## Get the target info though the dictionary
    #print(id_dict['blueWins'][target_id])
