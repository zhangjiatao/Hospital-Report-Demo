from elasticsearch import Elasticsearch
import os
'''
初始话elasticsearch数据
'''
DATA_PATH = '/Users/zhangjiatao/Documents/MyProject/hospital/data/'

def init_index(es):

	mapping={
		'properties':
		{
			'title':
			{
				'type': 'text',
				'analyzer': 'ik_max_word',
				'search_analyzer': 'ik_max_word'
			},
			'content':
			{
				'type': 'text',
				'analyzer': 'ik_max_word',
				'search_analyzer': 'ik_max_word'
			}
		}
	}
	es.indices.delete(index='templets', ignore = 400) # 清空
	es.indices.create(index='templets', ignore = [400, 404]) # 创建
	result = es.indices.put_mapping(index='templets', doc_type='report', body=mapping) # 建立映射


def init_data(es):
	data_list = []

	# readFile
	files = os.listdir(DATA_PATH)
	for file in files:
		content = ''
		with open(DATA_PATH + file, 'r', encoding = 'utf-8') as f:
			while True:
				line = f.readline()
				if line == '':
					break
				else:
					content += line
		f.close()
		data = {}
		data['title'] = file
		data['content'] = content
		es.index(index='templets', doc_type='report', body=data)



if __name__ == '__main__':
	es = Elasticsearch()
	init_index(es)
	init_data(es)