import re

def tokenizeText(text):
    pattern = r"""
    (?:[A-Za-z]\.){2,}[A-Z]
    | \w+(?:-\w+)+
    | \b([A-Za-z]+)(n't|'s|'ll|'em|'ve|'re|'d)\b
    | \b\w+\b
    | [.,!?;"()\[\]{}<>]
    """
    tokens = []
    for match in re.finditer(pattern, text, flags=re.VERBOSE):
        if match.group(1):
            tokens.extend([match.group(1), match.group(2)])
        else:
            tokens.append(match.group(0))
    return tokens

text = '''I can't believe I'm finally done with my exams! It's been a long, 
tough semester, but I'm so glad it's over. Now, I can finally relax and enjoy my summer break. 
I'm planning to spend lots of time with my friends and family, and maybe even take a little trip somewhere. 
I'm also looking forward to catching up on some reading and watching some TV shows. 
I can't wait to see what the rest of the year has in store.'''
tokens = tokenizeText(text)
tokens = list(set(tokens))
for i in range(0,len(tokens),4):
  print(tokens[i:i+4])

def is_plural_noun_ending_in_y(word):
    # Define vowels
    vowels = set("aeiou")

    # Define states
    S0 = "initial"
    S1 = "vowel"
    S2 = "consonant"
    S3 = "y"
    S4 = "i"
    S5 = "e"
    S6 = "s or final"
    # S7 = "epsilon"
    S7 = "final"

    # Initialize the state to initial
    state = S0

    # Process each character in the word
    for char in word:
      # print(state)
      if state == S0:
          if char in vowels:
              state = S1
          elif char.isalpha():
              state = S2
          elif not char.isalpha():
              return False

      elif state == S1:
          if char =='y':
              state = S3
          elif char.isalpha():
              if char in vowels:
                state = S1
              else:
                state = S2
          elif not char.isalpha():
              return False

      elif state == S2:
          if char =='i':
              state = S4
          elif char.isalpha():
              if char in vowels:
                state = S1
              else:
                state = S2
          elif not char.isalpha():
              return False

      elif state == S3 or state == S5:
          if char == 's':
              state = S6
          elif char.isalpha():
              if char in vowels:
                state = S1
              else:
                state = S2
          elif not char.isalpha():
              return False

      elif state == S4:
          if char == 'e':
              state = S5
          elif char.isalpha():
              if char in vowels:
                state = S1
              else:
                state = S2
          elif not char.isalpha():
              return False

    if state == S6:
        # Final validation step, should be accepting state only for valid ending
        return True

# Test cases
words = ["boys", "toys", "ponies", "skies", "puppies", "boies", "toies", "ponys"]
results = {word: is_plural_noun_ending_in_y(word) for word in words}

for word, result in results.items():
    print(f"{word}: {'Accepted' if result else 'Rejected'}")


import string
def pluralizeFST(word):
    state = 'start'
    exceptionals = ['x' , 'z' , 's']
    result = []
    for letter in word[::-1]:
        if state == 'start':
          if letter == '#':
            state = 'next#'
          else :
            return None
        elif state == 'next#':
          if letter == 's':
            state = 'nexts'
          else :
            return None
        elif state == 'nexts':
          if letter == '^':
            state = 'morpheme'
          else :
            return None
        elif state == 'morpheme':
          if letter in exceptionals:
            state = 'word'
            result.append('s')
            result.append('e')
            result.append(letter)
          else :
            state = 'word'
            result.append('s')
            result.append(letter)
        elif state == 'word':
          result.append(letter)
    return ''.join(result[::-1])

test = ["fox^s#", "boy^s#", "bus^s#", "quiz^s#", "dog^s#"]
result = {word: pluralizeFST(word) for word in test}
for i , k in result.items():
  print(i , ' : ', k)

