from numpy import median
import numpy as np

a = ["age", "type_employer", "fnlwgt", "education", "education_num", "marital", "occupation", "relationship", "race",
     "sex", "capital_gain", "capital_loss", "hr_per_week", "country", "income"]


class DataSet:
    def __init__(self):
        self.data = []
        self.loss_mid = 0
        self.gain_mid = 0
        self.hours_mid = 0
        self.age_mid = 0
        self.classfied_dataset = None


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
    dataset_high.loss_mid = median(np.array(loss_high))
    dataset_high.gain_mid = median(np.array(gain_high))
    dataset_high.age_mid = median(np.array(age_high))
    dataset_high.hours_mid = median(np.array(hours_high))
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

    classfiled_data['occupation']['white-color'] = classfiled_data['occupation']['Exec-managerial']
    del classfiled_data['occupation']['Exec-managerial']

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
    # 工作时间划分直接分10块吧，1-10,11-20...100，
    for x in range(10):
        a_set = []
        for y in range(10 * (x + 1)):
            a_set.append(str(y + 1))
        tiny(a_set, 'hr_per_week', str(10 * (x + 1)) + 's')
    # 年龄以5划分
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

def test():
    """测试模型"""
    with open('/home/find/down/adult.test', 'r')as fin:
        line = fin.readline()
        while line:

            line = fin.readline()