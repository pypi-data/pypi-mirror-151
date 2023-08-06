import copy
import re


# @params
# tokens: list
# raw_labels: list of list
# raw_text: str
# ex.
# tokens = ['明日', 'は', '田中', 'さん', 'に', '会う']
# raw_labels = [[3, 5, 'PERSON']]
# raw_text = ['明日は田中さんに会う']
#
# @return
# label_list: list
# ex.
# label_list = ['O', 'O', 'B-PERSON', 'O', 'O', 'O']
def convert_to_token_labels(tokens: list, raw_labels: list, raw_text: str, subword=None, mode='BIO'):
    raw_text = raw_text.lower()
    tokenized_text = "".join(tokens)
    if subword:
        new_tokens = [t.strip(subword) if len(t) > len(subword) else t for t in tokens]
        tokenized_text = "".join(new_tokens)
    i, j = 0, 0
    new_labels = copy.deepcopy(raw_labels)
    while i < len(tokenized_text) and j < len(raw_text):
        if tokenized_text[i] == raw_text[j]:
            i += 1
            j += 1
            continue
        while tokenized_text[i] != raw_text[j]:
            j += 1
        for new_label, label in zip(new_labels, raw_labels):
            if j <= label[0]:
                new_label[0] = label[0] - (j - i)
                new_label[1] = label[1] - (j - i)
            elif j < label[1]:
                new_label[1] = label[1] - (j - i)
    # init return list
    label_list = ['O'] * len(tokens)

    for label in new_labels:
        begin = label[0]
        end = label[1]
        label_text = label[2]
        position = 0
        targets = []

        for idx, word in enumerate(tokens):
            if type(subword) is str:
                word = re.sub(subword, "", word)
            if begin <= position < end:
                targets.append(idx)
            position += len(word)

        if mode == 'BIEO':
            if len(targets) == 1:
                label_list[targets[0]] = f'B-{label_text}'
            elif len(targets) == 2:
                label_list[targets[0]] = f'B-{label_text}'
                label_list[targets[1]] = f'E-{label_text}'
            elif len(targets) >= 3:
                label_list[targets.pop(0)] = f'B-{label_text}'
                label_list[targets.pop(-1)] = f'E-{label_text}'
                for i in targets:
                    label_list[i] = f'I-{label_text}'
        else:
            if len(targets) == 1:
                label_list[targets[0]] = f'B-{label_text}'
            elif len(targets) >= 2:
                label_list[targets.pop(0)] = f'B-{label_text}'
                label_list[targets.pop(-1)] = f'I-{label_text}'
                for i in targets:
                    label_list[i] = f'I-{label_text}'

    return label_list


if __name__ == "__main__":
    # tokenized_text = ['明日', 'は', '田中', 'さん', 'に', '会う']
    # tokenized_text = ['明日', 'は', '田', '##中', 'さん', 'に', '会う']
    # labels = [[3, 5, 'PERSON']]
    # print(convert(tokenized_text, labels, subword="##"))

    # i am tommy.
    # [[5, 10, 'PER']]
    tokenized_text = ['i', 'am', 'tom', '##my', '.']
    labels = [[5, 10, 'PER']]
    raw_text = "i am tommy."
    print(convert_to_token_labels(tokenized_text, labels, raw_text=raw_text, subword="##"))
