import csv
import pandas as pd
import time
import datetime
from datetime import date
from collections import Counter
import pymysql
import operator

def load_user(filename):
    csv = pd.read_csv("user_list_" + filename + ".csv")
    user_list = []
    for i in range(len(csv)):
        user_list.append(csv["id"][i])

    return user_list

def count_days(next_date, now_date):
    next_year_s,  next_mon_s,  next_day_s  =  next_date.split('-')
    now_year_s,  now_mon_s,  now_day_s  =  now_date.split('-')
    now_d = date(int(now_year_s), int(now_mon_s), int(now_day_s))
    next_d = date(int(next_year_s), int(next_mon_s), int(next_day_s))
    total =  (next_d - now_d).days
    total += 1
    return total

def load_csv(uid):
    data = []
    title = ['Illegal or Unethical', 'Job Search', 'Finance and Banking', 'Alcohol', 'Entertainment', 'Nudity and Risque', 'Sports', 'Travel', 'Reference', 'Malicious Websites', 'Marijuana', 'Medicine', 'Child Abuse', 'Phishing', 'Sports Hunting and War Games', 'Gambling', 'Dating' , 'News and Media', 'Streaming Media and Download', 'Restaurant and Dining', 'Health and Wellness', 'AdvertisingArts and Culture', 'Weapons (Sales)', 'Internet Radio and TV', 'Explicit Violence', 'Drug Abuse', 'Extremist Groups', 'Dynamic DNS', 'Meaningless Content', 'Government and Legal Organizations', 'General Organizations', 'Personal Vehicles', 'Web-based Applications', 'Not Rated', 'Information Technology', 'Folklore', 'Information and Computer Security', 'Advocacy Organizations', 'Freeware and Software Downloads', 'Sex Education', 'Alternative Beliefs', 'Spam URLs', 'Tobacco', 'Web Chat', 'Domain Parking', 'Abortion', 'Global Religion', 'Web Hosting', 'Unclassified', 'Digital Postcards', 'Games', 'Society and Lifestyles', 'Discrimination', 'Internet Telephony', 'Hacking', 'Newsgroups and Message Boards', 'Social Networking', 'Lingerie and Swimsuit', 'Armed Forces', 'Personal Websites and Blogs', 'Arts and Culture', 'Proxy Avoidance', 'Business', 'Political Organizations', 'Child Education', 'Content Servers', 'Instant Messaging', 'File Sharing and Storage', 'Brokerage and Trading', 'Plagiarism', 'Personal Privacy', 'Search Engines and Portals' , 'Secure Websites', 'Other Adult Materials', 'Peer-to-peer File Sharing', 'Real Estate', 'Pornography', 'Education', 'Dynamic Content' , 'Freeware Downloads', 'Web-based Email', 'Shopping']
    csv = pd.read_csv("history_day_cat_all.csv")
    for i in range(0, len(csv), 1):
        if any(csv["id"][i] in s for s in uid):
            shopping = 0
            tdict = {}
            tdict.update({"id":csv["id"][i]})
            tdict.update({"date":csv["visit_time"][i]})
            for cate in title:
                tdict.update({cate:csv[cate][i]})

            data.append(tdict)

        else:
            pass

    return data

def value_add(dict1, dict2):
    title_new = ['Illegal or Unethical', 'Job Search', 'Finance and Banking', 'Alcohol', 'Entertainment', 'Nudity and Risque', 'Sports', 'Travel', 'Reference', 'Malicious Websites', 'Marijuana', 'Medicine', 'Child Abuse', 'Phishing', 'Sports Hunting and War Games', 'Gambling', 'Dating' , 'News and Media', 'Streaming Media and Download', 'Restaurant and Dining', 'Health and Wellness', 'AdvertisingArts and Culture', 'Weapons (Sales)', 'Internet Radio and TV', 'Explicit Violence', 'Drug Abuse', 'Extremist Groups', 'Dynamic DNS', 'Meaningless Content', 'Government and Legal Organizations', 'General Organizations', 'Personal Vehicles', 'Web-based Applications', 'Not Rated', 'Information Technology', 'Folklore', 'Information and Computer Security', 'Advocacy Organizations', 'Freeware and Software Downloads', 'Sex Education', 'Alternative Beliefs', 'Spam URLs', 'Tobacco', 'Web Chat', 'Domain Parking', 'Abortion', 'Global Religion', 'Web Hosting', 'Unclassified', 'Digital Postcards', 'Games', 'Society and Lifestyles', 'Discrimination', 'Internet Telephony', 'Hacking', 'Newsgroups and Message Boards', 'Social Networking', 'Lingerie and Swimsuit', 'Armed Forces', 'Personal Websites and Blogs', 'Arts and Culture', 'Proxy Avoidance', 'Business', 'Political Organizations', 'Child Education', 'Content Servers', 'Instant Messaging', 'File Sharing and Storage', 'Brokerage and Trading', 'Plagiarism', 'Personal Privacy', 'Search Engines and Portals' , 'Secure Websites', 'Other Adult Materials', 'Peer-to-peer File Sharing', 'Real Estate', 'Pornography', 'Education', 'Dynamic Content' , 'Freeware Downloads', 'Web-based Email', 'Shopping']
    tdict = {}

    if dict2 == None:
        return dict1

    for cate in title_new:
        tmp = 0
        tmp = dict1[cate] + dict2[cate]
        tdict.update({cate:tmp})

    tdict.update({"id":dict1["id"]})
    tdict.update({"date":dict1["date"]})

    return tdict

