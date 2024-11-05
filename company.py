company = open("company_db.txt", "r")
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
    query_types = []
    
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
            query_types.append(t)
            c_t = token_type_valid(q[2], t)

            if c_t != True:
                valid_query = False
                return valid_query, query_tokens
            else:
                query_tokens = query.split()
    else:
        if query_tokens[0] not in keys or query_tokens[1] not in ops:
                valid_query = False
                return valid_query, query_tokens
            
        t = token_type(types, keys.index(query_tokens[0]))
        query_types.append(t)
        c_t = token_type_valid(query_tokens[2], t)

        if c_t != True:
            valid_query = False
            return valid_query, query_tokens
        
    return valid_query, query_tokens, query_types

def eval_db(ts, db, tt):
    db_enteries = []

    if len(ts) > 3:
        if tt[0] == str and tt[1] == int:
            query_str = "db_entry[" +"'" + ts[0] + "'" + "]" + "" + ts[1] + "" + "'" + ts[2] + "'" + " " + ts[3] + " " + "db_entry[" +"'" + ts[4] + "'" + "]" + "" + ts[5] + "" + ts[6]
        elif tt[0] == str and tt[1] == str:
            query_str = "db_entry[" +"'" + ts[0] + "'" + "]" + "" + ts[1] + "" + "'" + ts[2] + "'" + " " + ts[3] + " " + "db_entry[" +"'" + ts[4] + "'" + "]" + "" + ts[5] + "" + "'" + ts[6] + "'"
        elif tt[0] == int and tt[1] == str:
            query_str = "db_entry[" +"'" + ts[0] + "'" + "]" + "" + ts[1] + "" + ts[2] + " " + ts[3] + " " + "db_entry[" +"'" + ts[4] + "'" + "]" + "" + ts[5] + "" + "'" + ts[6] + "'"
        else:
            query_str = "db_entry[" +"'" + ts[0] + "'" + "]" + "" + ts[1] + "" + ts[2]

    else:
        if tt[0] == str:
            query_str = "db_entry[" +"'" + ts[0] + "'" + "]" + "" + ts[1] + "" + "'" + ts[2] + "'"
        else:
            query_str = "db_entry[" +"'" + ts[0] + "'" + "]" + "" + ts[1] + "" + ts[2]

    for db_entry in db:
        if eval(query_str):
            db_enteries.append(db_entry)
    return db_enteries

########## CODE ###########

comp_db, comp_keys, comp_types = file_database(company)
# print(comp_db, comp_keys, comp_types)

query = input("Find all records with: ")
while query != "exit":
    valid, tokens, types = parse(query, comp_keys, comp_types)
    print(valid, tokens, types)
    if valid == True:
        enteries = eval_db(tokens, comp_db, types)
        print(enteries)
    query = input("Find all records with: ")