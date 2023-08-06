# encoding=utf-8
from .io import *
import random


class DataStructure:
    spo = {
        "sentence": "内容简介《宜兴紫砂图典》由故宫出版社出版",
        "triplets": [
            {"s": {"text": "宜兴紫砂图典", "l": 5, "r": 11},
             "p": {"text": "出版社", "l": 15, "r": 18},
             "o": {"text": "故宫出版社", "l": 13, "r": 18}}],
        "source": "baidu"
    }
    ner_input_example = '这句话一共有两个实体分别为大象和老鼠。'
    ner_label_example = list('OOOOOOOOOOOOO') + ['B-s', 'I-s'] + ['O'] + ['B-o', 'I-o'] + ['O']


'''
try:
    from ltp import LTP
except:
    pass

class STEM(object):
    def __init__(self, IPT_MODEL_PATH):
        self.ltp = LTP(IPT_MODEL_PATH)

    def start(self, sentence):
        seg, hidden = self.ltp.seg([sentence])
        dep = self.ltp.dep(hidden)  # , graph=False)
        seg, dep = seg[0], dep[0]
        for i in dep:
            # 主谓宾
            if 'SBV' == i[2]:
                subject = seg[i[0]]
                verb = seg[i[1]]
            if 'VOB' in i[2]:
                if seg[i[1]] == verb:
                    object = seg[i[]]

                return subject

        return None
class STEM(object):
    def __init__(self, IPT_MODEL_PATH):
        self.ltp = LTP(IPT_MODEL_PATH)

    def start(self, sentence):
        """
        用语义角色标注工具
        :param sentence: "他叫汤姆去拿外衣。"
        :return:  events: [['他', '叫', '汤姆', '去', '拿', '外衣'], ['汤姆', '拿', '外衣']]
        """
        # 语义角色标注方法
        seg, hidden = self.ltp.seg([sentence])
        srl = self.ltp.srl(hidden)
        seg, srl = seg[0], srl[0]
        events = []
        for wdx, each_srl in enumerate(srl):
            if each_srl:
                args = []
                for arg in each_srl:
                    args.extend(seg[arg[1]:arg[2] + 1])
                # 添加上谓词
                args.insert(each_srl[0][2] - each_srl[0][1] + 1, seg[wdx])
                events.append(args)
        # print(events)
        return events

    def start_dep_method(self, sentence):
        # seg, hidden = self.ltp.seg([sentence])
        # dep = self.ltp.dep(hidden)#, graph=False)
        # seg, dep = seg[0], dep[0]
        # for i in dep:
        #     # 主谓宾
        #     if 'SBV' == i[2]:
        #         subject = seg[i[0]]
        #         verb = seg[i[1]]
        #     if 'VOB' in i[2]:
        #         if seg[i[1]] == verb:
        #             object = seg[i]
        #         return subject
        return None

IPT_MODEL_PATH = './tiny'
stem = STEM(IPT_MODEL_PATH)
sentence = '美国袭击伊拉克'
a = stem.start(sentence)
'''


# 这个是另一种
# 数据示例为：{"sentence": "兴族闪蝶，Morpho patroclus，Morpho achilles patroclus，节肢动物门、昆虫纲、鳞翅目、蛱蝶科、闪蝶属的一种蝴蝶", "triplets": [{"s": {"text": "兴族闪蝶", "l": 0, "r": 4}, "p": {"text": "目", "l": 60, "r": 61}, "o": {"text": "鳞翅目", "l": 58, "r": 61}}, {"s": {"text": "蛱蝶科", "l": 62, "r": 65}, "p": {"text": "目", "l": 60, "r": 61}, "o": {"text": "鳞翅目", "l": 58, "r": 61}}, {"s": {"text": "蝴蝶", "l": 72, "r": 74}, "p": {"text": "目", "l": 60, "r": 61}, "o": {"text": "鳞翅目", "l": 58, "r": 61}}, {"s": {"text": "闪蝶属", "l": 66, "r": 69}, "p": {"text": "目", "l": 60, "r": 61}, "o": {"text": "鳞翅目", "l": 58, "r": 61}}], "source": "baidu"}
def subject_object_labeling_new(spo_list, text):
    pass


