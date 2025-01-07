import matplotlib.pyplot as plt
import math
import statistics as stat

####################################################

def mean(data):
    sum = 0
    for val in data:
        sum += val
    average = sum/len(data)
    return average

def variance(data):
    sum = 0
    for num in data:
        sum += (num - mean(data))**2
    vari = sum/len(data)
    return vari

def stand_dev(data):
    de = math.sqrt(variance(data))
    return de

def file_read(file, lines = False):
    f = open(file, "r")
    if lines == True:
        f = f.readlines()
    else:
        f = f.read()
    return f

def sentence_list_speaker(speaker, db, dict, index_key):
    sentences = []
    for i in dict[speaker][index_key]:
        sentences.append((((db[i].split(": "))[1]).split("\n"))[0])
    return sentences

def normalize(x, a):
    norm = (x)/(((x**2) + a)**(1/2))
    return norm

def pol_calc(sentence, pos_list, neg_list, vad, negate, dim):
    pun = [".", "?", "!"]
    flips = [",", ";", ":"]
    negation = False
    diminish = False
    pol = 0
    for word_og in sentence:
        p_n = None
        for i in word_og:
            if i in pun or i in flips and "$" not in word_og and not word_og.isupper():
                word = word[0:word.index(i)]
            else:
                word = word_og
        for vad_word in vad:
            if word == vad_word:
                if diminish:
                    pol += (float(vad[vad_word])) * .2
                    diminish = False
                else:
                    pol += float(vad[vad_word])
                if float(vad[vad_word]) > 0:
                    p_n = True
                else:
                    p_n = False
        for wp in pos_list:
            if word == wp:
                pol += .293
        for wn in neg_list:
            if word == wn:
                pol -= .293
        for w_negate in negate:
            if word == w_negate:
                negation = True
        for wd in dim:
            if word == wd:
                diminish = True
                

        #this works to add polarity for all caps
        #but because this is a debate and not a post, ive removed it

        #count = 0
        # for l in word:
        #     if l.isupper():
        #         count +=1
        #     if count == len(word) and len(word) > 1:
        #         if p_n == True:
        #             pol += .293
        #         else:
        #             pol -= .293

        if word_og[-1] == "!":
            if pol > 0:
                pol += .293
            else:
                pol -= .293

    if negation == True:
        pol = pol * -1
        negation = False

    return pol

def pol_per_sentence(sentence, pos_list, neg_list, vad, negate, dim):
    pun = [".", "?", "!"]
    flips = [",", ";", ":"]
    compound = False
    negation = False

    pieces = []
    pols = 0

    for i in flips:
        for s in sentence:
            if s[-1] == i:
                compound = True
                pieces.append(sentence[0:sentence.index(s)+1])
                pieces.append(sentence[sentence.index(s)+1:])

    if pieces:
        for i in pieces:
            sum_pol = pol_calc(i, pos_list, neg_list, vad, negate,dim)
            pols += sum_pol

    else:
        pol_value = pol_calc(sentence, pos_list, neg_list, vad, negate,dim)
        pols += pol_value

    norm_pol = normalize(pols, 15)
    return norm_pol

def pol_speaker(speaker):
    pol_list = []
    for i in range(0, len(speaker)):
        polarity= pol_per_sentence(speaker[i], pos_words, neg_words, vad_dict, negation_words, diminisher)
        pol_list.append(polarity)
    return pol_list

def all_chunks(chunks):
    all_sentences = []
    clean = []
    comma_list = []
    pun = [".", "?", "!"]
    flips = [",", ";", ":"]
    exception = ["Mr.", "Ms.", "Mrs."]

    for ch in chunks:
        if "[" in ch:
            first = ch.index("[")
            last = ch.index("]")
            ch = ch.replace(ch[first:last+1], "")
        test = ch.split()
        index_counter = 0
        comma_counter = 0
        for word in test:
            if word in exception:
                pass

            elif word[-1] in pun and not word.isupper():
                splice = (test[index_counter:test.index(word) +1])
                index_counter = test.index(word) + 1
                all_sentences.append(splice)
               
        if comma_list:
            all_sentences.append(comma_list)
            comma_list = []

    for i in all_sentences:
        if i:
            clean.append(i)

    return clean

# def str_complie(list_str):
#     string = ""

