import copy
import operator
import matplotlib.pyplot as plt

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
    exceptions = ["'", "\"", ",", "—", ".", ";", ":", "?", "!"]
    paren = ["(", ")"]
    dash = "--"
    all_words = []

    for i in range(0,len(indicies)):
        first_pass = (paper[indicies[i]].replace("\n", " ")).split(" ")
        full_words= []
        for i in first_pass:
            i = i.lower()
            for letter in i:
                if letter in exceptions:
                    try:
                        la = i.index(letter)
                        if la == 0:
                            i = i[1:] 
                        else:
                            i = i[0:la]
                        full_words.append(i)
                    except:
                        continue


                if letter in paren:
                    try:
                        la = i.index(letter)
                        if la == 0:
                            i = i[1:]
                            full_words.append(i)
                        else:
                            i = i[0:la]
                            full_words.append(i)
                    except:
                        continue

            if dash in i:
                la1 = i.index(dash)
                full_words.append(i[0:la1])
                full_words.append(i[la1+2:])

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

def c_sq(auth, dis, word_num):
    auth_d = count_words(auth) # gets the word count for auther
    dis_d = count_words(dis) #word count for disputed
    auth_tup = dict_tuple(auth_d, 1) #tuple for author words
    dis_tup = dict_tuple(dis_d, 1) #tuple for disputed words
    merge_tup = dict_tuple(merge_dicts(auth_d, dis_d), 1) #tuple for author and disputed

    chi_sq = 0

    auth_share = len(auth_d) / (len(auth_d) + len(dis_d))
    dis_share = 1 - auth_share
    
    for word in merge_tup[0:word_num]:
        word_c = word[1]
        for ao in auth_tup:
            if ao[0] == word[0]:
                auth_o = ao[1]
        for do in dis_tup:
            if do[0] == word[0]:
                dis_o = do[1]

        auth_e = auth_share * word_c
        dis_e = dis_share * word_c

        chi_sq += ((auth_e - auth_o)**2) / auth_e + ((dis_e - dis_o)**2) /dis_e

    return chi_sq

###################################################

# author_words = {"Hamilton":{}, "Madison":{}, "Jay":{}, "Disputed":{}}

ham_words = clean(fed, by_author["Hamilton"])
mad_words = clean(fed, by_author["Madison"])
jay_words = clean(fed, by_author["Jay"])
dis_words = clean(fed, by_author["Disputed"])

ham_chis = []
mad_chis = []
jay_chis = []
scale = []

for i in range(100,900,100):
    h = c_sq(ham_words, dis_words, i)
    m = c_sq(mad_words, dis_words, i)
    j = c_sq(jay_words, dis_words, i)
    ham_chis.append(h)
    mad_chis.append(m)
    jay_chis.append(j)
    scale.append(i)

# print(ham_chi, mad_chi, jay_chi)

plt.title("Chi-Square Value VS. Numer of Words")
plt.xlabel("Words")
plt.ylabel("Value")
plt.grid()
plt.plot([scale,scale,scale], [ham_chis, mad_chis,jay_chis])
plt.show()