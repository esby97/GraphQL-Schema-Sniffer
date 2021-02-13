# GraphQL-Schema-Sniffer
Extract GraphQL Schema from some hints when introspection is not allowed.

# Preview
GraphQL supports the introspection system, which allows users to ask GraphQL schema.
However, for security reasons, most services do not support the introspection system.

***GraphQL-Schema-Sniffer*** can still extract schema under these circumstances.

# Idea
GraphQL provides some hints about Schema and Types. This tool extracts schema by applying some REGEX to hints.

* hint 1

`{"errors":[{"message":"Cannot query field \"BRUTEFORCE\" on type \"Query\". Did you mean \"HINTS\"?","locations":[{"line":1,"column":2}],"extensions":{"code":"GRAPHQL_VALIDATION_FAILED"}}]}`
* hint 2

`{"errors":[{"message":"Cannot query field \"BRUTEFORCE\" on type \"Query\". Did you mean \"HINTS\" or \"HINTS\"?","locations":[{"line":1,"column":2}],"extensions":{"code":"GRAPHQL_VALIDATION_FAILED"}}]}`
* hint 3

`{"errors":[{"message":"Field \"BRUTEFORCE\" must not have a selection since type \"TYPE\" has no subfields.","locations":[{"line":1,"column":15}],"extensions":{"code":"GRAPHQL_VALIDATION_FAILED"}}]}`

# Output
The output will come out like this.

`{'hotel': {'booking': {'id': 'ID',
                       'language': 'String',
                       'name': 'String',
                       'phone': 'String',
                       'price': 'Int'},
           'id': 'ID',
           'page': 'Int'},
 'project': {'team': {'account': 'String',
                      'address': 'String',
                      'desc': 'String',
                      'email': 'String',
                      'manager': 'String',
                      'name': 'String'}},
 'user': {'email': 'String',
          'id': 'Int',
          'nickname': 'String',
          'phone': 'String'}}`
 
 # How to use
 1. git clone or download this project.
 2. set URL and something you want in `setting.py`.
 3. set wordlist in `/wordlist`. (`1000_word.csv` is default)
 4. run `graphql_bruteforce.py` or `graphql_bruteforce_alpha.py`
 5. output will be created in `/output`
 
 # How does it work?
 
 ## 1. choose wordlist - 2 ways
In order to get a hint, you have to put a value in the query and send it.

`URL/graphql?query={ SOME_VALUE }`

The important thing is which word to choose.
I use two ways to get some hints.
 
1. wordlist bruteforce(`graphql_bruteforce.py`)
 
    I download wordlists from github. 
    
    1000 words. https://gist.github.com/deekayen/4148741
    
    10000 words. https://github.com/first20hours/google-10000-english

2. generate alphabet sequence(`graphql_bruteforce_alpha.py`)
    You can generate alphabet sequences in `make_wordlist.py`.
    
    You can select alphabet that you want to use in `setting.py`. and default value is "e, s, i, a, r, n, t, o". It is most frequently used alphabet ( I searched it from google.... )
    
    It makes wordlist like ee,es,ei,ea,er,en,et,eo,se,ss,si,sa,sr ... and use this word to bruteforcing.
    
## 2. make hierarchy - BFS queue
If you find some top-level(?) schema( 'user', 'hotel', 'project' on the output above ), you should also do additional search on these schemas. If you find a new schema there, you have to do the same thing over and over again.

`URL/graphql?query={ hotel }`

`URL/graphql?query={ hotel { booking } }`

`URL/graphql?query={ hotel { booking { language } } }`

I do this using **BFS(Breadth-First Search)** algorithm. The "Search" begins in the order in which they entered the queue. Therefore, the work is carried out in hierarchical order.

You can set the **depth** value so that the work is not too long. 3~5 is recommended.
    
    
