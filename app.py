import re
import json

from flask import Flask
from flask import render_template, send_from_directory
app = Flask(__name__)

from render import render, render_markdown
from loader import Problem, ProblemInfo, OnlineJudge
import loader
loader.init()
loader.init_data()
from loader import data, config, oj_list

@app.errorhandler(404)
def page_404(e):
    return render_template('errorpage.html', **data,
		error_code = 404,
		error_info = 'Not Found'
	), 404

@app.errorhandler(500)
def page_500(e):
    return render_template('errorpage.html',
		error_code = 500,
		error_info = 'Internal Server Error'
	), 500

@app.route('/source/<path:filename>') 
def source_file(filename):
    return send_from_directory('source', filename) 

@app.route('/favicon.png') 
def favicon_file():
    return send_from_directory('.', 'favicon.png') 

@app.route('/')
def index():
	return render_template('index.html', **data, 
		content = render_markdown(open('index.md', 'r+', encoding='utf8').read()),
		style = 'index'
	)

@app.route('/problemset/<oj>')
def problemset(oj):	
	if not oj in oj_list.keys():
		return page_404(None)
	return render_template('problemset.html', **data,
		oj = oj_list[oj],
		problemset = oj_list[oj].problemlist.values(),
		style = 'problemset'
	)

@app.route('/problem/<oj>/<pid>')
def problem(oj, pid):
	if not oj in oj_list.keys() or not pid in oj_list[oj].problemlist.keys():
		return page_404(None)
	info = json.load(open('source/{oj}/{pid}/main.json'.format(oj=oj, pid=pid), encoding='utf8'))
	plain = open('source/{oj}/{pid}/description.md'.format(oj=oj, pid=pid), 'r+', encoding='utf8').read()
	problem_info = ProblemInfo(
		time = info['time'],
		memory = info['memory'],
		judge = info['judge'],
		url = info['url'],
		title = info['title'],
		description_type = info['description_type']
	)
	problem_data = dict()
	for string in ('\n' + plain).split('\n# '):
		key = string.find('\n')
		if key == -1:
			continue
		title = string[0:key]
		statement = render(string[key:], problem_info.description_type, oj)
		if re.sub(r'\s', '', statement) == '':
			continue
		problem_data[title] = statement
	return render_template('problem.html', **data,
		oj = oj_list[oj],
		problem = oj_list[oj].problemlist[pid],
		problem_info = problem_info,
		problem_data = problem_data,
		style = 'problem'
	)

@app.route('/search/<input>')
def search(input):
	keywords = re.findall(r'\w+', input.upper())
	problemset = []
	for oj in oj_list.values():
		for problem in oj.problemlist.values():
			flag = True
			for keyword in keywords:
				if not problem.search(keyword):
					flag = False
					break
			if flag:
				problemset.append(problem)
	return render_template('problemset.html', **data,
		keywords = keywords,
		problemset = problemset,
		style = 'search'
	)

if __name__ == '__main__':
	app.run()