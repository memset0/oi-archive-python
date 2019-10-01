import re, json
import markdown as markdown_lib
from flask import Flask
from flask import render_template
from flask import send_from_directory
app = Flask(__name__)

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

def markdown(text):
	text = markdown_lib.markdown(text, extensions=['markdown.extensions.extra'])
	return text

def render(text, type, oj):
	# 人类智慧结晶
	if type == 'markdown':
		text = markdown(text)
	if oj == 'tsinsen':
		text = text.replace('<div id="pcont1" style="margin-top:20px; display:block;">', '')
		data = re.findall('<div class="pddata">[\s\S]*?</div>', text)
		for item in data:
			text = text.replace(item, '<pre>' + item[20:-6].replace('<br/>', '') + '</pre>')
	elif oj == 'bzoj':
		text = text.replace('<div class="content"><span class="sampledata">', '<pre>')
		text = text.replace('</span></div>', '</pre>')
		text = text.replace('<br/>\n', '<br/>')
		text = text.replace('<div class="content"><p><a href="problemset.php?search="></a></p></div>', '')
		text = re.sub('<p>[\s]*', '<p>', text)
	text = text.replace('src="source/', 'src="/source/')
	text = re.sub('<pre>\n*', '<pre>', text)
	text = re.sub('\n*</pre>', '</pre>', text)
	text = re.sub('<pre[\s\S]*?>', '<div class="mdui-typo"><pre>', text)
	text = re.sub('</pre>', '</pre></div>', text)
	text = re.sub('<table[\s\S]*?>', '<div class="table mdui-table-fluid"><table class="mdui-table">', text)
	text = re.sub('</table>', '</table></div>', text)
	return text

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

@app.errorhandler(404)
def page_404(e):
    return render_template('errorpage.html', **data,
		error_code = 404,
		error_info = 'Not Found'
	), 404

@app.errorhandler(500)
def page_500(e):
    return render_template('errorpage.html', **data,
		error_code = 500,
		error_info = 'Internal Server Error'
	), 500

@app.route('/source/<path:filename>') 
def source_file(filename):
    return send_from_directory('source', filename) 

@app.route('/')
def index():
	return render_template('index.html', **data, 
		style = 'index'
	)

@app.route('/problemset/<oj>')
def problemset(oj):	
	if not oj in data['oj_data'].keys():
		return page_404(None)
	return render_template('problemset.html', **data,
		oj = oj,
		name = data['oj_data'][oj]['name'],
		problemset = oj_problemset[oj],
		style = 'problemset'
	)

@app.route('/problem/<oj>/<pid>')
def problem(oj, pid):
	if not oj in data['oj_data'].keys():
		return page_404(None)
	prob = json.load(open('source/{oj}/{pid}/main.json'.format(oj=oj, pid=pid)))
	plain = open('source/{oj}/{pid}/description.md'.format(oj=oj, pid=pid), 'r+', encoding='utf8').read()
	content = {}
	for string in ('\n' + plain).split('\n# '):
		key = string.find('\n')
		if key == -1:
			continue
		title = string[0:key]
		statement = render(string[key:], prob['description_type'], oj)
		if re.sub('\s', '', statement) == '':
			continue
		content[title] = statement
	return render_template('problem.html', **data,
		oj = oj,
		pid = pid,
		prob = prob,
		data = content,
		config = data['oj_config'].get(oj, dict()),
		style = 'problem'
	)

@app.route('/search/<keyword>')
def search(keyword):
	problemset = []
	for prob in dictionary:
		if prob.search(keyword):
			problemset.append(prob)
	return render_template('problemset.html', **data,
		name = keyword,
		problemset = problemset,
		style = 'search'
	)

if __name__ == '__main__':
	app.run()