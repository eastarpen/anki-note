import genanki
import anki
import parse_youdao


def read_words(filename):
    words = []
    with open(filename) as fin:
        for word in fin.readlines():
            word = word.strip()
            if word == "": continue
            words.append(word)
    return words

def get_fields(filename, html_path = './html/'):
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

def generage_deck(noteFields, deck_name, model_name, audio_path='./audio/'):
      # include uk
    # model_fields = ["english", "uk", "us", "uk_audio", "us_audio", "chinese"]
    # back = "{{english}} <br> 英{{uk}}{{uk_audio}} 美{{us}}{{us_audio}} <hr id=answer> {{chinese}}"
    # remove uk
    model_fields = ["english", "us", "us_audio", "chinese"]
    back = "{{english}} <br> {{us}}{{us_audio}} <hr id=answer> {{chinese}}"
    css = '.card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; } '
    model_templates = ["model", "{{english}}", back]
    deck = anki.Ankideck(deck_name, model_name, model_fields, model_templates, css)
    audios = []
    for fields in noteFields:
        english, uk, us, chinese = fields[0], fields[1], fields[2], fields[3]
        uk_audio, us_audio = f"[sound:uk_audio_{english}.mp3]", f"[sound:us_audio_{english}.mp3]"
        # lst = [english, uk, us, uk_audio, us_audio, chinese]
        lst = [english, us, us_audio, chinese]
        deck.addNote(lst)
        # audios.append(f"{audio_path}uk_audio_{english}.mp3")
        audios.append(f"{audio_path}us_audio_{english}.mp3")
    package = genanki.Package(deck)
    package.media_files=audios
    package.write_to_file(f"{deck_name}.apkg")


if __name__ == '__main__':
    filename = './data/words-01.txt'
    fields = get_fields(filename)
    generage_deck(fields, "CET6::ETC::01", "XDF")
