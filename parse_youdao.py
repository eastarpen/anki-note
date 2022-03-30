from bs4 import BeautifulSoup

def get_content(word, filename):
    """
    pass in a word and a html (full path) file's name which is crawled by dict.youdao.com/w/?
    return (word, uk_soundmark, us_soundmark, chinese_meaning)
    """
    html = BeautifulSoup(open(filename, "r", encoding="utf-8"), "lxml").find(id="phrsListTab")
    content = str(html.text).split()
    uk_sm, us_sm = content[2], content[4]
    s = ""
    for e in content[5:]: s += e
    return word, uk_sm, us_sm, s