def count_sum(cate):
    title_new = ['Illegal or Unethical', 'Job Search', 'Finance and Banking', 'Alcohol', 'Entertainment', 'Nudity and Risque', 'Sports', 'Travel', 'Reference', 'Malicious Websites', 'Marijuana', 'Medicine', 'Child Abuse', 'Phishing', 'Sports Hunting and War Games', 'Gambling', 'Dating' , 'News and Media', 'Streaming Media and Download', 'Restaurant and Dining', 'Health and Wellness', 'AdvertisingArts and Culture', 'Weapons (Sales)', 'Internet Radio and TV', 'Explicit Violence', 'Drug Abuse', 'Extremist Groups', 'Dynamic DNS', 'Meaningless Content', 'Government and Legal Organizations', 'General Organizations', 'Personal Vehicles', 'Web-based Applications', 'Not Rated', 'Information Technology', 'Folklore', 'Information and Computer Security', 'Advocacy Organizations', 'Freeware and Software Downloads', 'Sex Education', 'Alternative Beliefs', 'Spam URLs', 'Tobacco', 'Web Chat', 'Domain Parking', 'Abortion', 'Global Religion', 'Web Hosting', 'Unclassified', 'Digital Postcards', 'Games', 'Society and Lifestyles', 'Discrimination', 'Internet Telephony', 'Hacking', 'Newsgroups and Message Boards', 'Social Networking', 'Lingerie and Swimsuit', 'Armed Forces', 'Personal Websites and Blogs', 'Arts and Culture', 'Proxy Avoidance', 'Business', 'Political Organizations', 'Child Education', 'Content Servers', 'Instant Messaging', 'File Sharing and Storage', 'Brokerage and Trading', 'Plagiarism', 'Personal Privacy', 'Search Engines and Portals' , 'Secure Websites', 'Other Adult Materials', 'Peer-to-peer File Sharing', 'Real Estate', 'Pornography', 'Education', 'Dynamic Content' , 'Freeware Downloads', 'Web-based Email', 'Shopping']
    sum = 0
    if cate == {}:
        return sum

    else:
        for item in title_new:
            sum += cate[item]

        return sum

def cate_avg(cate, count):
    title_new = ['Illegal or Unethical', 'Job Search', 'Finance and Banking', 'Alcohol', 'Entertainment', 'Nudity and Risque', 'Sports', 'Travel', 'Reference', 'Malicious Websites', 'Marijuana', 'Medicine', 'Child Abuse', 'Phishing', 'Sports Hunting and War Games', 'Gambling', 'Dating' , 'News and Media', 'Streaming Media and Download', 'Restaurant and Dining', 'Health and Wellness', 'AdvertisingArts and Culture', 'Weapons (Sales)', 'Internet Radio and TV', 'Explicit Violence', 'Drug Abuse', 'Extremist Groups', 'Dynamic DNS', 'Meaningless Content', 'Government and Legal Organizations', 'General Organizations', 'Personal Vehicles', 'Web-based Applications', 'Not Rated', 'Information Technology', 'Folklore', 'Information and Computer Security', 'Advocacy Organizations', 'Freeware and Software Downloads', 'Sex Education', 'Alternative Beliefs', 'Spam URLs', 'Tobacco', 'Web Chat', 'Domain Parking', 'Abortion', 'Global Religion', 'Web Hosting', 'Unclassified', 'Digital Postcards', 'Games', 'Society and Lifestyles', 'Discrimination', 'Internet Telephony', 'Hacking', 'Newsgroups and Message Boards', 'Social Networking', 'Lingerie and Swimsuit', 'Armed Forces', 'Personal Websites and Blogs', 'Arts and Culture', 'Proxy Avoidance', 'Business', 'Political Organizations', 'Child Education', 'Content Servers', 'Instant Messaging', 'File Sharing and Storage', 'Brokerage and Trading', 'Plagiarism', 'Personal Privacy', 'Search Engines and Portals' , 'Secure Websites', 'Other Adult Materials', 'Peer-to-peer File Sharing', 'Real Estate', 'Pornography', 'Education', 'Dynamic Content' , 'Freeware Downloads', 'Web-based Email', 'Shopping']
    dict = {}
    if count == 0:
        return cate

    else:
        for item in title_new:
            dict.update({item:cate[item]/count})

        dict.update({"id":cate["id"]})
        return dict

