import genanki
import anki
import parse_youdao


def read_words(filename):
    """
    read word from file named filename
    """
    words = []
    with open(filename) as fin:
        for word in fin.readlines():
            word = word.strip()
            if word == "": continue
            words.append(word)
    return words

def get_fields(filename, html_path):
    """
    pass in a file named filename stored words, and the words page stored directory
    return fields list
    format of element in fields list is like (word, uk_soundmark, us_soundmark, chinese_meaning)
    if any word failed to be parsed, it should store into ./wrong.txt, and you shell get information from console output
    """
    if html_path[-1] != '/':
        html_path += '/'
    words = read_words(filename)
    fields = []
    wrong = None
    for word in words:
        filename = f"{html_path}{word}.html"
        try:
            fields.append(parse_youdao.get_content(word, filename))
        except:
            print(f"{word} wrong!")
            if wrong == None:
                wrong = open("./wrong.txt", "w")
            wrong.write(word+'\n')
    if wrong != None: wrong.close()
    return fields

def generage_deck_UK(noteFields, deck_name, model_name, audio_path):
    """
    generate deck
    should only called by package_word_english_to_chinese
    """
    if audio_path[-1] != '/':
        audio_path += '/'
    model_fields = ["english", "uk", "uk_audio", "chinese"]
    back = "{{english}} <br> {{uk}}{{uk_audio}} <hr id=answer> {{chinese}}"
    css = '.card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; } '
    model_templates = ["Card 1", "{{english}}", back]
    deck = anki.Ankideck(deck_name, model_name, model_fields, model_templates, css)
    audios = []
    for fields in noteFields:
        english, uk, chinese = fields[0], fields[1], fields[3]
        uk_audio = f"[sound:uk_audio_{english}.mp3]"
        lst = [english, uk, uk_audio, chinese]
        deck.addNote(lst)
        audios.append(f"{audio_path}uk_audio_{english}.mp3")
    package = genanki.Package(deck)
    package.media_files=audios
    package.write_to_file(f"{deck_name}.apkg")

def generage_deck_US(noteFields, deck_name, model_name, audio_path):
    """
    generate deck
    should only called by package_word_english_to_chinese
    """
    model_fields = ["english", "us", "us_audio", "chinese"]
    back = "{{english}} <br> {{us}}{{us_audio}} <hr id=answer> {{chinese}}"
    css = '.card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; } '
    model_templates = ["Card 1", "{{english}}", back]
    deck = anki.Ankideck(deck_name, model_name, model_fields, model_templates, css)
    audios = []
    for fields in noteFields:
        english, us, chinese = fields[0], fields[2], fields[3]
        us_audio = f"[sound:us_audio_{english}.mp3]"
        lst = [english, us, us_audio, chinese]
        deck.addNote(lst)
        audios.append(f"{audio_path}us_audio_{english}.mp3")
    package = genanki.Package(deck)
    package.media_files=audios
    package.write_to_file(f"{deck_name}.apkg")

def package_word_english_to_chinese(deckName,  wordsFile, resourceDir,modelName = "Word_ETC", us=True):
    """
    :param: wordsFile file name of which stored the wordsFile
    :param: resourceDir directory where stored the data, should contains audio/ and html/
    make and package deck whose card type is Word_ETC, and US style defaulted
    """
    if resourceDir[-1] != '/':
        resourceDir += '/'
    fields = get_fields(wordsFile, resourceDir+'html/')
    if us:
        generage_deck_US(fields, deckName, modelName, resourceDir+'audio/')
    else:
        generage_deck_UK(fields, deckName, modelName, resourceDir+'audio/')

if __name__ == '__main__':
    package_word_english_to_chinese("CET6::ETC::Words-02", )