#     for i in list_str:
#         string = string + i

#     return string

def graph_pol(pol_list, candidate):
    p = {}
    n = {}
    m = {}
    styles = ["g*-", "r*-", "b*-"]
    for i in range(0, len(pol_list)):
        if pol_list[i] > 0.05:
            p[i] = pol_list[i]
        elif pol_list[i] < -0.05:
            n[i] = pol_list[i]
        else:
            m[i] = pol_list[i]

    plt.title(f"{candidate} Polarity")
    plt.xlabel("Sentence Index")
    plt.ylabel("Normalized Polarity")
    plt.yticks([-1.00, -.75,-.50,-.25,0,.25,.50,.75,1.00])
    plt.grid()
    for i in [p,n,m]:
        plt.plot(i.keys(), i.values(), styles[[p,n,m].index(i)])
    plt.show()

def pie_pol(pol_list, candidate):
    labels = ["Positive", "Negative", "Neutral"]
    p = 0 
    n = 0
    m = 0
    for i in range(0, len(pol_list)):
        if pol_list[i] > 0.05:
            p+=1
        elif pol_list[i] < -0.05:
            n+=1
        else:
            m+=1
    sizes = [p,n,m]
    fig,ax = plt.subplots()
    plt.title(f"{candidate} Polarity Sentence Sentiment Percentages")
    ax.pie(sizes,labels=labels, autopct='%1.1f%%', colors=['green', "red", "blue"])
    plt.show()

def stats(pols):
    p = [] 
    n = []

    for i in range(0, len(pols)):
        if pols[i] > 0.05:
            p.append(pols[i])
        elif pols[i] < -0.05:
            n.append(pols[i])

    pos = {"mean":mean(p), "std":stand_dev(p), "med":stat.median(p), 'max':max(p), "min":min(p)}
    neg = {"mean":mean(n), "std":stand_dev(n), "med":stat.median(n), 'max':max(n), "min":min(n)}

    return pos, neg

####################################################################

negation_words = ["no", "not", "rather", "couldn't", "wasn't", "didn't", "wouldn't", "shouldn't", "weren't", "don't", "doesn't", "haven't", "hasn't", "won't", "wont", "hadn't", "never", "none", "nobody", "nothing", "neither", "nor", "nowhere", "isn't", "can't", "cannot", "mustn't", "mightn't", "shan't", "without", "needn't"]
diminisher = ["hardly", "less", "little", "rarely", "scarcely", "seldom"]

pos = file_read("sen_files/positive_words.txt")
neg = file_read("sen_files/negative_words.txt")

vader = file_read("sen_files/vader_lexicon_polarity_values.txt")
debate = file_read("sen_files/Trump_Harris_Debate.txt", True)

pos_words = [i for i in pos.split('\n')]
neg_words = [i for i in neg.split('\n')]

vad_dict = {}

for i in vader.split('\n'):
    i = i.split('\t')
    vad_dict[i[0]] = i[1]

speakers = {}

debate_sens = debate[7:]

for i in debate_sens:
    if i == "\n":
        debate_sens.remove(i)

for en in debate_sens:
    parts = en.split(":")
    if len(parts) > 1:
        name=parts[0]
        if name not in speakers:
            speakers[name] = {"indexes":[], "polar":[]}
            speakers[name]['indexes'].append(debate_sens.index(en))
        elif name in speakers:
            speakers[name]['indexes'].append(debate_sens.index(en))

harris = sentence_list_speaker("HARRIS", debate_sens, speakers, "indexes")
trump = sentence_list_speaker("TRUMP", debate_sens, speakers, "indexes")

harris_full = all_chunks(harris)
trump_full = all_chunks(trump)

harris_pol= pol_speaker(harris_full)
trump_pol= pol_speaker(trump_full)

# print(len(harris_full), len(harris_pol)) #298
# print(len(trump_full), len(trump_pol)) # 627

graph_pol(harris_pol, "Harris")
pie_pol(harris_pol, "Harris")

harris_p, harris_n = stats(harris_pol)
print(harris_p, harris_n)

print("trump")

graph_pol(trump_pol, "Trump")
pie_pol(trump_pol, "Trump")

trump_p, trump_n = stats(trump_pol)
print(trump_p, trump_n)