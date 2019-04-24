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

## 使用说明