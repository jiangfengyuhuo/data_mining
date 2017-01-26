from numpy import median
import numpy as np

a = ["age", "type_employer", "fnlwgt", "education", "education_num", "marital", "occupation", "relationship", "race",
     "sex", "capital_gain", "capital_loss", "hr_per_week", "country", "income"]
# 由于后面对数据进行了化简，所以需要将部分字段重新映射
tiny_map = {"Never-worked": "not-working", "Without-pay": "not-working", "Local-gov": "other-govt",
            "State-gov": "other-govt", "Self-emp-inc": "self-employed", "Self-emp-not-inc": "self-employed",
            "Craft-repair": "blue-collar", "Farming-fishing": "blue-collar", "Handlers-cleaners": "blue-collar",
            "Machine-op-inspct": "blue-collar", "Transport-moving": "blue-collar", "Other-service": "service",
            "Priv-house-serv": "service", "Cambodia": "SE-Asia", "Laos": "SE-Asia", "Philippines": "SE-Asia",
            "Thailand": "SE-Asia", "Vietnam": "SE-Asia", "Canada": "British-Commonwealth",
            "England": "British-Commonwealth", "India": "British-Commonwealth", "Ireland": "British-Commonwealth",
            "Scotland": "British-Commonwealth", "China": "China", "Hong": "China", "Taiwan": "China",
            "Columbia": "South-America", "Ecuador": "South-America", "El-Salvador": "South-America",
            "Peru": "South-America", "Cuba": "other", "Iran": "other", "Japan": "other",
            "Dominican-Republic": "Latin-America", "Guatemala": "Latin-America", "Haiti": "Latin-America",
            "Honduras": "Latin-America", "Jamaica": "Latin-America", "Mexico": "Latin-America",
            "Nicaragua": "Latin-America", "Outlying-US(Guam-USVI-etc)": "Latin-America", "Puerto-Rico": "Latin-America",
            "Trinadad&Tobago": "Latin-America", "France": "Euro_1", "Germany": "Euro_1", "Holand-Netherlands": "Euro_1",
            "Italy": "Euro_1", "Greece": "Euro_2", "Hungary": "Euro_2", "Poland": "Euro_2", "Portugal": "Euro_2",
            "Yugoslavia": "Euro_2", "10th": "dropout", "11th": "dropout", "12th": "dropout", "1st-4th": "dropout",
            "5th-6th": "dropout", "7th-8th": "dropout", "9th": "dropout", "Preschool": "dropout", "Assoc-acdm": "Assoc",
            "Assoc-voc": "Assoc", "Married-AF-spouse": "Married", "Married-civ-spouse": "Married",
            "Married-spouse-absent": "not-married", "Separated": "not-married", "Divorced": "not-married", }
hour_map = {"1": "10s", "2": "10s", "3": "10s", "4": "10s", "5": "10s", "6": "10s", "7": "10s", "8": "10s", "9": "10s", "10": "10s", "11": "20s", "12": "20s", "13": "20s", "14": "20s", "15": "20s", "16": "20s", "17": "20s", "18": "20s", "19": "20s", "20": "20s", "21": "30s", "22": "30s", "23": "30s", "24": "30s", "25": "30s", "26": "30s", "27": "30s", "28": "30s", "29": "30s", "30": "30s", "31": "40s", "32": "40s", "33": "40s", "34": "40s", "35": "40s", "36": "40s", "37": "40s", "38": "40s", "39": "40s", "40": "40s", "41": "50s", "42": "50s", "43": "50s", "44": "50s", "45": "50s", "46": "50s", "47": "50s", "48": "50s", "49": "50s", "50": "50s", "51": "60s", "52": "60s", "53": "60s", "54": "60s", "55": "60s", "56": "60s", "57": "60s", "58": "60s", "59": "60s", "60": "60s", "61": "70s", "62": "70s", "63": "70s", "64": "70s", "65": "70s", "66": "70s", "67": "70s", "68": "70s", "69": "70s", "70": "70s", "71": "80s", "72": "80s", "73": "80s", "74": "80s", "75": "80s", "76": "80s", "77": "80s", "78": "80s", "79": "80s", "80": "80s", "81": "90s", "82": "90s", "83": "90s", "84": "90s", "85": "90s", "86": "90s", "87": "90s", "88": "90s", "89": "90s", "90": "90s", "91": "100s", "92": "100s", "93": "100s", "94": "100s", "95": "100s", "96": "100s", "97": "100s", "98": "100s", "99": "100s", "100": "100s", }
age_map = {"1": "5s", "2": "5s", "3": "5s", "4": "5s", "5": "5s", "6": "10s", "7": "10s", "8": "10s", "9": "10s", "10": "10s", "11": "15s", "12": "15s", "13": "15s", "14": "15s", "15": "15s", "16": "20s", "17": "20s", "18": "20s", "19": "20s", "20": "20s", "21": "25s", "22": "25s", "23": "25s", "24": "25s", "25": "25s", "26": "30s", "27": "30s", "28": "30s", "29": "30s", "30": "30s", "31": "35s", "32": "35s", "33": "35s", "34": "35s", "35": "35s", "36": "40s", "37": "40s", "38": "40s", "39": "40s", "40": "40s", "41": "45s", "42": "45s", "43": "45s", "44": "45s", "45": "45s", "46": "50s", "47": "50s", "48": "50s", "49": "50s", "50": "50s", "51": "55s", "52": "55s", "53": "55s", "54": "55s", "55": "55s", "56": "60s", "57": "60s", "58": "60s", "59": "60s", "60": "60s", "61": "65s", "62": "65s", "63": "65s", "64": "65s", "65": "65s", "66": "70s", "67": "70s", "68": "70s", "69": "70s", "70": "70s", "71": "75s", "72": "75s", "73": "75s", "74": "75s", "75": "75s", "76": "80s", "77": "80s", "78": "80s", "79": "80s", "80": "80s", "81": "85s", "82": "85s", "83": "85s", "84": "85s", "85": "85s", "86": "90s", "87": "90s", "88": "90s", "89": "90s", "90": "90s", "91": "95s", "92": "95s", "93": "95s", "94": "95s", "95": "95s", "96": "100s", "97": "100s", "98": "100s", "99": "100s", "100": "100s", }

