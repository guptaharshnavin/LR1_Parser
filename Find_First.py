from typing import List
from prettytable import PrettyTable

grammar: List[List[str]] = []  # Used To Store Grammar Entered By The User
first_collection = []  # Used To Store First Of Every Production In Grammar


def get_input():
    no_of_prod = int(input('Please Enter The Number Of Productions In The Grammar : '))
    print('\n------INSTRUCTIONS------')
    print('1. Capital Symbols Are Used To Denote Non-Terminal Symbols')
    print('2. Lowercase Symbols Are Used To Denote Terminal Symbols')
    print('3. Do Not Include Whitespaces In The Grammar')
    print('4. Epsilon Can Be Represented By e')
    print('5. First Grammar Should Begin With S')
    print('6. Example: S->aA|B|e')
    print('------------------------\n')

    global grammar
    print('Please Enter Grammar Productions')
    for i in range(no_of_prod):
        ing = input()

        if i == 0:
            if ing[0] != 'S':
                print('Invalid Grammar Production: 1st Production Must Start With S')
                break

        inl = []
        for s in ing:
            if s == '-' or s == '>':
                continue
            inl.append(s)
        grammar.append(inl)


def return_first(input_grammar):
    glist = []
    tlist = []

    for i in range(1, len(input_grammar)):
        if input_grammar[i] == '|':
            glist.append(tlist)
            tlist = []
        else:
            tlist.append(input_grammar[i])
    glist.append(tlist)

    first_list: List[List[str]] = []
    for g in glist:
        # Outer Loop Accessing Individual Product Of Every Non-Terminal
        for c in g:
            # Inner Loop Accessing The Individual Token Of Production
            if c == '$':
                continue
            if c == 'e':
                # If The Token Is Epsilon, Then First Find Stops, For The Production
                first_list.append(c)
                break
            elif c.islower():
                # If The Token Is A Terminal, It Is Added To The First
                first_list.append(c)
            elif c.isupper():
                # If Non-Terminal Is Same As For The Production Under Processing, Ignore Non-Terminal
                if c == input_grammar[0]:
                    continue
                # Selection Of Production For Non-Terminal
                sel_prod = []
                global grammar
                for gr in grammar:
                    if gr[0] == c:
                        sel_prod = gr
                        break

                # Determining First Of Non-Terminal
                non_term_first = return_first(sel_prod)
                # Appending First Of Non-Terminal To First List
                for i in non_term_first:
                    if i == 'e':  # Ignore Epsilon, Dont Add Into First List
                        continue
                    if i in first_list:
                        continue  # Dont Add Already Present Elements In First List, Dont Add Duplicate Elements
                    first_list.append(i)
                # If Epsilon Is Not Present In Non-Term First, Then First Find Stops For The Production
                if 'e' not in non_term_first:
                    break
    return first_list


def print_output():
    global grammar
    global first_collection

    output_table = PrettyTable()
    output_table.field_names = ["Production", "First"]

    for i in range(0, len(grammar)):
        prod = grammar[i][0] + '->'
        for j in range(1,len(grammar[i])):
            prod = prod + grammar[i][j]

        first = '{'
        for j in range(0, len(first_collection[i])):
            if j == len(first_collection[i]) - 1:
                first = first + first_collection[i][j] + '}'
            else:
                first = first + first_collection[i][j] + ','
        output_table.add_row([prod, first])

    print(output_table)


get_input()
for g in grammar:
    first_collection.append(return_first(g))
print_output()