# coding=utf-8
import csv
import itertools
import time
import sys


# Main function of Apriori
def apriori_association_rule_mining(dataSet, judge, minsup, minconf):
    data_size = len(dataSet)
    sample_size = 0
    for i in range(len(judge)):
        sample_size += int(judge[i][1])
    feature_length = len(dataSet[0])
    print("start level 1")

    rule_k1 = []
    conf, supp = con_dataDic(dataSet, judge)

    # k = 1 =================================================================
    t1 = time.time()
    for i in range(feature_length):
        rule_k1.append([])
        mymap = {}
        for j in range(data_size):
            tmp_rule = {dataSet[j][i]}  # extract element from each row and each col, to form an independent rules.
            if dataSet[j][i] in mymap:
                continue
            else:
                mymap[dataSet[j][i]] = 1
                rule_k1[i].append([tmp_rule, 0.00001, 0.0])
    # print("time1:")
    # t2 = time.time()
    # print (t2 - t1)
    for i in range(feature_length):
        # t2 = time.time()
        # cal_sup_conf(rule_k1[i], dataSet, judge)  # Calculate the support and confidence of rule_k1
        cal_sup_conf_v2(rule_k1[i], conf, supp, data_size)
        # t3 = time.time()
        # print("time chabie:")
        # print (t3 - t2)
        rule_scan(rule_k1[i], 0.0001, 0.0)  # rule out the rule with minsup and minconf under threshold
        # rule_sort(rule_k1[i])  # sort the rules by support in rule_k1

    # k = 2 =================================================================
    # 要想办法优化一下此处，此处会发生同一列特征的不同种类之间相互组合的情况，应该要加以避免才可以
    print("start level 2")
    rule_k2 = []  # initialize rule_k2 with two rules in each tuple
    for i in range(feature_length):
        for j in range(i + 1, feature_length):
            for m in range(len(rule_k1[i])):
                for n in range(len(rule_k1[j])):
                    tmp_rule = rule_k1[i][m][0] | rule_k1[j][n][0]  # extract each two different rules from rule_k1 to form rule_k2
                    tmp_rule = sorted(tmp_rule)
                    rule_k2.append([tmp_rule, 0.0, 0.0])  # add new rules into rule_k2
    # cal_sup_conf(rule_k2, dataSet, judge)
    cal_sup_conf_v2(rule_k2, conf, supp, data_size)
    rule_scan(rule_k2, 0.0001, 0.0)
    # rule_sort(rule_k2)  # sort the rules by support in rule_k2

    # k = 3 =================================================================
    rule_k3 = []  # initialize rule_k2 with three rules in each tuple
    print("start level 3")
    # rule3starttime = time.time()
    for i in range(len(rule_k2)):
        for j in range(i + 1, len(rule_k2)):
            tmp_rule = set(rule_k2[i][0]) | set(rule_k2[j][0])  # extract each two different rules from rule_k2 to form rule_k3
            tmp_rule = sorted(tmp_rule)
            if len(tmp_rule) != 3:
                continue
            flag = 0
            for k in range(len(rule_k3)):  # check whether tmp_rule is in rule_k3
                if rule_k3[k][0] == tmp_rule:
                    flag = 1
                    break

            if flag == 0:
                if judge_rule_subset(tmp_rule, rule_k2, 2) == 0:  # rule out the rule of which 2 elements subnet is not in rule_k2
                    continue
                else:
                    rule_k3.append([tmp_rule, 0.0, 0.0])  # add new rules into rule_k3
    # rule3endTime = time.time()
    # print("rule3time",rule3endTime-rule3starttime)
    # cal_sup_conf(rule_k3, dataSet, judge)
    cal_sup_conf_v2(rule_k3, conf, supp, data_size)
    rule_scan(rule_k3, 0.0001, 0.0)
    # rule_sort(rule_k3)

    '''
       #k=4 ==========================================================================
        rule_k4 = []  # initialize rule_k4 with four rules in each tuple
        for i in range(len(rule_k3)):
            for j in range(i + 1, len(rule_k3)):
                 tmp_rule = rule_k3[i][0] | rule_k3[j][0]  # extract each two different rules from rule_k3 to form rule_k4
                 if len(tmp_rule)>4:
                     continue
                 if judge_rule_subset(tmp_rule,rule_k3,3) and judge_rule_subset(tmp_rule,rule_k2,2) == 0:  # rule out the rule of which 2 elements subset is not in rule_k2 or 3 elements subset is not in rule_k3
                     continue
                 flag = 0
                 for k in range(len(rule_k4)):
                     if rule_k4[k][0] == tmp_rule:
                         flag = 1
                         break
                 if flag == 0:
                     rule_k4.append([tmp_rule, 0.0, 0.0])  # add new rules into rule_k4
        cal_sup_conf_v2(rule_k4, conf, supp, sample_size)
        rule_scan(rule_k4, 0.0, 0.0)
        rule_sort(rule_k4)
        return rule_k1, rule_k2, rule_k3, rule_k4
    '''

    # k=4-8 ==========================================================================
    rule_k4_9 = []
    for rule in range(4, 10):
        print("start level", rule)
        rule_k4_9.append([])
        if rule == 4:
            for i in range(len(rule_k3)):
                for j in range(i + 1, len(rule_k3)):
                    tmp_rule = set(rule_k3[i][0]) | set(rule_k3[j][0])  # extract each two different rules from rule_k3 to form rule_k4
                    tmp_rule = sorted(tmp_rule)
                    if len(tmp_rule) != rule:
                        continue
                    flag = 0
                    for k in range(len(rule_k4_9[rule - 4])):
                        if sorted(tmp_rule) in rule_k4_9[rule - 4][k]:
                            flag = 1
                            break

                    if flag == 0:
                        if judge_rule_subset(tmp_rule, rule_k3, 3) == 0:  # rule out the rule of which 3 elements subnet is not in rule_k3
                            continue
                        else:
                            rule_k4_9[rule - 4].append([tmp_rule, 0.0, 0.0])  # add new rules into rule_k4
        else:
            for i in range(len(rule_k4_9[rule - 5])):
                for j in range(i + 1, len(rule_k4_9[rule - 5])):
                    tmp_rule = set(rule_k4_9[rule - 5][i][0]) | set(
                        rule_k4_9[rule - 5][j][0])
                    tmp_rule = sorted(tmp_rule)
                    if len(tmp_rule) != rule:
                        continue
                    flag = 0
                    for k in range(len(rule_k4_9[rule - 4])):
                        if sorted(tmp_rule) in rule_k4_9[rule - 4][k]:
                            flag = 1
                            break

                    if flag == 0:
                        if judge_rule_subset(tmp_rule, rule_k4_9[rule - 5],
                                             rule - 1) == 0:  ## rule out the rule of which rule-1 elements subnet is not in rule-1
                            continue
                        else:
                            rule_k4_9[rule - 4].append([tmp_rule, 0.0, 0.0])

        cal_sup_conf_v2(rule_k4_9[rule - 4], conf, supp, data_size)
        rule_scan(rule_k4_9[rule - 4], 0.0001, 0.0)
    rule_k4 = rule_k4_9[0]
    rule_k5 = rule_k4_9[1]
    rule_k6 = rule_k4_9[2]
    rule_k7 = rule_k4_9[3]
    rule_k8 = rule_k4_9[4]
    rule_k9 = rule_k4_9[5]
    return rule_k1, rule_k2, rule_k3, rule_k4, rule_k5, rule_k6, rule_k7, rule_k8, rule_k9