def min_edit_distance(str1, str2):
    m, n = len(str1), len(str2)

    # Create a matrix to store results of subproblems
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the matrix
    for i in range(m + 1):
        dp[i][0] = i  # Cost of deleting all characters from str1 to get to an empty str2
    for j in range(n + 1):
        dp[0][j] = j  # Cost of inserting all characters to str1 to get to str2

    # Fill the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,    # Deletion
                               dp[i][j - 1] + 1,    # Insertion
                               dp[i - 1][j - 1] + 2)  # Substitution

    # Backtrack to find the operations
    def backtrack_operations():
        operations = []
        i, j = m, n
        while i > 0 or j > 0:
            if i == 0:
                operations.append(f"Insert '{str2[j - 1]}'")
                j -= 1
            elif j == 0:
                operations.append(f"Delete '{str1[i - 1]}'")
                i -= 1
            elif str1[i - 1] == str2[j - 1]:
                i -= 1
                j -= 1
            else:
                if dp[i][j] == dp[i - 1][j] + 1:
                    operations.append(f"Delete '{str1[i - 1]}'")
                    i -= 1
                elif dp[i][j] == dp[i][j - 1] + 1:
                    operations.append(f"Insert '{str2[j - 1]}'")
                    j -= 1
                elif dp[i][j] == dp[i - 1][j - 1] + 1:
                    operations.append(f"Substitute '{str1[i - 1]}' with '{str2[j - 1]}'")
                    i -= 1
                    j -= 1
        return operations[::-1]  # Reverse to get the order of operations

    # Compute the minimum edit distance and the operations
    min_distance = dp[m][n]
    operations = backtrack_operations()
    for i in dp[::-1]:
      print(i)
    print()

    return min_distance, operations

# Example usage
str1 = "intention"
str2 = "execution"

distance, operations = min_edit_distance(str1, str2)
print(f"Minimum Edit Distance: {distance}\n")
print("Edit Operations:")
for op in operations:
    print(op)


import re
from collections import defaultdict, Counter
from itertools import product

# Tokenization function
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# Create vocabulary and bigram frequency table
def build_language_model(corpus):
    tokens = tokenize(corpus)
    vocabulary = set(tokens)

    # Build bigram frequency table
    bigram_freq = defaultdict(Counter)
    for i in range(len(tokens) - 1):
        bigram_freq[tokens[i]][tokens[i + 1]] += 1

    # Normalize to get probabilities
    bigram_prob = defaultdict(dict)
    for word, following in bigram_freq.items():
        total = sum(following.values())
        for next_word, count in following.items():
            bigram_prob[word][next_word] = count / total

    return vocabulary, bigram_prob

# Generate candidate words with 1-edit distance
def generate_candidates(word, vocabulary):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    candidates = set()

    # Insertions
    for i in range(len(word) + 1):
        for char in alphabet:
            candidate = word[:i] + char + word[i:]
            if candidate in vocabulary:
                candidates.add(candidate)

    # Deletions
    for i in range(len(word)):
        candidate = word[:i] + word[i+1:]
        if candidate in vocabulary:
            candidates.add(candidate)

    # Substitutions
    for i in range(len(word)):
        for char in alphabet:
            if char != word[i]:
                candidate = word[:i] + char + word[i+1:]
                if candidate in vocabulary:
                    candidates.add(candidate)

    # Transpositions
    for i in range(len(word) - 1):
        candidate = word[:i] + word[i+1] + word[i] + word[i+2:]
        if candidate in vocabulary:
            candidates.add(candidate)

    return candidates

# Compute sentence probability using bigram model
def sentence_probability(sentence, bigram_prob):
    tokens = tokenize(sentence)
    prob = 1.0
    for i in range(len(tokens) - 1):
        current_word = tokens[i]
        next_word = tokens[i + 1]
        if current_word in bigram_prob and next_word in bigram_prob[current_word]:
            prob *= bigram_prob[current_word][next_word]
        else:
            prob *= 1e-6  # small probability for unknown bigrams
    return prob

# Spell checker function
def spell_checker(input_text, corpus):
    vocabulary, bigram_prob = build_language_model(corpus)

    # Tokenize and identify non-words
    tokens = tokenize(input_text)
    corrected_sentence = []

    for word in tokens:
        if word not in vocabulary:
            candidates = generate_candidates(word, vocabulary)
            if candidates:
                best_candidate = None
                best_prob = 0
                for candidate in candidates:
                    # Replace the word with the candidate and calculate the probability of the entire sentence
                    temp_sentence = input_text.replace(word, candidate, 1)
                    prob = sentence_probability(temp_sentence, bigram_prob)
                    if prob > best_prob:
                        best_prob = prob
                        best_candidate = candidate
                corrected_sentence.append(best_candidate if best_candidate else word)
            else:
                corrected_sentence.append(word)
        else:
            corrected_sentence.append(word)

    return ' '.join(corrected_sentence)

