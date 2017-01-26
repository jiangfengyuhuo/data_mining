from numpy import median
import numpy as np

a = ["age", "type_employer", "fnlwgt", "education", "education_num", "marital", "occupation", "relationship", "race",
     "sex", "capital_gain", "capital_loss", "hr_per_week", "country", "income"]
# 每一行存储一条数据，每个adult的数据
# 小于50k的数据
data_low = []
data_high = []
loss_low = []
gain_low = []
loss_high = []
gain_high = []
with open('/home/find/down/adult.data', 'r')as fin:
    line = fin.readline()
    while line:
        line = line.replace('\n', '')
        if line:
            line = line.split(", ")
            if line[len(line)-1] == '>50K':
                data_high.append(line)
                gain_high.append(int(line[10]))
                loss_high.append(int(line[11]))
            else:
                data_low.append(line)
                gain_low.append(int(line[10]))
                loss_low.append(int(line[11]))
        line = fin.readline()


"""分类以后的处理
classfiled_data['age'] = {type: num;}
classfiled_data = {'age':{type: num...}}
"""
# @todo: 年龄还需要分类，还有工作时长
def classfy(gain, loss, data):
    classfiled_data = {}
    loss_median = median(np.array(loss))
    gain_median = median(np.array(gain))
    for node in a:
        classfiled_data[node] = {}
    for line in data:
        if len(line) < 5:
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

                # 对收入进行划分

    def income_classfy(category, mid_value):
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
    tiny(["Craft-repair", "Farming-fishing", "Handlers-cleaners", "Machine-op-inspct", "Transport-moving"], 'occupation',
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

    for key in classfiled_data:
        print(key)
        print(classfiled_data[key])

classfy(gain_low, loss_low, data_low)
classfy(gain_high, loss_high, data_high)