import re
from collections import Counter
import random


class TrigramModel:
    def __init__(self, text):
        self.text = text

        self.words = text.split()
        self.unigram_counter = Counter(self.words)

        self.bigram_tokens = [
            "--".join(pair) for pair in zip(self.words[:-1], self.words[1:])
        ]
        self.bigram_counter = Counter(self.bigram_tokens)

        self.trigram_tokens = [
            "--".join(triple)
            for triple in zip(self.words[:-2], self.words[1:-1], self.words[2:])
        ]
        self.trigram_counter = Counter(self.trigram_tokens)

        self.unigram_probabilities = {}
        for word in self.unigram_counter:
            self.unigram_probabilities[word] = self.unigram_counter[word] / len(
                self.words
            )

        self.bigram_probabilities = {}
        for bigram in self.bigram_tokens:
            unigram_context, curr_word = bigram.split("--")
            prob = self.bigram_counter[bigram] / self.unigram_counter[unigram_context]
            if unigram_context in self.bigram_probabilities:
                self.bigram_probabilities[unigram_context][curr_word] = prob
            else:
                self.bigram_probabilities[unigram_context] = {curr_word: prob}

        self.trigram_probabilities = {}
        for trigram in self.trigram_tokens:
            split_trigram = trigram.split("--")
            bigram_context, curr_word = (
                "--".join(split_trigram[0:2]),
                split_trigram[2],
            )
            prob = self.trigram_counter[trigram] / self.bigram_counter[bigram_context]
            if bigram_context in self.trigram_probabilities:
                self.trigram_probabilities[bigram_context][curr_word] = prob
            else:
                self.trigram_probabilities[bigram_context] = {curr_word: prob}

    def sample_word_unigram(self):
        words = list(self.unigram_probabilities.keys())
        probabilities = list(self.unigram_probabilities.values())
        sampled_word = random.choices(words, weights=probabilities, k=1)[0]
        return sampled_word

    def sample_word_bigram(self, unigram_context):
        if unigram_context not in self.bigram_probabilities:
            return self.sample_word_unigram()
        words = list(self.bigram_probabilities[unigram_context].keys())
        probabilities = list(self.bigram_probabilities[unigram_context].values())
        sampled_word = random.choices(words, weights=probabilities, k=1)[0]
        return sampled_word

    def sample_word_trigram(self, bigram_context):
        if bigram_context not in self.trigram_probabilities:
            unigram_context = bigram_context.split("--")[1]
            return self.sample_word_bigram(unigram_context)
        words = list(self.trigram_probabilities[bigram_context].keys())
        probabilities = list(self.trigram_probabilities[bigram_context].values())
        sampled_word = random.choices(words, weights=probabilities, k=1)[0]
        return sampled_word


text = open("./time_machine.txt", "r").read()
text = re.sub("[^A-Za-z]+", " ", text).lower()
trigram = TrigramModel(text)

DEFAULT_LENGTH = 15
context = input("Input initial context (only words separated by space): ")
length = input(f"Enter length of generated text (default: {DEFAULT_LENGTH}): ")
if len(length) == 0:
    length = DEFAULT_LENGTH

split_context = context.split()
# if initial context is less than 2 words
if len(split_context) == 0:
    word = trigram.sample_word_unigram()
    split_context = [word]
if len(split_context) == 1:
    word = trigram.sample_word_bigram(split_context[0])
    context = " ".join([split_context[0], word])

print(context, end=" ")
context = "--".join(context.split()[-2:])
for _ in range(int(length)):
    word = trigram.sample_word_trigram(context)
    print(word, end=" ")
    context = f"{context.split('--')[1]}--{word}"
print()
