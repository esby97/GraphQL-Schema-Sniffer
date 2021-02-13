import csv
import json
import os

############ You should set this ################
url = ""                # url that you want to send request (e.g. https://somesites.com/graphql))
depth = 5               # depth that you want
#################################################

############ You can change this ################
absFilePath = os.path.abspath(__file__)
path = os.path.split(absFilePath)[0]
wordlist_PATH = path + "\\wordlist\\1000_word.csv"
output_PATH = path + "\\output\\output.json"
headers = { "content-type": "application/json", 'user-agent' : ''}
#################################################

######### for ver_alpha #########################
alpha = ['e', 's', 'i', 'a', 'r', 'n', 't' ,'o'] # frequently used alphabet. You can change this.
hop = 10000             # number that you send at once
max_length = 10         # max
length = 5              # user choice
wordlist_FOLDER = path + "\\wordlist\\"
#################################################

def csv2list(filename, delimiter=','):
    try:
        with open(filename , 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data
    except Exception as e:
        #print(e)
        return False

def list2csv(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def context2dict(dic, context, value):
    if context:
        cmd = "dic" + ''.join([ "['" + x + "']" for x in context]) + "=value"
        exec(cmd)
        return dic
    else:
        dic.update(value)
        return dic

def dict2json(dic, filename):
    with open(filename, 'w') as f:
        json.dump(dic, f)
