voting_data = list(open("voting_record_dump109.txt"))

## Task 1

def create_voting_dict():
    """
    Input: None (use voting_data above)
    Output: A dictionary that maps the last name of a senator
            to a list of numbers representing the senator's voting
            record.
    Example: 
        >>> create_voting_dict()['Clinton']
        [-1, 1, 1, 1, 0, 0, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1]

    This procedure should return a dictionary that maps the last name
    of a senator to a list of numbers representing that senator's
    voting record, using the list of strings from the dump file (strlist). You
    will need to use the built-in procedure int() to convert a string
    representation of an integer (e.g. '1') to the actual integer
    (e.g. 1).

    You can use the split() procedure to split each line of the
    strlist into a list; the first element of the list will be the senator's
    name, the second will be his/her party affiliation (R or D), the
    third will be his/her home state, and the remaining elements of
    the list will be that senator's voting record on a collection of bills.
    A "1" represents a 'yea' vote, a "-1" a 'nay', and a "0" an abstention.

    The lists for each senator should preserve the order listed in voting data. 
    """
    diction = {}
    for i in voting_data:
        l = i.split()
        dict_list = []
        for j in l[3:]:
            dict_list.append(int(j))
        diction[l[0]] = dict_list;
    return diction
    
## Task 2

def policy_compare(sen_a, sen_b, voting_dict):
    """
    Input: last names of sen_a and sen_b, and a voting dictionary mapping senator
           names to lists representing their voting records.
    Output: the dot-product (as a number) representing the degree of similarity
            between two senators' voting policies
    Example:
        >>> voting_dict = {'Fox-Epstein':[-1,-1,-1,1],'Ravella':[1,1,1,1]}
        >>> policy_compare('Fox-Epstein','Ravella', voting_dict)
        -2
    """
    result = 0
    for i in range(len(voting_dict[sen_a])):
        result += voting_dict[sen_a][i] * voting_dict[sen_b][i]
    return result


## Task 3

def most_similar(sen, voting_dict):
    """
    Input: the last name of a senator, and a dictionary mapping senator names
           to lists representing their voting records.
    Output: the last name of the senator whose political mindset is most
            like the input senator (excluding, of course, the input senator
            him/herself). Resolve ties arbitrarily.
    Example:
        >>> vd = {'Klein': [1,1,1], 'Fox-Epstein': [1,-1,0], 'Ravella': [-1,0,0]}
        >>> most_similar('Klein', vd)
        'Fox-Epstein'

    Note that you can (and are encouraged to) re-use you policy_compare procedure.
    """
    name = ""
    compare = -10000
    for i in voting_dict.keys():
        if i != sen:
            temp = policy_compare(sen, i, voting_dict)
            if temp > compare:
                compare = temp
                name = i
    return name
    

## Task 4

def least_similar(sen, voting_dict):
    """
    Input: the last name of a senator, and a dictionary mapping senator names
           to lists representing their voting records.
    Output: the last name of the senator whose political mindset is least like the input
            senator.
    Example:
        >>> vd = {'Klein': [1,1,1], 'Fox-Epstein': [1,-1,0], 'Ravella': [-1,0,0]}
        >>> least_similar('Klein', vd)
        'Ravella'
    """
    name = ""
    compare = 10000
    for i in voting_dict.keys():
        if i != sen:
            temp = policy_compare(sen, i, voting_dict)
            if temp < compare:
                compare = temp
                name = i
    return name

## Task 5

most_like_chafee    = most_similar('Chafee', create_voting_dict()) 
least_like_santorum = least_similar('Santorum', create_voting_dict())



# Task 6

def find_average_similarity(sen, sen_set, voting_dict):
    """
    Input: the name of a senator, a set of senator names, and a voting dictionary.
    Output: the average dot-product between sen and those in sen_set.
    Example:
        >>> vd = {'Klein': [1,1,1], 'Fox-Epstein': [1,-1,0], 'Ravella': [-1,0,0]}
        >>> find_average_similarity('Klein', {'Fox-Epstein','Ravella'}, vd)
        -0.5
    """
    Sum = 0
    for i in sen_set:
        Sum += policy_compare(sen, i, voting_dict)
    return Sum / len(sen_set)

#looking for democrates
democrats = {}
for i in voting_data:
    l = i.split()
    if l[1] == "D":
        dict_list = []
        for j in l[3:]:
            dict_list.append(int(j))
        democrats[l[0]] = dict_list;
        
voting_dict = create_voting_dict()
maxim = -1000
for i in voting_dict.keys():
    temp = find_average_similarity(i, democrats.keys(), voting_dict)
    if temp > maxim:
        maxim = temp
        name = i
most_average_Democrat = name # give the last name (or code that computes the last name)
print(name)

# Task 7

def find_average_record(sen_set, voting_dict):
    """
    Input: a set of last names, a voting dictionary
    Output: a vector containing the average components of the voting records
            of the senators in the input set
    Example: 
        >>> voting_dict = {'Klein': [-1,0,1], 'Fox-Epstein': [-1,-1,-1], 'Ravella': [0,0,1]}
        >>> find_average_record({'Fox-Epstein','Ravella'}, voting_dict)
        [-0.5, -0.5, 0.0]
    """
    v = []
    for i in sen_set:
        if not v:
            v = voting_dict[i]
        else:
            for j in range(len(voting_dict[i])):
                v[j] += voting_dict[i][j]
    for i in range(len(v)):
        v[i] = v[i] / len(sen_set)
    return v

average_Democrat_record = find_average_record(democrats, voting_dict) # (give the vector)
maxim = -1000
for i in voting_dict.keys():
    temp = 0
    for j in range(len(average_Democrat_record)):
        temp += average_Democrat_record[j] * voting_dict[i][j]
    if temp > maxim:
        maxim = temp
        name = i
print(name)

# Task 8

def bitter_rivals(voting_dict):
    """
    Input: a dictionary mapping senator names to lists representing
           their voting records
    Output: a tuple containing the two senators who most strongly
            disagree with one another.
    Example: 
        >>> voting_dict = {'Klein': [-1,0,1], 'Fox-Epstein': [-1,-1,-1], 'Ravella': [0,0,1]}
        >>> bitter_rivals(voting_dict)
        ('Fox-Epstein', 'Ravella')
    """
    oponents = {}
    compare = 100000
    for i in voting_dict.keys():
        oponents[i] = least_similar(i, voting_dict)
    for i in oponents:
        temp = policy_compare(i, oponents[i], voting_dict)
        if temp < compare:
            compare = temp
            names = (i, oponents[i])
    return names