# 这个是传统格式的
# 数据格式示例：{"postag": [{"word": "兴族闪蝶", "pos": "nz"}, {"word": "，", "pos": "w"}, {"word": "Morpho patroclus", "pos": "nz"}, {"word": "，", "pos": "w"}, {"word": "Morpho achilles patroclus", "pos": "nz"}, {"word": "，", "pos": "w"}, {"word": "节肢动物门", "pos": "nz"}, {"word": "、", "pos": "w"}, {"word": "昆虫纲", "pos": "nz"}, {"word": "、", "pos": "w"}, {"word": "鳞翅目", "pos": "n"}, {"word": "、", "pos": "w"}, {"word": "蛱蝶科", "pos": "nz"}, {"word": "、", "pos": "w"}, {"word": "闪蝶属", "pos": "nz"}, {"word": "的", "pos": "u"}, {"word": "一种", "pos": "m"}, {"word": "蝴蝶", "pos": "n"}], "text": "兴族闪蝶，Morpho patroclus，Morpho achilles patroclus，节肢动物门、昆虫纲、鳞翅目、蛱蝶科、闪蝶属的一种蝴蝶", "spo_list": [{"predicate": "目", "object_type": "目", "subject_type": "生物", "object": "鳞翅目", "subject": "兴族闪蝶"}, {"predicate": "目", "object_type": "目", "subject_type": "生物", "object": "鳞翅目", "subject": "蛱蝶科"}, {"predicate": "目", "object_type": "目", "subject_type": "生物", "object": "鳞翅目", "subject": "蝴蝶"}, {"predicate": "目", "object_type": "目", "subject_type": "生物", "object": "鳞翅目", "subject": "闪蝶属"}]}
def subject_object_labeling(spo_list, text):
    # TODO
    '''
    百度那种有spo字典的数据，给标成。草，看不懂，得找找哪里用的
    :param spo_list:
    :param text:
    :return: labeling_list
    '''

    def _spo_list_to_spo_predicate_dict(spo_list):
        spo_predicate_dict = dict()
        for spo_item in spo_list:
            predicate = spo_item["predicate"]
            subject = spo_item["subject"]
            object = spo_item["object"]
            spo_predicate_dict.setdefault(predicate, []).append((subject, object))
        return spo_predicate_dict

    def _index_q_list_in_k_list(q_list, k_list):
        """Known q_list in k_list, find index(first time) of q_list in k_list"""
        q_list_length = len(q_list)
        k_list_length = len(k_list)
        for idx in range(k_list_length - q_list_length + 1):
            t = [q == k for q, k in zip(q_list, k_list[idx: idx + q_list_length])]
            # print(idx, t)
            if all(t):
                # print(idx)
                idx_start = idx
                return idx_start

    def _labeling_type(spo, spo_type):
        idx_start = _index_q_list_in_k_list(q_list=spo, k_list=text)
        labeling_list[idx_start] = 'B-' + spo_type
        if len(spo) == 2:
            labeling_list[idx_start + 1] = 'I-' + spo_type
        elif len(spo) >= 3:
            labeling_list[idx_start + 1: idx_start + len(spo)] = ['I-' + spo_type] * (len(spo) - 1)
        else:
            pass

    spo_predicate_dict = _spo_list_to_spo_predicate_dict(spo_list)
    labeling_list = ['O'] * len(text)
    # count = 0
    for predicate, spo_list_form in spo_predicate_dict.items():
        if predicate in text:
            for (spo_subject, spo_object) in spo_list_form:
                # if predicate not in spo_subject and predicate not in spo_object:
                _labeling_type(spo_subject, 'SUB')
                _labeling_type(spo_object, 'OBJ')
                _labeling_type(predicate, 'PRE')
                # count += 1
                # print(count)
                # if count == 2:
                #     print()
            if labeling_list != ['O'] * len(text):
                return labeling_list
    return None


def label(text, labels):
    '''
    返回两列的标记数据序列
    :param text:
    :param labels:
    :return:
    '''
    train_sequence = '\n'.join(
        ['\t'.join(i) if i[0] != ' ' else '[null]\t{}'.format(i[1]) for i in zip(list(text), labels)])
    return train_sequence


def convert_crf_format_10_fold(corpus, objdir_path):
    '''
    把已经是crf格式的数据，分成十折。
    para:

    '''
    # corpus = list(range(1,22))
    j_mkdir(objdir_path)
    split_position = int(len(corpus) / 10)
    for k in range(0, 10):
        if k == 9:
            dev_set = corpus[k * split_position:]
            train_set = corpus[:k * split_position]
        else:
            dev_set = corpus[k * split_position: (k + 1) * split_position]
            train_set = corpus[:k * split_position] + corpus[(k + 1) * split_position:]
        writetxt_w_list(train_set, os.path.join(objdir_path, 'train{}.txt'.format(k + 1)))
        writetxt_w_list(dev_set, os.path.join(objdir_path, 'test{}.txt'.format(k + 1)))
        writetxt_w_list(dev_set, os.path.join(objdir_path, 'dev{}.txt'.format(k + 1)))


