#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import traceback
from copy import deepcopy
import re
import time
from nltk.corpus import brown, words as wd
import xlsxwriter
import progressbar as pb
from math import log, ceil
from os import popen
import whois
from datetime import datetime, timedelta
import threading
import csv 
import gc
from operator import attrgetter
import signal  

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'

from django.conf import settings
from domain.models import Zone

fname = 'No Path selected'
fname2 = 'No Path selected'
file_size = 0
start_time = time.time()
word_man = ['online']
bad_keywords_list = 'aaaaaaaaaaaabbbbbbbbbasdaaasdffdsa-abbabc'


class progress_timer:
    def __init__(self, n_iter, description="Something"):
        self.n_iter = n_iter
        self.iter = 0
        self.description = description + ': '
        self.timer = None
        self.initialize()

    def initialize(self):
        widgets = [self.description, pb.Percentage(), ' ',
                   pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
        self.timer = pb.ProgressBar(widgets=widgets, maxval=self.n_iter).start()

    def update(self, q=1):
        self.timer.update(self.iter)
        self.iter += q

    def finish(self):
        self.timer.finish()


freq_words = open("words-by-frequency.txt").read().split()
wordcost = dict((k, log((i + 1) * log(len(freq_words)))) for i, k in enumerate(freq_words))
maxword = max(len(x) for x in freq_words)
freq_words = None


def infer_spaces(s):
    global maxword

    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i - maxword):i]))
        return min((c + wordcost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)

    cost = [0]
    for i in range(1, len(s) + 1):
        c, k = best_match(i)
        cost.append(c)

    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        out.append(s[i - k:i])
        i -= k

    return " ".join(reversed(out))


link = set()
words = set(list(wd.words()) + list(brown.words()) + word_man)
some_variable = 0


def fcn(domain, pt):
	global words, link, some_variable, result_list
	# for domain in new_content:     
	if domain.split(".")[1] not in ["com\n", "net\n ", "com\r\n", "net\r\n"]:
		pass
	elif len(domain) >= 60:
		pass
	else:
		keywords = []
		bad_keywords = []
		tmp = domain.split(".")[0]   
		temp = str(domain).lstrip('.')
		tmp = temp.split(".")[0]
		parts1 = [w for w in re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', tmp)]
		parts = []
		if len(parts1) <= 3:
			for part in parts1:
				temp = (infer_spaces(part).split())
				parts += (temp)
			parts_no_numbers = [x for x in parts if not x.isdigit()]
			digits = [x for x in parts if x.isdigit()]
			if len(parts_no_numbers) <= 3 and len(digits) <= 1:
				super_tmp = ''
				for part in parts_no_numbers:
				    if part not in words:
				        break
				    if len(part) > 3:
				        keywords.append(part)
				        super_tmp = tmp.replace(part, ' ')
				        tmp = deepcopy(super_tmp)
				bad_keywords = super_tmp.split()

		if len(keywords) and len(bad_keywords) == 0:
			uslov_date = False
			uslov = False
	   		try:
				whois_data = whois.query(domain.replace('\r\n', ''))
				date_created = whois_data.creation_date
				expiration_date = whois_data.expiration_date
				uslov_date = True
			except:
				pass
			if uslov_date and (date_created + timedelta(weeks=104) <= expiration_date):
				uslov = True
			if uslov:
				result_list.append({'domain': domain, 'keywords': keywords})
	pt.update()
	return 1

def fcn2(domain_dict, pt):
	global some_variable, all_domains, link	
	domain = domain_dict['domain']
	keywords = domain_dict['keywords']
	some_variable += 1		
	keywords = sorted(keywords, key=len, reverse=True)
	ready_to_write = True
	condition = True
	matched_lines = []
	for keyword in keywords:
		# if keyword not in full_content:
		#     ready_to_write = False
		#     break
		# elif len(matched_lines) == 0 and condition:
		if condition:
			# matched_lines = [line.lower() for line in all_domains if keyword in line.lower()]
			matched_lines = Zone.objects.filter(name__icontains=keyword)
			matched_lines_ids = map(attrgetter('id'), matched_lines)
			condition = False
		else:
			matched_lines = Zone.objects.filter(name__icontains=keyword, id__in=matched_lines_ids)
			if matched_lines.exists():
				matched_lines_ids = map(attrgetter('id'), matched_lines)
			else:
				break
	if matched_lines.exists() and ready_to_write:
		matched_lines = map(attrgetter('name'), matched_lines) 	
		f = open('final_response.csv', 'a')	
		for matched_domain in matched_lines:
			fields=[(domain).replace('\n', '').replace('\r', ''), (matched_domain).replace('\n', '').replace('\r', '')]
			writer = csv.writer(f)
			writer.writerow(fields)			
			link.add(matched_domain)
		f.close()					
	pt.update()
	
result_list = []
all_domains = set()

def main_filter():
	global result_list, all_domains, link
	f = open("Domains_to_sell.txt", "r")
	content = set(f.readlines())
	f.close()
	pt = progress_timer(description='phase 1: ', n_iter=len(content))
	threads = []
	for domain in content:
		t = threading.Thread(target=fcn, args=(domain, pt, ))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	content = None
	pt = None	
	gc.collect()
	print '----', len(result_list)
	# file = open("org.2014-08-25.txt", "r")
	# all_domains = set(file.readlines())	
	# file.close()

	pt2 = progress_timer(description='phase 2: ', n_iter=len(result_list))
	for result in result_list:
		fcn2(result, pt2)
	all_domains = None
	pt2 = None
	gc.collect()

	# f = open('emails.csv', 'a')
	# for data in link:
	# 	pro = popen("whois '" + str((data).replace('\n', '').replace('\r', '')) + "' | egrep -i 'Registrant Email|Admin Email'", 'r')
	# 	email = pro.read()
	# 	pro.close()
	# 	fields=[(data).replace('\n', '').replace('\r', ''), email.replace('\n', '').replace('\r', '')]
	# 	writer = csv.writer(f)
	# 	writer.writerow(fields)
	# f.close()
	# fcn2(result_list, pt2)

if __name__ == '__main__':
	main_filter()
	print '---END---', int(time.time() - start_time), some_variable