# Example usage
corpus = """
the quick brown fox jumps over the lazy dog
the quick brown fox is very quick and brown
"""
input_text = "the quikc brwn fox jmps ovr the lazy dog"

corrected_text = spell_checker(input_text, corpus)
print(f"Original Text: {input_text}")
print(f"Corrected Text: {corrected_text}")


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report

import warnings; warnings.filterwarnings('ignore')

# Sample data
data = {
    'text': [
        "I love this movie, it's fantastic!",
        "What a great film, I really enjoyed it.",
        "Terrible movie, I hated it.",
        "This was the worst film I have ever seen.",
        "An amazing experience, highly recommend!",
        "Not good, waste of time.",
        "Absolutely wonderful, I would watch it again!",
        "Boring and dull, did not like it at all.",
        "A masterpiece of storytelling, deeply moving.",
        "I was bored throughout the entire film.",
        "The plot was intriguing and kept me on edge.",
        "Awful acting, the characters were unbelievable.",
        "This film exceeded my expectations, truly impressive!",
        "I can't believe I wasted my time on this.",
        "A delightful romp, full of humor and charm.",
        "The special effects were top-notch, loved it!",
        "Very predictable, nothing new to offer.",
        "One of the best movies I've seen in a while!",
        "Disappointing ending that ruined the whole film.",
        "The cinematography was stunning, breathtaking visuals.",
        "An utter disappointment, not worth watching.",
        "Captivating performances, a real treat.",
        "The dialogue felt forced and unnatural.",
        "I found it quite engaging and thought-provoking.",
        "The pacing was slow, but it had its moments.",
        "A forgettable experience, didn't leave an impression.",
        "The soundtrack was beautiful and fitting for the scenes.",
        "I didn't connect with the characters at all.",
        "A heartwarming tale, full of life lessons.",
        "The humor fell flat, not my cup of tea."
    ],
    'label': [
        'positive', 'positive', 'negative', 'negative', 'positive',
        'negative', 'positive', 'negative', 'positive', 'negative',
        'positive', 'negative', 'positive', 'negative', 'positive',
        'positive', 'negative', 'positive', 'negative', 'positive',
        'negative', 'positive', 'negative', 'positive', 'negative',
        'positive', 'negative', 'positive', 'positive', 'positive'
    ]
}


# Create DataFrame
df = pd.DataFrame(data)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.5
                                                    , random_state=42)

# Function to train Naive Bayes with Add-k smoothing
def train_naive_bayes(X_train, y_train, k):
    vectorizer = CountVectorizer()
    X_train_counts = vectorizer.fit_transform(X_train)

    # Get class labels and number of classes
    classes = np.unique(y_train)
    class_counts = {label: np.sum(y_train == label) for label in classes}
    total_counts = sum(class_counts.values())

    # Count feature occurrences per class
    feature_counts = {label: np.zeros(X_train_counts.shape[1]) for label in classes}

    for idx, label in enumerate(y_train):
        feature_counts[label] += X_train_counts[idx].toarray()[0]

    # Add-k smoothing
    vocab_size = len(vectorizer.get_feature_names_out())
    for label in classes:
        feature_counts[label] += k  # Add-k smoothing
        feature_counts[label] /= (class_counts[label] + k * vocab_size)

    return vectorizer, feature_counts, class_counts

# Function to predict
def predict(X_test, vectorizer, feature_counts, class_counts):
    X_test_counts = vectorizer.transform(X_test)
    predictions = []

    for doc in X_test_counts:
        class_probabilities = {}
        for label in class_counts:
            # Calculate the log probabilities for numerical stability
            class_prob = np.log(class_counts[label] / sum(class_counts.values()))
            word_prob = np.sum(doc.toarray() * np.log(feature_counts[label] + 1e-9))  # Small value for stability
            class_probabilities[label] = class_prob + word_prob

        predictions.append(max(class_probabilities, key=class_probabilities.get))

    return predictions

# Evaluate the model for different k values
k_values = [0.25, 0.75, 1.0]
results = {}

