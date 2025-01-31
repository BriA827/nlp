import math

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
    pun = ["!", "?"]
    exceptions = ["Mr."]
    great = ["I", "Mr.", "Joe", "Camilla", "Biddy", "Wemmick's", "Herbert", "Miss", "Estella", "Pumblechook"]
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
                            if l.split()[m][-1]=='"' and l.split()[m+1] in great:
                                print(l.split()[m:m+7])
                        except:
                            # print(l.split()[m])
                            pass


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

    return m, d

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

    return m, d

#########################################
#par comma, sen par, chap quote

scarlet = file_read("Scarlet_Letter.txt", True)
great = file_read("Great_Expectations.txt", True)

scar_dict = book_dict(scarlet, "Chapter", ".")
great_dict = book_dict(great, "Chapter", "\n")

sen_par(great_dict)

#WORKS
scar_cp = comma_par(scar_dict)
great_cp = comma_par(great_dict)
# print(scar_cp, great_cp)

#Works?
scar_qc = quotes_chap(scar_dict)
great_qc = quotes_chap(great_dict)
# print(scar_qc, great_qc)