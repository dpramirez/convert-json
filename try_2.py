import json
import numpy as np
import pandas as pd

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


train_data = []
df = pd.read_json('all_new.json')
df = df.T
df_data = pd.DataFrame(columns=['name', 'x_points','y_points'])

for index, row in df.iterrows(): # 
    
    region =row['regions']
    filename = row['filename']
    filename = 'test_images/{}'.format(filename)
    count = 0 # lines
    
    y_all_point = []
    x_all_point = [] # list list
    
    for reg in region: #  
        y_Values = reg['shape_attributes']['all_points_y']
        x_Values = reg['shape_attributes']['all_points_x']
        for y in y_Values:
            y_all_point.append(y)
        x_all_point.append(x_Values)
    new_all_x_point = [] 
    large_list = len(y_all_point)
    pre_quantity = 0 
    movements = 0
    for iterator in range(len(x_all_point)):
        new_x = [-2] * large_list
        for point_x in range(len(x_all_point[iterator])):
            if pre_quantity <= movements < pre_quantity + len(x_all_point[iterator]):
                new_x[movements] = x_all_point[iterator][point_x]
                movements += 1       
        pre_quantity = pre_quantity + len(x_all_point[iterator])        
        new_all_x_point.append(new_x)
    print('************************************************************************')
    print('it x-axis: ', x_all_point)
    print('it y-axis: ', y_all_point)
    print('new x point: ', new_all_x_point)            
    print('************************************************************************')
        #print(count, len(y_all_point), x_all_point)
    data ={'lanes':new_all_x_point , 'h_samples':y_all_point,'raw_file':filename}    
    with open("label.json", "a") as outfile:
                 outfile.write(json.dumps(data,cls = NpEncoder))
                 outfile.write('\n')
   