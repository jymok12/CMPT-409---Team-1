# Read Data
# 1. If the modified csv file or the minimum id txt file does not exist, then this will generate the modified csv file and the minimum id txt file
# 2. Each id in the modified csv file is subtracted by the minimum id
# 3. Read the modified csv file
# 4. Get the id list
# 5. Search the target id in the id list
# 6. Get the info of the target id


# Libraries
import pandas as pd
import os


# File Names
minimum_id_file_name = 'minimum_id.txt'
original_csv_file_name = 'high_diamond_ranked_10min.csv'
modified_csv_file_name = 'high_diamond_ranked_10min_updated.csv'


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


# Read the modified csv file
def read_modified_csv():
    return pd.read_csv(modified_csv_file_name)


# Read the minimum id txt file
def read_minimum_id_txt():
    minimum_id_file = open(minimum_id_file_name, 'r')
    return int(minimum_id_file.readlines()[0])


# Linear search
# Returns
# target_index: the index of target, -1: target id does not exist
def linear_search(id_list, target_id):
    for i in range(len(id_list)):
        if id_list[i] == target_id:
            return i
    return -1


# Get the id list
def get_id_list(modified_csv):
    return modified_csv['gameId'].to_list()


# Get the target info
def get_target_info(modified_csv, target_index):
    return modified_csv.iloc[target_index]


# Main function
if __name__ == "__main__":
    # Generate files
    if (not check_files()):
        generate_modified_csv()

    # Read files
    modified_csv = read_modified_csv()
    minimum_id = read_minimum_id_txt()

    # Get the id list
    id_list = get_id_list(modified_csv)

    # Execute the linear search function
    target_id = 228013878
    target_index = linear_search(id_list, target_id)
    print('Target Index:', target_index)

    # Get the target info
    print(get_target_info(modified_csv, target_index))
    