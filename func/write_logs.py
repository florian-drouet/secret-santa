def write_logs(dict_giver_receiver, random_seed, nb_of_tries):
    with open('logs/logs.txt', "w") as log:
        for giver in dict_giver_receiver.keys():
            log.write(f"{giver.capitalize()} gives to {dict_giver_receiver[giver].capitalize()}\n")
        log.write(f"\nRandom seed was set to {random_seed} in {nb_of_tries} time(s)")