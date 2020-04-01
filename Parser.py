from typing import List
import functools
from prettytable import PrettyTable

grammar: List[List[str]] = []  # Used To Store Grammar Entered By The User
augmented_grammar = []  # Used To Store Augmented Grammar With Dot
node_collection = []  # Collection Of Tree Nodes
parse_table_head = []  # Used To Store The Header Row Of Parse Table
parse_table_entries = []  # Used To Store Parse Table Rows


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
    global node_collection
    node_collection.append(curr_node)


def shift_dot(input_prod):
    dot_index = input_prod.index('.')  # Store Index Of '.'
    next_char = input_prod[dot_index + 1]  # Store Character To The Right Of Dot

    # Shifting Dot One Position Right
    prod_copy = input_prod.copy()
    prod_copy[dot_index] = next_char
    prod_copy[dot_index + 1] = '.'

    return prod_copy  # Return Updated Production


def create_parse_header():
    global augmented_grammar
    terminal_list = []  # To Store Various Terminal Symbols
    non_terminal_list = []  # To Store Various Non Terminal Symbols

    for g in augmented_grammar:
        for s in g:
            if s == '.' or s == "S'":
                continue
            if s.isupper():
                if s in non_terminal_list:
                    continue
                non_terminal_list.append(s)
            if s.islower():
                if s in terminal_list:
                    continue
                terminal_list.append(s)
    terminal_list.sort()
    terminal_list.append('$')
    non_terminal_list.sort()
    global parse_table_head
    for t in terminal_list:
        parse_table_head.append(t)

    for n in non_terminal_list:
        parse_table_head.append(n)
    parse_table_head = ['Node No.'] + parse_table_head


def get_node_index(first_prod):
    i = 0
    while i < len(node_collection):
        n = node_collection[i]
        if functools.reduce(lambda p, l: p and l, map(lambda m, k: m == k, first_prod, n[0]), True):
            return i
        i = i + 1


def print_all_nodes():
    global node_collection
    for i in range(0, len(node_collection)):
        print('------------------')
        print('Node ' + str(i))

        print_str = ""
        for j in range(0, len(node_collection[i])):
            print_str = node_collection[i][j][0] + "->"

            for k in range(1, len(node_collection[i][j])):
                print_str = print_str + node_collection[i][j][k]
            print(print_str)


def update_parse_table_final_node(c_prod, index_pos):
    curr_prod = c_prod.copy()
    comma_index = curr_prod.index(',')
    prod = curr_prod[0:comma_index]
    look_ahead = curr_prod[comma_index + 1:]
    local_augmented_grammar = []
    aug_line = ["S'", 'S', '.']
    local_augmented_grammar.append(aug_line)
    global grammar
    for g in grammar:
        aug_line = [g[0]]
        for i in range(1, len(g)):
            if g[i] == '|':
                local_augmented_grammar.append(aug_line)
                aug_line = [g[0]]
                continue
            aug_line.append(g[i])
        local_augmented_grammar.append(aug_line)

    for i in range(0, len(local_augmented_grammar)):
        g = local_augmented_grammar[i]
        if functools.reduce(lambda p, l: p and l, map(lambda m, k: m == k, prod, g[0:len(g) - 1]), True):
            parse_table_row = []
            for p in parse_table_head:
                parse_table_row.append(' ')
            parse_table_row[0] = index_pos
            string = 'r' + str(i)

            if i == 0:
                parse_table_row[parse_table_head.index('$')] = 'accept'
                parse_table_entries.append(parse_table_row)
                continue

            for l in look_ahead:
                parse_table_row[parse_table_head.index(l)] = string
            parse_table_entries.append(parse_table_row)
            break


def update_parse_table(next_prod, char_right_dot, i, index_node):
    # next_prod : Dot Shifted Production
    # char_right_dot : Character To Right Of Dot
    # i : Index Of Current Node
    # index_node : Index Of Node To Point To

    row_exists = False
    row_index = -1
    pt = 0
    for pt in range(0, len(parse_table_entries)):
        if parse_table_entries[pt][0] == i:
            row_exists = True
            row_index = pt
            break

    if not row_exists:
        parse_table_row = []
        for p in parse_table_head:
            parse_table_row.append(' ')

        if char_right_dot.isupper():
            parse_table_row[0] = i
            parse_table_row[parse_table_head.index(char_right_dot)] = str(index_node)
        if char_right_dot.islower():
            parse_table_row[0] = i
            parse_table_row[parse_table_head.index(char_right_dot)] = 'S' + str(index_node)
        parse_table_entries.append(parse_table_row)
    else:
        parse_table_row = parse_table_entries[row_index]

        if char_right_dot.isupper():
            parse_table_row[parse_table_head.index(char_right_dot)] = str(index_node)
        if char_right_dot.islower():
            parse_table_row[parse_table_head.index(char_right_dot)] = 'S' + str(index_node)
        parse_table_entries[row_index] = parse_table_row


def create_tree():
    global node_collection  # Accessing The Node Collection, Stores All Nodes Of Tree
    last_node_index = len(node_collection)
    i = 0
    while i < len(node_collection):
        curr_node = node_collection[i]  # curr_node -> Current Node That Is Being Processed
        j = 0
        while j < len(curr_node):
            curr_prod = curr_node[j]  # curr_prod -> Current Production That Is Being Processed

            dot_index = curr_prod.index('.')
            char_right_dot = curr_prod[dot_index + 1]  # Character To Right Of Dot
            if curr_prod[dot_index + 1] == ',':
                update_parse_table_final_node(curr_prod, i)
                # Node Is A Final Item, Requires No Further Processing
                j = j + 1
                continue

            next_prod = shift_dot(curr_prod)

            already_exists = False
            index_node = -1  # Index Of Already Existing Node
            z = 0
            for z in range(0, len(node_collection)):
                n = node_collection[z]
                # Iterating Through Existing Nodes, To Check If Node Already Exists
                if functools.reduce(lambda p, l: p and l, map(lambda m, k: m == k, next_prod, n[0]), True):
                    index_node = z  # Store Index Of Already Existing Node
                    # print("DEBUG : Node Already Exists")
                    already_exists = True

            if already_exists:
                update_parse_table(next_prod, char_right_dot, i, index_node)
                j = j + 1
                continue

            new_node = [next_prod]  # Creating New Node Of Tree
            dot_index = new_node[0].index('.')  # Index Of Dot In First Prod Of New Node

            if new_node[0][dot_index + 1] == ',':
                # Node Is A Final Item
                node_collection.append(new_node)
                update_parse_table(next_prod, char_right_dot, i, last_node_index)
                last_node_index = last_node_index + 1
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
            update_parse_table(next_prod, char_right_dot, i, last_node_index)
            last_node_index = last_node_index + 1
            j = j + 1
        i = i + 1


get_input()
construct_augmented_grammar()
create_parse_header()
create_first_node()
create_tree()
print('\nTree Nodes')
print_all_nodes()

parse_table = PrettyTable()
parse_table.field_names = parse_table_head
print('\nParse Table')
for p in parse_table_entries:
    parse_table.add_row(p)
print(parse_table)
