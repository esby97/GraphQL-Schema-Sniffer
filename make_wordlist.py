import setting as s
import csv

def make_wordlist(n):
    # check if it already exist!
    check = s.csv2list(s.wordlist_FOLDER + f"wordlist{n}.csv")
    if check:
        return check[0]
    
    # if not, check wordlist(n-1) exist
    ex_list = s.csv2list(s.wordlist_FOLDER + f"wordlist{n-1}.csv")
    if ex_list == False:
        if n == 0:
            ex_list = ['']
        else:
            ex_list = make_wordlist(n-1)
    else:
        ex_list = ex_list[0]

    # make new_list        
    new_list = []
    for ex in ex_list:
        for a in s.alpha:
            new_list.append(ex + a)

    # save & return
    s.list2csv(new_list, s.wordlist_FOLDER + f"wordlist{n}.csv")
    return new_list

if __name__ == "__main__":
    make_wordlist(s.max_length)
