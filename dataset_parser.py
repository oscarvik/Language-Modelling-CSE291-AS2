import json
import string

exclude = set(string.punctuation)

filename = "../../CopyLanguage-Modelling-CSE291-AS2/data/brown/brown.train.txt"
out_file = "../../CopyLanguage-Modelling-CSE291-AS2/data/brown/brown.train.json"

vocab_file = '../../CopyLanguage-Modelling-CSE291-AS2/data/ptb.vocab.json'

file = open(filename, "r")
vocab = json.load(open(vocab_file, "r"))["w2i"]

unk = "<unk>"
eos = 3

skipped = 0
no_unknowns = 0

data = {}
i = 0
for sentence in file.readlines():
    sentence = ''.join(ch for ch in sentence if ch not in exclude)
    words = sentence.strip().split(" ")
    if not len(sentence) or len(words) > 59:
        skipped += 1
        continue

    input_vector = [2]
    for word in sentence.split(" "):
        if not len(word) or (len(word) == 1 and ord(word) == 10):
            continue

        word = word.lower()
        if word in vocab:
            input_vector.append(vocab[word])
        else:
            #print(word, [ord(c) for c in word])
            no_unknowns += 1
            input_vector.append(vocab[unk])

    length = len(input_vector)
    target_vector = input_vector[1:] + [eos]

    input_vector += [0] * (60 - length)
    target_vector += [0] * (60 - length)

    data[i] = {
        "input": input_vector,
        "target": target_vector,
        "length": length
    }
    i+=1

print("Data parsed:")
print("\tNo unknowns:", no_unknowns)
print("\tNo sentences:", i)
json.dump(data, open(out_file, "w"))
