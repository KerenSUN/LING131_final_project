from random import choice
from collections import defaultdict


def load_grammar(filename):
    f = open(filename)
    rules = defaultdict(list)
    for line in f:
        lhs = line.split()[0]
        rhs = line.split()[2:]
        rules[lhs].append(rhs)
    return rules


def make_template(rules, root_symbol, template):
    if root_symbol not in rules:
        template.append(root_symbol)
    else:
        rhs = choice(rules[root_symbol])

        for part in rhs:
            make_template(rules, part, template)

    return template


def load_lexicon(filename1, filename2):
    f1 = open(filename1)
    f2 = open(filename2)

    output_file = open("all_lexicon.txt", "w")
    for line in f1:
        output_file.write(line)
    output_file.close()
    output_file = open("all_lexicon.txt", "a")
    for line in f2:
        output_file.write(line)
    output_file.close()
    f = open("all_lexicon.txt")

    lexicon = defaultdict(list)
    lexicon["<NULL>"] = [""]
    for line in f:
        linelist = line.split()
        linejoin = " ".join(linelist[0:-1])
        lexicon[linelist[-1]].append(linejoin + " ")
    # print(lexicon)
    return lexicon


def make_sentence(template, lexicon):
    sentence = ""
    for POS in template:
        candidates = lexicon[POS]
        sentence += choice(candidates)
    sentence = sentence[0].upper() + sentence[1:-1]
    sentence += choice([".", "!"])
    return sentence

