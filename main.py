from deep_translator import GoogleTranslator
from textblob import TextBlob
import re
import ru_local as ru


def translate_text(text, target_language='en'):
    """
    Переводит текст на указанный язык.

    Args:
        text (str): Текст для перевода.
        target_language (str): Язык, на который нужно перевести текст.

    Returns:
        str: Переведенный текст.
    """
    translator = GoogleTranslator(source='auto', target=target_language)
    return translator.translate(text)


def analyze_sentiment(text):
    """
    Анализирует тональность текста.

    Args:
        text (str): Текст для анализа.

    Returns:
        dict: Словарь с результатами анализа, включающий:
            - polarity (float): Полярность текста (от -1 до 1).
            - subjectivity (float): Субъективность текста (от 0 до 1).
            - sentiment (str): Общая тональность текста
              (позитивная, негативная или нейтральная).
            - objectivity_percent (float): Объективность текста в процентах.
            - subjectivity_percent (float): Субъективность текста в процентах.
    """
    english_text = translate_text(text, 'en')
    analysis = TextBlob(english_text)

    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0.1:
        sentiment = ru.POSITIVE
    elif polarity < -0.1:
        sentiment = ru.NEGATIVE
    else:
        sentiment = ru.NEUTRAL

    return {
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "objectivity_percent": (1 - subjectivity) * 100,
        "subjectivity_percent": subjectivity * 100,
    }


def count_words(text):
    """
    Подсчитывает количество слов в тексте.

    Args:
        text (str): Текст для подсчета.

    Returns:
        int: Количество слов.
    """
    return len(text.split())


def count_vowels(text):
    """
    Подсчитывает количество гласных в тексте.

    Args:
        text (str): Текст для подсчета.

    Returns:
        int: Количество гласных.
    """
    vowels = 'aeiouyаоуыэиёеяю'
    return sum(1 for letter in text.lower() if letter in vowels)


def count_sentences(text):
    """
    Подсчитывает количество предложений в тексте.

    Args:
        text (str): Текст для подсчета.

    Returns:
        int: Количество предложений.
    """
    if not text or text.strip() == '':
        return 0

    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)


def detect_language(text):
    """
    Определяет язык текста (RU или ENG).

    Args:
        text (str): Текст для анализа.

    Returns:
        str: Язык.
    """
    no_space = text.replace(' ', '')
    total_u = sum(ord(letter) for letter in no_space)
    
    if total_u // len(no_space) > 500:
        return 'RU'
    return 'ENG'


def fre_index(text):
    """
    Вычисляет индекс читаемости текста по формуле Флеша.

    Args:
        text (str): Текст для анализа.

    Returns:
        float: Индекс читаемости.
    """
    if count_words(text) == 0:
        return 0

    asl = count_words(text) / count_sentences(text)
    asw = count_vowels(text) / count_words(text)

    if detect_language(text) == 'RU':
        return 206.835 - 1.52 * asl - 65.14 * asw
    return 206.835 - 1.015 * asl - 84.6 * asw


def reading_difficulty(text):
    """
        Вычисляет сложноость чтения текста, исходя их формулы Флеша.

        Args:
            text (str): Текст для анализа.

        Returns:
            str: Сложность чтения.
    """
    if fre_index(text) > 80:
        return ru.SIMPLE

    elif fre_index(text) > 50:
        return ru.MEDIUM

    elif fre_index(text) > 25:
        return ru.HARD

    elif fre_index(text) < 25:
        return ru.IMPOSSIBLE


if __name__ == "__main__":
    text = input(ru.TEXT)

    results = analyze_sentiment(text)

    print(f"{ru.SENTIMENT} {results['sentiment']}")
    print(f"{ru.POLARITY} {results['polarity']}")
    print(f"{ru.OBJJECTIVITY}: {results['objectivity_percent']}%")
    print(f"{ru.WORDS}: {count_words(text)}")
    print(f"{ru.VOWELS}: {count_vowels(text)}")
    print(f"{ru.SENTENCES} {count_sentences(text)}")
    print(f"{ru.LANGUAGE}: {detect_language(text)}")
    print(f"{ru.FRE_INDEX}: {fre_index(text)}")
    print(reading_difficulty(text))
