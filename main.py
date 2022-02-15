import requests
import srsly
from processors.api import TextWithRules

from settings import RULES_PATH, DATA_PATH


def data_from_jsonl():
    sentences = list(srsly.read_jsonl(str(DATA_PATH)))[0]
    mapped_sentences = []
    for sentence in sentences:
        mapped_sentences.append(sentence[0])

    rules = ''
    with open(str(RULES_PATH), "r") as file:
        rules = file.read()

    parse_chunks(mapped_sentences, rules)


def parse_chunks(mapped_sentences, rules):
    chunk_size = 10
    for i in range(0, len(mapped_sentences), chunk_size):
        sentences = mapped_sentences[i:i + chunk_size]
        container = TextWithRules(sentences, rules)
        json_data = container.to_JSON()
        response = requests.post("http://localhost:8888/api/odin/extract",
                                 data=json_data,
                                 headers={'content-type': 'application/json; charset=utf-8'},
                                 timeout=None
                                 )

        content = response.content.decode("utf-8")


if __name__ == '__main__':
    data_from_jsonl()
