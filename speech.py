corpus = open("corpus.txt", "r")
# print(corpus.read())

import math
import matplotlib.pyplot as plt

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

def corpus_to_db(file):
    cd = []
    file_split = (file.read()).split("§")
    for s in file_split:
        if s == "":
            continue
        else:
            text = s.split()
            dict = {}

            name = []
            ints = []
            for word in text:
                try:
                    int(word)
                    ints.append(word)
                    break
                except:
                    name.append(word)

            dict["name"] = name

            if len(ints[0]) == 1:
                dict["term"] = int(ints[0])
                index = text.index(ints[0])+1
                ints.append(text[index])
                dict["year"] = int(ints[1])
                dict["text"] = text[index+1:-1]

            else:
                dict["term"] = 1
                index = text.index(name[-1])+1
                ints.append(text[index])
                dict["year"] = int(ints[0])
                dict["text"] = text[index+1:-1]

            cd.append(dict)
    return cd

def word_v_year(data):
    plt.title("Speech Length VS. Inaugural Year")
    plt.xlabel("Year")
    plt.ylabel("Speech Length")

    num = len(data)

    for n in range(0,num):
        xs = []
        ys = []
        for i in data[n]:
            ind = data[n].index(i)
            xs.append(data[n][ind]["year"])
            ys.append(len(data[n][ind]["text"]))

        plt.plot(xs,ys, "*-")

        mew = mean(ys)
        sigma = stand_dev(ys)

        for p in [mew, mew+sigma, mew-sigma]:
            plt.plot(xs, [p for i in range(0,len(xs))], "r-", linewidth=2)

    plt.grid()
    plt.show()

def gauss(x,mew,sigma):
    v = (1)/(sigma * math.sqrt(2*math.pi)) * (math.e)**((-1/2)*(((x-mew)/sigma)**2))
    return v


############# FINISH GAUSSIAN PLOTS #############
# def gauss_plot(data):
    plt.title("Distribution of Inaugural Speech Lengths")
    plt.xlabel("Speech Length")
    plt.ylabel("Propability Density")

    num = len(data)

    for n in range(0,num):
        xs = []
        for i in data[n]:
            ind = data[n].index(i)
            xs.append(len(data[n][ind]["text"]))
        ys = [gauss()]

        plt.plot(xs,ys, "b*-")

        mew = mean(ys)
        sigma = stand_dev(ys)

        for p in [mew, mew+sigma, mew-sigma]:
            plt.plot(xs, [p for i in range(0,len(xs))], "r-", linewidth=2)

    plt.grid()
    plt.show()

def sentence_finder(data, graph=True):
    pun = [".", "?", "!"]
    exception = ["Mr.", "Ms.", "Mrs."]
    len_mean = []
    years = []
    for sp in data:
        years.append(sp["year"])
        sentences = []
        counter = 0
        for word in sp["text"]:
            if word in exception:
                counter += 1
            else:
                for cha in word:
                    if cha in pun:
                        sentences.append(counter)
                        counter = 0
                counter += 1
        len_mean.append(mean(sentences))

    if graph == True:
        plt.title("Average Sentence Length vs. Inaugural Year")
        plt.xlabel("Year")
        plt.ylabel("Sentence Length")
        plt.grid()
        plt.plot(years, len_mean, "b*-")
        plt.show()

    return len_mean

def word_len(data, value, condition, graph=True):
    exceptions = ["'", ",","—","."]
    years = []
    per = []
    for sp in data:
        years.append(sp["year"])
        counter = 0
        for word in sp["text"]:
            for cha in word:
                if cha in exceptions:
                    word = word.replace(cha,"")
            
            if eval(f"{len(word)} " + f"{condition} " + f"{value}") == True:
                counter +=1
        per.append((counter/len(sp["text"]))*100)
        counter = 0

    if graph == True:
        plt.title(f"% of Words {condition} {value} vs. Inaugural Year")
        plt.xlabel("Year")
        plt.ylabel(f"% of Words {condition} {value}")
        plt.grid()
        plt.plot(years, per, "b*-")
        plt.show()

    return per

def syllables(data, graph=True):
    vowels = ["A","E","I","O","U","a","e","i","o","u"]
    years = []
    syls = []
    for sp in data:
        years.append(sp["year"])
        counter = 0
        for word in sp["text"]:
            bin = []

            for cha in word:
                if cha in vowels:
                    bin.append(1)
                else:
                    bin.append(0)

            vs = diph_triph(bin)
            counter += vs

            if word[-1] == "e":
                counter -=1
            if word[len(word)-2] == "l" and word[-1] == "e":
                counter += 1
        syls.append(counter/len(sp["text"]))

    if graph == True:
        plt.title("Average Syllables Per Word vs. Inaugural Year")
        plt.xlabel("Inaugural Year")
        plt.ylabel("Average Syllables")
        plt.grid()
        plt.plot(years, syls, "b*-")
        plt.show()

    return syls
            
def diph_triph(binn):
    vowel_count = 0
    for i in binn:
        if i == 1:
            vowel_count +=1
    
    while 1 in binn:
        ind = binn.index(1)
        di_tri = 0
        try:
            if binn[ind+1] == 1:
                di_tri +=1
                vowel_count -=1
                if binn[ind+2] ==1:
                    di_tri += 1
                    vowel_count -= 1
        except:
            pass

        for n in range(0,di_tri+1):
            binn.remove(1)

    return vowel_count

def flesch(data, w_s, s_w, graph = True):
    levels = []
    for i in range(0,len(w_s)):
        level = (0.39 * w_s[i]) + (11.8*s_w[i]) - 15.59
        levels.append(level)

    years = []
    for sp in data:
        years.append(sp["year"])

    if graph == True:
        plt.title("Flesch-Kincaid Grade Level vs. Inaugural Year")
        plt.xlabel("Inaugural Year")
        plt.ylabel("Grade Level")
        plt.grid()
        plt.plot(years, levels, "b*-")
        
        for p in [6,9,13]:
            plt.plot(years, [p for i in range(0,len(years))], "r")

        plt.show()

    return levels

def plots(years,len_mean,syls,levels):
    plt.title("Average Sentence Length vs. Inaugural Year")
    plt.xlabel("Year")
    plt.ylabel("Sentence Length")
    plt.grid()
    plt.subplot(3,1,1)
    plt.plot(years, len_mean, "b*-")

    plt.title("Average Syllables Per Word vs. Inaugural Year")
    plt.xlabel("Inaugural Year")
    plt.ylabel("Average Syllables")
    plt.grid()
    plt.subplot(3,1,2)
    plt.plot(years, syls, "b*-")

    plt.title("Flesch-Kincaid Grade Level vs. Inaugural Year")
    plt.xlabel("Inaugural Year")
    plt.ylabel("Grade Level")
    plt.grid()
    plt.subplot(3,1,3)
    plt.plot(years, levels, "b*-")
        
    for p in [6,9,13]:
        plt.plot(years, [p for i in range(0,len(years))], "r")

    plt.show()

################

speeches = corpus_to_db(corpus)

# word_v_year([speeches[0:38],speeches[38:-1]])

avg_sen = sentence_finder(speeches, False)

# percents = word_len(speeches, 8, ">=")

avg_syls = syllables(speeches, False)

grades = flesch(speeches,avg_sen, avg_syls, False)

plots([sp["year"] for sp in speeches], avg_sen, avg_syls, grades)