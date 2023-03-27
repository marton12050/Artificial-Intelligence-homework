import copy
import sys

def normalize(dist):
    return [x * 1 / (sum(dist)) for x in dist]

def enumaration_ask(X, e, bn):
    Q =[]
    for i in range(X.get_state()):
        Q.append(enumaration_all(bn, copy.deepcopy(e)|{str(X.get_index()): i}))
        #print("got one",i)
    return normalize(Q)

def enumaration_all(vars: list, e) -> float:
    if not vars:
        return 1.0
    Y = vars[0]
    if str(Y.get_index()) in e:
        return Y.get_P(e) * enumaration_all(vars[1:], e)
    else:
        probs = []
        e2 = copy.deepcopy(e)
        for y in range(Y.get_state()):
            e2[str(Y.get_index())] = y
            probs.append(Y.get_P(e2) * enumaration_all(vars[1:], e2))
        return sum(probs)


class BayesNode:
    def get_state(self):
        return self.num_state

    def set_index(self, idx):
        self.index = idx

    def get_P(self, e):
        prob = ""
        prob += str(e[str(self.index)])
        for p in range(self.num_parent):
            prob += "," + str(e[self.parents[p]])
        return self.probs[prob]

    def get_index(self):
        return self.index

    def __init__(self, data):
        self.index = None
        data = data.split('\t')
        self.num_state = int(data[0])
        self.num_parent = int(data[1])
        parents = []
        for i in range(self.num_parent):
            parents.append(data[i+2])
        self.parents = parents
        #print(parents,end="")
        self.probs = dict()

        for i in range(2+self.num_parent, len(data)):
            if self.num_parent == 0:
                tempprob = data[i].split(",")
                for j in range(len(tempprob)):
                    self.probs[str(j)] = float(tempprob[j])
            else:
                temp = data[i].split(":")
                tempprob = temp[1].split(",")
                for j in range(len(tempprob)):
                    self.probs[str(j) + ","+ temp[0]] = float(tempprob[j])

       # print(self.probs)


f = sys.stdin
#f = open("input1.txt", "r")
#nodes
N_v = int(f.readline())
Bayes_nodes = []
for i in range(N_v):
   # print(i,end="")
    temp = BayesNode(f.readline())
    temp.set_index(i)
    Bayes_nodes.append(temp)

#evidenciák
N_e = int(f.readline())
evidences = dict()
for i in range(N_e):
    idx, value = f.readline().split("\t")
    evidences[idx] = int(value)
#print("evidence",evidences)

#a cél változó amitől függ a hasznonsság
goalvar_idx = int(f.readline())
#print(goalvar_idx)
choose_state = int(f.readline())

#haszonsság
usefullness = dict()
for i in range(Bayes_nodes[goalvar_idx].get_state()):
    for j in range(choose_state):
        usefullness[str(i)+","+str(j)] = float(f.readline().split()[2])
#print(usefullness)
#f.close()
# task
The_probs = enumaration_ask(Bayes_nodes[goalvar_idx], evidences, Bayes_nodes)

best = sum([The_probs[x]*usefullness[str(x)+","+str(0)] for x in range(Bayes_nodes[goalvar_idx].get_state())])
best_idx = 0
for i in range(choose_state):
    current = sum([The_probs[x]*usefullness[str(x)+","+str(i)] for x in range(Bayes_nodes[goalvar_idx].get_state())])
    if current > best:
        best = current
        best_idx = i
for i in The_probs:
    print(i)
print(best_idx)