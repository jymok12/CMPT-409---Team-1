# Read Data
# 1. If the modified csv file or the minimum id txt file does not exist, then this will generate the modified csv file and the minimum id txt file
# 2. Each id in the modified csv file is subtracted by the minimum id
# 3. Read the modified csv file and the minimum id txt file
# 4. Get the id list and the id dictionary
# 5. Search the target id in the id list
# 6. Search the target id in the id dictionary


# Libraries
import pandas as pd
import os


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
# target_index: the index of target, -1: target id does not exist
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
    print(output)

    # Get the target index in the list
    target_index = linear_search_list_index(id_list, target_id)
    print(target_index)

    # Get the target info though the target index
    print(get_target_info_list_index(modified_csv, target_index))

    # Search in the dictionary
    # Check the target in the dictionary
    output = linear_search_dict(id_dict, target_id)
    print(output)

    # Get the target info though the dictionary
    print(id_dict['blueWins'][target_id])
