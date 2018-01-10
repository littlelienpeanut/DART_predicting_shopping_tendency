'''find over 30 days users'''
import json
import time
import csv
import datetime
from datetime import date

def  parse_ymd ( s ):
    s = s[0:10]
    year_s, mon_s, day_s  =  s.split ('-')
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


def main():

    print("LOADING USER INFO TO MEMORY")

    with open("user_list.json", mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as json_data:
        jdata = json.load(json_data, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)
        __UserList__ = json.loads(jdata, object_hook=None);

    print("50%")

    with open("user_dict.json", mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as json_udict:
        judictdata = json.load(json_udict, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)
        __UserDict__ = json.loads(judictdata, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)

    print("FINISHED")

    while True:
        days = input("How long? ")
        cnt = input("How many? ")
        print("FIND OVER " + days + " DAYS USER")
        count = 0
        count_30 = 0
        user_time = []
        data_count = []
        user_time_30up = []
        user_time_30up_id = []
        for j in range(0, len(__UserList__)):
            for i in range(0, len(__UserDict__[__UserList__[j]]["history"])):
                user_time.append(parse_ymd(__UserDict__[__UserList__[j]]["history"][i]["visit_time"]))
            min_time = min(user_time)
            max_time = max(user_time)
            range_of_days = count_days(min_time, max_time)

            count = count + 1
            if range_of_days >= int(days) and len(__UserDict__[__UserList__[j]]["history"]) > int(cnt) :
                user_time_30up.append(__UserList__[j])
                user_time_30up_id.append(j+1)
                count_30 = count_30 + 1

            user_time[:] = []



        print("TOTAL USERS #: " + str(count))
        print("OVER " + days + " DAYS over " + cnt + " history #: " + str(count_30))
        print("OVER " + days + " DAYS over " + cnt + " historys USERS ID: "+ str(user_time_30up_id))

        with open("over_3000_userlist.csv", "w") as fout:
            wr = csv.writer(fout)
            title = ["id"]
            wr.writerow(title)

            for i in range(len(user_time_30up)):
                user_id = []
                user_id.append(user_time_30up[i][2:-1])
                wr.writerow(user_id)


if __name__ == '__main__':
    main()
