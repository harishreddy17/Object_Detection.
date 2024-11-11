import numpy as np

def check_interaction(results):
    interactions = []

    
    for i, row1 in results.iterrows():
        for j, row2 in results.iterrows():
            if i < j:  
                if (row1['name'], row2['name']) in [('person', 'bottle',), ('person', 'chair'),('person','laptop')]:
                    if is_interacting(row1, row2):
                        interaction_desc = f"{row1['name']} interacting with {row2['name']}"
                        interactions.append((row1, row2, interaction_desc))

    return interactions

def is_interacting(obj1, obj2):
    
    center1 = ((obj1['xmin'] + obj1['xmax']) / 2, (obj1['ymin'] + obj1['ymax']) / 2)
    center2 = ((obj2['xmin'] + obj2['xmax']) / 2, (obj2['ymin'] + obj2['ymax']) / 2)
 
    distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)

    
    box1_area = (obj1['xmax'] - obj1['xmin']) * (obj1['ymax'] - obj1['ymin'])
    box2_area = (obj2['xmax'] - obj2['xmin']) * (obj2['ymax'] - obj2['ymin'])
   
    x_overlap = max(0, min(obj1['xmax'], obj2['xmax']) - max(obj1['xmin'], obj2['xmin']))
    y_overlap = max(0, min(obj1['ymax'], obj2['ymax']) - max(obj1['ymin'], obj2['ymin']))
    overlap_area = x_overlap * y_overlap

    overlap_threshold = 0.10  

    return distance < 50 or (overlap_area > 0 and overlap_area / min(box1_area, box2_area) > overlap_threshold)