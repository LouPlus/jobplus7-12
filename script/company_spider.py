import requests
import random
from faker import Faker
from jobplus.models import db, User, Company, Job
fake = Faker('zh_CN')
class LagouSpider(object):
	url = 'https://www.lagou.com/gongsi/0-0-0.json'
	def formdata(self, page):
		return {
			'first': 'false',
			'pn': page,
			'sortField': 0,
			'havemark': 0
		}
	@property
	def headers(self):
		return {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
			'Referer': 'https://www.lagou.com/gongsi/',
			'Cookie': 'WEBTJ-ID=20180807111813-165126463ad23d-05cb6fbf1029c-182e1503-1049088-165126463aed62; _ga=GA1.2.410131003.1533611894; _gid=GA1.2.879117640.1533611894; user_trace_token=20180807111813-852558e9-99f0-11e8-b757-525400f775ce; LGUID=20180807111813-85255de5-99f0-11e8-b757-525400f775ce; JSESSIONID=ABAAABAABEEAAJA0597CF539A3ECC19D9C0734825CAA4C8; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=dc0f80d61fad146960fa56ffd06b8bf3; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; login=false; unick=""; _putrc=""; LG_LOGIN_USER_ID=""; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533611894,1533619552,1533698991; LGSID=20180808173724-a827a8be-9aee-11e8-b8b7-525400f775ce; TG-TRACK-CODE=index_checkmore; SEARCH_ID=3ba1ccfb7a43445d9139281da9476747; _gat=1; LGRID=20180808182932-f087f828-9af5-11e8-a356-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533724174'
		}
	@property
	def company(self):
		for page in range(2, 4):
			r = requests.post(self.url, data=self.formdata(page), headers=self.headers)
			result = r.json()['result']
			for company in result:
				yield company

class FakerData(object):

	def __init__(self):
		self.lagou = LagouSpider()
	def fake_company(self):
		for company in self.lagou.company:
			c = User(
				username=company['companyShortName'],
				email=fake.email(),
				role=User.ROLE_COMPANY
			)
			c.password = '123456'
			db.session.add(c)
			try:
				db.session.commit()
			except:
				db.session.rollback()
				continue
			d = Company(
				logo = 'http://www.lgstatic.com/thumbnail_200x200/' + company['companyLogo'],
				site='https://shiyanlou.com',
				location=company['city'],
			)
			d.user_id = c.id
			db.session.add(d)
			db.session.commit()
	def fake_job(self):
		companies = User.query.filter_by(role=User.ROLE_COMPANY).all()
		for i in range(100):
			job = Job(
				name=fake.word() + '',
				salary_low=random.randrange(3000, 8000, 1000),
				salary_high=random.randrange(8000, 20000, 10000),
				location=company.detail.location,
				tag=','.join([fake.word() for i in range(3)]),
				company=company,
				experience_requirement=random.choice(['不限', '1', '1-3', '3-5', '5+']),
				degree_requirement=random.choice('不限', '本科', '硕士', '博士'),
			)
			db.session.add(job)
			db.session.commit()
def run():
	f = FakerData()
	f.fake_company()
