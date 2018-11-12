import copy


def find_path(graph, start, end, alpha, path=[]):
    """
    method to find path in graph which represents fsa
    :param graph: graph which represents fsa
    :param start: from state
    :param end: to state
    :param alpha: set of transitions
    :param path: support
    :return:
    """
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    if len(graph[start]) < 2:
        return None
    for node in graph[start]:
        if node not in path and node not in alpha:
            newpath = find_path(graph, node, end, alpha, path)
            if newpath: return newpath
    return None


def contains_disjoint_states(graph, states, alpha):
    """
    Method to determine is some states are disjoint
    :param graph: graph which represents fsa
    :param states: set of states
    :param alpha: set of transitions
    :return:
    """
    for i in range(len(states)):
        for j in range(i + 1, len(states)):
            if not (find_path(graph, states[i], states[j], alpha) or find_path(graph, states[j], states[i], alpha)):
                return 1
    return 0


def is_fsa_complete(graph, alpha):
    """
    Method to determine if fsa is complete
    :param graph: graph: graph which represents fsa
    :param alpha: set of transitions
    :return:
    """
    complete = 1
    for state in d:
        for tr in alpha:
            if tr not in d[state]:
                complete = 0
    return complete


def are_states_reachable(graph, states, initial_state, alpha):
    """
    Method to determine if all state in fsa are reachable from initial one
    :param graph: graph which represents fsa
    :param states: set of state
    :param initial_state: start state
    :param alpha: set of transitions
    :return:
    """
    for state in states:
        if not find_path(graph, initial_state, state, alpha):
            return 0
    return 1


def is_fsa_deterministic(graph, alpha):
    """
    Method to determine if fsa is deterministic
    :param graph: graph which represents fsa
    :param alpha: set of transitions
    :return:
    """
    for state in d:
        tr = graph[state]
        for i in range(len(tr)):
            for j in range(i + 1, len(tr)):
                if tr[i] in alpha and tr[j] in alpha:
                    if tr[i] == tr[j]:
                        return 0
    return 1


def is_adjacent_states(graph, from_st, to_st):
    # print(graph, from_st, to_st)
    s = ''
    for i,st in enumerate(graph[from_st]):
        if i % 2 == 1 and st == to_st:
            s += graph[from_st][i - 1] if len(s)==0 else "|"+graph[from_st][i - 1]
    if from_st == to_st:
        if len(s) == 0:
            s += 'eps'
        else:
            s += '|eps'
    else:
        if len(s) == 0: return "{}"
    return s


def print_table(r):
    for k in range(len(r)):
        print("layer", k)
        for i in range(len(r[k])):
            for j in range(len(r[k][i])):
                print(r[k][i][j], end=' ')
            print()


def kleene_algorithm(graph, states, initial_state, alpha, final_states, transitions):
    """
    r[0] represents previous steps of kleene_algorithm
    r[1] represents future computations of algorighm
    :param graph:
    :param states:
    :param initial_state:
    :param alpha:
    :param final_state:
    :param transitions:
    :return: Regular expression for given DFSA
    """
    r = [[[]]]
    # print(states)
    # r[0].append(states)
    k = 0
    # r[k] = [[[] for i in range(len(states))] for i in range(len(states))]
    r = [[["z" for i in states] for i in states] for i in range(2)]
    for k in range(-1, len(states)):
        r[0] = copy.deepcopy(r[1])
        for i, st1 in enumerate(states):
            for j, st2 in enumerate(states):
                if k == -1:
                    r[1][i][j] = is_adjacent_states(graph, st1, st2)  # st can go
                else:
                    r[1][i][j] = '(' + r[0][i][k] + ')(' + r[0][k][k] + ')*(' + r[0][k][j] + ')|(' + r[0][i][j] + ')'
        # print(k)
        # print_table(r)
    # print()
    # print(r[1][0][0])
    d = {}
    for i,st in enumerate(states):
        d[st] = i
    s = ''
    if len(final_states[0]) == 0:
        return "{}"
    s += r[1][0][d[final_states[0]]]
    for st in final_states[1:]:
        s += '|' + r[1][0][d[st]]

    return s


er1 = 0
er2 = 0
er3 = 0
er4 = 0
er5 = 0
er6 = 0
w1 = 0
w2 = 0
report = 0

lines = []
f = open("fsa.txt")
for line in f:
    lines += [line]
f.close()

data = []
for line in lines:
    line = "".join(line.split("}")[:1])
    line = "".join(line.split("={")[1:])
    line = line.split(",")
    data.append(line)

try:
    states = data[0]
    alpha = data[1]
    init = data[2][0]
    fin = data[3]
    transitions = data[4]
    transitions = [x.split(">") for x in transitions]
except Exception:
    f = open('result.txt', 'w')
    f.write("Error:\nE5: Input file is malformed")
    f.close()
    exit(1)

if init == "":
    er4 = 1
if fin == "":
    w1 = 1

d = {}
for state in states:
    if not state.isalnum():
        f = open('result.txt', 'w')
        f.write("Error:\nE5: Input file is malformed")
        f.close()
        exit(1)
    d[state] = []

for tr in transitions:
    if tr[1] not in alpha:
        er3 = 1
        name_of_invalid_tr = tr[1]
    if tr[0] not in states or tr[2] not in states:
        er1 = 1
        name_of_invalid_state = tr[0] if tr[0] not in states else tr[2]
    else:
        d[tr[0]] = d[tr[0]] + [tr[1], tr[2]]

# print(d)
# print(d['on'][0][0])

er2 = contains_disjoint_states(d, states, alpha)
report = is_fsa_complete(d, alpha)
er6 = not is_fsa_deterministic(d, alpha)
w2 = not are_states_reachable(d, states, init, alpha)

f = open('result.txt', 'w')
if er1:
    f.write("Error:\nE1: A state '" + name_of_invalid_state + "' is not in set of states")
if er2:
    f.write("Error:\nE2: Some states are disjoint")
# if er3:
    # f.write("Error:\nE3: A transition '" + name_of_invalid_tr + "' is not represented in the alphabet")
if er4:
    f.write("Error:\nE4: Initial state is not defined")
if er6:
    f.write("Error:\nE6: FSA is nondeterministic")
# if not (er1 or er2 or er3 or er4):
#     f.write("FSA is complete" if report else "FSA is incomplete")
#     if w1 or w2:
#         f.write("\nWarning:")
#     if w1:
#         f.write("\nW1: Accepting state is not defined")
#     if w2:
#         f.write("\nW2: Some states are not reachable from initial state")
if not (er1 or er2 or er6 or er4):
    s = kleene_algorithm(d, states, init, alpha, fin, transitions)
    f.write(s)
f.close()
