from libvoikko import Voikko
from random import choice
from random_finnish_word import get_random_word
import sys

v = Voikko("fi")
SIJAMUOTO = "SIJAMUOTO"
NUMBER = "NUMBER"
TENSE = "TENSE"
PERSON = "PERSON"
PARTICIPLE = "PARTICIPLE"

TENSE_MAP = {"present_simple": "present", "past_imperfective": "past imperfect"}

SIJAMUOTO_LIST = [
    "nimento",
    "omanto",
    "osanto",
    "olento",
    "tulento",
    "kohdanto",
    "sisaolento",
    "sisaeronto",
    "sisatulento",
    "ulkoolento",
    "ulkoeronto",
    "ulkotulento",
    "vajanto",
    "seuranto",
    "keinonto",
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
PERSON_LIST = ["1", "2", "3"]


def get_random_case(word: str) -> dict[str, str] | None:
    analysis_list = v.analyze(word)
    if not analysis_list:
        return None
    analysis = next(a for a in analysis_list if a["BASEFORM"] == word)
    if not analysis:
        return None
    word_class = analysis["CLASS"]

    match word_class:
        case "nimisana":
            return {
                "BASEFORM": word,
                "CLASS": word_class,
                "NUMBER": choice(NUMBER_LIST),
                "SIJAMUOTO": choice(SIJAMUOTO_LIST),
            }
        case "teonsana":
            return get_random_verb_form(word)
        case "laatusana":
            return None

    return None


def verify_word(word: str, target_form: dict[str, str]) -> bool:
    analysis = v.analyze(word)
    return any(_verify_word_helper(a, target_form) for a in analysis)


def _verify_word_helper(analysis: dict, target_form: dict[str, str]):
    for key, value in target_form.items():
        if key not in analysis or analysis[key] != value:
            return False
    return True


def get_random_verb_form(word: str) -> dict[str, str]:
    tense = choice(["present", "imperfect", "perfect"])
    match tense:
        case "present":
            return {
                "BASEFORM": word,
                "CLASS": "teonsana",
                "TENSE": "present_simple",
                "PERSON": choice(PERSON_LIST),
                "NUMBER": choice(NUMBER_LIST),
            }
        case "imperfect":
            return {
                "BASEFORM": word,
                "CLASS": "teonsana",
                "TENSE": "past_imperfective",
                "PERSON": choice(PERSON_LIST),
                "NUMBER": choice(NUMBER_LIST),
            }
        # case "perfect":
        # TODO: return target base form for the word "olla"
        # TODO: set BASEFORM as the actual target word instead of infinitive
        # return {"BASEFORM": word, "CLASS": "laatusana", "PARTICIPLE": "past_active"}


def main():
    if len(sys.argv) <= 1:
        print("Usage: inflection.py xml_file_path [word_class]")
        return
    dictionary_path = sys.argv[1]

    word_class = ""
    if len(sys.argv) >= 2:
        word_class = sys.argv[2]
        if word_class != "noun" and word_class != "verb":
            print("Parameter word_class can only have value 'noun' or 'verb'")
            return

    right_count = 0
    wrong_count = 0

    print(
        "Welcome to the Finnish word inflection exercise. At any point, type 'end' to finish and see your score."
    )

    while True:
        current_word_class = (
            choice(["noun", "verb"]) if word_class == "" else word_class
        )
        # TODO: do not return word from dictionary which itself has no analysis result from voikko
        random_word = get_random_word(dictionary_path, current_word_class)
        target_form = get_random_case(random_word)
        if target_form is None:
            continue

        if current_word_class == "noun":
            _prompt_noun(random_word, target_form)
        elif current_word_class == "verb":
            _prompt_verb(random_word, target_form)
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


def _prompt_noun(random_word: str, target_form: dict[str, str]):
    number = target_form[NUMBER]
    case = SIJAMUOTO_MAP[target_form[SIJAMUOTO]]
    print("Write the word", random_word, "in the", number, case, "form")


def _prompt_verb(random_word: str, target_form: dict[str, str]):
    if TENSE in target_form:
        tense = TENSE_MAP[target_form[TENSE]]
        person = target_form[PERSON]
        number = target_form[NUMBER]
        print(
            "Write the word",
            random_word,
            "in the",
            person,
            "person",
            number,
            tense,
            "form",
        )
    else:
        print("Write the word", random_word, "in the past perfect form")


if __name__ == "__main__":
    main()
