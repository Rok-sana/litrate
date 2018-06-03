import codecs
import re
from langdetect import detect
import urllib.request
import requests


def get_word_accentuation(word):
    ukr_vowels = "аоуеиіяюєї"
    res = []
    for c in word:
        if c in ukr_vowels:
            res.append("_")
        if ord(c) == 769:
            res.pop(len(res) - 1)
            res.append("o")
    return res


def find_word1(word):
    url = "http://ukrlit.org/slovnyk/"
    cont = requests.get(url + word)
    mathced = re.findall(r'(?ui)(?<=<article class="word__description">\n                    <p><strong>)[^\n\t ,.<]*',
                         str(cont.text))
    answer = list(map(lambda x: x.lower(), mathced))
    if len(answer) > 0:
        return answer[0]
    return word


def find_word2(word):
    url = "http://sum.in.ua/?swrd="
    cont = requests.get(url + word)
    mathced = re.findall(r'(?ui)(?<=<div itemprop="articleBody"><p><strong itemprop="headline" class="title">)[^\n\t]*(?=</strong>)',
                         str(cont.text))
    answer = list(map(lambda x: x.lower(), mathced))
    if answer:
        mathced = re.findall(
            r'(?ui)([^\t\n]*)<span class="stressed[^\t\n]*">(.)</span><span class="stress">́</span>([^\t\n]*)',
            str(answer[0]))
        if not mathced:
            return word
        res = mathced[0][0] + mathced[0][1] + chr(769) + mathced[0][2]
        return res
    if len(answer) > 0:
        return answer[0]
    return word


def find_word(word):
    return find_word1(word)
    #return find_word2(word)


def get_normalized_lines(text):
    lines = text.lower().split('\n')
    for i in range(len(lines)):
        lines[i] = re.findall(r"[\w']+", lines[i])
    normalized_lines = []
    for line in lines:
        if len(line) == 0:
            continue
        normalized_lines.append([])
        for word in line:
            normalized_lines[len(normalized_lines) - 1] += get_word_accentuation(find_word(word))
    return normalized_lines


def valid_line(line):
    for c in line:
        if c == 'o':
            return True
    return False


def split_same_sizes_lines(lines):
    len_lines = dict()
    for line in lines:
        curr_len = len(line)
        if not len_lines.get(curr_len):
            len_lines[curr_len] = []
        len_lines[curr_len].append(line)
    resulting_lines = dict()
    for curr_len in len_lines:
        resulting_lines[curr_len] = ['_'] * curr_len
        for i in range(curr_len):
            accentuation = 0
            for line in len_lines[curr_len]:
                if valid_line(line):
                    accentuation += int(line[i] == 'o')
            resulting_lines[curr_len][i] = float(accentuation) / float(len(len_lines[curr_len]))
    return resulting_lines


def generate_horey(l):
    horey = [0.0] * l
    for i in range(l):
        if i % 2 == 0:
            horey[i] = 1
    return horey


def generate_yamb(l):
    yamb = [0.0] * l
    for i in range(l):
        if (i + 1) % 2 == 0:
            yamb[i] = 1
    return yamb


def generate_dactil(l):
    dactil = [0.0] * l
    for i in range(l):
        if i % 3 == 0:
            dactil[i] = 1
    return dactil


def generate_amphibr(l):
    amphibr = [0.0] * l
    for i in range(l):
        if (i + 2) % 3 == 0:
            amphibr[i] = 1
    return amphibr


def generate_anapest(l):
    anapest = [0.0] * l
    for i in range(l):
        if (i + 1) % 3 == 0:
            anapest[i] = 1
    return anapest


def get_SSE(ideal_y, y):
    e_2 = [(ideal_y[i] - y[i])**2 for i in range(len(y))]
    return sum(e_2)


def check_resulting_line(line):
    l = len(line)
    check_l = [0] * l
    horey = generate_horey(l)
    yamb = generate_yamb(l)
    dactil = generate_dactil(l)
    amphibr = generate_amphibr(l)
    anapest = generate_anapest(l)
    answer = ["horey", "yamb", "dactil", "amphibr", "anapest"]
    e_2 = [get_SSE(horey, line),
           get_SSE(yamb, line),
           get_SSE(dactil, line),
           get_SSE(amphibr, line),
           get_SSE(anapest, line)]
    e_2_check = [get_SSE(horey, check_l),
           get_SSE(yamb, check_l),
           get_SSE(dactil, check_l),
           get_SSE(amphibr, check_l),
           get_SSE(anapest, check_l)]
    for i in range(len(e_2)):
        e_2[i] /= e_2_check[i]
    return answer[e_2.index(min(e_2))], e_2.index(min(e_2))


def define_poem_size(file_path):
    answer = ["хорей", "ямб", "дактиль", "амфибрахий", "анапест"]
    answer_indx = [0, 0, 0, 0, 0]
    with codecs.open(file_path, "r", encoding="utf8") as f:
        text = f.read()
        lines = get_normalized_lines(text)
        res_lines = split_same_sizes_lines(lines)
        for k in res_lines:
            if k == 0:
                continue
            acc = float(sum(res_lines[k])) / k
            if acc > 0.05:
                local_answer, i = check_resulting_line(res_lines[k])
                answer_indx[i] += 1
    return answer[answer_indx.index(max(answer_indx))]
