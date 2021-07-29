import requests
import json


# 搜索歌曲数，范围为1-50
each_num = 10
# api
url = r'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'


while True:
    pname = input("输入搜索歌手名字： ")
    if pname:
        payload = {"qqmusic_ver":"1298", "new_json":"1", "n":each_num, "w":pname}
        response = requests.get(url, params=payload)

        if response.status_code == 200:
            print("连接成功，稍等获取{}的歌曲名....".format(pname.strip('\n')))
            # 删除无用字符，用来进行json格式转换
            data = response.text.strip('MusicJsonCallback6311264544382232(')[0:-1]
            data = json.loads(data)

            # data = json.dumps(data, indent=4, ensure_ascii=False) # json格式输出，解决中文乱码
            for i in data['data']['song']['list']:
                name = i['name']
                print(name)
        else:
            print("cannot find songs with {} singer".format(pname))
            continue
    else:
        break











# with open(data_store, 'a') as f:
#     f.write(name)

