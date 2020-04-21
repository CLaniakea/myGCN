import os
import csv

#待处理数据目录
s_data = '../source_data'

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
print(len(road))
print(len(road[0]))
roads_dict = {}#按照road序
cnt_road_dict = {}#顺序
with open(s_data + '/roads.csv', 'r', encoding='UTF-8') as f:
    reader = f.readlines()
    for line in reader[1:]:
        block = line.split(',')[1] + line.split(',')[-2]
        if block not in roads_dict:
            roads_dict[block] = line.split(',')[0]
        # print(roads_dict)
print(roads_dict)
print(len(roads_dict.keys()))
cnt = 0
dst = open(s_data+'/entity2id.txt', 'w', encoding='UTF-8')
for rd in road:
    if rd in roads_dict:
        dst.writelines(rd + '\t' + roads_dict[rd] + '\n')
        cnt_road_dict[rd] = cnt
        cnt += 1
dst.close()
print("cnt = ",cnt)


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]



#建立邻接矩阵
adj = [[0]*cnt for i in range(cnt)]
#1，2
with open(s_data + '/road-road.csv', 'r', encoding='UTF-8') as f:
    reader = f.readlines()
    cross_road = 0
    for rd in road:#对每一条路遍历
        # print(roads_dict[rd])
        if rd in roads_dict:
            for line in reader[1:]:
                line = line.strip('\n')
                if roads_dict[rd] == line.split(',')[0]:
                    # print(get_key(roads_dict, line.split(',')[1]))
                    # print(road)
                    get_key_road = ''.join(get_key(roads_dict, line.split(',')[1]))#list to str
                    if get_key_road in road:
                        # print(rd, get_key_road)
                        adj[cnt_road_dict[rd]][cnt_road_dict[get_key_road]] = 1
                        cross_road += 1
        else:
            continue

with open(s_data + '/road-road.csv', 'r', encoding='UTF-8') as f:
    reader = f.readlines()
    for rd in road:#对每一条路遍历
        # print(roads_dict[rd])
        if rd in roads_dict:
            for line in reader[1:]:
                line = line.strip('\n')
                if roads_dict[rd] == line.split(',')[1]:
                    get_key_road = ''.join(get_key(roads_dict, line.split(',')[0]))
                    if get_key_road in road:
                        # print(rd, get_key_road)
                        adj[cnt_road_dict[rd]][cnt_road_dict[get_key_road]] = 1
                        cross_road += 1
        else:
            continue
print(cross_road)
print(adj)

#写邻接矩阵 ',' 区分
with open(s_data + '/adj.txt', 'w', encoding='UTF-8') as f:
    for line in adj:
        f.writelines(str(line)[1:-1] + '\n')