# Chech whether all of the subset_size subset of test_rule is in rule_set
def judge_rule_subset(test_rule, rule_set, subset_size):
    subset = list(itertools.combinations(test_rule, subset_size))  # figure out subset_size subset of test_rule
    flag = 0
    for i in range(len(subset)):
        temp_rule = sorted(subset[i])  # for each subset_size subset
        flag = 0
        for j in range(len(rule_set)):  # check whether temp_rule is in rule_set
            if rule_set[j][0] == temp_rule:
                flag = 1
                break
        if flag == 0:
            break
    return flag


def con_dataDic(dataSet, judge):
    feature_length = len(dataSet[0])
    data_size = len(dataSet)
    conf = {}
    supp = {}
    pos = []
    for i in range(1, 10):
        for j in itertools.combinations([0, 1, 2, 3, 4, 5, 6, 7, 8], i):
            pos.append(list(j))
    for i in range(data_size):
        for j in range(len(pos)):
            tmp_rule = []
            for k in pos[j]:
                tmp_rule.append(dataSet[i][k])
            tmp_rule.sort()
            tmp_tuple = tuple(tmp_rule)
            if tmp_tuple in conf:
                conf[tmp_tuple] += 1
            else:
                conf[tmp_tuple] = 1
            if judge[i][0] == '1':
                if tmp_tuple in supp:
                    supp[tmp_tuple] += 1
                else:
                    supp[tmp_tuple] = 1
    return conf, supp


