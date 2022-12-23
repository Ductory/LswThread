#LswThread - Made by Dangfer
#功能：获取最爱春雷2021的全部帖子
import hashlib
import requests
import time
import re
from urllib.parse import urlencode

def thread(uid):
	#pattern
	pSmiley = r'class="BDE_Smiley".*src='
	pImage = r'class="BDE_Image".* >'
	pVideo = r'<div.*/div>'
	pn = 1
	num = getThreadNum(uid) #获取帖子总数
	param = {'is_thread': '1',
			 'need_content': '1',
			 'pn': '',
			 'uid': uid}
	with open('lsw.html', 'w', encoding='utf-8') as f:
		f.write('<ol>\n')
		while num > 0:
			param['pn'] = str(pn)
			pn += 1
			num -= 60 #每次获取60个帖子
			param['sign'] = sign(param)
			url = 'http://c.tieba.baidu.com/c/u/feed/userpost?' + urlencode(param)
			response = requests.get(url).json()
			for i in response['post_list']:
				content = i['content']
				if 'first_post_content' in i:
					for t in i['first_post_content']:
						tmp = t['type'] #对表情、图片、视频特殊处理
						if tmp == 2: #smiley
							content = re.sub(pSmiley, 'src=', content, 1)
						elif tmp == 3: #image
							content = re.sub(pImage, f'src="{t["origin_src"]}">', content, 1)
						elif tmp == 5: #video
							content = re.sub(pVideo, f'<a target= "_blank" href="{t["link"]}"><img src="{t["src"]}"></a>', content, 1)
				f.write(f"<li>在<a target='_blank' href='https://tieba.baidu.com/f?kw={i['forum_name']}'>{i['forum_name']}</a>吧发帖：<a target='_blank' href='https://tieba.baidu.com/p/{i['thread_id']}'>{i['title']}</a>&emsp;<span>{time.strftime('%Y年%m月%d日 %H时%M分%S秒', time.localtime(int(i['create_time'])))}</span><p>{content}</p><hr>\n")
		f.write('</ol>')
	return

def getThreadNum(uid):
	param = {'need_post_count': '1',
			 'uid': uid}
	param['sign'] = sign(param)
	url = 'http://c.tieba.baidu.com/c/u/user/profile?' + urlencode(param)
	response = requests.get(url).json()
	return response['user']['thread_num']

def sign(src):
	s = ''
	if 'sign' in src: #重新签名
		del src['sign']
	#生成报文
	for k, v in src.items():
		s += k + '=' + v
	s += 'tiebaclient!!!'
	return hashlib.md5(s.encode('utf-8')).hexdigest()

#264432381 雷绍武的uid
#5530535828 最爱春雷2021的uid
thread('5530535828') #获取最爱春雷2021的全部帖子