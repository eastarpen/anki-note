def single_word(word, path, fout):
    html_url = f'https://dict.youdao.com/w/{word}/'
    us_audio_url = f'https://dict.youdao.com/dictvoice?audio={word}&type=2'
    uk_audio_url = f'https://dict.youdao.com/dictvoice?audio={word}&type=1'
    fout.write(f'curl "{html_url}" > {path}html/{word}.html\n')
    fout.write(f'curl "{us_audio_url}" > {path}audio/us_audio_{word}.mp3\n')
    fout.write(f'curl "{uk_audio_url}" > {path}audio/uk_audio_{word}.mp3\n')
    fout.write('sleep 2s\n\n')

def generage_shell(words, path='./'):
    path = path if path[-1] == '/' else path + '/'
    fout = open('get_words.sh', "w")
    fout.write(f'mkdir -p {path}html/ {path}audio\n\n')
    for word in words:
        single_word(word, path, fout)
    fout.close()
