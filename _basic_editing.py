#!/usr/bin/pypy

from Tkinter import *
import ttk
from ttk import *

from copy import deepcopy
from nltk.corpus import brown, words as wd
import progressbar as pb
from math import log, ceil, floor
import threading, re, time, thread
import csv, sys, gc, os, django
os.environ['DISPLAY'] = ':0'
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads, Log

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


def bar(tk, progress, v):
    all_globals = globals()
    value = all_globals['value']
    text = all_globals['text']
    progress['value'] = ceil(value)

    v.set(text)
    tk.update_idletasks()
    tk.update()
    tk.after(1, bar, tk, progress, v)

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


def fcn(domain_data, pt):
    global words, link, some_variable, result_list
    domain = domain_data[0]
    if domain.split(".")[1] not in ["com\n", "net\n ", "com\r\n", "net\r\n", "com", "net"]:
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
            if len(parts_no_numbers) <= 3 and len(digits) <= 0:
                super_tmp = ''
                for part in parts_no_numbers:                    
                    if part not in words:
                        if (4 < len(part) < 11) and len(parts_no_numbers) == 1:
                            keywords.append(part)
                            super_tmp = tmp.replace(part, ' ')
                            tmp = deepcopy(super_tmp)
                        else:
                            break
                    if len(part) > 3:
                        keywords.append(part)
                        super_tmp = tmp.replace(part, ' ')
                        tmp = deepcopy(super_tmp)
                bad_keywords = super_tmp.split()

        if len(keywords) and len(bad_keywords) <= 0:
            result_list.append({'domain': domain, 'keywords': keywords})
    pt.update()
    return 1


def fcn2(domain_dict, pt, all_domains, date):
    global some_variable, link, iterno
    domain = domain_dict['domain']
    keywords = domain_dict['keywords']
    some_variable += 1
    keywords = sorted(keywords, key=len, reverse=True)
    ready_to_write = True
    condition = True
    matched_lines = []
    matched_lines_copy = []
    for keyword in keywords:
        if len(matched_lines) == 0 and condition:
            matched_lines = [line.lower() for line in all_domains if keyword in line.lower()]
            matched_lines_copy = [[line.replace(keyword, ''), line.lower()] for line in matched_lines]
            condition = False
        else:
            matched_lines_copy = [line for line in matched_lines_copy if keyword in line[0]]
    matched_lines = [line[1] for line in matched_lines_copy]
    if len(matched_lines) and ready_to_write:
        for matched_domain in matched_lines:
            iterno += 1
            page = floor(iterno / 5000) + 1
            entry = RawLeads(
                name_zone=(matched_domain).replace('\n', '').replace('\r', ''),
                name_redemption=(domain).replace('\n', '').replace('\r', ''),
                date=date,
                page=page
            )
            entry.save()
    pt.update()


result_list = []
all_domains = set()
iterno = 0

def main_filter(com_path, net_path, org_path, info_path, redemption_path, date):
    global result_list, all_domains, link, value, text

    usefull_data = []
    with open(redemption_path, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
	    domain = row[0].strip('"')
            teemp = (domain, )
            usefull_data.append(teemp)
        usefull_data.pop(0)    
    Log.objects.filter(date=sys.argv[6]).update(number_of_all=len(usefull_data))
    increment = (100.0/len(usefull_data))
    text = 'phase 1 '
    pt = progress_timer(description='phase 1: ', n_iter=len(usefull_data))
    threads = []
    for domain_data in usefull_data:
        value += increment
        fcn(domain_data, pt)
        # t = threading.Thread(target=fcn, args=(domain_data, pt))
        # threads.append(t)
        # t.start()
    # for t in threads:
    #     t.join()    
    Log.objects.filter(date=sys.argv[6]).update(number_of_redemption=len(result_list))
    usefull_data = None
    pt = None
    gc.collect()
    print '\n'

    threads = []
    if org_path:
        file = open(org_path, "r")
        all_domains = set(file.readlines())
        file.close()
        pt2 = progress_timer(description='phase 2: ', n_iter=len(result_list))
        increment = (100.0/len(result_list))
        value = 0
        text = 'phase 2 '
        for result in result_list:
            fcn2(result, pt2, all_domains, date)
            value += increment
            #t = threading.Thread(target=fcn2, args=(result, pt2, all_domains))
            #threads.append(t)
            #t.start()
        gc.collect()
        print '\n'
    else:
        print 'skipping phase 2...\n'

    if net_path:
        file = open(net_path, "r")
        all_domains = set(file.readlines())
        file.close()
        pt2 = progress_timer(description='phase 3: ', n_iter=len(result_list))
        for result in result_list:
            fcn2(result, pt2, all_domains, date)
            # t = threading.Thread(target=fcn2, args=(result, pt2, all_domains))
            # threads.append(t)
            # t.start()
        gc.collect()
        print '\n'
    else:
        print 'skipping phase 3...\n'

    if info_path:
        file = open(info_path, "r")
        all_domains = set(file.readlines())
        file.close()
        pt2 = progress_timer(description='phase 4: ', n_iter=len(result_list))
        for result in result_list:
            fcn2(result, pt2, all_domains, date)
            # t = threading.Thread(target=fcn2, args=(result, pt2, all_domains))
            # threads.append(t)
            # t.start()
        all_domains = None
        pt2 = None
        gc.collect()
        print '\n'
    else:
        print 'skipping phase 4...\n'

    if com_path:
        file = open(com_path, "r")
        all_domains = set(file.readlines())
        file.close()
        pt2 = progress_timer(description='phase 5: ', n_iter=len(result_list))
        for result in result_list:
            fcn2(result, pt2, all_domains, date)
            # t = threading.Thread(target=fcn2, args=(result, pt2, all_domains))
            # threads.append(t)
            # t.start()

        all_domains = None
        pt2 = None
        gc.collect()
        print '\n'
    else:
        print 'skipping phase 5...\n'


def threadmain():
    global value
    tk = Tk()
    progress = Progressbar(tk, orient=HORIZONTAL, length=100, mode='determinate')
    v = StringVar()
    Label(tk, textvariable=v).pack()
    progress.pack()
    tk.after(1, bar, tk, progress, v)
    tk.mainloop()


if __name__ == '__main__':
    value = 0.0
    text = ''
    # try:
    #     thread.start_new_thread(threadmain, ())
    # except:
    # 	  pass
    if not Log.objects.filter(date=sys.argv[6]).exists():
        entry = Log(date=sys.argv[6])
        entry.save()
    main_filter(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    duration = int(time.time() - start_time)
    Log.objects.filter(date=sys.argv[6]).update(duration=duration)
