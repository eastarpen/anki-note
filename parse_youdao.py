from bs4 import BeautifulSoup

def get_content(word, filename):
    html = BeautifulSoup(open(filename, "r", encoding="utf-8"), "lxml").find(id="phrsListTab")
    content = str(html.text).split()
    uk_sm, us_sm = content[2], content[4]
    s = ""
    for e in content[5:]: s += e
    return word, uk_sm, us_sm, s


if __name__ == '__main__':
    words = []
    with open('./data/words-01.txt') as fin:
        for line in fin.readlines():
            line = line.strip()
            if line == "": continue
