# -*- coding: UTF-8 -*-

import csv
import pandas as pd
import time
import datetime
from datetime import date
from collections import Counter
import pymysql
import operator

def load_csv():
    data = []
    title = ["Abortion", "Advocacy Organizations", "Alcohol", "Alternative Beliefs", "Dating", "Gambling", "Lingerie and Swimsuit", "Marijuana" , "Nudity and Risque", "Other Adult Materials", "Pornography", "Sex Education", "Sports Hunting and War Games", "Tobacco", "Weapons (Sales)", "File Sharing and Storage", "Freeware and Software Downloads", "Internet Radio and TV", "Internet Telephony", "Peer-to-peer File Sharing", "Streaming Media and Download", "Armed Forces", "Business", "Finance and Banking", "General Organizations", "Government and Legal Organizations", "Information Technology", "Information and Computer Security", "Search Engines and Portals", "Secure Websites", "Web Hosting", "Web-based Applications", "Advertising" "Arts and Culture", "Auction", "Brokerage and Trading", "Child Education", "Content Servers", "Digital Postcards", "Domain Parking", "Dynamic Content", "Education", "Entertainment", "Folklore", "Games", "Global Religion", "Health and Wellness", "Instant Messaging", "Job Search", "Meaningless Content", "Medicine", "News and Media", "Newsgroups and Message Boards", "Personal Privacy", "Personal Vehicles", "Personal Websites and Blogs", "Political Organizations", "Real Estate", "Reference", "Restaurant and Dining", "Shopping", "Social Networking", "Society and Lifestyles", "Sports", "Travel", "Web Chat", "Web-based Email", "Child Abuse", "Discrimination", "Drug Abuse", "Explicit Violence", "Extremist Groups", "Hacking", "Illegal or Unethical", "Plagiarism", "Proxy Avoidance", "Dynamic DNS", "Malicious Websites", "Phishing", "Spam URLs", "Unclassified", "Shopping and Auction", "Arts and Culture", "Not Rated", "Freeware Downloads"]
    csv = pd.read_csv("history_day_cat_10.csv")
    for i in range(0, len(csv), 1):
        tdict = {}
        tdict.update({"id":csv["id"][i]})
        tdict.update({"date":csv["visit_time"][i]})
        for cate in title:
            tdict.update({cate:csv[cate][i]})
        data.append(tdict)
    return data

def load_1460():
    #get id list
    data = []
    csv = pd.read_csv("user_14_60_10.csv")
    now_id = csv["id"][0]
    data.append(now_id)
    for i in range(0, len(csv)-2, 2):
        if now_id != csv["id"][i] and csv["1st_prop"][i] != 0 and csv["1st_prop"][i+1] != 0:
            now_id = csv["id"][i]
            data.append(now_id)

    return data

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
    sql = "SELECT bday, gender, marr FROM user_detail WHERE id=" + "'" + id + "'"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    except:
        print("fetch error")

    connection.close()

def tr_gender(input):
    dict = {'1': 'Male', '2': 'Female','3': 'Other'}
    return dict[input]

def tr_mar(input):
    dict = {'1':'Single', '2':'Couple','3':'Married','4':'Other','5':'Other'}
    return dict[input]

def count_days(next_date, now_date):
    next_year_s,  next_mon_s,  next_day_s  =  next_date.split('-')
    now_year_s,  now_mon_s,  now_day_s  =  now_date.split('-')
    now_d = date(int(now_year_s), int(now_mon_s), int(now_day_s))
    next_d = date(int(next_year_s), int(next_mon_s), int(next_day_s))
    total =  (next_d - now_d).days
    #total += 1
    return total

