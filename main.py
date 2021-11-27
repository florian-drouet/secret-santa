from func.giver_receiver import get_giver_receiver 

names = ["amelie", "victoria", "benjamin", "florian", "carolina", "matthieu"]
constraints = set([("florian", "victoria"), ("benjamin", "amelie"), ("matthieu", "carolina")])

print(get_giver_receiver(names, constraints))
