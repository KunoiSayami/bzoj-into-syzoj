#!/usr/bin/env python
import json
import os

from bs4 import BeautifulSoup


class OutputGenerator:
    def __init__(self, id: int, title: str, time_limit: int, memory_limit: int, description: str, input_format: str,
                 output_format: str, input_sample: str, output_sample: str, hint: str, source: str, img: list[str]):
        self.id = id
        self.title = title.strip()
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.description = description.strip()
        self.input_format = input_format.strip()
        self.output_format = output_format.strip()
        self.input_sample = input_sample.strip()
        self.output_sample = output_sample.strip()
        self.hint = hint.strip()
        self.source = source.strip()
        self.img = img

    def to_dict(self) -> dict[str, [str, int]]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description.replace('\n', '\n<br />'),
            'time_limit': self.time_limit,
            'memory_limit': self.memory_limit,
            'input_format': self.input_format.replace('\n', '\n<br />'),
            'output_format': self.output_format.replace('\n', '\n<br />'),
            'input_sample': self.input_sample.replace('\n', '\n<br />'),
            'output_sample': self.output_sample.replace('\n', '\n<br />'),
            'source': self.source,
            'hint': self.hint,
            'img': self.img
        }


def get_img(s: str) -> str:
    if s.startswith('..'):
        return s.rsplit('/', maxsplit=1)[1]
    return s


def generator(item: str, s: str, *, p: bool = False) -> OutputGenerator:
    soup = BeautifulSoup(s, 'lxml')
    ret = soup.find(class_='ui-content-header').text.strip()
    title, tmp = ret.split('\u65f6\u95f4\u9650\u5236\uff1a')
    time_limit, memory_limit = tmp.split('\u7a7a\u95f4\u9650\u5236\uff1a')
    ret = soup.find(class_='card-inner')
    # print(title, time_limit, memory_limit
    if (imgs := soup.findAll('img')) and p:
        list(map(lambda x: get_img(x['src']), imgs))
    description, tmp = ret.text.replace('\xa0', '').split('\u9898\u76ee\u63cf\u8ff0',
                                                          maxsplit=1)[1].split('\u8f93\u5165\u683c\u5f0f', maxsplit=1)
    input_format, tmp = tmp.split('\u8f93\u51fa\u683c\u5f0f', maxsplit=1)
    output_format, tmp = tmp.split("\u6837\u4f8b\u8f93\u5165", maxsplit=1)
    input_sample, tmp = tmp.split("\u6837\u4f8b\u8f93\u51fa", maxsplit=1)
    # print(tmp)
    output_sample, tmp = tmp.split('\u63d0\u793a', maxsplit=1)
    hint, source = tmp.split('\u9898\u76ee\u6765\u6e90', maxsplit=1)
    b = OutputGenerator(int(item.split('.')[0]), title, int(time_limit.strip().split('s')[0]),
                        int(memory_limit.lower().split('m')[0].strip()), description,
                        input_format, output_format, input_sample, output_sample, hint, source,
                        list(map(lambda x: x['src'].rsplit('/', maxsplit=1)[1], imgs)))
    if p:
        print(b.to_dict())
    return b


def main():
    for item in os.listdir("bzojch-master/p"):
        with open(f'bzojch-master/p/{item}', errors='ignore') as fin:
            try:
                x = generator(item, fin.read())
                with open(f'bzojch-master/json/{item.split(".html")[0]}.json', 'w') as fout:
                    json.dump(x.to_dict(), fout, ensure_ascii=False, indent='\t', separators=(',', ': '))
            except ValueError:
                print('error:', item)

def main2():
    with open('bzojch-master/p/1001.html', errors='ignore') as fin:
        generator('1111', fin.read(), p=True)


main()
