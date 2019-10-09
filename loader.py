import json

class Problem:
	def __init__(self, oj, oj_name, pid, title, order=-1):
		self.oj = oj
		self.oj_name = oj_name
		self.pid = pid
		self.title = title
		self.order = order
	def __str__(self):
		return self.title
	def search(self, keyword):
		keyword = keyword.upper()
		if keyword == self.oj.upper() or keyword == self.pid.upper() or keyword == self.oj.upper() + self.pid.upper():
			return True
		if keyword in self.title.upper():
			return True
		return False

class ProblemInfo:
	def __init__(self, time, memory, judge, url, title, description_type):
		self.time = time
		self.memory = memory
		self.judge = judge
		self.url = url
		self.title = title
		self.description_type = description_type

class OnlineJudge:
	def __init__(self, key, name, enable, problemlist, submit_link=None, testdata_link=None, submission_link=None, statistics_link=None, discussion_link=None):
		self.key = key
		self.name = name
		self.problemlist = problemlist
		self.submit_link = submit_link
		self.testdata_link = testdata_link
		self.submission_link = submission_link
		self.statistics_link = statistics_link
		self.discussion_link = discussion_link

def init():
	global config, oj_list
	config = json.load(open('config.json', encoding='utf8'))
	oj_list = dict()
	for oj_key, oj_data in config['oj'].items():
		if not oj_data['enable']:
			continue
		problemlist = dict()
		for problem in json.load(open('source/{oj}/problemlist.json'.format(oj=oj_key))):
			problemlist[problem['pid']] = Problem(
				oj = oj_key,
				oj_name = oj_data['name'],
				pid = problem['pid'],
				title = problem['title']
			)
		oj_list[oj_key] = OnlineJudge(**oj_data,
			key = oj_key,
			problemlist = problemlist
		)

def init_data():
	global data
	data = dict()
	data['config'] = config
	data['oj_list'] = oj_list