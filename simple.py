import json
import emails
from emails.template import JinjaTemplate as T
from pprint import pprint

def send_mail(person, chore):
    message = emails.html(subject=T('New Chore {{ chore_name }}'),
                        html=T('<p>Dear {{ name }}! There is a new Chore this month! Your delightful time with the {{ chore_name }} in the house! With love. '),
                        mail_from=('Casa Rosita', 'gabelula@gmail.com'))

    message.send(to=(person['name'], person['email']),
                render={'name': person['name'], 'chore_name': chore})

                
def get_chores():
    with open('chores.json') as data_file:    
        chores = json.load(data_file)

    return chores

def set_chores(chores):
    with open('chores.json', 'w') as outfile:
        json.dump(chores, outfile, indent=4, sort_keys=True)

def rotate_chores(chores):
    new_chores = {}

    i = 0
    l = len(chores)
    for k in chores.keys():
        i = i + 1
        if i == l:
            new_chores[k] = chores.values()[0]     
        else:
            new_chores[k] = chores.values()[i]

    return new_chores

def main():
    chores = get_chores()

    # rotate chores
    new_chores = rotate_chores(chores)

    # Send mails
    for c in new_chores:
        send_mail(new_chores[c]['person'], c)

    set_chores(new_chores)

    print "Succesful sent all the mails and rotates chores. The new chores are:"
    for k in new_chores:
        print "Chore %s: %s" % (k, new_chores[k]['person']['name'])

if __name__ == '__main__':
    main()