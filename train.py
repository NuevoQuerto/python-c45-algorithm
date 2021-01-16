# Nama: Agung Rizal Suryo Laskono
# NIM: 171011402317

import pandas as pd
import numpy as np
import math

class C45:
    def __init__(self, data, target):
        self.data = data
        self.target = target

    # S: Himpunan Kasus
    # N: Jumlah Partisi Dalam S
    # Pi: Proporsi Dari Si Terhadap S
    def entropy(self, s, n):
        total = 0
        for pi in s:
            total += 0 if pi == 0 else (-pi/n * math.log(pi/n, 2))
        return total

    # S: Entropy Dari Himpunan Kasus
    # A: Atribut
    # N: Jumlah Partisi Atribut A
    # |Si|: Jumlah Kasus Pada Partisi Ke-i
    # |S| / _s: Jumlah Kasus Dalam S
    # Entropy(Si) = Entropy Dari Kasus Pada Partisi Ke-i
    # gain([4, 10], [[0, 4],[1, 4],[3, 2]], [4, 5, 5], 14)
    def gain(self, s, a, n, _s):
        # 0.863120569 - ((4/14 * 0) + (5/14 * 0.72193) + (5/14 * 0.97095)
        total = 0
        for si in range(len(n)):
            total += (n[si]/_s * self.entropy(a[si], n[si]))
        total = self.entropy(s, _s) - total
        return total

    # S: Himpunan Kasus
    # A: Atribut
    # Si: Jumlah Sampel Untuk Atribut A    
    def split_info(self, s, a):
        total = 0
        for si in a:
            total += 0 if si == 0 else (-si/s * math.log(si/s, 2))
        return total
        
    # S: Himpunan Kasus
    # A: Atribut
    # Gain(S,A): Information Gain Pada Atribut A
    # SplitInfo(S,A): Split Information Pada Atribut A
    def gain_ratio(self, s, a, n, _s):
        return self.gain(s, a, n, _s) / self.split_info(_s, n)
        
    def generate_tree(self):
        #print(self.data.head())
        #print(self.data.info())
        #print( self.data[ (self.data['Outlook'] == 'Rainy') ] )
        #print( self.data[ (self.data['Outlook'] == 'Rainy') & (self.data['Play'] == 'Yes') ] )
        print(self.data.iloc[0,0])
        
        # Perhitungan Node 1 (Root)
        total_data = self.data[self.target].count()
        number_of_cases_target_category = [total_case for total_case in self.data[self.target].value_counts()] # Misal No, Yes [4, 10]
        decision_tree = []
        #print('Humidity = {}'.format(self.data.loc[self.data['Humidity'] > 78, self.target].count())) # Jumlah Kasus (14)
        #print(self.data.loc[self.data['Humidity'] > 78, self.target].value_counts()) # Jumlah No, Yes [4, 10]
        
        # Percobaan
        print(self.entropy(number_of_cases_target_category, total_data))
        data_filter = self.data.drop([self.target], axis=1)
        target_category = self.data[self.target].unique() # Misal [No, Yes]
        #print(data_filter['Outlook'].unique())
        #print(data_filter[data_filter['Outlook'].isin(target_category)])
        #print(self.data[self.data['Outlook'] == 'Sunny'])
        
        attributes = self.data.columns
        mark_attribute = [self.target]
        node_loc = []
        attr_loc = ""
        #categorical_attr_loc = "(self.data[attribute] == categories[index])"
        #discrete_attr_loc = ""
        total_attribute = self.data.shape[1]
        discrete_branch = {}
        print(attributes)
        print(total_attribute)
        #print(self.data.loc[self.data['Outlook'] == 'Sunny', self.target].value_counts())
        for training in range(0, 3):
            gain_ratio_attributes = []
            
            for attribute in attributes:
                if attribute not in mark_attribute:
                    categories = self.data[attribute].unique()
                    total_cases_categorie = []
                    total_cases_categorie_target = []
                    
                    if pd.api.types.is_integer_dtype(self.data[attribute].dtype):
                        # Data Disktrit atau Kontinyu
                        gains = []
                        gain_ratios = []
                        categories = np.delete(categories, np.argwhere(categories == np.max(categories))) # Hilangkan Angka Paling Besar
                        print('Diskrit')
                        print("{} = {}".format(attribute, categories))
                        for index in range(len(categories)):
                            total_cases_categorie.append([self.data.loc[eval("(self.data[attribute] <= categories[index])" + attr_loc), self.target].count(), 
                                                        self.data.loc[eval("(self.data[attribute] > categories[index])" + attr_loc), self.target].count()])
                            _less = []
                            for t_index in range(len(target_category)):
                                if target_category[t_index] in self.data.loc[eval("(self.data[attribute] <= categories[index])" + attr_loc), self.target].value_counts():
                                    _less.append(self.data.loc[eval("(self.data[attribute] <= categories[index])" + attr_loc), self.target].value_counts()[target_category[t_index]])
                                else:
                                    _less.append(0)
                            _greater = []
                            for t_index in range(len(target_category)):
                                if target_category[t_index] in self.data.loc[eval("(self.data[attribute] > categories[index])" + attr_loc), self.target].value_counts():
                                    _greater.append(self.data.loc[eval("(self.data[attribute] > categories[index])" + attr_loc), self.target].value_counts()[target_category[t_index]])
                                else:
                                    _greater.append(0)
                            total_cases_categorie_target.append([_less, _greater])
                        for index in range(len(total_cases_categorie)):
                            print(total_cases_categorie)
                            print(total_cases_categorie_target)
                            gains.append(self.gain(number_of_cases_target_category, total_cases_categorie_target[index], total_cases_categorie[index], total_data))
                            gain_ratios.append(self.gain_ratio(number_of_cases_target_category, total_cases_categorie_target[index], total_cases_categorie[index], total_data))
                            print("Gain Ratio {} <>{} = {}".format(attribute, categories[index], self.gain_ratio(number_of_cases_target_category, total_cases_categorie_target[index], total_cases_categorie[index], total_data))) # Gain Ratio Humidity
                            
                        # Pilih Cabang Dari Nilai Gain Yang Terbesar
                        #if len(discrete_branch) == 0:
                        gains_index = np.argwhere(gains == np.max(gains))[0][0]
                        discrete_branch[attribute] = [categories[gains_index], total_cases_categorie[gains_index], total_cases_categorie_target[gains_index]]
                        
                        gain_ratio_attributes.append(gain_ratios[np.argwhere(gains == np.max(gains))[0][0]])
                    else:
                        # Data Kategorikal
                        print("Kategorikal")
                        for index in range(len(categories)):
                            # Testing Perubahan
                            print(categories)
                            #print('testing {}'.format(self.data.loc[(self.data[attribute] == categories[index]) & (self.data['Humidity'] > 78), self.target].count()))
                            #print('testing {}'.format(self.data.loc[eval(categorical_attr_loc), self.target].count()))
                            
                            #total_cases_categorie.append(self.data.loc[(self.data[attribute] == categories[index]), self.target].count())
                            #print("Check = {}".format(attr_loc))
                            total_cases_categorie.append(self.data.loc[eval("(self.data[attribute] == categories[index])" + attr_loc), self.target].count())
                            #total_cases_categorie_target.append([total_case for total_case in self.data.loc[(self.data[attribute] == categories[index]), self.target].value_counts()])
                            total_cases_categorie_target.append([total_case for total_case in self.data.loc[eval("(self.data[attribute] == categories[index])" + attr_loc), self.target].value_counts()])
                        print(total_cases_categorie)
                        print(total_cases_categorie_target)
                        gain_ratio_attributes.append(self.gain_ratio(number_of_cases_target_category, total_cases_categorie_target, total_cases_categorie, total_data))
                        print("Gain Ratio {} = {}".format(attribute, self.gain_ratio(number_of_cases_target_category, total_cases_categorie_target, total_cases_categorie, total_data)))
            
            # Pilih Root/Node Dari Nilai Gain Ratio Yang Terbesar
            filter_attributes = [f_a for f_a in attributes if f_a not in mark_attribute]
            print('filter_attributes = {}'.format(filter_attributes))
            print(gain_ratio_attributes)
            print(np.max(gain_ratio_attributes))
            attr_index = np.argwhere(gain_ratio_attributes == np.max(gain_ratio_attributes))[0][0]
            print("gain_ratio_attributes = {}".format(gain_ratio_attributes))
            #print(filter_attributes)
            #print(attr_index)
            #print(discrete_branch)
            #print(discrete_branch[filter_attributes[attr_index]])
            #print(target_category)
            
            if pd.api.types.is_integer_dtype(self.data[filter_attributes[attr_index]].dtype):
                # Buat Cabang Diskrit/Kontinyu
                break_discrete = 0
                print('{} <={} = {}'.format(filter_attributes[attr_index], discrete_branch[filter_attributes[attr_index]][0], self.data.loc[self.data[filter_attributes[attr_index]] <= discrete_branch[filter_attributes[attr_index]][0], self.target].count())) # Jumlah Kasus (14)
                _less = []
                for t_index in range(len(target_category)):
                    if target_category[t_index] in self.data.loc[eval("(self.data[filter_attributes[attr_index]] <= discrete_branch[filter_attributes[attr_index]][0])" + attr_loc), self.target].value_counts():
                        #print(self.data.loc[self.data[filter_attributes[attr_index]] <= discrete_branch[filter_attributes[attr_index]][0], self.target].value_counts()) # Jumlah No, Yes [4, 10]
                        _less.append(self.data.loc[self.data[filter_attributes[attr_index]] <= discrete_branch[filter_attributes[attr_index]][0], self.target].value_counts()[target_category[t_index]])
                    else:
                        _less.append(0)
                print('_less = {}'.format(_less))
                _np_less = np.array(_less)
                if _np_less.size - _np_less[_np_less == 0].size == 1:
                    break_discrete += 1
                    print("if {} <= {}:\n\t'{}'".format(filter_attributes[attr_index], discrete_branch[filter_attributes[attr_index]][0], target_category[np.argwhere(_np_less != 0)[0][0]]))
                else:
                    node_loc.append('(self.data["{}"] <= {})'.format(filter_attributes[attr_index], discrete_branch[filter_attributes[attr_index]][0]))
                    #total_data = self.data.loc[self.data[filter_attributes[attr_index]] <= discrete_branch[filter_attributes[attr_index]][0], self.target].count() # Sama
                    #number_of_cases_target_category = [total_case for total_case in self.data.loc[self.data[filter_attributes[attr_index]] <= discrete_branch[filter_attributes[attr_index]][0], self.target].value_counts()]
                    attr_loc +=  ' & (self.data["{}"] <= {})'.format(filter_attributes[attr_index], discrete_branch[filter_attributes[attr_index]][0]) # Sama
                    print(attr_loc)
                        
                print('{} >{} = {}'.format(filter_attributes[attr_index], discrete_branch[filter_attributes[attr_index]][0], self.data.loc[self.data[filter_attributes[attr_index]] > discrete_branch[filter_attributes[attr_index]][0], self.target].count())) # Jumlah Kasus (14)
                _greater = []
                for t_index in range(len(target_category)):
                    if target_category[t_index] in self.data.loc[eval("(self.data[filter_attributes[attr_index]] > discrete_branch[filter_attributes[attr_index]][0])" + attr_loc), self.target].value_counts():
                        #print(self.data.loc[self.data[filter_attributes[attr_index]] > discrete_branch[filter_attributes[attr_index]][0], self.target].value_counts()) # Jumlah No, Yes [4, 10]
                        _greater.append(self.data.loc[self.data[filter_attributes[attr_index]] > discrete_branch[filter_attributes[attr_index]][0], self.target].value_counts()[target_category[t_index]])
                    else:
                        _greater.append(0)
                _np_greater = np.array(_greater)
                if _np_greater.size - _np_greater[_np_greater == 0].size == 1:
                    break_discrete += 1
                    print("if {} > {}:\n\t'{}'".format(filter_attributes[attr_index], discrete_branch[filter_attributes[attr_index]][0], target_category[np.argwhere(_np_greater != 0)[0][0]]))
                else:
                    node_loc.append('(self.data["{}"] > {})'.format(filter_attributes[attr_index], discrete_branch[filter_attributes[attr_index]][0]))
                    #total_data = self.data.loc[self.data[filter_attributes[attr_index]] > discrete_branch[filter_attributes[attr_index]][0], self.target].count()
                    #number_of_cases_target_category = [total_case for total_case in self.data.loc[self.data[filter_attributes[attr_index]] > discrete_branch[filter_attributes[attr_index]][0], self.target].value_counts()]
                    attr_loc +=  ' & (self.data["{}"] > {})'.format(filter_attributes[attr_index], discrete_branch[filter_attributes[attr_index]][0])
                    print(attr_loc)
                if break_discrete == 2:
                    break
            else:
                # Buat Cabang Kategorikal
                break_categorical = 0
                _categories = self.data[filter_attributes[attr_index]].unique()
                _categories_target = [] # Misal No, Yes [1, 0]
                print(_categories)
                for c_index in range(len(_categories)):
                    _t = []
                    for t_index in range(len(target_category)):
                        print(filter_attributes[attr_index])
                        print(_categories[c_index])
                        if target_category[t_index] in self.data.loc[eval("(self.data[filter_attributes[attr_index]] == _categories[c_index])" + attr_loc), self.target].value_counts():
                            _t.append(self.data.loc[eval("(self.data[filter_attributes[attr_index]] == _categories[c_index])" + attr_loc), self.target].value_counts()[target_category[t_index]])
                            print(self.data.loc[eval("(self.data[filter_attributes[attr_index]] == _categories[c_index])" + attr_loc), self.target].value_counts()[target_category[t_index]])
                        else:
                            print(0)
                            _t.append(0)
                    _categories_target.append(_t)
                print("_categories_target = {}".format(_categories_target))
                for _ct_i in range(len(_categories_target)):
                    _np_categories_target = np.array(_categories_target[_ct_i])
                    if _np_categories_target.size - _np_categories_target[_np_categories_target == 0].size == 1:
                        break_categorical += 1
                        print("if {} == {}:\n\t'{}'".format(filter_attributes[attr_index], _categories[_ct_i], target_category[np.argwhere(_np_categories_target != 0)[0][0]]))
                    else:
                        node_loc.append('(self.data["{}"] == "{}")'.format(filter_attributes[attr_index], _categories[_ct_i]))
                        attr_loc += ' & (self.data["{}"] == "{}")'.format(filter_attributes[attr_index], _categories[_ct_i])
                        print(attr_loc)
                print("_categories_target size = {}".format(len(_categories_target)))
                if break_categorical == len(_categories_target):
                    break
                    
                #total_cases_categorie.append(self.data.loc[eval("(self.data[attribute] == categories[c_index])" + attr_loc), self.target].count())
            
            print(node_loc)
            print(self.data[filter_attributes[attr_index]])
            total_data = self.data.loc[eval(' & '.join(node_loc)), self.target].count() # Sama
            number_of_cases_target_category = [total_case for total_case in self.data.loc[eval(' & '.join(node_loc)), self.target].value_counts()]
            print("number_of_cases_target_category {}".format(number_of_cases_target_category))
            mark_attribute.append(filter_attributes[attr_index])
            print(mark_attribute)
            print(node_loc)
            #print(_greater)
            #print([total_case for total_case in self.data.loc[self.data[attribute] <= categories[index], self.target].value_counts()])
        
        
dataset = pd.read_csv('data.csv')
train = C45(dataset, 'Play')
# dataset = pd.read_csv('heart_failure_clinical_records_dataset.csv')
# train = C45(dataset, 'DEATH_EVENT')
# dataset = pd.read_csv('Iris.csv')
# train = C45(dataset, 'Species')

#print("Gain Ratio Outlook = {}".format(gain_ratio([4, 10], [[0, 4],[1, 4],[3, 2]], [4, 5, 5], 14))) # Gain Ratio Outlook
#print(train.gain([4, 10], [[0, 4],[1, 4],[3, 2]], [4, 5, 5], 14))
train.generate_tree()