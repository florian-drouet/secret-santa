from func.giver_receiver import get_giver_receiver
from func.gmail_func import get_mails, send_mails
from func.write_logs import write_logs

names, emails, wish_list = get_mails("Secret Santa 2021")

constraints = set([
    ("florian", "victoria", "couple"),
    ("benjamin", "amelie", "couple"),
    ("matthieu", "carolina", "couple"),
    ("florian", "matthieu", "unique"),
    ("matthieu", "florian", "unique"),
    ("victoria", "amelie", "unique"),
    ("benjamin", "victoria", "unique"),
    ("amelie", "carolina", "unique"),
    ("carolina", "benjamin", "unique")])
dict_giver_receiver, random_seed, nb_of_tries = get_giver_receiver(names=names, constraints=constraints)

write_logs(dict_giver_receiver, random_seed, nb_of_tries)

#send_mails(dict_giver_receiver=dict_giver_receiver, emails=emails, wish_list=wish_list)