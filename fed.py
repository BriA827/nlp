import copy
import operator

feds = open("fed_papers.txt", "r")
fed = feds.read().split("FEDERALIST No.")

by_author = {"Hamilton":[], "Madison":[], "Jay":[], "Disputed":[]}
for f in fed[1:len(fed)]:
    f = f.split(" ")
    title = f[1].split('\n')
    if title[2] == "HAMILTON":
        by_author["Hamilton"].append(int(title[0]))
    elif title[2] == "MADISON":
        by_author["Madison"].append(int(title[0]))
    elif title[2] == "JAY":
        by_author["Jay"].append(int(title[0]))
    elif title[2] == "DISPUTED":
        by_author["Disputed"].append(int(title[0]))

# print(by_author)

################################################

def clean(paper, indicies):
    exceptions = ["'", "\"", ",","—",".", ";", ":", "?", "!"]
    paren = ["(", ")"]
    all_words = []

    for i in range(0,len(indicies)):
        first_pass = (paper[indicies[i]].replace("\n", " ")).split(" ")
        full_words= []
        for i in first_pass:
            i = i.lower()
            for o in exceptions:
                if o in i:
                    la = i.index(o)
                    if la == 0:
                       i = i[1:] 
                    else:
                        i = i[0:la]
                    full_words.append(i)
            for p in paren:
                if p in i:
                    la = i.index(p)
                    if la == 0:
                        i = i[1:]
                        full_words.append(i)
                    else:
                        i = i[0:la]
                        full_words.append(i)
            else:
                full_words.append(i)
        for w in full_words[5:]:
            all_words.append(w)
    return all_words

def distinct(words):
    dist_words = []
    for w in words:
        if w in dist_words:
            pass
        elif w == "":
            pass
        else:
            dist_words.append(w)
    return(dist_words)

def count_words(words):
    counting = {}
    dis_words = distinct(words)

    for d in dis_words:
        counting[d] = 0

    for w in words:
        if w == "":
            pass
        else:
            counting[w] += 1

    return counting

def merge_dicts(d1, d2):
    merged = copy.deepcopy(d1)
    for key in d2:
        if key in merged:
            merged[key] += d2[key]
        else:
            merged[key] = d2[key]
    return merged

def dict_tuple(dic, k):
    t = list(dic.items())
    sort = sorted(t, key=operator.itemgetter(k), reverse=True)
    return sort

def c_sq(auth_d, dis_d):
    auth_d = count_words(auth_d)
    dis_d = count_words(dis_d)
    auth_tup = dict_tuple(auth_d, 1)
    dis_tup = dict_tuple(dis_d, 1)
    merge_tup = dict_tuple(merge_dicts(auth_d, dis_d), 1)

    chi_sq = 0
    

###################################################

# author_words = {"Hamilton":{}, "Madison":{}, "Jay":{}, "Disputed":{}}

ham_words = clean(fed, by_author["Hamilton"])
mad_words = clean(fed, by_author["Madison"])
jay_words = clean(fed, by_author["Jay"])
dis_words = clean(fed, by_author["Disputed"])

c_sq(ham_words, dis_words)