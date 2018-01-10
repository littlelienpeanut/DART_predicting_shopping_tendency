import pymysql
import time
import json
import datetime
import requests
import csv
import re
import pandas as pd
import numpy as np
from datetime import date

global __UserList__
global __UserDict__

#DART01 server
def connection(id):
    connection = pymysql.connect(host='',
                                 port=,
                                 user='',
                                 password='',
                                 db='people400',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor
                                 )

    cursor = connection.cursor()
    sql = "SELECT history.id, history.visit_time, history.title, history.domain FROM history " + "WHERE history.id='" + id + "'" + "ORDER BY history.id ASC, history.visit_time ASC "
    print(sql)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    except:
        print("fetch error")

    connection.close()

def parse_ymd ( s ):
    s = s[0:10]
    year_s ,  mon_s ,  day_s  =  s . split ( '-' )
    total = year_s + mon_s + day_s
    return  int(total)

def count_days(min_date, max_date):
    year1_s = min_date / 10000
    mon1_s = min_date % 10000 / 100
    day1_s = min_date % 100
    year2_s = max_date / 10000
    mon2_s = max_date % 10000 / 100
    day2_s = max_date % 100

    d1 = date(int(year1_s), int(mon1_s), int(day1_s))
    d2 = date(int(year2_s), int(mon2_s), int(day2_s))

    total = (d2 - d1).days
    return total

def getCategory(uri):
    """ return: empty str '' => failed to get category
        PS: "Unclassified" is valid (returned by FortiGuard)
    """
    API = 'http://www.fortiguard.com/webfilter?q='
    cat = ''
    try:
        # import requests
        r = requests.get(API + uri, timeout=60)
        # print r.content[:200]
        # print len(r.content)
        html = r.content

        # import re
        result = re.search(b'Category:(.*)" />', html)  # previous version
        if result is None:  # 2nd chance
            result = re.search(b':(.*)</h4>', html)  # since 2015-08-31

        cat = result.group(1).strip()

    except:  # more exceptions & errors -- ref: http://docs.python-requests.org/en/latest/user/quickstart/
        #print "getCategory error: " + uri
        import traceback
        traceback.print_exc()
        # f = open('e:\\tmp\\error.html', 'w+')
        # f.write(uri + ":\n" + html)
        # f.close()


    ## based on urllib2:
    ## Q: why not urllib2? (http://stackoverflow.com/questions/2018026/should-i-use-urllib-or-urllib2-or-requests)
    #     try:
    #         # import urllib2
    #         response = urllib2.urlopen(API+uri)
    #         html = response.read()  # print html
    #         # print html[:200]
    #         print len(html)
    #
    #         # import re
    #         result = re.search('Category:(.*)</h3> <a', html)
    #         cat = result.group(1).strip()
    #     except AttributeError:
    #         print "Invalid Response: " + uri
    #         print html[:1000]
    # #            f = open('e:\\tmp\\error.html', 'w+')
    # #            f.write(uri+":\n" + html)
    # #            f.close()
    #     except httplib.BadStatusLine:
    #         print "BadStatusLine(httplib): " + uri
    #     except: # e.g. URLError
    #         print "more getCategory error: " + uri
    #         import traceback
    #         traceback.print_exc()

    # if cat is None or cat == 'Unclassified':
    if cat is None:
        cat = ''

    # cat = 'TEST'

    #print "getCategory: " + uri + ":" + cat
    if len(cat) > 50:
        # raise ValueError
        print("getCategory warning: len(cat) > 50 -- " + cat)
        # cat = ''
    return cat

def load_csv():
    data = pd.read_csv('webcat_merge_utf8.csv')
    __cate__ = {}
    for i in range(0, len(data), 1):
        __cate__[data['uri'][i]] = data['cat'][i]
    return __cate__

def load_json():
    global __UserList__
    global __UserDict__

    with open("./user_list.json", mode='r') as json_data:
        jdata = json.load(json_data, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)
        __UserList__ = json.loads(jdata, object_hook=None);


    print("50%")

    with open("./user_dict.json", mode='r') as json_udict:
        judictdata = json.load(json_udict, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)
        __UserDict__ = json.loads(judictdata, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)