class DataSet:
    def __init__(self):
        self.data = []
        self.loss_mid = 0
        self.gain_mid = 0
        self.hours_mid = 0
        self.age_mid = 0
        self.classfied_dataset = None
        self.len_data = 0


dataset_low = DataSet()
dataset_high = DataSet()
with open('/home/find/down/adult.data', 'r')as fin:
    line = fin.readline()
    gain_high = []
    loss_high = []
    gain_low = []
    loss_low = []
    hours_low = []
    hours_high = []
    age_low = []
    age_high = []
    while line:
        line = line.replace('\n', '')
        if line:
            line = line.split(", ")
            if line[len(line) - 1] == '>50K':
                dataset_high.data.append(line)
                gain_high.append(int(line[10]))
                loss_high.append(int(line[11]))
                age_high.append(int(line[0]))
                hours_high.append(int(line[12]))
            else:
                dataset_low.data.append(line)
                gain_low.append(int(line[10]))
                loss_low.append(int(line[11]))
                age_low.append(int(line[0]))
                hours_low.append(int(line[12]))
        line = fin.readline()
    # 获取部分中位数
    dataset_low.loss_mid = median(np.array(loss_low))
    dataset_low.gain_mid = median(np.array(gain_low))
    dataset_low.age_mid = median(np.array(age_low))
    dataset_low.hours_mid = median(np.array(hours_low))
    dataset_low.len_data = len(dataset_low.data)
    dataset_high.loss_mid = median(np.array(loss_high))
    dataset_high.gain_mid = median(np.array(gain_high))
    dataset_high.age_mid = median(np.array(age_high))
    dataset_high.hours_mid = median(np.array(hours_high))
    dataset_high.len_data = len(dataset_high.data)
"""分类以后的处理
classfiled_data['age'] = {type: num;}
classfiled_data = {'age':{type: num...}}
"""