def cal_sup_conf_v2(rule_list, conf, supp, data_size):
    rule_size = len(rule_list)
    for i in range(rule_size):
        tmp_rule = rule_list[i][0]
        if i % 100 == 0:
            print (str(list(tmp_rule)), "\tcheckpoint\t", i)
        sum1 = 0.0
        sum2 = 0.0
        tmp_rule = list(tmp_rule)
        tmp_rule.sort()
        tmp_tuple = tuple(tmp_rule)
        if tmp_tuple in conf:
            sum2 = conf[tmp_tuple] * 1.0
        if tmp_tuple in supp:
            sum1 = supp[tmp_tuple] * 1.0
        rule_list[i][1] = sum1 / data_size  # index 1 is support
        if sum2 == 0.0:
            rule_list[i][2] = 0.0  # index 2 is confidence
        else:
            rule_list[i][2] = sum1 / sum2
    return

#function of ruling out rules with minsup and minconf under threshold
def rule_scan(rule_list, minsup, minconf):
    for i in range(len(rule_list) - 1, -1, -1):
        if rule_list[i][1] <= minsup:
            rule_list.pop(i)
    for i in range(len(rule_list) - 1, -1, -1):
        if rule_list[i][2] <= minconf:
            rule_list.pop(i)
    return


#function of sorting rules by support
def rule_sort(rule):
    rule_size = len(rule)
    quick_sort(rule, 0, rule_size - 1)


def quick_sort(rule, low, high):
    mid = 0
    if low >= high:
        return
    mid = divide(rule, low, high)
    quick_sort(rule, low, mid - 1)
    quick_sort(rule, mid + 1, high)


def divide(rule, low, high):
    rule_tmp = rule[low]
    while True:
        while low < high and rule[high][2] <= rule_tmp[2]:
            high = high - 1
        if low < high:
            rule[low] = rule[high]
            low = low + 1
        while low < high and rule[low][2] >= rule_tmp[2]:
            low = low + 1
        if low < high:
            rule[high] = rule[low]
            high = high - 1
        if low >= high:
            break
    rule[low] = rule_tmp
    return low


