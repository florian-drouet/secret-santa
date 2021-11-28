from os import name
import sys
import random
import numpy as np
import pandas as pd

def init_matrix(names, constraints=None):
    """Function used to initialize matrix of participants with constraints"""
    number_of_participants = len(names)

    if number_of_participants <= 2:
        print('WARNING: not enough participants')
        sys.exit(1)

    matrix = np.ones((len(names), len(names)))
    np.fill_diagonal(matrix, 0)
    guests = pd.DataFrame(matrix, index=names, columns=names).astype(int)

    if constraints is not None:
        for constraint in constraints:
            guests.loc[constraint[0]][constraint[1]] = 0
            guests.loc[constraint[1]][constraint[0]] = 0
    
    return guests


def get_giver_receiver(names, constraints):
    """Function used to define who gifts who"""

    guests = init_matrix(names=names, constraints=constraints)
    random_seed = random.randrange(1000)

    while guests.sum().sum() != 0:
        dict_giver_receiver = dict()
        guests = init_matrix(names=names, constraints=constraints)
        print(guests)
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