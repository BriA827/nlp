import matplotlib.pyplot as plt

####################################################

def get_stopwords() :
    stop_words = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", \
                   "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can","could", \
                   "did", "do", "does", "doing", "done", "down", "during", "each", "few", "for", "from", "further", "had", "has",\
                   "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", \
                   "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it",\
                   "it's", "its", "itself", "just","let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", \
                   "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", \
                   "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their",\
                   "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", \
                   "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",\
                   "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", \
                   "where's", "which", "while", "who", "who's", "whom", "will","why", "why's", "with", "would", "you", "you'd",\
                   "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]
    return(stop_words)

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

def pol_per_sentence(sentence, pos_list, neg_list, vad, negate):
    pun = [".", "?", "!"]
    flips = [",", ";", ":"]
    pol = 0
    negation = False
    print(sentence)
    for word_og in sentence:
        p_n = None
        for i in word_og:
            if i in pun or i in flips and "$" not in word_og and not word_og.isupper():
                word = word[0:word.index(i)]
            else:
                word = word_og
        for vad_word in vad:
            if word == vad_word:
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
        
    norm_pol = normalize(pol, 15)
    return norm_pol

def pol_speaker(speaker):
    pol_list = []
    for i in range(0, len(speaker)):
        polarity= pol_per_sentence(speaker[i], pos_words, neg_words, vad_dict, negation_words)
        pol_list.append(polarity)
    return pol_list

def all_chunks(chunks):
    all_sentences = []
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
                for w in splice:
                    if w[-1] in flips and "$" not in w:
                        try:
                            all_sentences.remove(splice)
                        except:
                            pass
                        comma_list.append(splice[comma_counter:splice.index(w)+1])
                        comma_counter  = splice.index(w) +1
        if comma_list:
            all_sentences.append(comma_list)
            comma_list = []

    return all_sentences

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
    plt.grid()
    for i in [p,n,m]:
        plt.plot(i.keys(), i.values(), styles[[p,n,m].index(i)])
    plt.show()

def pie_pol(pol_list, candidate):
    labels = ["Positive", "Negative", "Neutral"]

####################################################################

negation_words = ["no", "not", "nothing", "never", "none", "nowhere", "neither", "nobody"]

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
# trump_full = all_chunks(trump)

harris_pol= pol_speaker(harris_full)
# trump_pol= pol_speaker(trump_full)

# print(len(harris_full), len(harris_pol)) #485
# print(len(trump_full), len(trump_pol)) # 989

# print(harris_pol)

# graph_pol(harris_pol, "Harris")