for k in k_values:
    vectorizer, feature_counts, class_counts = train_naive_bayes(X_train, y_train, k)
    predictions = predict(X_test, vectorizer, feature_counts, class_counts)
    accuracy = accuracy_score(y_test, predictions)
    results[k] = accuracy
    print(f"Accuracy for k={k}: {accuracy:.4f}")
    print(classification_report(y_test, predictions))

# Summary of results
print("Summary of Results:")
for k, accuracy in results.items():
    print(f"k={k}: Accuracy={accuracy:.4f}")


class D2Dictionary:
  def __init__(self, matrix , rows , cols):
    import numpy as np
    matrix = np.array(matrix)
    if matrix.shape[0] != len(rows) or matrix.shape[1] != len(cols):
      raise ValueError(f"The Dimensions do not match, Given dimension {matrix.shape}, Provided rows and columns {rows , cols} respectively")
    self._matrix = matrix
    self._rows   = rows
    self._cols   = cols
    self._rowIds = {word:i for i , word in enumerate(rows)}
    self._colIds = {word:i for i , word in enumerate(cols)}
    if len(self._rowIds) != len(self._rows):
      raise ValueError("The rows are not unique")
    if len(self._colIds) != len(self._cols):
      raise ValueError("The columns are not unique")

  def __getitem__(self, index):
    if isinstance(index , tuple):
      if len(index) == 2:
        row , col = index
        return self._matrix[self._rowIds[row] , self._colIds[col]]
      elif len(index) == 1:
        row = index
        return self._matrix[self._rowIds[row] , :]

  def __setitem__(self, index, value):
    if isinstance(index , tuple):
      if len(index) == 2:
        row , col = index
        self._matrix[self._rowIds[row] , self._colIds[col]] = value

  def show(self):
    import pandas as pd
    return pd.DataFrame(self._matrix , index=self._rows , 
    columns=self._cols)

  def shape(self):
    return self._matrix.shape

  def rows(self):
    return self._rows

  def cols(self):
    return self._cols

import numpy as np

transmissions = [
    [0.5  , 0.25 , 0.25 , 0    , 0   ],
    [0.25 , 0.5  , 0    , 0    , 0.25],
    [0.25 , 0    , 0.25 , 0.25 , 0.25],
    [0.75 , 0    , 0.25 , 0    , 0   ],
    [0.25 , 0    , 0.25 , 0    , 0.5 ],
]
rows = ['<s>' , 'NN' , 'VB' , 'JJ' , 'RB'  ]
cols = ['NN'  , 'VB' , 'JJ' , 'RB' , '</s>']

transmissions = D2Dictionary(transmissions , rows , cols)

emmissions = [
    [0.1  , 0.01 , 0.01],
    [0.01 , 0.1  , 0.01],
    [0    , 0    , 0.1 ],
    [0    , 0    , 0.1 ]
]

sentence = 'time flies fast'

row  = ['NN'  , 'VB' , 'JJ' , 'RB']
cols = sentence.split(' ')

emmissions = D2Dictionary(emmissions , row , cols)

def viterbi(sentence, transmissions, emmissions , show = True):
    import math
    import numpy as np

    # Prepare sentence and tag structures
    sentence = sentence.split(' ')
    cols = ['<s>'] + sentence + ['</s>']
    tags = emmissions.rows()
    rows = ['<s>'] + tags + ['</s>']

    # Initialize DP table and pointer table
    table = np.full((len(rows), len(cols)), -np.inf)  # Use -inf     for log-space
    table = D2Dictionary(table, rows, cols)
    pointer = D2Dictionary([[None for _ in range(len(cols))] for _ 
    in range(len(rows))], rows, cols)

    # Start state
    table['<s>', '<s>'] = 0  # log(1) = 0
    pointer['<s>', '<s>'] = 'Origin'

    # Initialization for first word
    assigned = []
    first_word = sentence[0]
    for tag in tags:
        emmit = emmissions[tag, first_word]
        transit = transmissions['<s>', tag]
        if emmit > 0 and transit > 0:
            table[tag, first_word] = math.log(emmit) + \
            math.log(transit) + table['<s>', '<s>']
            pointer[tag, first_word] = '<s>'
            assigned.append(tag)

    # Iteration for intermediate words
    for i in range(1, len(sentence)):
        word = sentence[i]
        prev_word = sentence[i - 1]
        new_assigned = []
        for tag in tags:
            emmit = emmissions[tag, word]
            if emmit <= 0:
                continue
            for prev_tag in assigned:
                transit = transmissions[prev_tag, tag]
                if transit <= 0:
                    continue
                prob = table[prev_tag, prev_word] + \
                math.log(transit) + math.log(emmit)
                if prob > table[tag, word]:
                    table[tag, word] = prob
                    pointer[tag, word] = prev_tag
            if table[tag, word] > -np.inf:
                new_assigned.append(tag)
        assigned = new_assigned

    # Final iteration for </s>
    last_word = sentence[-1]
    for tag in assigned:
        transit = transmissions[tag, '</s>']
        if transit > 0:
            prob = table[tag, last_word] + math.log(transit)
            if prob > table['</s>', '</s>']:
                table['</s>', '</s>'] = prob
                pointer['</s>', '</s>'] = tag



    # Back Tracking :
    posTags = {word:None for word in sentence}
    current = pointer['</s>' , '</s>']
    for word in sentence[::-1] :
      posTags[word] = current
      current = pointer[current , word]

    if show :
      table.show()
      pointer.show()
    return posTags , table , pointer

