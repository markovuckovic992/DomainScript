#!/usr/bin/pypy
import requests
requests.adapters.DEFAULT_RETRIES = 3
from os import popen
from copy import deepcopy
from nltk.corpus import brown, words as wd, cess_esp as cess, udhr
import progressbar as pb
from math import log, ceil, floor
import threading, re, time, thread
import csv, sys, gc, os, django, hashlib
from django.db import connection
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
import binascii
from domain.models import RawLeads, Log, AllHash, Setting, Tlds

master_data = []
fname = 'No Path selected'
fname2 = 'No Path selected'
file_size = 0
start_time = time.time()
word_man = ['online']

bad_keywords_list = 'aaaaaaaaaaaabbbbbbbbbasdaaasdffdsa-abbabc'

# SETTINGS!
sett = Setting.objects.get(id=1)
com_net = sett.com_net  # 0 com, 1 net, 2 both
length = sett.length
number_of_digits = sett.number_of_digits
number_of_keywords = sett.number_of_keywords
allow_bad_keywords = sett.allow_bad_keywords
min_length = sett.min_length
max_length = sett.max_length
redempion_row = sett.redempion_row - 1
# END!
# TLDs
tlds = []
TLDS = Tlds.objects.all()
for TLD in TLDS:
    tlds.append(TLD.extension)
# end
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

freq_words = open("merged.txt").read().split()
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
words = set(list(wd.words()) + list(brown.words()) + word_man + list(udhr.words()) + list(cess.words()))
some_variable = 0