# @todo: 年龄还需要分类，还有工作时长
# hour也按照中位数来处理吧。还有年龄也是。
def classfy(gain, loss, data):
    classfiled_data = {}
    loss_median = loss
    gain_median = gain
    for node in a:
        classfiled_data[node] = {}
    for line in data:
        if len(line) < 10:
            continue
        for node in a:
            if line[a.index(node)] in classfiled_data[node]:
                classfiled_data[node][line[a.index(node)]] += 1
            else:
                classfiled_data[node][line[a.index(node)]] = 1

    def tiny(a_list, category, new_name):
        if new_name not in classfiled_data[category]:
            classfiled_data[category][new_name] = 0
        for key in list(classfiled_data[category]):
            if key in a_list and key != new_name:
                classfiled_data[category][new_name] += classfiled_data[category][key]
                del classfiled_data[category][key]

    def income_classfy(category, mid_value):
        """对收入进行分类，简化成none, low, high三个级别"""
        classfiled_data[category]['low'] = 0
        classfiled_data[category]['none'] = 0
        classfiled_data[category]['high'] = 0
        for key in list(classfiled_data[category]):
            if key in ['low', 'none', 'high']:
                continue
            if int(key) <= 0:
                classfiled_data[category]['none'] += classfiled_data[category][key]
            elif int(key) < mid_value:
                classfiled_data[category]['low'] += classfiled_data[category][key]
            else:
                classfiled_data[category]['high'] += classfiled_data[category][key]
            del classfiled_data[category][key]

    # 1 删除两个多余的元素
    del classfiled_data['education_num']
    del classfiled_data['fnlwgt']
    tiny(['Never-worked', 'Without-pay'], 'type_employer', 'not-working')
    tiny(['Local-gov', 'State-gov'], 'type_employer', 'other-govt')
    tiny(['Self-emp-inc', 'Self-emp-not-inc'], 'type_employer', 'self-employed')
    # 职业上的合并
    tiny(["Craft-repair", "Farming-fishing", "Handlers-cleaners", "Machine-op-inspct", "Transport-moving"],
         'occupation',
         'blue-collar')
    tiny(['Other-service', 'Priv-house-serv'], 'occupation', 'service')
    tiny(["Cambodia", "Laos", "Philippines", "Thailand", "Vietnam"], 'country', 'SE-Asia')
    tiny(["Canada", "England", "India", "Ireland", "Scotland", ], 'country', 'British-Commonwealth')
    tiny(['China', 'Hong', 'Taiwan'], 'country', 'China')
    tiny(["Columbia", "Ecuador", "El-Salvador", "Peru"], 'country', 'South-America')
    tiny(["Cuba", "Iran", "Japan"], 'country', 'other')
    tiny(["Dominican-Republic", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua",
          "Outlying-US(Guam-USVI-etc)", "Puerto-Rico", "Trinadad&Tobago", ], 'country', 'Latin-America')
    tiny(["France", "Germany", "Holand-Netherlands", "Italy", ], 'country', 'Euro_1')
    tiny(["Greece", "Hungary", "Poland", "Portugal", "Yugoslavia", ], 'country', 'Euro_2')

    tiny(["10th", "11th", "12th", "1st-4th", "5th-6th", "7th-8th", "9th", "Preschool", ], 'education', 'dropout')
    tiny(['Assoc-acdm', 'Assoc-voc'], 'education', 'Assoc')
    tiny(["Married-AF-spouse", "Married-civ-spouse"], 'marital', "Married")
    tiny(["Married-spouse-absent", "Separated", "Divorced"], 'marital', 'not-married')
    # 一个不好的点是，用中位数切割以后，数据分散在了两端，中间没有数据
    income_classfy('capital_gain', gain_median)
    income_classfy('capital_loss', loss_median)
    # 数据都是( ] 取上不取下
    # 工作时间划分直接分10块吧，1-10,11-20...100，相应映射到10s,20s,30,
    for x in range(10):
        a_set = []
        for y in range(10 * (x + 1)):
            a_set.append(str(y + 1))
        tiny(a_set, 'hr_per_week', str(10 * (x + 1)) + 's')
    # 年龄以5划分1-5:5s
    for x in range(20):
        a_set = []
        for y in range(5 * (x + 1)):
            a_set.append(str(y + 1))
        tiny(a_set, 'age', str(5 * (x + 1)) + 's')

    for key in classfiled_data:
        print(key)
        print(classfiled_data[key])
    return classfiled_data


dataset_low.classfied_dataset = classfy(dataset_low.gain_mid, dataset_low.loss_mid, dataset_low.data)
dataset_high.classfied_dataset = classfy(dataset_high.gain_mid, dataset_high.loss_mid, dataset_high.data)


def test(line):
    """测试数据"""
    # P(每个元素|收入大于50k)
    p_low = 0.0
    p_high = 0.0
    gain = int(line[-5])
    loss = int(line[-4])

    def get_level(value, mid_value):
        if value <= 0:
            return 'none'
        elif value < mid_value:
            return 'low'
        else:
            return 'high'
    for node in a[:-1]:
        i = a.index(node)
        if node in ["fnlwgt", "education_num"]: continue
        if line[i] in tiny_map:
            line[i] = tiny_map[line[i]]
        # 年龄
        if i == 0:
            line[i] = age_map[line[i]]
        # 工作时长
        if i == 12:
            line[i] = hour_map[line[i]]
        # 收入部分
        if node == 'capital_gain':
            line[i] = get_level(gain, dataset_low.gain_mid)
        if node == 'capital_loss':
            line[i] = get_level(loss, dataset_low.loss_mid)
        p_low *= dataset_low.classfied_dataset[node][line[i]] / dataset_low.len_data
        # 收入部分
        if node == 'capital_gain':
            line[i] = get_level(gain, dataset_high.gain_mid)
        if node == 'capital_loss':
            line[i] = get_level(loss, dataset_high.loss_mid)
        p_high *= dataset_high.classfied_dataset[node][line[i]] / dataset_high.len_data
    if p_low > p_high:
        return '<=50k'
    else:
        return '>50k'


print("训练数据的总数：\n >50k\t%d\n<=50k\t%d" % (len(dataset_high.data), len(dataset_low.data)))

with open('/home/find/down/adult.test', 'r')as fin:
    line = fin.readline()
    right = 0
    wrong = 0
    while line:
        # 去掉无效行
        if len(line) < 25:
            line = fin.readline()
            continue
        line = line.replace('\n', '')
        line = line[:-1]
        line = line.split(', ')
        ans = test(line).upper()
        if line[-1] == ans:
            right += 1
        else:
            wrong += 1
        print("%s%s" %(line[-1], ans))
        line = fin.readline()

print("模型的判断正确的次数：\t%d\n错误的次数\t%d\n正确率:\t%f" % (right, wrong, (right / (right + wrong))))
