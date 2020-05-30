import py2neo
import os
import json
import copy
import sys
d = os.path.dirname(__file__)
print(d)
sys.path.append(os.path.dirname(d)) # 添加自己指定的搜索路径


def getFiles(path, prefix):
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) \
    for file in files if file.startswith(prefix)]

class search_return():
	"功能: 对数据库进行搜索操作\
	参数 search_name 为搜索名"
	def __init__(self,search_name):
		self.search_name = search_name
		self.graph = py2neo.Graph("http://localhost:7474",auth=("neo4j","password"))


	def node(self):
		str1 =  "MATCH(n{name:'%s'})RETURN n"%(self.search_name)
		return self.graph.run(str1).to_subgraph()

	def picture_path(self):
		path = os.path.dirname(os.path.dirname(d)) + "\\static\\pictures"
		return [os.path.abspath(os.path.join(root, file)) for root, dirs, files in os.walk(path) \
		    	for file in files if file.startswith(self.search_name)]

	def relationships(self,limit = 25):
		str1 = "match(n{name: '%s'})-[r]-(b) RETURN r LIMIT %s"%(self.search_name,limit)	
		return self.graph.run(str1)

	def dict(self):
		a = str(self.node())  #fuck neo4j
		return dict(self.node()) if self.node() else None
	def singleNode_json(self):
		node = self.node();
		a = str(node)  #fuck neo4j
		a = dict(node)
		a["id"] = node.identity
		return json.dumps({"nodes":[a],"links":[]})



	def json(self):
		links = []
		nodes = []
		nodes_set = set()
		links_set = set()

		for record in self.relationships():
			link = record.to_subgraph()
			a = str(link)   # fuck py2neo
			print('a',a)

			if link.start_node.identity not in nodes_set:
				dic = dict(link.start_node)
				dic['id'] = link.start_node.identity
				nodes_set.add(link.start_node.identity)
				nodes.append(dic)
			if link.end_node.identity not in nodes_set:
				dic = dict(link.end_node)
				dic['id'] = link.end_node.identity
				nodes_set.add(link.end_node.identity)
				nodes.append(dic)

			if link.identity not in links_set:
				dic = dict(link)
				dic['relationships'] = type(link).__name__
				dic['id'] = link.identity
				dic['source'] = link.start_node.identity
				dic['target'] = link.end_node.identity
				links.append(dic)
				links_set.add(link.identity)


		a = json.dumps({"nodes" : nodes,"links" : links})
		return a



if __name__ == '__main__':
	name = "美国"

	path = '../../static/data/json/search_return.json'
	dd = search_return(name)
	print(dd.json())
	print(dd.singleNode_json())
