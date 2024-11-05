feds = open("fed_papers.txt", "r")
fed = feds.read().split("FEDERALIST No.")

by_author = {"Hamilton":[], "Madison":[], "Jay":[], "Shared":[], "Disputed":[]}
for f in fed[1:len(fed)]:
    f = f.split(" ")
    print(f[1].split('\n'))
    if f[1].split('\n') == "Hamilton":
        by_author["Hamilton"].append()
