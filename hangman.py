from wordfreq import top_n_list


def organize(words):
    longest_word = 25
    organized_words = []
    for _ in range(longest_word):
        organized_words.append([])
    for word in words:
        if word.isalpha():
            letters = len(word)
            if letters < longest_word:
                organized_words[letters].append(word)
    return organized_words


def hangman(words, letters):
    groups = {}
    for word in words[letters]:
        word = word.lower()
        for letter in set(word):
            pattern = ""
            for i in range(letters):
                if word[i] != letter:
                    pattern += word[i]
                else:
                    pattern += "_"

            if pattern not in groups:
                groups[pattern] = []

            if word not in groups[pattern]:
                groups[pattern].append(word)

    return groups


language = "en"
most_common_words = 10000
words = top_n_list(language, most_common_words)
words = organize(words)

for letters in range(3, 10):
    groups = hangman(words, letters)
    for group in groups:
        if len(groups[group]) > 10:
            print(group, groups[group])