tags , table , pointer = viterbi(sentence , transmissions , emmissions)
print(tags)
print(table.show())
print(pointer.show())

from collections import defaultdict, Counter
import math

class BigramModel:
    def __init__(self, corpus):
        self.unigramFreq = Counter()
        self.bigramFreq = defaultdict(Counter)
        self.totalWords = 0
        self.train(corpus)

    def train(self, corpus):
        for sentence in corpus:
            words = ['<s>'] + sentence.split() + ['</s>']
            self.totalWords += len(words)
            self.unigramFreq.update(words)
            for i in range(len(words) - 1):
                self.bigramFreq[words[i]][words[i + 1]] += 1

    def bigramProbability(self, w1, w2):
        if self.unigramFreq[w1] == 0:
            return 0
        return self.bigramFreq[w1][w2] / self.unigramFreq[w1]

    def sentenceProbability(self, sentence):
        words = ['<s>'] + sentence.split() + ['</s>']
        probability = 0
        for i in range(len(words) - 1):
            prob = self.bigramProbability(words[i], words[i + 1])
            if prob > 0:
                probability += math.log(prob)
            else:
                probability += float('-inf')
        return math.exp(probability) if probability > float('-inf') else 0

    def predict(self, word):
        if word not in self.bigramFreq:
            return None
        next_word = max(self.bigramFreq[word], key=self.bigramFreq[word].get)
        return next_word

corpus = [
    "the cat sat on the mat",
    "the cat is small",
    "the dog sat on the rug",
    "a dog chased the cat"
]

model = BigramModel(corpus)
word = str(input("Enter the word\t: "))
print(f"\nMost probable word following '{word}': {model.predict(word)}")

sentence = str(input("Enter the sentence\t: "))
print(f"\nProbability of the sentence '{sentence}': {model.sentenceProbability(sentence):.10f}")

import math
from collections import Counter, defaultdict

def computeTfIdf(documents):
    """
    Compute the TF-IDF matrix for the given documents.
    Args:
        documents (list of str): List of training documents.

    Returns:
        tfIdfMatrix (dict of dict): TF-IDF scores for each word in 
        each document.
        vocabulary (set): Set of all unique words in the corpus.
    """
    tokenizedDocs = [doc.lower().split() for doc in documents]
    vocabulary = set(word for doc in tokenizedDocs for word in doc)

    termFrequencies = [Counter(doc) for doc in tokenizedDocs]
    docLengths = [len(doc) for doc in tokenizedDocs]
    tfMatrix = [
        {word: freq / docLengths[i] for word, freq in 
        termFreq.items()}
        for i, termFreq in enumerate(termFrequencies)
    ]

    docCount = len(documents)
    wordDocFrequency = defaultdict(int)
    for doc in tokenizedDocs:
        for word in set(doc):
            wordDocFrequency[word] += 1

    idfScores = {
        word: math.log(docCount / wordDocFrequency[word])
        for word in vocabulary
    }

    tfIdfMatrix = [
        {word: tfMatrix[i].get(word, 0) * idfScores[word] for word 
        in vocabulary}
        for i in range(docCount)
    ]

    return tfIdfMatrix, vocabulary