#import data
def apriori_data_import(file_name):
    dataSet = []
    judge = []
    feature = []
    data_file = open(file_name, 'r')
    file_reader = csv.reader(data_file)
    for row in file_reader:
        if file_reader.line_num == 1:
            feature = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
            continue
        judge.append([row[14], row[9]])
        tmp_data = [feature[0] + "_" + row[0], feature[1] + "_" + row[1], feature[2] + "_" + row[2],
                    feature[3] + "_" + row[3], feature[4] + "_" + row[4], feature[5] + "_" + row[5],
                    feature[6] + "_" + row[6], feature[7] + "_" + row[7], feature[8] + "_" + row[8]]
        dataSet.append(tmp_data)
    """
    #transform 'carrier', 'appname' features from digits to string 
    carrier_record = []
    appname_record = []
    carrier_text = []
    appname_text = []
    carrier_record_file = open('./carrier_record.csv', 'r')
    carrier_reader = csv.reader(carrier_record_file)
    appname_record_file = open('./appname_record.csv', 'r')
    appname_reader = csv.reader(appname_record_file)
    for row in carrier_reader:
        carrier_record.append(row[1])
    for row in appname_reader:
        appname_record.append(row[1])
    carrier_record_file.close()
    appname_record_file.close()
    for sample in dataSet:
        carrier_index = int(eval(sample[0]))
        appname_index = int(eval(sample[5]))
        sample[0] = carrier_record[carrier_index]
        sample[5] = appname_record[appname_index]
    """
    # print(dataSet)
    # print(judge)
    data_file.close()
    return dataSet, judge


# 写入数据
def result_writer(rule_k1, rule_k2, rule_k3, rule_k4, rule_k5, rule_k6, rule_k7, rule_k8, rule_k9):
    apriori_output_k1 = open('0506/wifi_usa_0504_compose/apriori_output_k1.csv', 'wb')
    apriori_output_k2 = open('0506/wifi_usa_0504_compose/apriori_output_k2.csv', 'wb')
    apriori_output_k3 = open('0506/wifi_usa_0504_compose/apriori_output_k3.csv', 'wb')
    apriori_output_k4 = open('0506/wifi_usa_0504_compose/apriori_output_k4.csv', 'wb')
    apriori_output_k5 = open('0506/wifi_usa_0504_compose/apriori_output_k5.csv', 'wb')
    apriori_output_k6 = open('0506/wifi_usa_0504_compose/apriori_output_k6.csv', 'wb')
    apriori_output_k7 = open('0506/wifi_usa_0504_compose/apriori_output_k7.csv', 'wb')
    apriori_output_k8 = open('0506/wifi_usa_0504_compose/apriori_output_k8.csv', 'wb')
    apriori_output_k9 = open('0506/wifi_usa_0504_compose/apriori_output_k9.csv', 'wb')
    apriori_writer_k1 = csv.writer(apriori_output_k1)
    apriori_writer_k2 = csv.writer(apriori_output_k2)
    apriori_writer_k3 = csv.writer(apriori_output_k3)
    apriori_writer_k4 = csv.writer(apriori_output_k4)
    apriori_writer_k5 = csv.writer(apriori_output_k5)
    apriori_writer_k6 = csv.writer(apriori_output_k6)
    apriori_writer_k7 = csv.writer(apriori_output_k7)
    apriori_writer_k8 = csv.writer(apriori_output_k8)
    apriori_writer_k9 = csv.writer(apriori_output_k9)
    apriori_writer_k1.writerow(['rule', 'support', 'confidence'])
    apriori_writer_k2.writerow(['rule', 'support', 'confidence'])
    apriori_writer_k3.writerow(['rule', 'support', 'confidence'])
    apriori_writer_k4.writerow(['rule', 'support', 'confidence'])
    apriori_writer_k5.writerow(['rule', 'support', 'confidence'])
    apriori_writer_k6.writerow(['rule', 'support', 'confidence'])
    apriori_writer_k7.writerow(['rule', 'support', 'confidence'])
    apriori_writer_k8.writerow(['rule', 'support', 'confidence'])
    apriori_writer_k9.writerow(['rule', 'support', 'confidence'])
    for i in range(len(rule_k1)):
        for rule_line in rule_k1[i]:
            apriori_writer_k1.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    for rule_line in rule_k2:
        apriori_writer_k2.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    for rule_line in rule_k3:
        apriori_writer_k3.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    for rule_line in rule_k4:
        apriori_writer_k4.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    for rule_line in rule_k5:
        apriori_writer_k5.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    for rule_line in rule_k6:
        apriori_writer_k6.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    for rule_line in rule_k7:
        apriori_writer_k7.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    for rule_line in rule_k8:
        apriori_writer_k8.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    for rule_line in rule_k9:
        apriori_writer_k9.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    apriori_output_k1.close()
    apriori_output_k2.close()
    apriori_output_k3.close()
    apriori_output_k4.close()
    apriori_output_k5.close()
    apriori_output_k6.close()
    apriori_output_k7.close()
    apriori_output_k8.close()
    apriori_output_k9.close()

    # 将所有rule合并并排序
    rule_all = []
    for i in range(len(rule_k1)):
        for rule_line in rule_k1[i]:
            rule_all.append(rule_line)
    for x in rule_k2:
        rule_all.append(x)
    for x in rule_k3:
        rule_all.append(x)
    for x in rule_k4:
        rule_all.append(x)
    for x in rule_k5:
        rule_all.append(x)
    for x in rule_k6:
        rule_all.append(x)
    for x in rule_k7:
        rule_all.append(x)
    for x in rule_k8:
        rule_all.append(x)
    for x in rule_k9:
        rule_all.append(x)
    print("start sort")
    rule_all_sorted = sorted(rule_all, key=lambda x: (-x[2], -x[1]))
    # print(rule_all_sorted)
    apriori_output_all = open('0506/wifi_usa_0504_compose/apriori_rule_all.csv', 'wb')
    apriori_writer_all = csv.writer(apriori_output_all)
    apriori_writer_all.writerow(['rule', 'support', 'confidence'])
    for rule_line in rule_all_sorted:
        apriori_writer_all.writerow([str(list(rule_line[0])), rule_line[1], rule_line[2]])
    apriori_output_all.close()
    return


