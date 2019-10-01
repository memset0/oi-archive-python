import json

class Problem:
	def __init__(self, oj, pid, title):
		self.oj = oj
		self.oj_name = data['oj_data'][oj]['name']
		self.pid = pid
		self.title = title
	def search(self, keyword):
		if keyword == self.oj or keyword == self.pid or keyword == self.oj + self.pid:
			return True
		if keyword in self.title:
			return True
		return False

def load_oj_data():
	result = {}
	for info in json.load(open('source/problemset.json','r')):
		name = info['id']; del info['id']
		if name == 'main':
			continue
		info['data'] = json.load(open('source/{name}/problemlist.json'.format(name=name),'r'))
		result[name] = info
	return result

def load_oj_config():
	result = json.load(open('config.json','r'))
	return result

data = {
	'oj_data': load_oj_data(),
	'oj_config': load_oj_config()
}

def load_dictionary():
	global dictionary, oj_problemset
	dictionary = []
	oj_problemset = {}
	for oj, info in data['oj_data'].items():
		problemset = []
		for prob in info['data']:
			problemset.append(Problem(
				oj = oj,
				pid = prob['pid'],
				title = prob['title']
			))
		dictionary.extend(problemset)
		oj_problemset[oj] = problemset
	return dictionary

load_dictionary()