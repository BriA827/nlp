def file_read(file, lines = False):
    f = open(file, "r")
    if lines == True:
        f = f.readlines()
    else:
        f = f.read()
    return f

#########################################

scarlet = file_read("Scarlet_Letter.txt", True)

paras = []
count = 0

for i in scarlet:
    if len(i)>2:
        scarlet[scarlet.index(i)] = i[0:-1]

    paras.append(scarlet[count:scarlet.index(i)])
    count = scarlet.index(i) +1
    


# for i in scarlet:
    
#     print(type(i), i)

print(paras)