if __name__ == '__main__':
    t = time.time()
    sys.setrecursionlimit(1000000)
    file_name = '0506/wifi_usa_0504_composed.csv'
    dataSet, judge = apriori_data_import(file_name)
    # dataSet = [['1', '22', '111'],
    #            ['2', '22', '333'],
    #            ['3', '33', '333'],
    #            ['1', '11', '111'],
    #            ['3', '22', '333'],
    #            ['2', '33', '222'],
    #            ['1', '11', '333'],
    #            ['2', '22', '222'],
    #            ['1', '22', '111'],
    #            ['3', '11', '222'],
    #            ['2', '33', '333'],
    #            ['4', '44', '444']]4G CMHK	2	DNS
    # judge = ['0',
    #          '0',
    #          '1',
    #          '1',
    #          '0',
    #          '0',
    #          '1',
    #          '0',
    #          '0',
    #          '1',
    #          '0',
    #          '1']

    """
    carrier	          synHour	appname
    3	                22	toolbox
    HOME	            6	DNS
    HOME	            12	apusapps
    AT&T	            20	DNS
    ZTE	                22	google
    HOME	            10	supo
    Verizon Wireless	4	DNS
    Verizon Wireless	4	audible
    Verizon Wireless	15	DNS
    MetroPCS	        23	instagram
    AT&T	            15	UID(1013)
    Verizon Wireless	4	icenta
    HOME	            22	turboc
    3	                0	facebook
    """
    rule_k1, rule_k2, rule_k3, rule_k4, rule_k5, rule_k6, rule_k7, rule_k8, rule_k9 = apriori_association_rule_mining(
        dataSet, judge, 0.0001, 0.5)
    result_writer(rule_k1, rule_k2, rule_k3, rule_k4, rule_k5, rule_k6, rule_k7, rule_k8, rule_k9)
    print ('Total time:')
    totalTime = time.time() - t
    print (totalTime)

