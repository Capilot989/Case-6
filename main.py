from deep_translator import GoogleTranslator
from textblob import TextBlob


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
        sentiment = "позитивная"
    elif polarity < -0.1:
        sentiment = "негативная"
    else:
        sentiment = "нейтральная"

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
    count = text.count('.') + text.count('?') + text.count('!')
    return count if count > 0 else 1


def detect_language(text):
    """
    Определяет язык текста (RU или ENG).

    Args:
        text (str): Текст для анализа.

    Returns:
        str: Язык.
    """
    no_space = text.replace(' ', '')
    if not no_space:
        return 'UNKNOWN'

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
        return 'Текст очень легко читается (для младших школьников).'

    elif fre_index(text) > 50:
        return 'Простой текст (для школьников).'

    elif fre_index(text) > 25:
        return 'Текст немного трудно читать (для студентов).'

    elif fre_index(text) < 25:
        return 'Текст трудно читается (для выпускников ВУЗов).'


if __name__ == "__main__":
    text = input("Введите текст: ")

    results = analyze_sentiment(text)

    print(f"Тональность: {results['sentiment']}")
    print(f"Полярность: {results['polarity']}")
    print(f"Объективность: {results['objectivity_percent']}%")
    print(f"Количество слов: {count_words(text)}")
    print(f"Количество гласных: {count_vowels(text)}")
    print(f"Количество предложений: {count_sentences(text)}")
    print(f"Язык: {detect_language(text)}")
    print(f"Индекс читаемости (FRE): {fre_index(text)}")
    print(reading_difficulty(text))