def value_add(dict1, dict2):
    title = ["Abortion", "Advocacy Organizations", "Alcohol", "Alternative Beliefs", "Dating", "Gambling", "Lingerie and Swimsuit", "Marijuana" , "Nudity and Risque", "Other Adult Materials", "Pornography", "Sex Education", "Sports Hunting and War Games", "Tobacco", "Weapons (Sales)", "File Sharing and Storage", "Freeware and Software Downloads", "Internet Radio and TV", "Internet Telephony", "Peer-to-peer File Sharing", "Streaming Media and Download", "Armed Forces", "Business", "Finance and Banking", "General Organizations", "Government and Legal Organizations", "Information Technology", "Information and Computer Security", "Search Engines and Portals", "Secure Websites", "Web Hosting", "Web-based Applications", "Advertising" "Arts and Culture", "Auction", "Brokerage and Trading", "Child Education", "Content Servers", "Digital Postcards", "Domain Parking", "Dynamic Content", "Education", "Entertainment", "Folklore", "Games", "Global Religion", "Health and Wellness", "Instant Messaging", "Job Search", "Meaningless Content", "Medicine", "News and Media", "Newsgroups and Message Boards", "Personal Privacy", "Personal Vehicles", "Personal Websites and Blogs", "Political Organizations", "Real Estate", "Reference", "Restaurant and Dining", "Shopping", "Social Networking", "Society and Lifestyles", "Sports", "Travel", "Web Chat", "Web-based Email", "Child Abuse", "Discrimination", "Drug Abuse", "Explicit Violence", "Extremist Groups", "Hacking", "Illegal or Unethical", "Plagiarism", "Proxy Avoidance", "Dynamic DNS", "Malicious Websites", "Phishing", "Spam URLs", "Unclassified", "Shopping and Auction", "Arts and Culture", "Not Rated", "Freeware Downloads"]
    tdict = {}

    if dict2 == None:
        return dict1

    for cate in title:
        tmp = 0
        tmp = dict1[cate] + dict2[cate]
        tdict.update({cate:tmp})

    tdict.update({"id":dict1["id"]})
    tdict.update({"date":dict1["date"]})

    return tdict