def read_seq_res(path, labels):
    '''
    读序列标注三列数据的方法
    :param path:
    :param labels:
    :return:
    '''
    with codecs.open(path, 'r', 'utf-8') as rd:
        seqs_str = rd.read().strip()
    seqs_list = seqs_str.split('\n\n')
    text, raw_label, predict_label = [], [], []
    for seq in seqs_list:
        seq_split = seq.split('\n')
        text_tmp = ''
        raw_index_dict, pre_index_dict = {}, {}
        for label in labels:
            raw_index_dict.setdefault(label, [])
            pre_index_dict.setdefault(label, [])
        for idx, line in enumerate(seq_split):
            tmp = line.split('\t')
            text_tmp += tmp[0]
            if tmp[1] in labels:
                raw_index_dict[tmp[1]].append(idx)
            if tmp[2] in labels:
                pre_index_dict[tmp[2]].append(idx)
        text.append(text_tmp)
        raw_label.append(raw_index_dict)
        predict_label.append(pre_index_dict)
    return text, raw_label, predict_label


def kfold(corpus, path, k=9, is_shuffle=True):
    '''
    k是10份中训练集占了几份
    '''
    j_mkdir(path)
    if is_shuffle:
        random.shuffle(corpus)
    split_position = int(len(corpus) / 10)
    train_set, dev_set = corpus[:k * split_position], corpus[k * split_position:]
    writetxt_w_list(train_set, os.path.join(path, 'train.tsv'), num_lf=1)
    writetxt_w_list(dev_set, os.path.join(path, 'test.tsv'), num_lf=1)
    writetxt_w_list(dev_set, os.path.join(path, 'dev.tsv'), num_lf=1)


# 读取crf序列格式的数据
def read_seq_data(path):
    content = readtxt_list_all_strip(path)
    lines = [i.split('\t') if i else '' for i in content]
    print(lines)
    sequences, labels, sequence, label = [], [], [], []
    for idx, line in enumerate(lines):
        if line == '':
            if sequence:
                sequences.append(sequence)
                labels.append(label)
                sequence, label = [], []
        else:
            sequence.append(line[0])
            label.append(line[1])
        if idx == len(lines) - 1 and sequence:
            sequences.append(sequence)
            labels.append(label)
    return sequences, labels


def split_5_percent(lines, sample_precent=5):
    random.seed(8)
    # lines = list(range(1, 109))
    idx_lines = [(idx, i) for idx, i in enumerate(lines)]
    div = int(len(lines) / 100)
    sample_num = div * sample_precent
    sample = random.sample(idx_lines, sample_num)
    sorted_sample = sorted(sample, key=lambda x: x[0])
    remove_idx = [i[0] for i in sorted_sample]
    less_has_raw_line_info = [str(i[0] + 1) + '\t' + str(i[1]) for i in sorted_sample]
    most = [i for idx, i in enumerate(lines) if not idx in remove_idx]
    print(less_has_raw_line_info)
    print(most)
    return most, less_has_raw_line_info
def split_sentences(sentences, mode='chinese'):
    # sentences->Str
    # example '12“345。”“6789”'
    if mode == 'chinese':
        split_signs = list('。！？…')
        other_sign = "”"
    elif mode == 'english':
        split_signs = list('.!?')
        other_sign = '"'
    else:
        print('暂时还没有')
        split_signs = list('.!?')
        other_sign = '"'
    splited_sentences = []
    start_idx = 0
    for idx, char in enumerate(sentences):
        if idx == len(sentences) - 1:
            if char in split_signs:
                splited_sentences.append(sentences[start_idx:idx + 1].strip())
                start_idx = idx + 1
            else:
                splited_sentences.append(sentences[start_idx:].strip())
        else:
            if char in split_signs:
                if sentences[idx + 1] == other_sign:
                    if idx < len(sentences) - 2:
                        # 处理。”。
                        if sentences[idx + 2] not in split_signs:
                            splited_sentences.append(sentences[start_idx:idx + 2].strip())
                            start_idx = idx + 2
                elif sentences[idx + 1] not in split_signs:
                    splited_sentences.append(sentences[start_idx:idx + 1].strip())
                    start_idx = idx + 1
    return splited_sentences
def pos_huanyuan():
    from nltk.stem import WordNetLemmatizer
    data = nlpertools.readtxt_list_all_strip('ie-selfmedia/')
    wnl = WordNetLemmatizer()
    # lemmatize nouns
    print(wnl.lemmatize('cars', 'n'))
    print(wnl.lemmatize('men', 'n'))

    # lemmatize verbs
    print(wnl.lemmatize('running', 'v'))
    print(wnl.lemmatize('ate', 'v'))
