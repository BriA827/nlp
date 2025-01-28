import math

###########################################

def file_read(file, lines = False):
    f = open(file, "r")
    if lines == True:
        f = f.readlines()
    else:
        f = f.read()
    return f

def variance(data):
    sum = 0
    for num in data:
        sum += (num - 1)**2
    vari = sum/len(data)
    return vari

def stand_dev(data):
    de = math.sqrt(variance(data))
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
    m = 0
    for i in file.keys():
        para_count = len(file[i]["paras"])
        sen_count = 0

def word_par(file):
    w = 0
    p = 0

    for i in file.keys():
        para_count = len(file[i]["paras"])
        p+= para_count

        for l in range(para_count):
            w += len((file[i]["paras"][l]).split())
    
    return w/p

# def word_sen(file):
#     pass

def comma_par(file):
    c_list = []
    p_list = []

    for i in file.keys():
        para_count = len(file[i]["paras"])
        p_list.append(para_count)
        c = 0

        for l in range(para_count):
            for m in file[i]["paras"][l]:
                if "," in m:
                    c += 1

        c_list.append(c)

    s = []
    for i in range(len(c_list)):
        s.append(c_list[i]/p_list[i])

    return sum(s)/len(s), stand_dev(c_list)

def quotes_chap(file):
    q = 0
    c = len(file)
    
    for i in file.keys():
        for l in file[i]['paras']:
            for w in l:
                if "\"" in w:
                    q += 1

    return (q/2)/c

#########################################
#par comma, par sen, chap quote

scarlet = file_read("Scarlet_Letter.txt", True)
great = file_read("Great_Expectations.txt", True)

scar_dict = book_dict(scarlet, "Chapter", ".")
great_dict = book_dict(great, "Chapter", "\n")

scar_wp = word_par(scar_dict)
great_wp = word_par(great_dict)
# print(scar_wp, great_wp)

scar_cp = comma_par(scar_dict)
great_cp = comma_par(great_dict)
print(scar_cp, great_cp)

scar_qc = quotes_chap(scar_dict)
great_qc = quotes_chap(great_dict)
# print(scar_qc, great_qc)