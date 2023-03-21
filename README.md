
## 项目目录
D:.
├─.idea
│  └─inspectionProfiles
├─Agri_KG_QA1   
├─data              保存抽取出的csv文件        
├─data_process      保存有原始数据，并将所需数据抽取出来
├─dict              保存抽取出的实体部分
└─templates

## 数据处理
1. 将以下数据下载后放在data_process中
数据提取：
链接：https://pan.baidu.com/s/1ZJ9vwr2MdWhuYsM8_-AOaA?pwd=3lmn 
提取码：3lmn 
2. 创建文件夹data和dict
3. 运行data_process文件夹下的main.py文件夹。(运行前请连接neo4j)

## QA
1. 运行方法：直接运行QA.py即可。
2. 目前可回答问题：
    1. <地点>适合种植什么？
    2. <地点>属于哪种气候？
    3. <作物>有那些营养元素？
    note: 由于数据不够完善，难免有没有答案的情况，这是改进的方向。