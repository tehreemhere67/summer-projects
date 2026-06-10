
import string

def read_file(filename):
    with open(filename, "r") as f:
        text = f.read()
    return text

def clean_and_split(text): ##takes the text, lowercases it, removes punctuation, and splits it into a list of words.
    text = text.lower()
    text = "".join(char for char in text if char not in string.punctuation)
    word_list = text.split()
    return word_list

def count_words(word_list):
    counts = {}
    for word in word_list:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

def filter_stopwords(counts):
    stopwords = {"the", "a", "an", "and", "is", "in", "it", "of", "to", "was", "that", "for", "on", "are", "with", "his", "they", "at", "be", "this", "from", "or", "had", "by", "not", "but", "have", "he", "she", "you", "we", "as", "do", "did"}
    filtered = {}
    for word, count in counts.items():
        if word not in stopwords:
            filtered[word] = count
    return filtered

def get_top_words(counts, n):
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]

def show_bar_chart(top_words):# returns the top n most frequent words
    for word, count in top_words:
        bar = "█" * (count // 5)
        print(f"{word:15} {bar} {count}")

def main():
    filename = input("Enter the filename: ")
    n = int(input("How many top words to show: "))
    file = read_file(filename)
    word_list = clean_and_split(file)
    counts = count_words(word_list)
    filtered = filter_stopwords(counts)
    top_words = get_top_words(filtered, n)
    show_bar_chart(top_words)

main()