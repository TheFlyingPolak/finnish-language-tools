from libvoikko import Voikko
from random import choice
from random_finnish_word import get_random_word
import sys

Voikko.setLibrarySearchPath("c:/Voikko")
v = Voikko(u"fi")
SIJAMUOTO = "SIJAMUOTO"
NUMBER = "NUMBER"

SIJAMUOTO_LIST = [
    "nimento", "omanto", "osanto", "olento", "tulento", "kohdanto",
    "sisaolento", "sisaeronto", "sisatulento",
    "ulkoolento", "ulkoeronto", "ulkotulento",
    "vajanto", "seuranto", "keinonto",
]

SIJAMUOTO_MAP = {
    "nimento": "nominative",
    "omanto": "genitive",
    "osanto": "partitive",
    "olento": "essive (being)",
    "tulento": "translative (becoming)",
    "kohdanto": "accusative",
    "sisaolento": "inessive (in)",
    "sisaeronto": "elative (from)",
    "sisatulento": "illative (to)",
    "ulkoolento": "adessive (at)",
    "ulkoeronto": "ablative (from)",
    "ulkotulento": "allative (to)",
    "vajanto": "abessive (without)",
    "seuranto": "comitative (with)",
    "keinonto": "instructive",
}

NUMBER_LIST = ["singular", "plural"]


def get_random_case(word: str) -> dict[str, str] | None:
    analysis = v.analyze(word)
    if not analysis:
        return None
    word_baseform = analysis[0]["BASEFORM"]
    word_class = analysis[0]["CLASS"]

    match word_class:
        case "nimisana":
            return {"BASEFORM": word_baseform, "CLASS": word_class, "NUMBER": choice(NUMBER_LIST), "SIJAMUOTO": choice(SIJAMUOTO_LIST)}
        case "teonsana":
            return {}
        case "laatusana":
            return {}

    return {}

def verify_word(word: str, target_form: dict[str, str]) -> bool:
    analysis = v.analyze(word)
    target_sijamuoto = target_form[SIJAMUOTO]
    target_number = target_form[NUMBER]
    return any(a[SIJAMUOTO] == target_sijamuoto and a[NUMBER] == target_number for a in analysis)

def main():
    if len(sys.argv) <= 1:
        print("Usage: inflection.py xml_file_path")
        return
    dictionary_path = sys.argv[1]

    right_count = 0
    wrong_count = 0

    print("Welcome to the Finnish word inflection exercise. At any point, type 'end' to finish and see your score.")

    while True:
        random_word = get_random_word(dictionary_path, "noun")
        target_form = get_random_case(random_word)
        if target_form is None:
            continue
        number = target_form[NUMBER]
        case = SIJAMUOTO_MAP[target_form[SIJAMUOTO]]

        print("Write the word", random_word, "in the", number, case, "form")
        input_word = input()

        if input_word == "end":
            print("You have ended the exercise. Your score:")
            print("Correct:", right_count)
            print("Incorrect:", wrong_count)
            return

        result = verify_word(input_word, target_form)
        if result:
            right_count += 1
            print("Correct!")
        else:
            wrong_count += 1
            print("Incorrect!")

if __name__ == '__main__':
    main()