def main():
    #variable

    title = ['Illegal or Unethical', 'Job Search', 'Finance and Banking', 'Alcohol', 'Entertainment', 'Nudity and Risque', 'Sports', 'Travel', 'Ref erence', 'Malicious Websites', 'Marijuana', 'Medicine', 'Child Abuse', 'Phishing', 'Sports Hunting and War Games', 'Gambling', 'Dating' , 'News and Media', 'Streaming Media and Download', 'Restaurant and Dining', 'Shopping', 'Health and Wellness', 'AdvertisingArts and Cu lture', 'Weapons (Sales)', 'Internet Radio and TV', 'Explicit Violence', 'Drug Abuse', 'Extremist Groups', 'Dynamic DNS', 'Meaningless Content', 'Government and Legal Organizations', 'General Organizations', 'Personal Vehicles', 'Web-based Applications', 'Not Rated', 'I nformation Technology', 'Folklore', 'Information and Computer Security', 'Advocacy Organizations', 'Freeware and Software Downloads', ' Shopping and Auction', 'Sex Education', 'Alternative Beliefs', 'Spam URLs', 'Tobacco', 'Auction', 'Web Chat', 'Domain Parking', 'Aborti on', 'Global Religion', 'Web Hosting', 'Unclassified', 'Digital Postcards', 'Games', 'Society and Lifestyles', 'Discrimination', 'Inter net Telephony', 'Hacking', 'Newsgroups and Message Boards', 'Social Networking', 'Lingerie and Swimsuit', 'Armed Forces', 'Personal Web sites and Blogs', 'Arts and Culture', 'Proxy Avoidance', 'Business', 'Political Organizations', 'Child Education', 'Content Servers', ' Instant Messaging', 'File Sharing and Storage', 'Brokerage and Trading', 'Plagiarism', 'Personal Privacy', 'Search Engines and Portals' , 'Secure Websites', 'Other Adult Materials', 'Peer-to-peer File Sharing', 'Real Estate', 'Pornography', 'Education', 'Dynamic Content' , 'Freeware Downloads', 'Web-based Email']
    now_date = 0
    now_id = 0
    i = 0
    next_date = 0
    out_put = []


    #main

    print("csv file loading")
    data = load_csv()
    id_list = load_1460()
    print("loading complete")
    """test"""
    print(id_list)
    """test"""
    while i < len(data):

        tdict = {}
        tmp_cate = {}

        #first time
        if now_id == 0:
            now_date = data[i]["date"]
            now_id = data[i]["id"]
            tdict.update({"id":data[i]["id"]})
            tdict.update({"date":data[i]["date"]})
            for cate in title:
                tdict.update({cate:data[i][cate]})

        #id changed
        elif now_id != data[i]["id"]:
            now_id = data[i]["id"]
            now_date = data[i]["date"]
            tdict.update({"id":data[i]["id"]})
            tdict.update({"date":data[i]["date"]})
            for cate in title:
                tdict.update({cate:data[i][cate]})

        else:
            #id is the same
            if now_id == data[i]["id"]:
                next_date = data[i]["date"]
                if count_days(next_date, now_date) > 7:

                    now_date = data[i]["date"]
                    tdict.update({"id":now_id})
                    tdict.update({"date":now_date})
                    for cate in title:
                        tdict.update({cate:data[i][cate]})
                    out_put.append(tdict)

                else:

                    for j in range(0, 7, 1):

                        if j == 0:
                            if i == 1:
                                tdict = value_add(data[0], None)


                            else:
                                tdict = {}
                                tdict = value_add(data[i], None)


                        if i+j+1 > len(data):
                            i = i + j - 1
                            break

                        elif now_id == data[i+j]["id"]:
                            if count_days(data[i+j]["date"], now_date) <= 7:
                                #count
                                tdict = value_add(tdict, data[i+j])

                                if i+j+1 == len(data):
                                    out_put.append(tdict)
                                    break


                            else:
                                tdict.update({"id":now_id})
                                tdict.update({"date":now_date})
                                out_put.append(tdict)
                                now_id = data[i+j]["id"]
                                now_date = data[i+j]["date"]
                                i = i + j - 1
                                break

                        else:
                            now_id = data[i+j]["id"]
                            now_date = data[i+j]["date"]
                            tdict.update({"id":now_id})
                            tdict.update({"date":now_date})
                            out_put.append(tdict)
                            i = i + j - 1
                            break

        i += 1

    with open("7days_cate_Xmas_10.csv","w") as f:
        wr = csv.writer(f)
        tmp_title = ["id", "bday", "gender", "marr", "date", "1st", "1st_prop", "2nd", "2nd_prop", "3rd",  "3rd_prop", "4th",  "4th_prop", "5th",  "5th_prop", "Shopping", "Shopping_prop"]
        row_sum = []
        wr.writerow(tmp_title)
        now_id = 0
        bgm = []

        for i in range(0, len(out_put), 1):

            #if this user is in the id_list
            if out_put[i]["id"] in id_list:
                if now_id == 0:
                    bgm = []
                    now_id = out_put[i]["id"]
                    tmp_bgm = connection(now_id)
                    if not tmp_bgm:
                        bday = "0000/00/00"
                        gender = "3"
                        mar = "4"
                    else:
                        bday = tmp_bgm[0]["bday"]
                        gender = tmp_bgm[0]["gender"]
                        mar = tmp_bgm[0]["marr"]

                sum = 0.0
                tmp_out_put = {}
                tmp_out_put.update(out_put[i])
                del tmp_out_put["id"]
                del tmp_out_put["date"]

                value = []
                value.append(out_put[i]["id"])

                if now_id != out_put[i]["id"]:
                    bgm = []
                    now_id = out_put[i]["id"]
                    tmp_bgm = connection(now_id)
                    if not tmp_bgm:
                        bday = "0000/00/00"
                        gender = "3"
                        mar = "4"
                    else:
                        bday = tmp_bgm[0]["bday"]
                        gender = tmp_bgm[0]["gender"]
                        mar = tmp_bgm[0]["marr"]

                value.append(bday)
                gen = tr_gender(str(gender))
                ma = tr_mar(str(mar))
                value.append(gen)
                value.append(ma)
                value.append(out_put[i]["date"])

                for cate in title:
                    tmp_out_put.update({cate:out_put[i][cate]})
                    sum = sum + out_put[i][cate]

                shopping = tmp_out_put[" Shopping and Auction"] + tmp_out_put["Shopping"] + tmp_out_put["Auction"]
                del tmp_out_put[" Shopping and Auction"]
                del tmp_out_put["Shopping"]
                del tmp_out_put["Auction"]
                tmp_out_put.update({"Shopping":shopping})


                #1st
                tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                value.append(tmp_cate)
                tmp_prob = tmp_out_put[tmp_cate]/sum
                value.append("%.3f" % tmp_prob)
                del tmp_out_put[tmp_cate]

                #2nd
                tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                value.append(tmp_cate)
                tmp_prob = tmp_out_put[tmp_cate]/sum
                value.append("%.3f" % tmp_prob)
                del tmp_out_put[tmp_cate]

                #3rd
                tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                value.append(tmp_cate)
                tmp_prob = tmp_out_put[tmp_cate]/sum
                value.append("%.3f" % tmp_prob)
                del tmp_out_put[tmp_cate]

                #4th
                tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                value.append(tmp_cate)
                tmp_prob = tmp_out_put[tmp_cate]/sum
                value.append("%.3f" % tmp_prob)
                del tmp_out_put[tmp_cate]

                #5th
                tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                value.append(tmp_cate)
                tmp_prob = tmp_out_put[tmp_cate]/sum
                value.append("%.3f" % tmp_prob)
                del tmp_out_put[tmp_cate]

                #Shopping
                value.append("Shopping")
                shopping = shopping / sum
                value.append("%.3f" % shopping)

                print(value[16])

                wr.writerow(value)
                value = []

            else:
                pass

if __name__ == '__main__':
    main()
