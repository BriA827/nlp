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

def pol_per_sentence(sentence, pos_list, neg_list):
    p = []
    n = []
    print(sentence)
    sentence = sentence.split()
    for word in sentence:
        for wp in pos_list:
            if word == wp:
                p.append(word)
        for wn in neg_list:
            if word == wn:
                n.append(word)
    print(sentence)
    print(p,n)
####################################################################

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
        elif name in speakers:
            speakers[name]['indexes'].append(debate_sens.index(en))

muir = sentence_list_speaker("MUIR", debate_sens, speakers, "indexes")
davis = sentence_list_speaker("DAVIS", debate_sens, speakers, "indexes")
harris = sentence_list_speaker("HARRIS", debate_sens, speakers, "indexes")
trump = sentence_list_speaker("TRUMP", debate_sens, speakers, "indexes")

# pol_per_sentence(muir[0], pos_words, neg_words)

print(speakers)