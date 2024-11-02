import sys
import string
import syllapy
from src.exception import CustomException
from nltk.tokenize import word_tokenize, sent_tokenize
from src.utils.utils import (
    word_counts,
    syllable_per_words,
    count_personal_pronouns,
    average_word_length,
)


def remove_punctuation(text: str):
    try:
        punctuation = set(string.punctuation) - {"."}  # . will tell the end of sentence
        filtered_text = "".join([char for char in text if char not in punctuation])
        return filtered_text
    except Exception as e:
        raise CustomException(e, sys)


def count_syllables(word):
    return syllapy.count(word)


def analyze_readability(text):
    try:
        text = text.lower()
        text = remove_punctuation(text)
        words = word_tokenize(text)
        sentences = sent_tokenize(text)

        complex_words = [word for word in words if count_syllables(word) > 2]
        average_sentence_length = len(words) / len(sentences)
        percentage_complex_words = len(complex_words) / len(words)
        fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
        average_number_words_per_sentence = len(words) / len(sentences)
        complex_word_count = len(complex_words)
        word_count = word_counts(words)
        syll_text = text.replace(".", "")
        syll_words = word_tokenize(syll_text)
        syllable_per_word = syllable_per_words(syll_words)
        personal_pronouns = count_personal_pronouns(text)
        average_word_len = average_word_length(words)

        return {
            "Average Sentence Length": average_sentence_length,
            "Percentage of Complex Words": percentage_complex_words,
            "Fog Index": fog_index,
            "Average Number of Words per Sentence": average_number_words_per_sentence,
            "Number of Complex Words": complex_word_count,
            "Word Counts": word_count,
            "Syllable per Word": syllable_per_word,
            "Personal Pronouns": personal_pronouns,
            "Average Word Length": average_word_len,
        }

    except Exception as e:
        raise CustomException(e, sys)
