import csv
import pandas as pd

def load_csv():
    data = {}
    csv = pd.read_csv("history_day_cat_alluser.csv")
    for i in range(0, len(csv), 1):
        tdict = {}
        tdict.update({"id":csv["id"][i]})
        tdict.update({"visit_time":csv["visit_time"][i]})
        tdict.update({"cate":csv["cate"][i]})
        data.update({i:tdict})


    return data


def main():
    #cate dict
    cate_list = {}
    web_cate = ["Abortion", "Advocacy Organizations", "Alcohol", "Alternative Beliefs", "Dating", "Gambling", "Lingerie and Swimsuit", "Marijuana" , "Nudity and Risque", "Other Adult Materials", "Pornography", "Sex Education", "Sports Hunting and War Games", "Tobacco", "Weapons (Sales)", "File Sharing and Storage", "Freeware and Software Downloads", "Internet Radio and TV", "Internet Telephony", "Peer-to-peer File Sharing", "Streaming Media and Download", "Armed Forces", "Business", "Finance and Banking", "General Organizations", "Government and Legal Organizations", "Information Technology", "Information and Computer Security", "Search Engines and Portals", "Secure Websites", "Web Hosting", "Web-based Applications", "Advertising" "Arts and Culture", "Auction", "Brokerage and Trading", "Child Education", "Content Servers", "Digital Postcards", "Domain Parking", "Dynamic Content", "Education", "Entertainment", "Folklore", "Games", "Global Religion", "Health and Wellness", "Instant Messaging", "Job Search", "Meaningless Content", "Medicine", "News and Media", "Newsgroups and Message Boards", "Personal Privacy", "Personal Vehicles", "Personal Websites and Blogs", "Political Organizations", "Real Estate", "Reference", "Restaurant and Dining", "Shopping", "Social Networking", "Society and Lifestyles", "Sports", "Travel", "Web Chat", "Web-based Email", "Child Abuse", "Discrimination", "Drug Abuse", "Explicit Violence", "Extremist Groups", "Hacking", "Illegal or Unethical", "Plagiarism", "Proxy Avoidance", "Dynamic DNS", "Malicious Websites", "Phishing", "Spam URLs", "Unclassified", "Shopping and Auction", "Arts and Culture", "Not Rated", "Freeware Downloads"]
    for i in range(0, len(web_cate), 1):
        cate_list.update({web_cate[i]:0})

    #user id list and variable
    user_cnt = -1
    now_id = 0
    id_list = []
    id_index = []


    #variable
    now_date = 0
    day_cate = {}
    total_cnt = 0
    date_list = []


    #main
    for num in range(1, 2, 1):
        print("csv loading: " + str(num))
        data = load_csv()
        print("csv loding complete")

        for i in range(0, len(data), 1):
            #print("Check: " + str(i) + "/" + str(len(data)))
            if data[i]["cate"] not in cate_list:
                data[i]["cate"] = "Not Rated"



            if now_id != data[i]["id"]:
                now_id = data[i]["id"]
                user_cnt += 1
                now_date = data[i]["visit_time"]
                tdict = {}
                tmp_cate_list = cate_list
                tdict.update({data[i]["visit_time"]:cate_list})
                day_cate.update({user_cnt:tdict})
                id_list.append(data[i]["id"])
                date_list.append(now_date)
                id_index.append(user_cnt)
                total_cnt += 1

            if now_date != data[i]["visit_time"]:
                now_date = data[i]["visit_time"]
                cate_list = cate_list.fromkeys(web_cate, 0)
                day_cate[user_cnt].update({now_date:cate_list})
                id_list.append(data[i]["id"])
                date_list.append(now_date)
                id_index.append(user_cnt)
                total_cnt += 1

            day_cate[user_cnt][now_date][data[i]["cate"]] += 1

        print(len(id_list))
        print(total_cnt)
        print("user # :" + str(user_cnt))
        with open('../history_day/history_day_cat_all.csv','w') as f:
                wr = csv.writer(f)
                file_title = ["id", "visit_time", 'Illegal or Unethical', 'Job Search', 'Finance and Banking', 'Alcohol', 'Entertainment', 'Nudity and Risque', 'Sports', 'Travel', 'Reference', 'Malicious Websites', 'Marijuana', 'Medicine', 'Child Abuse', 'Phishing', 'Sports Hunting and War Games', 'Gambling', 'Dating' , 'News and Media', 'Streaming Media and Download', 'Restaurant and Dining', 'Health and Wellness', 'AdvertisingArts and Culture', 'Weapons (Sales)', 'Internet Radio and TV', 'Explicit Violence', 'Drug Abuse', 'Extremist Groups', 'Dynamic DNS', 'Meaningless Content', 'Government and Legal Organizations', 'General Organizations', 'Personal Vehicles', 'Web-based Applications', 'Not Rated', 'Information Technology', 'Folklore', 'Information and Computer Security', 'Advocacy Organizations', 'Freeware and Software Downloads', 'Sex Education', 'Alternative Beliefs', 'Spam URLs', 'Tobacco', 'Web Chat', 'Domain Parking', 'Abortion', 'Global Religion', 'Web Hosting', 'Unclassified', 'Digital Postcards', 'Games', 'Society and Lifestyles', 'Discrimination', 'Internet Telephony', 'Hacking', 'Newsgroups and Message Boards', 'Social Networking', 'Lingerie and Swimsuit', 'Armed Forces', 'Personal Websites and Blogs', 'Arts and Culture', 'Proxy Avoidance', 'Business', 'Political Organizations', 'Child Education', 'Content Servers', 'Instant Messaging', 'File Sharing and Storage', 'Brokerage and Trading', 'Plagiarism', 'Personal Privacy', 'Search Engines and Portals' , 'Secure Websites', 'Other Adult Materials', 'Peer-to-peer File Sharing', 'Real Estate', 'Pornography', 'Education', 'Dynamic Content' , 'Freeware Downloads', 'Web-based Email', 'Shopping']
                title = ['Illegal or Unethical', 'Job Search', 'Finance and Banking', 'Alcohol', 'Entertainment', 'Nudity and Risque', 'Sports', 'Travel', 'Reference', 'Malicious Websites', 'Marijuana', 'Medicine', 'Child Abuse', 'Phishing', 'Sports Hunting and War Games', 'Gambling', 'Dating' , 'News and Media', 'Streaming Media and Download', 'Restaurant and Dining', 'Health and Wellness', 'AdvertisingArts and Culture', 'Weapons (Sales)', 'Internet Radio and TV', 'Explicit Violence', 'Drug Abuse', 'Extremist Groups', 'Dynamic DNS', 'Meaningless Content', 'Government and Legal Organizations', 'General Organizations', 'Personal Vehicles', 'Web-based Applications', 'Not Rated', 'Information Technology', 'Folklore', 'Information and Computer Security', 'Advocacy Organizations', 'Freeware and Software Downloads', 'Sex Education', 'Alternative Beliefs', 'Spam URLs', 'Tobacco', 'Web Chat', 'Domain Parking', 'Abortion', 'Global Religion', 'Web Hosting', 'Unclassified', 'Digital Postcards', 'Games', 'Society and Lifestyles', 'Discrimination', 'Internet Telephony', 'Hacking', 'Newsgroups and Message Boards', 'Social Networking', 'Lingerie and Swimsuit', 'Armed Forces', 'Personal Websites and Blogs', 'Arts and Culture', 'Proxy Avoidance', 'Business', 'Political Organizations', 'Child Education', 'Content Servers', 'Instant Messaging', 'File Sharing and Storage', 'Brokerage and Trading', 'Plagiarism', 'Personal Privacy', 'Search Engines and Portals' , 'Secure Websites', 'Other Adult Materials', 'Peer-to-peer File Sharing', 'Real Estate', 'Pornography', 'Education', 'Dynamic Content' , 'Freeware Downloads', 'Web-based Email']

                wr.writerow(file_title)

                for i in range(0, total_cnt, 1):
                    values = []
                    values.append(id_list[i])
                    values.append(date_list[i])
                    for cat in title:
                        values.append(day_cate[id_index[i]][date_list[i]][cat])
                    tmp_shopping = day_cate[id_index[i]][date_list[i]]["Shopping"] + day_cate[id_index[i]][date_list[i]]["Shopping and Auction"] + day_cate[id_index[i]][date_list[i]]["Auction"]
                    values.append(tmp_shopping)
                    wr.writerow(values)

                #initialize
                user_cnt = -1
                now_id = 0
                id_list = []
                id_index = []
                now_date = 0
                day_cate = {}
                total_cnt = 0
                date_list = []

if __name__ == '__main__':
    main()
