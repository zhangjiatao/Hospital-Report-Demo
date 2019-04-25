# 化验单

## 功能设计

1. 随机生成化验项目结果
2. 检索填写模板，如果检索信息中存在关键数值则进行抽取
3. 选择模板后，自动的将化验项目结果与抽取结果填入模板中
4. 将编辑内容保存

## 安装

1. 安装Elasticsearch:
```
brew install Elasticsearch
```
2. 安装python包:
```
pip install elasticsearch
```
3. 初始化数据(代码里面的数据路径需要修改,使路径指向data文件夹): 
```
python init.py
```
4. 启动程序:
```
python GUI.py
```

## 使用

![](https://github.com/zhangjiatao/Hospital-Report-Demo/blob/master/img/1.png)

* 化验项目为随机生成
* 在"诊断及意见"中输入医师诊断，输入的内容可以为检索模板的关键词，也可以是诊断内容
* 点击"检索模板"后可以在模板库中找到对应的模板
* 点击"应用模板"后可以将模板库中选中的模板应用到"诊断及意见"中，并将化验项目与输入中包含的关键数值自动填入模板中
* 点击"保存"后，可将报告以txt格式保存至reports目录下(需要在GUI.py下更改路径）