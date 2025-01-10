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

for i in scarlet:
    if "Chapter" in i:
        ind1 = i.index("C")
        chap = i[ind1:]
        ind2 = chap.index(".")
        chap = chap[0:ind2]
        scar_dict[chap] = ["", 0]
        count = chap
    else:
        l = i.split("\n")
        if "\n" not in l[0]:
            line = l[0]
            scar_dict[chap][0] = scar_dict[chap][0] + line
            
        elif "\n" not in l[1]:
            line = l[0]
            scar_dict[chap][0] = scar_dict[chap][0] + line

        else:
            scar_dict[chap][1] += 1

tst = "Chapter I THE CUSTOMHOUSE"
print(scar_dict[tst])