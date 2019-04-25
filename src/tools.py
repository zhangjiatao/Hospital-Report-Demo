'''
定义一些功能函数
'''
from elasticsearch import Elasticsearch
import json
import random
import report_item
import re

def createTable():
	'''
	用随机数自动填充并生成表格 ok
	return [{'name' : XX, 'value' : XX}{..}..]
	'''
	item_list = []
	name_list = list(set(report_item.item_dict.values()))

	for name in name_list:
		item = dict()
		item['name'] = name
		item['value'] = str(round(random.random(), 2))
		item_list.append(item)

	return item_list



def search(es, text):
	'''
	检索相关模板 ok
	return list
	'''
	dsl = {
		'query': {
		    'multi_match': {
		        'query': text,
		        'fields':[ 'title', 'content'],
		        'type': 'best_fields',

		    }
		}
	}

	result = es.search(index='templets', doc_type='report', body=dsl)
	print(json.dumps(result, indent=2, ensure_ascii=False))
	return result['hits']['hits']


def extract(text, item_list):
	'''
	抽取关键数值信息
	return {key:value}
	'''
	info_dict = {}

	# 先加入表格中的信息
	for item in item_list:
		info_dict[item['name']] = item['value']

	keyWords = report_item.keyWord_dict.keys()
	sentence_list = re.split( '[，,。\n]', text)
	pattern = re.compile(r'[0-9]+\.?[0-9]*')   # 查找数字

	print('========= 文本抽取结果 =========')
	for sentence in sentence_list:

		# 最长匹配方式确定每个句子中的类型
		sentence_type = ''
		for keyWord in keyWords:
			if keyWord in sentence and len(keyWord) > len(sentence_type):
				sentence_type = keyWord
		if sentence_type != '':
			values = pattern.findall(sentence)
			if len(values) >= 1:
				info_dict[sentence_type] = values[0]
				print(sentence, sentence_type, values[0])

	
	return info_dict

def fullfill(text, info_dict):
	'''
	用抽取值自动填充文本
	return text
	'''
	print('========= 填充信息 =========')
	print(info_dict)
	for info in info_dict.keys():
		text = text.replace('<e>%s<e>' % info ,info_dict[info])
	return text
