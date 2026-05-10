from xml.etree.ElementTree import parse as parse_xml
import random
import sys


def get_random_word(file_path: str, wclass_filter: str | None = None):
    """
    Parse Joukahainen XML Finnish dictionary and return a random word. Can specify what word class should be returned.
    :param file_path: Path to Joukahainen dictionary XML file
    :param wclass_filter: Type of word that should be returned. By default, returns any word type
    :return: Random word in base form
    """

    words = parse_dictionary(file_path, wclass_filter)
    return random.choice(words)


def parse_dictionary(file_path: str, wclass_filter: str | None = None) -> list[str]:
    tree = parse_xml(file_path)
    root = tree.getroot()

    words = []
    for word in root.findall("word"):
        classes = [c.text for c in word.findall("classes/wclass")]
        if any(c.startswith("pnoun_") for c in classes):
            continue
        if wclass_filter and wclass_filter not in classes:
            continue

        styles = [f.text for f in word.findall("style/flag")]
        if styles and "dialect" in styles:
            continue

        forms = [f.text for f in word.findall("forms/form")]

        # Compound words are written using the = character in the Joukahainen dictionary
        # e.g. arktinen -> pale=arktinen, arja=lainen
        # If the only form for a word is compound, take form as is and drop the = character.
        # Otherwise, take the first non-compound form
        clean_forms = [f for f in forms if "=" not in f]
        canonical = clean_forms[0] if clean_forms else forms[0].replace("=", "")

        if canonical:
            words.append(canonical)

    return words

def main():
    if len(sys.argv) <= 1:
        print("Usage: random_finnish_word.py xml_file_path [word_class_filter]")
        return
    path = sys.argv[1]
    word = get_random_word(path, sys.argv[2]) if len(sys.argv) > 2 else get_random_word(path)
    print(word)

if __name__ == '__main__':
    main()