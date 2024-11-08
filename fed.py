feds = open("fed_papers.txt", "r")
fed = feds.read().split("FEDERALIST No.")

by_author = {"Hamilton":[], "Madison":[], "Jay":[], "Disputed":[]}
for f in fed[1:len(fed)]:
    f = f.split(" ")
    title = f[1].split('\n')
    if title[2] == "HAMILTON":
        by_author["Hamilton"].append(title[0])
    elif title[2] == "MADISON":
        by_author["Madison"].append(title[0])
    elif title[2] == "JAY":
        by_author["Jay"].append(title[0])
    elif title[2] == "DISPUTED":
        by_author["Disputed"].append(title[0])
print(by_author)
