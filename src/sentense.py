import genanki
import anki

def get_fields(filename):
    """
    read sentenses from file named filename
    return list like [[english, chinese], [english, chinese]]
    """
    fields, ele = [], []
    with open(filename, "r", encoding="utf-8") as fin:
        i = 0;
        for line in fin.readlines():
            line = line.strip()
            if line == "": continue
            i += 1;
            ele.append(line)
            if i%2 == 0:
                fields.append(ele)
                ele = []
    return fields


def generage_deck(noteFields, deck_name, model_name):
    """
    generate deck
    should only called by package_word_english_to_chinese
    """
    model_fields = ["front", "back"]
    front = '<div class="textarea">{{front}}</div>'
    back = '<div class="textarea">{{front}}</div><hr><div class="textarea">{{back}}</div>'
    css = (''+ 
    '/* https://www.w3schools.com/css/tryit.asp?filename=trycss_form_textarea */\n'+
    '.textarea {\n'+
      '\twidth: 100%;\n'+
      '\theight: 150px;\n'+
      '\tpadding: 12px 20px;\n'+
      '\tbox-sizing: border-box;\n'+
      '\tborder: 2px solid #ccc;\n'+
      '\tborder-radius: 4px;\n'+
      '\tbackground-color: #f8f8f8;\n'+
      '\tfont-size: 16px;\n'+
      '\tfont-family: "Lucida Console";\n'+
      '\ttext-align: left;\n'+
    '}'
    )
    model_templates = ["Card 1", front, back]
    deck = anki.Ankideck(deck_name, model_name, model_fields, model_templates, css)
    for fields in noteFields:
        front, back = fields[0], fields[1]
        lst = [front, back]
        deck.addNote(lst)
    package = genanki.Package(deck)
    package.write_to_file(f"{deck_name}.apkg")

def package_sentenses(deckName,  sentensesFile,modelName = "text"):
    """
    :param: wordsFile file name of which stored the wordsFile
    :param: resourceDir directory where stored the data, should contains audio/ and html/
    make and package deck whose card type is Word_ETC, and US style defaulted
    """
    fields = get_fields(sentensesFile)
    generage_deck(fields, deckName, modelName)

if __name__ == '__main__':
    sentensesFile = "../data/sentences-01.txt"
    package_sentenses("CET6::CTE:sentence-01", sentensesFile)
