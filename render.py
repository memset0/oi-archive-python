import re
import markdown as markdown_lib

def render_markdown(text):
	text = markdown_lib.markdown(text, extensions=['markdown.extensions.extra'])
	return text

def render(text, type, oj):
	# 人类智慧
	if type == 'markdown':
		text = text.replace('\n* ', '\n\n* ')
		text = text.replace('\n- ', '\n\n- ')
		text = render_markdown(text)
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