def choose_id():

    global __UserList__
    global __UserDict__
    count = 0
    count_30 = 0
    user_time = []
    user_time_30up = []
    user_time_30up_id = []
    for j in range(0, len(__UserList__)):
        for i in range(0, len(__UserDict__[__UserList__[j]]["history"])):
            user_time.append(parse_ymd(__UserDict__[__UserList__[j]]["history"][i]["visit_time"]))
        min_time = min(user_time)
        max_time = max(user_time)
        range_of_days = count_days(min_time, max_time)

        count = count + 1

        if range_of_days >= 90 and len(__UserDict__[__UserList__[j]]["history"]) > 1000 :
            user_time_30up.append(__UserList__[j])
            user_time_30up_id.append(j+1)
            count_30 = count_30 + 1
        user_time[:] = []

    print("TOTAL USERS #: " + str(count))
    print("OVER 90 DAYS AND OVER 1000 history :" + str(count_30))

    return user_time_30up_id

def main():
    #variable

    global __UserList__
    count = 1
    choose_id_list = []
    __cate__ = {}
    cate_result = {}
    visit_time_tmp = []
    title_tmp = []
    title = []
    visit_time = []
    csv_index = 0

    print("Loading json db...")
    load_json()
    print("Loading complete")
    print("----------------------------------------")
    print("Creating user id list...")
    #choose_id_list = choose_id()
    print("Total users # = " + str(len(__UserList__)))
    for i in range(len(__UserList__)):
        print(__UserList__[i])
        choose_id_list.append(__UserList__[i])
    print("----------------------------------------")
    print("CSV file loading...")
    __cate__ = load_csv()

    for k in range(len(__UserList__)):
        print("Fetching user: " + str(k+1))
        print("Database connecting...")
        result = connection(choose_id_list[k])
        #result = connection('0000068fb609ce34cdf6c12648f8ee53')
        print("Connecting complete")
        print("Start fetching")
        for i in range(0, len(result), 1):

            print("User: " + str(k+1) + " " + str(i) + "/" + str(len(result)))
            #print("User: " + str(i) + " history: " + str(j))
            tdict = {}
            tmp_id = result[i]['id'].encode('UTF-8')
            tmptext = result[i]['domain'].encode('UTF-8')
            tmptext = str(tmptext)
            #print("domain: " + tmptext)
            #tmptext = __UserDict__[__UserList__[choose_id_list[i]]]["history"][j]["domain"]
            #visit_time_tmp = __UserDict__[__UserList__[choose_id_list[i]]]["history"][j]["visit_time"][0:10]
            visit_time_tmp = result[i]['visit_time'].strftime("%Y-%m-%d")
            title_tmp = result[i]['title'].encode('UTF-8')

            tdict.update({'id':tmp_id})
            tdict.update({'visit_time':visit_time_tmp})
            tdict.update({'title':title_tmp})
            tdict.update({"domain":tmptext})
            if tmptext in __cate__:
                tdict.update({'cate':__cate__[tmptext]})
                cate_result.update({csv_index:tdict})
                csv_index = csv_index + 1

            else :
                print("strange domain")
                tmp_cate = getCategory(tmptext)
                tmp_cate = str(tmp_cate)
                tdict.update({'cate':tmp_cate})
                cate_result.update({csv_index:tdict})
                __cate__[tmptext] = tmp_cate
                csv_index = csv_index + 1

        print("Fetching complete")
        print("")
        if k % 51 == 50:

            with open('history_all_detail_' + str(count) +'.csv','w') as f:
                wr = csv.writer(f)
                for i in cate_result:
                    values = []
                    values.append(str(cate_result[i]['id'])[2:-1])
                    values.append(cate_result[i]['visit_time'])
                    values.append(cate_result[i]['domain'])
                    values.append(cate_result[i]['title'])
                    values.append(cate_result[i]['cate'])
                    print(values)
                    wr.writerow(values)
                count = count + 1
                cate_result = {}
                csv_index = 0



if __name__ == '__main__':
    main()
