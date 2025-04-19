import requests
import pandas as pd
import numpy as np



def submit():
	with open(f"Ashen_Outpost_Records.csv", "r") as f:
		r = requests.post("http://94.237.63.241:48713/score", files={"csv_file": f})
		print(r.text)
	if 'Tampering' in r.text:
		return "Tampering"
	if 'insufficient' in r.text:
		return float(str(r.text).split('[')[1].split(']')[0])
	#print(r.text)

def change_matrix(dataframe2, n_changes, scale_change):
	"""
	Randomly increases or decreases values in the dataframe by selecting random indices and columns.
	The changes are scaled by `scale_change` and can be positive or negative.

	Parameters:
		dataframe (pd.DataFrame): The input dataframe to modify.
		n_changes (int): The number of random values to modify.
		scale_change (float): The maximum magnitude of the change (can be positive or negative).

	Returns:
		pd.DataFrame: The modified dataframe.
	"""
	print(f"changes {n_changes} {scale_change}")
	dataframe = dataframe2.copy()
	# Ensure n_changes does not exceed the total number of elements in the dataframe
	#n_changes = min(n_changes, dataframe.size)
	
	# Get the shape of the dataframe
	rows, cols = dataframe.shape
	
	# Generate random indices for rows and columns
	random_row_indices = np.random.choice(rows, size=n_changes, replace=True)
	random_col_indices = np.random.choice(cols, size=n_changes, replace=True)
	
	# Apply random changes to the selected indices
	for i in range(n_changes):
		row_idx = random_row_indices[i]
		col_idx = random_col_indices[i]
		# Generate a random change between -scale_change and +scale_change
		random_change = np.random.uniform(-scale_change, scale_change)
		#print(random_change)
		dataframe.iat[row_idx, col_idx] += random_change
	return dataframe

def greedy_training():
    # Load the original data
    aux = pd.read_csv('/home/julixquid/Workshop/ctf/ml_wasteland/original.csv', index_col=0)
    
	#aux.to_csv('/home/julixquid/Workshop/ctf/ml_wasteland/Ashen_Outpost_Records.csv')
    
    prev_aux = aux  # Initialize previous state
    aux =change_matrix(aux,1,1)
    aux.to_csv('/home/julixquid/Workshop/ctf/ml_wasteland/Ashen_Outpost_Records_Copy.csv')
    result = 0.0  # Initialize result
    new_result = submit()  # Get initial result
    
    while True:
        print(f"*** Current Result: {result}, New Result: {new_result}")
        
        # Handle tampering
        if new_result == 'Tampering':
            print("Tampering detected. Restoring previous state.")
            aux = prev_aux  # Restore previous state
            aux.to_csv('/home/julixquid/Workshop/ctf/ml_wasteland/Ashen_Outpost_Records.csv')
            new_result = result
            
        # Update result if improvement is found
        elif new_result > result:
            print("Improvement found. Updating result and saving checkpoint.")
            prev_aux = aux  # Save current state as checkpoint
            result = new_result  # Update best result
            aux.to_csv('/home/julixquid/Workshop/ctf/ml_wasteland/Ashen_Outpost_Records.csv')
            aux.to_csv('/home/julixquid/Workshop/ctf/ml_wasteland/Ashen_Outpost_Records_Copy.csv')  # Save current state to file
        
        # Modify the matrix based on the current result
        if new_result < 30:
            aux = change_matrix(aux, 30, 2)
        elif new_result < 40:
            aux = change_matrix(aux, 15, 2)
        elif new_result < 50:
            aux = change_matrix(aux, 10, 1)
        elif new_result < 55:
            aux = change_matrix(aux, 5, 1)
        elif new_result < 59:
            aux = change_matrix(aux, 2, 1)
        else:
            aux = change_matrix(aux, 1, 1)
        
        # Get new result after modification
        aux.to_csv('/home/julixquid/Workshop/ctf/ml_wasteland/Ashen_Outpost_Records.csv')
        new_result = submit()
        
        # Add a break condition to avoid infinite loop
        if result >= 60:  # Example break condition
            print("Target result achieved. Exiting.")
            break

greedy_training()