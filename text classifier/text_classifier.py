from sets import Set;
class text_classifier:
    def __init__(self, training):
        self.training = training
        self.labels = list(Set([t[1] for t in self.training]))
        v = Set()
        for t in self.training:
            for w in t[0]:
                v.add(w)
        self.V = len(v)
    
    # (count(w, x) + 1) / (count(x)+|V|)
    def compute(self, word, label):
        count_wx = 0
        for t in self.training:
            if t[1] == label:
                count_wx += t[0].count(word)
        count_x = 0
        for t in self.training:
            if t[1] == label:
                count_x += len(t[0])
        return (count_wx + 1.0) / (count_x + self.V)

    def prob(self, label):
        labels = [t[1] for t in self.training]
        label_count = labels.count(label)
        total = len(labels)
        return label_count * 1.0 / total

    def classify(self, test):
        results = []
        for l in self.labels:
            p = self.prob(l)
            for w in test:
                p *= self.compute(w, l)
            results.append((l, p))
        return max(results, key=lambda item:item[1])

training = [
    [["W1", "W2", "W3", "W4", "W5"], "C"],
    [["W1", "W1", "W4", "W3"], "C"],
    [["W1", "W2", "W5"], "C"],
    [["W5", "W6", "W1", "W2", "W3"], "W"],
    [["W4", "W5", "W6"], "W"],
    [["W4", "W6", "W3"], "F"],
    [["W2", "W2", "W4", "W3", "W5", "W5"], "F"],
]
test = ["W1", "W4", "W6", "W5", "W3"]
tc = text_classifier(training)
print(tc.classify(test))