def fcn(domain_data, pt):
    list_no = domain_data[1]
    forbids = ['[', '`', '\\', '-', '=', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '\\', '[', '\\', ']', '{', '}', ';', "'", '\\', ':', '"', '|', '<', ',', '.', '/', '<', '>', '?', ']']
    file = open('filtered_domains.txt', 'a')
    global words, link, some_variable, result_list, result_list_b
    domain = domain_data[0]
    inter = list(set(forbids) & set(domain.split(".")[0]))
    # FILTER 1
    allowed_extensions = ["com\n", "com", "com\r\n", "net\n ", "net\r\n", "net"]
    if com_net == 1:
        allowed_extensions = allowed_extensions[3:]
    elif com_net == 0:
        allowed_extensions = allowed_extensions[:3]
    # END FILTER 1
    if len(inter) > 0 or "." not in domain:
        pass
    elif domain.split(".")[1] not in allowed_extensions:
        pass
    elif len(domain) >= length:
        pass
    elif sum(char.isdigit() for char in domain) > number_of_digits:
        pass
    else:
        keywords = []
        bad_keywords = []
        tmp = domain.split(".")[0]
        temp = str(domain).lstrip('.')
        tmp = temp.split(".")[0]
        parts1 = [w for w in re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', tmp)]
        parts = []
        if len(parts1) <= number_of_keywords:
            for part in parts1:
                temp = (infer_spaces(part).split())
                parts += (temp)
            parts_no_numbers = [x for x in parts if not x.isdigit()]
            digits = [x for x in parts if x.isdigit()]
            if len(parts_no_numbers) <= number_of_keywords and len(digits) <= 0:
                super_tmp = ''
                for part in parts_no_numbers:
                    if part not in words:
                        break
                    elif len(part) > 3:
                        keywords.append(part)
                        super_tmp = tmp.replace(part, ' ')
                        tmp = deepcopy(super_tmp)
                bad_keywords = super_tmp.split()

        if len(keywords) and len(bad_keywords) <= 0:
            result_list.append({'domain': domain, 'keywords': keywords, 'list_no': list_no})
            file.write(str({'domain': domain, 'keywords': keywords}) + '\n')
        elif allow_bad_keywords:
            domain = domain_data[0]
            if domain.split(".")[1] not in ["com\n", "com\r\n", "com"]:
                pass
            else:
                tmp = domain.split(".")[0]
                temp = str(domain).lstrip('.')
                tmp = temp.split(".")[0]

                if (min_length < len(tmp) < max_length):
                    result_list_b.append({'domain': domain, 'keywords': [tmp], 'list_no': list_no})
                    file.write(str({'domain': domain, 'keywords': [tmp]}) + '\n')
    pt.update()


def fcn2(domain_dict, pt, path, date):
    global some_variable, link, iterno1, iterno2, iterno3, master_data
    domain = domain_dict['domain']
    keywords = domain_dict['keywords']
    some_variable += 1
    keywords = sorted(keywords, key=len, reverse=True)
    ready_to_write = True
    condition = True
    matched_lines = []
    matched_lines_copy = []

    # searching = ''
    # for keyword in keywords:
    #     searching += ' ' + keyword

    tube = popen('./getLines.sh ' + path + ' ' + keywords[0])
    matched_lines = tube.read().split()
    tube.close()
    matched_lines_copy = [[line.lower().replace(keywords[0], ''), line.lower()] for line in matched_lines]

    for keyword in keywords[1:]:
        matched_lines_copy = [line for line in matched_lines_copy if keyword in line[0]]

    matched_lines = [line[1] for line in matched_lines_copy]
    if len(matched_lines) and ready_to_write:
        for matched_domain in matched_lines:
            if (matched_domain).replace('\n', '').replace('\r', '') != (domain).replace('\n', '').replace('\r', ''):
                try:
                    base1 = matched_domain.split(".", 1)[0]
                    base2 = domain.split(".", 1)[0]
                    if '.com' in domain and base1 == base2 and '.com' not in matched_domain:
                        activated = 1
                    else:
                        activated = 0
                except:
                    activated = 0

                matched_domains = [matched_domain, ]
                activateds = [activated, ]

                if activated == 0:
                    if domain_dict['list_no'] == 1:
                        iterno1 += 1
                        page = floor(iterno1 / 5000) + 1
                    elif domain_dict['list_no'] == 2:
                        iterno2 += 1
                        page = floor(iterno2 / 5000) + 1
                    elif domain_dict['list_no'] == 3:
                        iterno3 += 1
                        page = floor(iterno3 / 5000) + 1
                else:
                    page = 1
                    # TLDs
                    for tld in tlds:
                        try:
                            base2 = domain.split(".", 1)[0]
                            request = requests.get('http://www.' + base2 + '.' + tld)
                            if request.status_code == 200:
                                matched_domains.append(base2 + '.' + tld)
                                activateds.append(2)
                        except:
                            pass

                indx = 0
                for matched_domain in matched_domains:
                    master_data.append({
                        "name_zone": (matched_domain).replace('\n', '').replace('\r', ''),
                        "name_redemption": (domain).replace('\n', '').replace('\r', ''),
                        "date": date,
                        "page": page,
                        "activated": activateds[indx],
                        "list_no": domain_dict['list_no']
                    })
                    indx += 1

    pt.update()


def fcn3(domain_dict, pt, path, date):
    global some_variable, link, iterno1, iterno2, iterno3, master_data
    domain = domain_dict['domain']
    keyword = domain_dict['keywords'][0]
    some_variable += 1
    ready_to_write = True
    condition = True
    matched_lines = []
    matched_lines_copy = []

    if len(matched_lines) == 0 and condition:
        tube = popen('./getLines.sh ' + path + ' ' + keyword)
        matched_lines_tmp = tube.read().split()
        tube.close()
        for line in matched_lines_tmp:
            if line.lower().startswith(keyword) or line.lower().endswith(keyword):
                matched_lines.append(line.lower())
        matched_lines_copy = [[line.lower().replace(keyword, ''), line.lower()] for line in matched_lines]
        condition = False
    else:
        matched_lines_copy = [line for line in matched_lines_copy if line[0].startswith(keyword) or line[0].endswith(keyword)]

    matched_lines = [line[1] for line in matched_lines_copy]
    if len(matched_lines) and ready_to_write:
        for matched_domain in matched_lines:
            if (matched_domain).replace('\n', '').replace('\r', '') != (domain).replace('\n', '').replace('\r', ''):
                try:
                    base1 = matched_domain.split(".", 1)[0]
                    base2 = domain.split(".", 1)[0]
                    if '.com' in domain and base1 == base2 and '.com' not in matched_domain:
                        activated = 1
                    else:
                        activated = 0
                except:
                    activated = 0

                matched_domains = [matched_domain, ]
                activateds = [activated, ]

                if activated == 0:
                    if domain_dict['list_no'] == 1:
                        iterno1 += 1
                        page = floor(iterno1 / 5000) + 1
                    elif domain_dict['list_no'] == 2:
                        iterno2 += 1
                        page = floor(iterno2 / 5000) + 1
                    elif domain_dict['list_no'] == 3:
                        iterno3 += 1
                        page = floor(iterno3 / 5000) + 1
                else:
                    page = 1
                    # TLDs
                    for tld in tlds:
                        try:
                            base2 = domain.split(".", 1)[0]
                            request = requests.get('http://www.' + base2 + '.' + tld)
                            if request.status_code == 200:
                                matched_domains.append(base2 + '.' + tld)
                                activateds.append(2)
                        except:
                            pass

                indx = 0
                for matched_domain in matched_domains:
                    master_data.append({
                        "name_zone": (matched_domain).replace('\n', '').replace('\r', ''),
                        "name_redemption": (domain).replace('\n', '').replace('\r', ''),
                        "date": date,
                        "page": page,
                        "activated": activateds[indx],
                        "list_no": domain_dict['list_no']
                    })
                    indx += 1

    pt.update()

def saveDate(master_data):
    cursor = connection.cursor()
    for data in master_data:
        entry = RawLeads(
            name_zone=data['name_zone'],
            name_redemption=data['name_redemption'],
            date=data['date'],
            page=data['page'],
            activated=data['activated'],
            list_no=data['list_no']
        )
        entry.save()

        hash = hashlib.md5()
        hash.update(str(entry.id))
        hash_base_id = hash.hexdigest()

        while AllHash.objects.filter(hash_base_id=hash_base_id).exists():
            hash_base_id = binascii.hexlify(os.urandom(16))

        new_entry = AllHash(hash_base_id=hash_base_id)
        new_entry.save()

        entry.hash_base_id = hash_base_id
        entry.save()
        time.sleep(0.05)

    cursor.execute("COMMIT;")

result_list = []
result_list_b = []
all_domains = set()
iterno1 = -1
iterno2 = -1
iterno3 = -1

def main_filter(com_path, net_path, org_path, info_path, us_path, e1_path, e2_path, e3_path, e4_path, redemption_path, r2, r3, date):
    global result_list, result_list_b, all_domains, link, master_data

    file = open('filtered_domains.txt', 'a')
    file.truncate()
    file.close()

    usefull_data = []
    with open(redemption_path, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            domain = row[redempion_row].strip('"').lower()
            teemp = (domain, 1)
            usefull_data.append(teemp)

    if r2 and r2 != 'none':
        with open(r2, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                domain = row[redempion_row].strip('"').lower()
                teemp = (domain, 2)
                usefull_data.append(teemp)

    if r3 and r3 != 'none':
        with open(r3, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                domain = row[redempion_row].strip('"').lower()
                teemp = (domain, 3)
                usefull_data.append(teemp)

    l = Log.objects.get(date=date)
    l.number_of_all = len(usefull_data)
    l.save()

    increment = (100.0 / len(usefull_data))
    text = 'phase 1 '
    pt = progress_timer(description='phase 1: ', n_iter=len(usefull_data))
    threads = []
    for domain_data in usefull_data:
        fcn(domain_data, pt)
    l = Log.objects.get(date=date)
    l.number_of_redemption = len(result_list + result_list_b)
    l.save()

    usefull_data = None
    pt = None
    gc.collect()

    if org_path and org_path != 'none':
        pt2 = progress_timer(description='phase 2: ', n_iter=len(result_list + result_list_b))
        for result in result_list:
            fcn2(result, pt2, org_path, date)
        for result in result_list_b:
            fcn3(result, pt2, org_path, date)

        saveDate(master_data)
        master_data = []
        pt2 = None
        gc.collect()
    else:
        pass

    if net_path and net_path != 'none':
        pt2 = progress_timer(description='phase 3: ', n_iter=len(result_list + result_list_b))
        for result in result_list:
            fcn2(result, pt2, net_path, date)
        for result in result_list_b:
            fcn3(result, pt2, net_path, date)

        saveDate(master_data)
        master_data = []
        pt2 = None
        gc.collect()
    else:
        pass

    if info_path and info_path != 'none':
        pt2 = progress_timer(description='phase 4: ', n_iter=len(result_list + result_list_b))
        for result in result_list:
            fcn2(result, pt2, info_path, date)
        for result in result_list_b:
            fcn3(result, pt2, info_path, date)

        saveDate(master_data)
        master_data = []
        pt2 = None
        gc.collect()
    else:
        pass

    if com_path and com_path != 'none':
        pt2 = progress_timer(description='phase 5: ', n_iter=len(result_list + result_list_b))
        for result in result_list:
            fcn2(result, pt2, com_path, date)
        for result in result_list_b:
            fcn3(result, pt2, com_path, date)

        saveDate(master_data)
        master_data = []
        pt2 = None
        gc.collect()
    else:
        pass

    if us_path and us_path != 'none':
        pt2 = progress_timer(description='phase 6: ', n_iter=len(result_list + result_list_b))
        for result in result_list:
            fcn2(result, pt2, us_path, date)
        for result in result_list_b:
            fcn3(result, pt2, us_path, date)

        saveDate(master_data)
        master_data = []
        pt2 = None
        gc.collect()
    else:
        pass

    if e1_path and e1_path != 'none':
        pt2 = progress_timer(description='phase 7: ', n_iter=len(result_list + result_list_b))
        for result in result_list:
            fcn2(result, pt2, e1_path, date)
        for result in result_list_b:
            fcn3(result, pt2, e1_path, date)

        saveDate(master_data)
        master_data = []
        pt2 = None
        gc.collect()
    else:
        pass

    if e2_path and e2_path != 'none':
        pt2 = progress_timer(description='phase 8: ', n_iter=len(result_list + result_list_b))
        for result in result_list:
            fcn2(result, pt2, e2_path, date)
        for result in result_list_b:
            fcn3(result, pt2, e2_path, date)

        saveDate(master_data)
        master_data = []
        pt2 = None
        gc.collect()
    else:
        pass

    if e3_path and e3_path != 'none':
        pt2 = progress_timer(description='phase 9: ', n_iter=len(result_list + result_list_b))
        for result in result_list:
            fcn2(result, pt2, e3_path, date)
        for result in result_list_b:
            fcn3(result, pt2, e3_path, date)

        saveDate(master_data)
        master_data = []
        pt2 = None
        gc.collect()
    else:
        pass

    if e4_path and e4_path != 'none':
        pt2 = progress_timer(description='phase 10: ', n_iter=len(result_list + result_list_b))
        for result in result_list:
            fcn2(result, pt2, e4_path, date)
        for result in result_list_b:
            fcn3(result, pt2, e4_path, date)

        saveDate(master_data)
        master_data = []
        pt2 = None
        gc.collect()
    else:
        pass

if __name__ == '__main__':
    if not Log.objects.filter(date=sys.argv[13]).exists():
        entry = Log(date=sys.argv[13])
        entry.save()
    main_filter(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        sys.argv[4],
        sys.argv[5],
        sys.argv[6],
        sys.argv[7],
        sys.argv[8],
        sys.argv[9],
        sys.argv[10],
        sys.argv[11],
        sys.argv[12],
        sys.argv[13],
    )
    duration = int(time.time() - start_time)

    l = Log.objects.get(date=sys.argv[13])
    l.duration = duration
    l.save()
