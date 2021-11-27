import email
from func.giver_receiver import get_giver_receiver
from func.gmail_func import get_mails, send_mails

names = ["amelie", "victoria", "benjamin", "florian", "carolina", "matthieu"]
constraints = set([("florian", "victoria"), ("benjamin", "amelie"), ("matthieu", "carolina")])

dict_giver_receiver = get_giver_receiver(names, constraints)
print(dict_giver_receiver)

names, emails, wish_list, = get_mails("Secret Santa 2021")

print(names)
print(emails)

#send_mails(dict_giver_receiver=dict_giver_receiver, emails=emails)