

a = ["age", "type_employer", "fnlwgt", "education", "education_num","marital", "occupation", "relationship", "race","sex","capital_gain", "capital_loss", "hr_per_week","country", "income"]
b = [''] * 15
# 每一行存储一条数据，每个adult的数据
data = []
with open('/home/find/down/adult.data', 'r')as fin:
    line = fin.readline()
    while line:
        line.replace('\n', '')
        if line:
            data.append(line.split(", "))
        line = fin.readline()

"""分类以后的处理
classfiled_data['age'] = {type: num;}
classfiled_data = {'age':{type: num...}}
"""
classfiled_data = {}
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

# 1 删除两个多余的元素
del classfiled_data['education_num']
del classfiled_data['fnlwgt']

# 2 合并几个出现次数比较小的分类
# 2.1 把not worked和without pay合并成not working，还有几个类似的
classfiled_data['type_employer']['not-working'] = classfiled_data['type_employer']['Never-worked'] + classfiled_data['type_employer']['Without-pay']
del classfiled_data['type_employer']['Never-worked']
del classfiled_data['type_employer']['Without-pay']
classfiled_data['type_employer']['other-govt'] = classfiled_data['type_employer']['Local-gov'] + classfiled_data['type_employer']['State-gov']
del classfiled_data['type_employer']['Local-gov']
del classfiled_data['type_employer']['State-gov']
classfiled_data['type_employer']['Self-Employed'] = classfiled_data['type_employer']['Self-emp-inc'] + classfiled_data['type_employer']['Self-emp-not-inc']
del classfiled_data['type_employer']['Self-emp-inc']
del classfiled_data['type_employer']['Self-emp-not-inc']
def tiny(a_list, category,new_name):
    global classfiled_data
    if new_name not in classfiled_data[category]:
        classfiled_data[category][new_name] = 0
    for key in list(classfiled_data[category]):
        if key in a_list and key != new_name:
            classfiled_data[category][new_name] += classfiled_data[category][key]
            del classfiled_data[category][key]
# 职业上的合并
tiny(["Craft-repair","Farming-fishing","Handlers-cleaners","Machine-op-inspct","Transport-moving"], 'occupation', 'blue-collar')

classfiled_data['occupation']['white-color'] = classfiled_data['occupation']['Exec-managerial']
del classfiled_data['occupation']['Exec-managerial']

classfiled_data['occupation']['service'] = classfiled_data['occupation']['Other-service'] + classfiled_data['occupation']['Priv-house-serv']
del classfiled_data['occupation']['Other-service']
del classfiled_data['occupation']['Priv-house-serv']

tiny(["Cambodia","Laos","Philippines","Thailand","Vietnam"], 'country', 'SE-Asia')
tiny(["Canada","England","India","Ireland","Scotland",], 'country', 'British-Commonwealth')
tiny(['China', 'Hong', 'Taiwan'], 'country', 'China')
tiny(["Columbia","Ecuador","El-Salvador","Peru"], 'country', 'South-America')
tiny(["Cuba","Iran","Japan"], 'country', 'other')
tiny(["Dominican-Republic","Guatemala","Haiti","Honduras","Jamaica","Mexico","Nicaragua","Outlying-US(Guam-USVI-etc)","Puerto-Rico","Trinadad&Tobago",], 'country', 'Latin-America')
tiny(["France","Germany","Holand-Netherlands","Italy",], 'country', 'Euro_1')
tiny(["Greece","Hungary","Poland","Portugal","Yugoslavia",], 'country', 'Euro_2')

tiny(["10th","11th","12th","1st-4th","5th-6th","7th-8th","9th","Preschool",], 'education', 'dropout')
tiny(['Assoc-acdm', 'Assoc-voc'], 'education', 'Assoc')
tiny(["Married-AF-spouse", "Married-civ-spouse"], 'marital', "Married")
tiny(["Married-spouse-absent","Separated","Divorced"], 'marital', 'not-married')





for key in classfiled_data:
    print(key)
    print(classfiled_data[key])
