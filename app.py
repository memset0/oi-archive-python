from flask import Flask
from flask import render_template
from flask import send_from_directory
app = Flask(__name__)

from render import *
from loader import *

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