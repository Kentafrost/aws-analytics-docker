import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def demographic(df):
    # Get the current file path and name
    current_file_path = os.path.abspath(__file__)
    current_file_name = os.path.basename(current_file_path)
    
    state_dict = {}
    full_dict = {'state': [], 'avg': [], 'max': [], 'min': []}
    
    for index, row in df.iterrows():
        state = row['State']
        male_population = row['Male Population']
        female_population = row['Female Population']
        
        if f'{state}_Male' not in state_dict:
            state_dict[f'{state}_Male'] = []
        state_dict[f'{state}_Male'].append(male_population)
        
        if f'{state}_Female' not in state_dict:
            state_dict[f'{state}_Female'] = []
        state_dict[f'{state}_Female'].append(female_population)
    
    # Calculate the average, max, and min for each month
    try:
        for country, populations in state_dict.items():
            state = country.split('_')[0]
            avg_population = round(np.mean(populations), 2)
            max_population = round(np.max(populations), 2)
            min_population = round(np.min(populations), 2)

            # Append the results to the full_dict
            full_dict['state'].append(state)
            full_dict['avg'].append(avg_population)
            full_dict['max'].append(max_population)
            full_dict['min'].append(min_population)
        return full_dict
    except Exception as e:
        print(f"Error occured while calculating on {current_file_name}: {e}")#

def plot_graph_graphic(full_dict, graph_name, path, cur):

    # Create a table if it doers not exist
    tbl_exists_chk = cur.execute('IF EXISTS(SELECT 1 FROM sys.tables WHERE name = {}').format(graph_name)
    if tbl_exists_chk == False:
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS price_trends_{} (month VARCHAR(10), avg_price FLOAT, max_price FLOAT, min_price FLOAT)".format(graph_name))
        except Exception as e:
            print(f"Error creating table: {e}")
    else:
        print("Table already exists")


    state = full_dict['state']
    avg_population = full_dict['avg']
    max_population = full_dict['max']
    min_population = full_dict['min']

    chk_query = "Select * from price_trends_{} where state = %s".format(graph_name)
    update_query = "Update price_trends_{} set avg = %s, max = %s, min = %s".format(graph_name)
            
    for data in full_dict:
        # checking per month
        chk_data = cur.execute(chk_query, (state))
    
        # if data does not exist, insert data
        if chk_data is None:
            try:
                cur.execute(update_query, (avg_population, max_population, min_population))
            except Exception as e:
                print(f"Error inserting data: {e}")
        else:
            print("Data already exists, skipping update")
            print(chk_data)
        
    db_msg = "DB_update_success{}".format(graph_name)
    
    try:
        plt.figure(figsize=(10, 6))
        # make the pie chart
        plt.pie(graph_name, state, avg_population, max_population, min_population)
        
        # Title and labels
        plt.title('Population by State')
        plt.xlabel('State')
        plt.ylabel('Population')
        
        plt.legend()
        plt.tight_layout()
        plt.xticks(rotation=45)  # Rotate month labels for better readability
        plt.savefig(f'{path}\save_png\{graph_name}.jpg')
        plt.close()
        graph_result = "Graph_Create_Success, Graph_name: {}".format(graph_name)
    except Exception as e:
        print(f"Error plotting graph: {e}")
    result = db_msg + graph_result

    return result