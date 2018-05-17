#! /usr/bin/python3

import requests
import argparse
from robobrowser import RoboBrowser
from urllib.parse import unquote

parser = argparse.ArgumentParser(description='get urls of document.png from a sympli.io project')
parser.add_argument('--project_id', required=True, help='project id', metavar='<id>')
parser.add_argument('--email', required=True, help='used as login', metavar='<email>')
parser.add_argument('--password', required=True, help='used as password', metavar='<password>')
args = parser.parse_args()

browser = RoboBrowser(parser='html.parser')

browser.open('https://app.sympli.io/login/')

form = browser.get_form(id='login-form')
form['email'] = args.email
form['password'] = args.password
browser.submit_form(form)

browser.open(f'https://app.sympli.io/app#!/projects/{args.project_id}')

accessToken = unquote(browser.session.cookies['accessToken'])

browser.session.headers['authorization'] = f'Bearer {accessToken}'
browser.session.headers['referer'] = 'https://app.sympli.io/app'
browser.session.headers['authority'] = 'app.sympli.io'
browser.session.headers['x-requested-with'] = 'XMLHttpRequest'

browser.open(f'https://app.sympli.io/api/v1/bundles?limit=*&project={args.project_id}')

j = browser.response.json()

for x in j['data']:
	blobUrlPrefix = x['blobUrlPrefix']
	print(f'{blobUrlPrefix}/bundle/document.png')

