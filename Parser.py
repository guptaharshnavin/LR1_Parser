from typing import List
import functools

grammar: List[List[str]] = []  # Used To Store Grammar Entered By The User
augmented_grammar = []  # Used To Store Augmented Grammar With Dot
node_collection = []  # Collection Of Tree Nodes


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


def first_interface(input_prod):
    final_first = []

    for i in input_prod:
        temp_list = ['$', i]
        temp_first = return_first(temp_list)
        j = 0
        while j < len(temp_first):
            if temp_first[j] in final_first:  # Skip Symbol If Already Present In First List
                j = j + 1
                continue
            final_first.append(temp_first[j])  # Adding New Symbol To First List
            j = j + 1
    return final_first


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


def construct_augmented_grammar():
    aug_line = ["S'", '.', 'S']

    global augmented_grammar
    augmented_grammar.append(aug_line)

    global grammar
    for g in grammar:
        aug_line = [g[0], '.']
        for i in range(1, len(g)):
            if g[i] == '|':
                augmented_grammar.append(aug_line)
                aug_line = [g[0], '.']
                continue
            aug_line.append(g[i])
        augmented_grammar.append(aug_line)
    print('DEBUG : Augment Grammar')
    print(augmented_grammar)


def create_first_node():
    # Function To Create First Node Of The Tree
    global node_collection
    global augmented_grammar

    line_one = augmented_grammar[0].copy()
    line_one.append(',')
    line_one.append('$')
    line_two = augmented_grammar[1].copy()
    line_two.append(',')
    line_two.append('$')

    curr_node = [line_one, line_two]  # Represent The Node I0 In The Tree
    i = 1
    while i < len(curr_node):
        curr_line = curr_node[i]  # Current Production
        dot_index = curr_line.index('.')  # Determining Index Of Dot In Current Production

        if curr_line[dot_index + 1] == ',':
            continue  # Continue If Dot On Rightmost Position

        first_prod = curr_line[dot_index + 2:]  # Elements To Find First Of
        j = 0
        while j < len(first_prod):
            if first_prod[j] == ',':
                first_prod.pop(j)
            else:
                j = j + 1

        first_res = first_interface(first_prod)  # First Result

        next_symbol = curr_line[dot_index + 1]

        if next_symbol.isupper():
            for a in augmented_grammar:
                if a[0] == next_symbol:
                    temp_a = a.copy()
                    temp_a.append(',')
                    for f in first_res:
                        temp_a.append(f)
                    curr_node.append(temp_a)

        i = i + 1
    print('DEBUG : Print First Node (Node 0)')
    print(curr_node)
    global node_collection
    node_collection.append(curr_node)


def shift_dot(input_prod):
    dot_index = input_prod.index('.')  # Store Index Of '.'
    next_char = input_prod[dot_index + 1]  # Store Character To The Right Of Dot

    # Shifting Dot One Position Right
    prod_copy = input_prod.copy()
    prod_copy[dot_index] = next_char
    prod_copy[dot_index + 1] = '.'
    print('DEBUG : Dot Shifted Prod')
    print(prod_copy)

    return prod_copy  # Return Updated Production


def create_tree():
    global node_collection  # Accessing The Node Collection, Stores All Nodes Of Tree

    i = 0
    while i < len(node_collection):
        curr_node = node_collection[i]  # curr_node -> Current Node That Is Being Processed
        print('DEBUG : Node ' + str(i))
        j = 0
        while j < len(curr_node):
            curr_prod = curr_node[j]  # curr_prod -> Current Production That Is Being Processed
            print('DEBUG : Prod ' + str(j))
            print(curr_prod)

            dot_index = curr_prod.index('.')
            if curr_prod[dot_index + 1] == ',':
                # Node Is A Final Item, Requires No Further Processing
                j = j + 1
                continue

            next_prod = shift_dot(curr_prod)

            already_exists = False
            for n in node_collection:
                # Iterating Through Existing Nodes, To Check If Node Already Exists
                if functools.reduce(lambda p, l: p and l, map(lambda m, k: m == k, next_prod, n[0]), True):
                    print("DEBUG : Node Already Exists")
                    already_exists = True

            if already_exists:
                j = j + 1
                continue

            new_node = [next_prod]  # Creating New Node Of Tree
            dot_index = new_node[0].index('.')  # Index Of Dot In First Prod Of New Node

            if new_node[0][dot_index + 1] == ',':
                # Node Is A Final Item
                node_collection.append(new_node)
                # Add New Node To Collection, And Stop Further Processing
                j = j + 1
                continue

            first_prod = new_node[0][dot_index + 2:]  # Elements To Find First Of
            k = 0
            while k < len(first_prod):
                if first_prod[k] == ',':
                    first_prod.pop(k)
                else:
                    k = k + 1

            first_res = first_interface(first_prod)  # First Result
            if len(first_res) == 0:
                first_res = ['$']
            next_symbol = new_node[0][dot_index + 1]

            if next_symbol.isupper():
                for a in augmented_grammar:
                    if a[0] == next_symbol:
                        temp_a = a.copy()
                        temp_a.append(',')
                        for f in first_res:
                            temp_a.append(f)
                        new_node.append(temp_a)

            node_collection.append(new_node)  # Append New Node To Node Collection
            j = j + 1
        i = i + 1


get_input()
construct_augmented_grammar()
create_first_node()
create_tree()
print('DEBUG : Printing Node Tree')
for n in node_collection:
    print(n)