class Run:
    def main(self, x):
        for dataset in range(0, 2, 1):
            #variable
            now_id = 0
            count_x = 0
            count_y = 0
            out_put = []
            uid = []
            tdict_x = {}
            tdict_y = {}
            holiday = "2016-12-25"


            #main
            if dataset == 0 :
                uid = load_user("tr")

            else:
                uid = load_user("te")


            print("csv loading...")
            data = load_csv(uid)

            for i in range(len(data)):
                if now_id == 0:
                    now_id = data[i]["id"]

                if now_id != data[i]["id"]:
                    out_put_x = {}
                    out_put_y = {}
                    count_x = count_sum(tdict_x) * 1.0
                    count_y = count_sum(tdict_y) * 1.0
                    out_put_x = cate_avg(tdict_x, count_x)
                    out_put_y = cate_avg(tdict_y, count_y)
                    out_put.append(out_put_y)
                    out_put.append(out_put_x)

                    #initial
                    tdict_x = {}
                    tdict_y = {}
                    count_x = 0
                    count_y = 0
                    now_id = data[i]["id"]

                if now_id == data[i]["id"]:
                    if abs(count_days(data[i]["date"], holiday)) > x:
                        if tdict_y == {}:
                            tdict_y = value_add(data[i], None)

                        else:
                            tdict_y = value_add(tdict_y, data[i])

                    elif abs(count_days(data[i]["date"], holiday)) < x+1:
                        if tdict_x == {}:
                            tdict_x = value_add(data[i], None)

                        else:
                            tdict_x = value_add(tdict_x, data[i])

            if dataset == 0:
                filename = "get_" + str(x) + "_y_1225_tr.csv"

            else:
                filename = "get_" + str(x) + "_y_1225_te.csv"

            with open(filename, "w") as fout:
                wr = csv.writer(fout)
                title = ["id", "Shopping_prop", "1st", "1st_prop", "2nd", "2nd_prop", "3rd",  "3rd_prop", "4th",  "4th_prop", "5th",  "5th_prop"]
                wr.writerow(title)
                tmp_out_put = {}

                for i in range(len(out_put)):

                    if out_put[i] == {}:
                        if i == 0:
                            tmp = []
                            tmp.append(out_put[i+1]["id"])
                            wr.writerow(tmp)
                            value = []

                        else:
                            tmp = []
                            if value == []:
                                tmp.append(out_put[i+1]["id"])
                                value = []

                            else:
                                tmp.append(value[0])
                                wr.writerow(tmp)
                                value = []

                    else:
                        tmp_out_put = []
                        tmp_out_put_shop = []
                        tmp_out_put = out_put[i]
                        tmp_out_put_shop = out_put[i]
                        value = []
                        value.append(tmp_out_put["id"])
                        del tmp_out_put["id"]
                        value.append("%.3f" % tmp_out_put["Shopping"])

                        #1st
                        tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                        value.append(tmp_cate)
                        value.append("%.3f" % tmp_out_put[tmp_cate])
                        del tmp_out_put[tmp_cate]

                        #2nd
                        tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                        value.append(tmp_cate)
                        value.append("%.3f" % tmp_out_put[tmp_cate])
                        del tmp_out_put[tmp_cate]

                        #3rd
                        tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                        value.append(tmp_cate)
                        value.append("%.3f" % tmp_out_put[tmp_cate])
                        del tmp_out_put[tmp_cate]

                        #4th
                        tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                        value.append(tmp_cate)
                        value.append("%.3f" % tmp_out_put[tmp_cate])
                        del tmp_out_put[tmp_cate]

                        #5th
                        tmp_cate = max(tmp_out_put.iteritems(), key=operator.itemgetter(1))[0]
                        value.append(tmp_cate)
                        value.append("%.3f" % tmp_out_put[tmp_cate])
                        del tmp_out_put[tmp_cate]

                        wr.writerow(value)
