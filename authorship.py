import math
import matplotlib.pyplot as plt
from scipy.stats import norm

###########################################

def file_read(file, lines = False):
    f = open(file, "r")
    if lines == True:
        f = f.readlines()
    else:
        f = f.read()
    return f

def variance(data, mean):
    sum = 0
    for num in data:
        sum += (num - mean)**2
    vari = sum/(len(data)-1)
    return vari

def stand_dev(data, mean):
    de = math.sqrt(variance(data, mean))
    return de

def book_dict(file, chapter, end):
    f_dict = {}
    count = None
    p = None

    for i in file:
        if chapter in i:
            ind1 = i.index("C")
            chap = i[ind1:]
            ind2 = chap.index(end)
            chap = chap[0:ind2]
            chap_l = chap.split(" ")
            cnt = chap_l[0] + " " + chap_l[1]

            f_dict[cnt] = {"title": chap_l, "paras":[]}
            count = cnt

        else:
            if "\n" in i:
                i = i.split("\n")
                i = i[0]

            if i != "":
                if p == None:
                    p = i
                else:
                    p = p + " " + i

            else:
                if p == None:
                    pass
                else:
                    f_dict[count]['paras'].append(p)
                    p = None

    
    return f_dict

def sen_par(file):
    pun = [".", "!", "?"]
    exceptions = ["Mr."]
    sentence_list = []
    p = 0

    for i in file.keys():
        para_count = len(file[i]["paras"])
        p += para_count
        s = 0
        for l in file[i]["paras"]:
            for m in range(len(l.split())):
                for e in pun:
                    if e in l.split()[m] and l.split()[m] not in exceptions:
                        try:
                            full = []
                            if l.split()[m][-1]=='"':
                                for n in l.split()[m+1:m+5]:
                                    if "ed" not in n:
                                        full.append(1)
                            if sum(full) > 0:
                                s+=1
                        except:
                            pass
                        s+=1
        sentence_list.append(s)

    c = [i/p for i in sentence_list]

    m = sum(sentence_list)/p
    d = stand_dev(c,m)
    return m,d, sentence_list

# def word_par(file):
    # w = 0
    # p = 0

    # for i in file.keys():
    #     para_count = len(file[i]["paras"])
    #     p+= para_count

    #     for l in range(para_count):
    #         w += len((file[i]["paras"][l]).split())
    
    # return w/p

# def word_sen(file):
#     pass

def comma_par(file):
    c_list = []
    p = 0

    for i in file.keys():
        para_count = len(file[i]["paras"])
        p += para_count
        c = 0

        for l in range(para_count):
            for m in file[i]["paras"][l]:
                if "," in m:
                    c += 1
        c_list.append(c)

    s = [i/p for i in c_list]

    m = sum(c_list)/p
    d = stand_dev(s, m)

    return m, d, c_list

def quotes_chap(file):
    q_list = []
    c = len(file)
    
    for i in file.keys():
        q = 0
        for l in range(len(file[i]["paras"])):
            for m in file[i]["paras"][l]:
                if '"' in m:
                    q+=1
        q_list.append(q/2)

    m = sum(q_list)/c
    d = stand_dev(q_list, m)

    return m, d, q_list

def kfac(m1,m2,d1,d2):
    t = abs(m2-m1)
    b = ((1/2) *((d2**2) + (d1**2)))**.5
    return t/b


def gauss(mews, stnds):
    ys = []
    xs = [a for a in range(round(-2*stnds+mews), round(2*stnds+mews))]

    for i in range(0,len(xs)):
        y = ((1)/(stnds* math.sqrt(2*math.pi)) * (math.e)**((-1/2)*(((xs[i]-mews)/stnds)**2)))
        ys.append(y)

    return xs, ys, mews, stnds

