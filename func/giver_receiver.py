import random
import numpy as np
import pandas as pd


def get_giver_receiver(names, constraints):

    random_seed = random.randrange(1000)

    matrix = np.ones((len(names), len(names)))
    np.fill_diagonal(matrix, 0)
    guests = pd.DataFrame(matrix, index=names, columns=names).astype(int)

    for constraint in constraints:
        guests.loc[constraint[0]][constraint[1]] = 0
        guests.loc[constraint[1]][constraint[0]] = 0

    while guests.sum().sum() != 0:
        dict_giver_receiver = dict()
        matrix = np.ones((len(names), len(names)))
        np.fill_diagonal(matrix, 0)
        guests = pd.DataFrame(matrix, index=names, columns=names).astype(int)

        for constraint in constraints:
            guests.loc[constraint[0]][constraint[1]] = 0
            guests.loc[constraint[1]][constraint[0]] = 0
        
        random_givers = random.sample(list(guests.index), k=len(names))
            
        for random_giver in random_givers:
            try:
                receiver = guests.loc[random_giver].index[random.choice(np.where(guests.loc[random_giver]!=0)[0])]
            except:
                random_seed += 1
            guests[receiver] = 0
            guests.loc[receiver, random_giver] = 0
            dict_giver_receiver[random_giver] = receiver
    
    return dict_giver_receiver