import re, json
import markdown as markdown_lib
from flask import Flask
from flask import render_template
from flask import send_from_directory
app = Flask(__name__)

def markdown(text):
	text = markdown_lib.markdown(text, extensions=['markdown.extensions.extra'])
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
		data = data['oj_data'][oj],
		config = data['oj_config'].get(oj, dict()),
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
		statement = string[key:]
		if re.sub('\s', '', statement) == '':
			continue
		if prob['description_type'] == 'markdown':
			statement = markdown(statement)
		content[title] = statement.replace('src="source/', 'src="/source/')
	return render_template('problem.html', **data,
		oj = oj,
		pid = pid,
		prob = prob,
		data = content,
		style = 'problem'
	)
	
@app.route('/source/<path:filename>') 
def custom_static(filename): 
    return send_from_directory('source', filename) 

if __name__ == '__main__':
	app.run()