def gauss_plot(data, title, m, d):
    x = []
    y = []
    mew = []
    stnd = []

    lines_x =[]
    lines_y = []

    for i in range(len(data)):
        vs = gauss(m[i], d[i])
        x.append(vs[0])
        y.append(vs[1])
        mew.append(vs[2])
        stnd.append(vs[3])

        lines_x.append(vs[2])
        lines_x.append(-2*vs[3]+vs[2])
        lines_x.append(2*vs[3]+vs[2])

        for n in range(len(lines_x)):
            j = ((1)/(vs[3] * math.sqrt(2*math.pi)) * (math.e)**((-1/2)*(((lines_x[i]-vs[2])/vs[3])**2)))
            lines_y.append(j)

    k = round(kfac(m[0], m[1], d[0], d[1]), 2)
    plt.text(0,0,f"K-Factor: {k}")

    plt.title(title)
    plt.grid()
    c = ["g", "b", "r", "y"]
    a = ["Hawthorne", "Dickens", "Unknown A", "Unknown B"]
    for i in range(len(x)):
        plt.plot(x[i], y[i], c[i], label=a[i])
        plt.plot([m[i]-d[i], m[i]-d[i]], [0, ((1)/(d[i]* math.sqrt(2*math.pi)) * (math.e)**((-1/2)*(((m[i]-d[i]-m[i])/d[i])**2)))], "r-")
        plt.plot([m[i], m[i]], [0, ((1)/(d[i]* math.sqrt(2*math.pi)) * (math.e)**((-1/2)*(((m[i]-m[i])/d[i])**2)))], "y--")
        plt.plot([m[i]+d[i], m[i]+d[i]], [0, ((1)/(d[i]* math.sqrt(2*math.pi)) * (math.e)**((-1/2)*(((m[i]+d[i]-m[i])/d[i])**2)))], "r-")

    for i in range(len(lines_x)):
        plt.plot(lines_x[i], lines_y[i], "r")

    plt.legend()

    plt.show()

def prob(features):
    """feautures is a list of tuples, hawthorne first then dickens"""
    prior0 = .5
    prior1 = .5

    for i in range(len(features)):
        posterior0 = prior0*features[i][0] / (prior0 * features[i][0] + prior1 * features[i][1])
        posterior1 = prior1*features[i][1] / (prior0 * features[i][0] + prior1 * features[i][1])
        prior0 = posterior0
        prior1 = posterior1

    return prior0, prior1

def feature_prob(x,m1,m2,d1,d2):
    y1 = ((1)/(d1* math.sqrt(2*math.pi)) * (math.e)**((-1/2)*(((x-m1)/d1)**2)))
    y2 = ((1)/(d2* math.sqrt(2*math.pi)) * (math.e)**((-1/2)*(((x-m2)/d2)**2)))
    return y1,y2

#########################################
#par comma, sen par, chap quote

scarlet = file_read("Scarlet_Letter.txt", True)
great = file_read("Great_Expectations.txt", True)
novela = file_read("Novel A.txt", True)
novelb = file_read("Novel B.txt", True)

scar_dict = book_dict(scarlet, "Chapter", ".")
great_dict = book_dict(great, "Chapter", "\n")
a_dict = book_dict(novela, "Chapter", "\n")
b_dict = book_dict(novelb, "CHAPTER", ".")

#WORKS
scar_sp = sen_par(scar_dict)
great_sp = sen_par(great_dict)
b_sp = sen_par(a_dict)
a_sp = sen_par(b_dict)
# print(scar_sp, great_sp)

#WORKS
scar_cp = comma_par(scar_dict)
great_cp = comma_par(great_dict)
a_cp = comma_par(a_dict)
b_cp = comma_par(b_dict)
# print(scar_cp, great_cp)

#Works?
scar_qc = quotes_chap(scar_dict)
great_qc = quotes_chap(great_dict)
a_qc = quotes_chap(a_dict)
b_qc = quotes_chap(b_dict)
# print(scar_qc, great_qc)

# gauss_plot([scar_sp[-1], great_sp[-1], a_sp[-1], b_sp[-1]], "Sentence Paragraph Distribution", [scar_sp[0], great_sp[0], a_sp[0], b_sp[0]], [scar_sp[1], great_sp[1], a_sp[1], b_sp[1]])
# gauss_plot([scar_cp[-1], great_cp[-1], a_cp[-1], b_cp[-1]], "Comma Paragraph Distribution", [scar_cp[0], great_cp[0], a_cp[0], b_cp[0]], [scar_cp[1], great_cp[1], a_cp[1], b_cp[1]])
# gauss_plot([scar_qc[-1], great_qc[-1], a_qc[-1], b_qc[-1]], "Quotes Chapter Distribution", [scar_qc[0], great_qc[0], a_qc[0], b_qc[0]], [scar_qc[1], great_qc[1], a_qc[1], b_qc[1]])

