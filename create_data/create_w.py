import os
import csv
#特征矩阵
'''
路况 0  ~  4
未捕捉到 -1
'''
#待处理数据目录
s_data = '../source_data'
ts_dict = {'畅通':0,'基本畅通':1,'行驶缓慢':2,'拥堵':3,'严重拥堵':4}
roads_dict = {}
cnt_road_dict = {}#顺序

road = []
with open(s_data + '/TSOctober1225.txt', encoding='UTF-8') as f:
    reader = f.readlines()
    for r in reader:
        list_r = r.split('：')[0]
        district = r.split(',')[-2]
        if list_r+district not in road:
            road.append(list_r+district)
        else:
            # print(list_r+district)
            continue
print(road)
# print(len(road))
# print(len(road[0]))

with open(s_data + '/roads.csv', 'r', encoding='UTF-8') as f:
    reader = f.readlines()
    for line in reader[1:]:
        block = line.split(',')[1] + line.split(',')[-2]
        if block not in roads_dict:
            roads_dict[block] = line.split(',')[0]
        # print(roads_dict)
# print(roads_dict)
# print(len(roads_dict.keys()))


cnt = 0
dst = open(s_data+'/entity2id.txt', 'w', encoding='UTF-8')
for rd in road:
    if rd in roads_dict:
        dst.writelines(rd + '\t' + roads_dict[rd] + '\n')
        cnt_road_dict[rd] = cnt
        cnt += 1
dst.close()
print(cnt_road_dict)
print("cnt = ",cnt)

#建立日期字典
time_dict = {}
cnt = 0
time_list = []
with open(s_data + '/TSOctober1225.txt', encoding='UTF-8') as f:
    reader = f.readlines()
    for r in reader:
        line = r.split(',')
        temp = line[-1].strip('\n')
        if temp not in time_list:
            time_list.append(temp)
            time_dict[temp] =  cnt
            cnt += 1
        else:
            continue
# print(time_dict)
# print(time_list)
# print(len(time_dict))
# print(len(time_list))

#1026 * 308
w_matrix = [[-1]*308 for i in range(len(time_list))]
'''
用roads_dict定位道路id -- 列
用time_dict定位时间id  -- 行
'''
with open(s_data + '/TSOctober1225.txt', encoding='UTF-8') as f:
    reader = f.readlines()
    for r in reader:
        line = r.split(',')
        time = line[-1].strip('\n')
        ts = line[-3]
        district = line[-2]
        line = r.split('：')
        road = line[0] + district
        if road in cnt_road_dict:
            w_matrix[time_dict[time]][cnt_road_dict[road]] = ts_dict[ts]
print(w_matrix)

'''
写入文件保存 w_matrix.txt
'''
with open(s_data + '/w_matrix.txt', 'w', encoding='UTF-8') as f:
    for line in w_matrix:
        f.writelines(str(line)[1:-1] + '\n')
print("write w_matrix successfully!")