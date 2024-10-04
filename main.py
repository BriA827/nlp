company = open("/home/kuni/nlp/company_db.txt", "r")
# print(company.read())

####### FUNCTIONS #############

def file_database(file):
    file_db = []
    people = []

    for key in file.readlines(1):
        keys = key.split()

    for t in file.readlines(2):
        key_type = t.split()

    for c in file.readlines():
        people.append(c.split())

    for person in people:
        dict = {}
        for category in person:
            try:
                cat = int(category)
            except:
                cat = str(category)
            dict[keys[person.index(category)]] = cat
        file_db.append(dict)

    return file_db, keys, key_type

def is_alpha(str):
    x = str.isalpha()
    return x

def is_int(str):
    x = str.isint()
    return x

def token_type(types, index):
    if types[index] == "S":
        type = str
    else:
        type = int
    return type

def token_type_valid(user_token, token_type):
    if token_type == str:
        alpha = is_alpha(user_token)
        if alpha == False:
            return False
        else:
            return True
        
    else:
        int = ord(user_token[0])
        if int >= 48 and int <= 57:
            return True
        else:
            return False
        
def parse(query, keys, types):
    ops = ["=", "==", ">", "<", "<=", ">="]
    valid_query = True
    multiple = False
    query_tokens = []
    query_list1 = []
    query_list2 = []
    
    #testing the length to be 3 with "and" "or" in the query
    if len(query.split(" ")) != 3:
        if "or" in query:
            query_list1.append(query.split("or"))
            multiple = True

        elif "and" in query:
            query_list1.append(query.split("and"))
            multiple = True
            #makes multiple queries into a list of each query

        else:
            valid_query = False
            return valid_query, query_tokens

    #if it is length 3, continue
    else:
        query_tokens = query.split()

    if multiple == True:
        for q in query_list1[0]:
            if q[0] == " ":
                q = q[1:]
            q_split = q.split(" ")
            query_list2.append(q_split)

    #testing the tokens
    if multiple == True:
        for q in query_list2:
            if q[0] not in keys or q[1] not in ops:
                valid_query = False
                return valid_query, query_tokens
            
            t = token_type(types, keys.index(q[0]))
            c_t = token_type_valid(q[2], t)

            if c_t != True:
                valid_query = False
                return valid_query, query_tokens
            else:
                query_tokens.append(q)
    else:
        if query_tokens[0] not in keys or query_tokens[1] not in ops:
                valid_query = False
                return valid_query, query_tokens
            
        t = token_type(types, keys.index(query_tokens[0]))
        c_t = token_type_valid(query_tokens[2], t)

        if c_t != True:
            valid_query = False
            return valid_query, query_tokens
        
    return valid_query, query_tokens, multiple

def eval_db(ts, num, db):
    if num == True:
        for token in ts:
            query_str = "db_entry[" +"'" + token[0] + "'" + "]" + "" + token[1] + "" + token[2]
            print(query_str)
    else:
        query_str = "db_entry[" +"'" + ts[0] + "'" + "]" + "" + ts[1] + "" + ts[2]
        print(query_str)

    for db_entry in db:
        if eval(query_str):
            print(db_entry)

########## CODE ###########

comp_db, comp_keys, comp_types = file_database(company)
# print(comp_db, comp_keys, comp_types)

query = input("Find all records with: ")
while query != "exit":
    valid, tokens, multiples = parse(query, comp_keys, comp_types)
    print(valid, tokens)
    if valid == True:
        eval_db(tokens, multiples, comp_db)
    query = input("Find all records with: ")