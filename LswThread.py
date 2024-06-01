# LswThread - Made by Dangfer
# 功能：获取最爱春雷2021的全部帖子
import requests
import time
import re
from hashlib import md5
from urllib.parse import urlencode

type Params = dict[str, str]
type Json = dict

def sign(param: Params) -> str:
	#如果已经存在, 则重新签名
	if 'sign' in param:
		del param['sign']
	param: Params = dict(sorted(param.items()))
	s: str = ''
	for k, v in param.items():
		s += k + '=' + v
	s += 'tiebaclient!!!'
	return md5(s.encode('utf-8')).hexdigest()

def gen_url(api: str, param: Params) -> str:
	param['sign'] = sign(param)
	return api + urlencode(param)

def api_json(api: str, param: Params) -> Json:
	url: str = gen_url(api, param)
	return requests.get(url).json()

def get_thread(uid: str, filename: str) -> None:
	#pattern
	pat_smiley: str = r'class="BDE_Smiley".*src='
	pat_image: str = r'class="BDE_Image".* >'
	pat_video: str = r'<div.*/div>'
	pn: int = 0
	param = {'is_thread': '1',
			 'need_content': '1',
			 'pn': '',
			 'uid': uid}
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(
"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.0.0/crypto-js.min.js"></script>
    <script>
        function open_video(event) {
            const sign = (param) => {
                let s = '';
                for (let [k, v] of Object.entries(param))
                    s += k + '=' + v;
                s += 'tiebaclient!!!';
                return CryptoJS.MD5(s).toString();
            };
            const urlencode = (param) => {
                return Object.entries(param).map(([k, v]) => 
                    encodeURIComponent(k) + '=' + encodeURIComponent(v)
                ).join('&');
            };
            const gen_url = (api, param) => {
                param['sign'] = sign(param);
                return api + urlencode(param);
            };
            const fetch_data = (url, callback) => {
                const proxy = 'https://cors-anywhere.herokuapp.com/';
                fetch(proxy + url)
                    .then(response => response.json())
                    .then(data => callback(data))
                    .catch(error => console.error('fetch failed'));
            };
            const get_video = (data) => {
                for (let con of data['post_list'][0]['content'])
                    if (con['type'] == 5)
                        window.open(con['link'], '_blank');
            };
            let img = event.target;
            let tid = img.getAttribute('data-tid');
            let param = {'kz': tid};
            fetch_data(gen_url('http://c.tieba.baidu.com/c/f/pb/page?', param), get_video);
        }

        window.onload = function() {
            let images = document.querySelectorAll('.video');
            images.forEach((img) => {
                img.addEventListener('click', open_video);
            });
        }
    </script>
</head>
<body>
<ol>
"""
		)
		def modify_image_url(url) -> str:
			match = re.match(r'http://tiebapic([^\?]+)', url)
			if match is None:
				return url
			else:
				return 'http://imgsrc' + match.group(1)
		while True:
			time.sleep(1)
			pn += 1
			print(pn)
			param['pn'] = str(pn)
			post_list: list = api_json('http://c.tieba.baidu.com/c/u/feed/userpost?', param)['post_list']
			if len(post_list) == 0:
				break
			for post in post_list:
				content = post['content']
				if 'first_post_content' in post:
					for frs in post['first_post_content']:
						match frs['type']: #对表情、图片、视频特殊处理
							case 2: #smiley
								content = re.sub(pat_smiley, 'src=', content, 1)
							case 3: #image
								content = re.sub(pat_image, f'src="{modify_image_url(frs["origin_src"])}">', content, 1)
							case 5: #video
								content = re.sub(pat_video, f'<img class="video" data-tid="{post['thread_id']}" src="{modify_image_url(frs["src"])}">', content, 1)
				f.write((
					f"<li>在<a target='_blank' href='https://tieba.baidu.com/f?kw={post['forum_name']}'>{post['forum_name']}</a>吧发帖："
					f"<a target='_blank' href='https://tieba.baidu.com/p/{post['thread_id']}'>{post['title']}</a>&emsp;"
					f"<span>{time.strftime('%Y年%m月%d日 %H时%M分%S秒', time.localtime(int(post['create_time'])))}</span>"
					f"<p>{content}</p></li><hr>\n"
				))
		f.write(
"""</ol>
</body>
</html>
"""
		)

if __name__ == '__main__':
	# get_thread('5530535828', '最爱春雷.html') #获取最爱春雷2021的全部帖子
	get_thread('264432381', '雷绍武.html') #获取雷绍武的全部帖子