def cosineSimilarity(vector1, vector2):
    """
    Compute the cosine similarity between two vectors.
    Args:
        vector1 (dict): Sparse representation of the first vector.
        vector2 (dict): Sparse representation of the second vector.

    Returns:
        similarity (float): Cosine similarity between the two 
        vectors.
    """
    dotProduct = sum(vector1[word] * vector2.get(word, 0) for word 
    in vector1)
    norm1 = math.sqrt(sum(value ** 2 for value in vector1.values()))
    norm2 = math.sqrt(sum(value ** 2 for value in vector2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dotProduct / (norm1 * norm2)

def documentSimilarity(tfIdfMatrix, docIndex1, docIndex2):
    """
    Compute the cosine similarity between two documents.
    Args:
        tfIdfMatrix (list of dict): TF-IDF matrix.
        docIndex1 (int): Index of the first document.
        docIndex2 (int): Index of the second document.

    Returns:
        similarity (float): Cosine similarity between the two 
        documents.
    """
    return cosineSimilarity(tfIdfMatrix[docIndex1], 
    tfIdfMatrix[docIndex2])

def wordSimilarity(tfIdfMatrix, vocabulary, word1, word2):
    """
    Compute the cosine similarity between two words based on their 
    TF-IDF vectors across all documents.
    Args:
        tfIdfMatrix (list of dict): TF-IDF matrix.
        vocabulary (set): Set of all unique words in the corpus.
        word1 (str): The first word.
        word2 (str): The second word.

    Returns:
        similarity (float): Cosine similarity between the two words.
    """
    if word1 not in vocabulary or word2 not in vocabulary:
        return 0.0

    wordVector1 = {i: doc.get(word1, 0) for i, doc in 
    enumerate(tfIdfMatrix)}
    wordVector2 = {i: doc.get(word2, 0) for i, doc in 
    enumerate(tfIdfMatrix)}

    return cosineSimilarity(wordVector1, wordVector2)

documents = [
    "the cat sat on the mat",
    "the dog sat on the rug",
    "a cat chased a mouse",
    "the mat was under the cat"
]

tfIdfMatrix, vocabulary = computeTfIdf(documents)

Documents = [f'Document {i}' for i in range(len(documents))]
columns   = [word for word in vocabulary]

import pandas as pd
test = pd.DataFrame(tfIdfMatrix, index=Documents, columns=columns)
print(test)

import math
from collections import Counter, defaultdict

def computePpmiMatrix(documents):
    """
    Compute the PPMI (Positive Pointwise Mutual Information) matrix 
    for the given documents.
    Args:
        documents (list of str): List of training documents.

    Returns:
        ppmiMatrix (dict of dict): PPMI scores for each word pair.
        vocabulary (set): Set of all unique words in the corpus.
    """
    tokenizedDocs = [doc.lower().split() for doc in documents]
    vocabulary = set(word for doc in tokenizedDocs for word in doc)

    cooccurrence = defaultdict(Counter)
    wordCounts = Counter()
    totalCount = 0

    for doc in tokenizedDocs:
        for i, word in enumerate(doc):
            wordCounts[word] += 1
            totalCount += 1
            for j in range(max(0, i - 4), min(len(doc), i + 5)):
                if i != j:
                    cooccurrence[word][doc[j]] += 1

    ppmiMatrix = defaultdict(dict)
    for word1 in vocabulary:
        for word2 in vocabulary:
            jointCount = cooccurrence[word1][word2]
            if jointCount == 0:
                ppmiMatrix[word1][word2] = 0
            else:
                pWord1 = wordCounts[word1] / totalCount
                pWord2 = wordCounts[word2] / totalCount
                pJoint = jointCount / totalCount
                pmi = math.log(pJoint / (pWord1 * pWord2), 2)
                ppmiMatrix[word1][word2] = max(pmi, 0)

    return ppmiMatrix, vocabulary

def cosineSimilarity(vector1, vector2):
    """
    Compute the cosine similarity between two vectors.
    Args:
        vector1 (dict): Sparse representation of the first vector.
        vector2 (dict): Sparse representation of the second vector.

    Returns:
        similarity (float): Cosine similarity between the two 
        vectors.
    """
    dotProduct = sum(vector1[word] * vector2.get(word, 0) for word 
    in vector1)
    norm1 = math.sqrt(sum(value ** 2 for value in vector1.values()))
    norm2 = math.sqrt(sum(value ** 2 for value in vector2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dotProduct / (norm1 * norm2)

def documentSimilarity(ppmiMatrix, doc1, doc2):
    """
    Compute the cosine similarity between two documents based on 
    PPMI vectors.
    Args:
        ppmiMatrix (dict of dict): PPMI matrix.
        doc1 (str): The first document.
        doc2 (str): The second document.

    Returns:
        similarity (float): Cosine similarity between the two 
        documents.
    """
    docVector1 = Counter(word for word in doc1.split())
    docVector2 = Counter(word for word in doc2.split())

    combinedVector1 = {word: sum(ppmiMatrix[word].get(w, 0) for w 
    in docVector1) for word in ppmiMatrix}
    combinedVector2 = {word: sum(ppmiMatrix[word].get(w, 0) for w 
    in docVector2) for word in ppmiMatrix}

    return cosineSimilarity(combinedVector1, combinedVector2)

def wordSimilarity(ppmiMatrix, word1, word2):
    """
    Compute the cosine similarity between two words based on their 
    PPMI vectors.
    Args:
        ppmiMatrix (dict of dict): PPMI matrix.
        word1 (str): The first word.
        word2 (str): The second word.

    Returns:
        similarity (float): Cosine similarity between the two words.
    """
    return cosineSimilarity(ppmiMatrix[word1], ppmiMatrix[word2])

documents = [
    "the cat sat on the mat",
    "the dog sat on the rug",
    "a cat chased a mouse",
    "the mat was under the cat"
]

ppmiMatrix, vocabulary = computePpmiMatrix(documents)
words = list(vocabulary)

test = pd.DataFrame(ppmiMatrix, index=words, columns=words)
doc1 = "the cat sat on the mat"
doc2 = "the dog sat on the rug"
print(f"\nCosine similarity between documents:\n'{doc1}' and \
'{doc2}': {documentSimilarity(ppmiMatrix, doc1, doc2):.4f}")


word1 = "cat"
word2 = "dog"
print(f"\nCosine similarity between words '{word1}' and '{word2}': \
{wordSimilarity(ppmiMatrix, word1, word2):.4f}")

print(test)

from collections import Counter, defaultdict
import math

class NaiveBayesClassifier:
    def __init__(self):
        self.senseCounts = Counter()
        self.wordCounts = defaultdict(Counter)
        self.totalWordsInSense = Counter()
        self.vocabulary = set()
        self.totalDocuments = 0

    def train(self, trainingData):
        for sentence, sense in trainingData:
            self.totalDocuments += 1
            self.senseCounts[sense] += 1
            words = sentence.lower().split()
            for word in words:
                self.wordCounts[sense][word] += 1
                self.totalWordsInSense[sense] += 1
                self.vocabulary.add(word)

    def predict(self, sentence):
        words = sentence.lower().split()
        vocabularySize = len(self.vocabulary)
        maxLogProb = float('-inf')
        bestSense = None

        for sense in self.senseCounts:
            logProb = math.log(self.senseCounts[sense] / 
            self.totalDocuments)
            for word in words:
                wordCount = self.wordCounts[sense][word]
                logProb += math.log((wordCount + 1) / 
                (self.totalWordsInSense[sense] + vocabularySize))

            if logProb > maxLogProb:
                maxLogProb = logProb
                bestSense = sense

        return bestSense

    def disambiguateWord(self, word, testSentence):
        return self.predict(testSentence)

trainingData = [
    ("I love fish. The smoked bass fish was delicious.", "fish"),
    ("The bass fish swam along the line.", "fish"),
    ("He hauled in a big catch of smoked bass fish.", "fish"),
    ("The bass guitar player played a smooth jazz line.", "guitar"),
]

testSentence = "He loves jazz. The bass line provided the \
foundation for the guitar solo in the jazz piece."

classifier = NaiveBayesClassifier()
classifier.train(trainingData)

print(testSentence)
predictedSense = classifier.disambiguateWord("bass", testSentence)
print(f"Predicted sense of 'bass': {predictedSense}")
