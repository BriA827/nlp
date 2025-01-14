def file_read(file, lines = False):
    f = open(file, "r")
    if lines == True:
        f = f.readlines()
    else:
        f = f.read()
    return f

#########################################

scarlet = file_read("Scarlet_Letter.txt", True)

scar_dict = {}
count = None
p = None

for i in scarlet:
    if "Chapter" in i:
        ind1 = i.index("C")
        chap = i[ind1:]
        ind2 = chap.index(".")
        chap = chap[0:ind2]
        chap_l = chap.split(" ")
        cnt = chap_l[0] + " " + chap_l[1]

        scar_dict[cnt] = {"title": chap_l, "paras":[]}
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
                scar_dict[count]['paras'].append(p)
                p = None

tst = "Chapter I"
print(scar_dict[tst]['paras'])