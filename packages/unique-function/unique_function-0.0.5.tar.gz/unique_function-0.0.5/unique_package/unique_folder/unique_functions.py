from collections import Counter
import argparse

cache = {}


def unique_symbols(text):
    if text in cache:
        return cache[text]
    counter = Counter(text)
    single = [symbol for symbol, count in counter.items() if count == 1]
    content = single
    cache[text] = content
    return single


def output_result(init_word, count_result):
    print(f'"{init_word}" => {len(count_result)} \n {", ".join(count_result)}   are present once')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=argparse.FileType("r"), help="path_to_text_file")
    parser.add_argument("--string", help="your string")
    args = parser.parse_args()
    print(args)
    text = args.file.read() if args.file else args.string
    result = unique_symbols(text)
    output_result(text, result)


if __name__ == "__main__":
    main()
