from func.giver_receiver import get_giver_receiver
from func.gmail_func import get_mails, send_mails

names, emails, wish_list = get_mails("Secret Santa 2021")

print(names)
print(emails)

#constraints = set([("florian", "victoria"), ("benjamin", "amelie"), ("matthieu", "carolina")])
dict_giver_receiver = get_giver_receiver(names=names, constraints=None)
print(dict_giver_receiver)

#send_mails(dict_giver_receiver=dict_giver_receiver, emails=emails, wish_list=wish_list)