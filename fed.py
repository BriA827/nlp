import copy
import operator
import numpy as np
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

def compile(auth,dis_d):
    auth_d = count_words(auth) # gets the word count for auther
    auth_tup = dict_tuple(auth_d, 1) #tuple for author words
    merge_tup = dict_tuple(merge_dicts(auth_d, dis_d), 1) #tuple for author and disputed
    return  auth_tup, merge_tup

def c_sq(auth, dis, word_num, merge_tup, auth_tup, dis_tup):
    chi_sq = 0

    auth_share = len(auth) / (len(auth) + len(dis))
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

def c_all():
    ham_chis = []
    mad_chis = []
    jay_chis = []
    scale = []

    for i in range(100,900,100):
        h = c_sq(ham_words, dis_words, i, ham_merge_tup, ham_tup, dis_tup)
        m = c_sq(mad_words, dis_words, i, mad_merge_tup, mad_tup, dis_tup)
        j = c_sq(jay_words, dis_words, i, jay_merge_tup, jay_tup, dis_tup)
        ham_chis.append(h)
        mad_chis.append(m)
        jay_chis.append(j)
        scale.append(i)

    plt.title("Chi-Square Value VS. Numer of Words")
    plt.xlabel("Words")
    plt.ylabel("Value")
    plt.grid()
    plt.plot(scale, ham_chis, "bo-") # ham is blue
    plt.plot(scale, mad_chis, "yo-") # mad is yellow
    plt.plot(scale, jay_chis, "go-") # jay is green
    plt.show()

def ind(dis, paper, auth_words):
    words = []
    words_count = []
    words_tup = []
    sqs = []
    for i in range(0,len(dis)):
        diwords = clean(paper, [dis[i]])
        dicount = count_words(diwords)
        ditup = dict_tuple(dicount,1)
        words.append(diwords)
        words_count.append(dicount)
        words_tup.append(ditup)

    for i in range(0,len(words)):
        auth_tup, auth_merge_tup = compile(auth_words, words_count[i])
        a = c_sq(auth_words, words[i], 500, auth_merge_tup, auth_tup, words_tup[i])
        sqs.append(a)

    return(sqs)

def c_ind():
    papers = []
    for i in by_author["Disputed"]:
        papers.append(i)
    authors = {"Hamilton":[], "Madison":[], "Jay":[]}
    for i in ham_ind:
        authors["Hamilton"].append(i)
    for i in mad_ind:
        authors["Madison"].append(i)
    for i in jay_ind:
        authors["Jay"].append(i)
    x = np.arange(len(papers))
    width = 0.25
    multiplier = 0
    fig, ax = plt.subplots(layout='constrained')

    for a, v in authors.items():
        offset = width *multiplier
        rects = ax.bar(x +offset, v, width, label=a)
        ax.bar_label(rects, padding=3)
        multiplier +=1

    ax.set_ylabel("Chi-Square Value")
    ax.set_title("Disputed Papers Chi-Square for Each Author")
    ax.set_xticks(x+width, papers)
    ax.legend(loc="upper left", ncols=3)
    plt.show()
###################################################

# author_words = {"Hamilton":{}, "Madison":{}, "Jay":{}, "Disputed":{}}

ham_words = clean(fed, by_author["Hamilton"])
mad_words = clean(fed, by_author["Madison"])
jay_words = clean(fed, by_author["Jay"])
dis_words = clean(fed, by_author["Disputed"])

dis_d = count_words(dis_words) #word count for disputed
dis_tup = dict_tuple(dis_d, 1) #tuple for disputed words

ham_tup, ham_merge_tup = compile(ham_words, dis_d)
mad_tup, mad_merge_tup = compile(mad_words, dis_d)
jay_tup, jay_merge_tup = compile(jay_words, dis_d)

# c_all()

ham_ind = ind(by_author["Disputed"], fed, ham_words)
mad_ind = ind(by_author["Disputed"], fed, mad_words)
jay_ind = ind(by_author["Disputed"], fed, jay_words)

# c_ind()

ham_c = c_sq(ham_words, dis_words, 500 , ham_merge_tup, ham_tup, dis_tup)
mad_c = c_sq(mad_words, dis_words, 500 , mad_merge_tup, mad_tup, dis_tup)
jay_c = c_sq(jay_words, dis_words, 500 , jay_merge_tup, jay_tup, dis_tup)

# print(ham_c)
# print(mad_c)
# print(jay_c)