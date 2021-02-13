import setting as s
import make_wordlist
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from collections import defaultdict


# Disable flag warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 

# regex
p = re.compile('(?<=Did you mean \\\\")[\w_]{1,20}(?=\\\\)')
p2 = re.compile('(?<=Did you mean \\\\")[\w_]{1,20}.{1,5} or .{1,5}[\w_]{1,20}(?=\\\\")')
p3 = re.compile('(?<=must not have a selection since type \\\\")[\w_]{1,20}(?=\\\\" has)')

def bruteforce(context=[]):
    # query set
    c = ['']+ context
    query_left = '{'.join(c) + '{'
    query_right = '}'*len(c)
    
    
    for length in range(s.length):    
        # make wordlist
        wordlist = make_wordlist.make_wordlist(length)     

        # request
        find = dict()
        data = []
        count = 0
        while count < len(wordlist):

            # query
            query = " ".join(wordlist[count:count + s.hop])
            data = r'{"query":"'+ query_left+ query + query_right + '"}'
            count += s.hop

            # request send
            res = requests.post(url=s.url, data=data, headers=s.headers, verify=False)
            m = p.findall(res.text)
            m2 = p2.findall(res.text)
            m3 = p3.findall(res.text)

            if m:
                find.update(dict.fromkeys(m, ''))
            if m2:
                _m2 = []
                for x in m2:
                    _m2 += x.split('\\" or \\"')
                find.update(dict.fromkeys(_m2, ''))
            if m3:
                find = m3[0] # Type ( e.g. String )

    return find


# BFS
visit = list()
queue = list()
context = []
output = defaultdict(dict)
queue.append(context)
print("[+] Start!")

while queue: # context queue, each node means each context.
    print("[*] queue left : ", len(queue), "..", queue[-2:])
    node = queue.pop(0)
    if node not in visit:
        visit.append(node)
        find = bruteforce(node)
        if find:
            output = s.context2dict(output, node, find)
            if type(find) == type(''):
                print("[+] Find Type : ", node, find)
            elif len(node) <= s.depth:
                queue.extend([node + [x] for x in list(find.keys())])
            else:
                print("[*] Depth Over.. I will not anaylize", node) # pass if depth is over
        s.dict2json(output, s.output_PATH)

print("[+] finished!!")

