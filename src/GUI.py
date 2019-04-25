from tkinter import ttk
import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter import *
import demo
from elasticsearch import Elasticsearch


REPORT_PATH = '/Users/zhangjiatao/Documents/MyProject/hospital/reports/report.txt'

item_list = []

def writeFile(file, item_list, text):

	with open(file, 'w', encoding = 'utf-8') as f:
		
		for item in item_list:
			f.write(item['name'] + ' : ' + item['value'] + '\n')

		f.write('---------------------\n')
		f.write(text + '\n')
	f.close()

def createTable():
	global item_list
	item_list = demo.createTable()
	print('here', item_list)


def initGUI():

	global item_list

	es = Elasticsearch()
	# =============== 初始化窗口 ===============
	window = tk.Tk()
	window.title('report demo')
	window.geometry('1000x700')  # 这里的乘是小x w * h

	# =============== frame设置 ===============
	fr_top = tk.Frame(window, height = 20, width = 1000)
	fr_top.pack()
	fr_left = tk.Frame(window)
	fr_left.pack(side='left')
	fr_right = tk.Frame(window)
	fr_right.pack(side='right')
	fr_lt = tk.Frame(fr_left)
	fr_lt.pack(side = 'top')
	fr_lb = tk.Frame(fr_left)

	fr_lb.pack(side = 'bottom')
	fr_rt = tk.Frame(fr_right)
	fr_rt.pack(side = 'top')
	fr_rb = tk.Frame(fr_right)
	fr_rb.pack(side = 'bottom')

	# =============== label =============== 

	lab1 = tk.Label(fr_top, text='检验报告单', font=('Arial', 25), height = 2)
	lab1.pack(side = 'top')
	lab2 = tk.Label(fr_rt, text='模板库', font=('Arial', 15), height = 2)
	lab2.pack(side = 'top')
	lab3 = tk.Label(fr_lt, text='诊断及意见', font=('Arial', 15), height = 2)
	lab3.pack(side = 'top')
	# lab4 = tk.Label(fr_top, text='', font=('Arial', 15), height = 2)
	# lab4.pack(side = 'bottom')

	# =============== 表格设置 =============== 
	columns = ('序号', '项目', '结果')
	treeview = ttk.Treeview(fr_top, height=14, show="headings", columns=columns)  # 表格
	treeview.column("序号", width=100, anchor='center')
	treeview.column("项目", width=500, anchor='center') # 表示列,不显示
	treeview.column("结果", width=500, anchor='center')
	treeview.heading("序号", text="序号") 
	treeview.heading("项目", text="项目") # 显示表头
	treeview.heading("结果", text="结果")
	treeview.pack(fill=BOTH)
	
	def writeTable():
		# 清空表格
		x = treeview.get_children()
		for item in x:
			treeview.delete(item)
		# 填入表格
		createTable()
		for index, item in enumerate(item_list): # 写入数据
		    treeview.insert('', index, values=(str(index + 1), item['name'], item['value']))

	writeTable()
	print(item_list)

	# =============== Listbox设置=============== 
	lb = tk.Listbox(fr_rt, width = 40, height=10, relief = 'raised',   fg="blue", bd = 2)
	lb.pack()
	res_list = demo.search(es, '模板')
	lb.delete(0, END)
	for res in res_list:
		res = res['_source']
		lb.insert('end', '#'+ res['title'].replace('.txt', '') + '#:  ' + res['content'])


	# =============== text控件 =============== 
	t = tk.Text(fr_lt, height=15, width=100, relief = 'raised', bd = 2)
	t.pack()

	# =============== button ===============
	def searchTemplets(): # 在鼠标焦点处插入输入内容
		'''
		检索模板button相应事件
		'''
		query = t.get('0.0', 'end')
		res_list = demo.search(es, query)
		lb.delete(0, END)
		for res in res_list:
			res = res['_source']
			lb.insert('end', res['title'].replace('.txt', '') + res['content'])
	b1 = tk.Button(fr_lb, text='检索模板', width=10,height=2, command=searchTemplets)
	b1.pack(side = 'left')

	def addText():
		'''
		获取text框中的文本，方便进行检索
		'''
		text = t.get('0.0', 'end')
		info_dict = demo.extract(text, item_list) # 抽取信息
		t.delete('0.0', 'end')
		text = lb.get(lb.curselection())
		text = re.sub(re.compile(r'#.*#:  ') , '', text)	
		text = demo.fullfill(text, info_dict) # 自动填充文本

		text = re.sub(re.compile(r'<e>.*<e>') , '__', text)
		# text = text.replace('<e>.*<e>', '____')
		t.insert('end',text)   # 获取当前选中的文本
	b2 = tk.Button(fr_rb, text='应用模板', width=10, height=2, command=addText)
	b2.pack()

	def saveReport():
		'''
		保存当前报告，并且刷新表格信息
		'''
		writeFile(REPORT_PATH, item_list, t.get('0.0', 'end'))
		t.delete('0.0', 'end') # 刷新text框
		writeTable() # 刷新表格


	b3 = tk.Button(fr_lb, text='保存', width=10,height=2, command=saveReport)
	b3.pack(side = 'right')

	window.mainloop()


if __name__ == '__main__':
	initGUI()
