import pandas as pd
import csv
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn import preprocessing
from sklearn import tree
from sklearn.metrics import roc_curve
from sklearn.metrics import accuracy_score
from sklearn.metrics import auc
import metrics
import datetime
import random

def load_final_csv():
    data_out_y = []
    data_out_x = []
    shop_y = []
    shop_x = []
    csv = pd.read_csv("final_csv_1225.csv")
    for i in range(0, len(csv), 2):
        data_x = {}
        data_y = {}

        # >7 days
        data_y.update({"id":csv["id"][i]})
        data_y.update({"bday":csv["bday"][i]})
        data_y.update({"gender":csv["gender"][i]})
        data_y.update({"marr":csv["marr"][i]})
        data_y.update({"1st":csv["1st"][i]})
        data_y.update({"1st_prop":csv["1st_prop"][i]})
        data_y.update({"2nd":csv["2nd"][i]})
        data_y.update({"2nd_prop":csv["2nd_prop"][i]})
        data_y.update({"3rd":csv["3rd"][i]})
        data_y.update({"3rd_prop":csv["3rd_prop"][i]})

        data_y.update({"shopping":csv["Shopping_prop"][i]})
        shop_y.append(csv["Shopping_prop"][i])

        # <8 days
        data_x.update({"id":csv["id"][i+1]})
        data_x.update({"bday":csv["bday"][i+1]})
        data_x.update({"gender":csv["gender"][i+1]})
        data_x.update({"marr":csv["marr"][i+1]})
        data_x.update({"1st":csv["1st"][i+1]})
        data_x.update({"1st_prop":csv["1st_prop"][i+1]})
        data_x.update({"2nd":csv["2nd"][i+1]})
        data_x.update({"2nd_prop":csv["2nd_prop"][i+1]})
        data_x.update({"3rd":csv["3rd"][i+1]})
        data_x.update({"3rd_prop":csv["3rd_prop"][i+1]})

        data_x.update({"shopping":csv["Shopping_prop"][i+1]})
        shop_x.append(csv["Shopping_prop"][i+1])

        data_out_y.append(data_y)
        data_out_x.append(data_x)

    return data_out_y, data_out_x, shop_y, shop_x

def shopping_avg_count(shop_y, shop_x):
    avg = 0
    will_shopping = []
    for i in range(len(shop_y)):
        if shop_x[i] - shop_y[i] > 0:
            will_shopping.append(1)
        if shop_x[i] - shop_y[i] <= 0:
            will_shopping.append(0)

        avg += shop_x[i] - shop_y[i]

    avg = avg / len(shop_y)
    return avg, will_shopping

def increase_or_not(will_shopping):
    count_will = 0
    count_not = 0

    for i in range(len(will_shopping)):
        if will_shopping[i] == 1:
            count_will += 1
        else:
            count_not += 1

    print("Proportionate increase: " + str(count_will))
    print("Proportionate decreased: " + str(count_not))

def data_split(feature, label, size):
    tmp = []
    tr_x = []
    tr_y = []
    te_x = []
    te_y = []
    tmp = list(zip(feature, label))
    random.shuffle(tmp)
    feature, label = zip(*tmp)

    for i in range(len(feature)):
        if i <= len(feature)*size:
            tr_x.append(feature[i])
            tr_y.append(label[i])

        else:
            te_x.append(feature[i])
            te_y.append(label[i])

    tr_x = np.array(tr_x).reshape((len(tr_x),-1))
    te_x = np.array(te_x).reshape((len(te_x),-1))

    #normalize
    tr_x = preprocessing.scale(tr_x)
    te_x = preprocessing.scale(te_x)

    return tr_x, tr_y, te_x, te_y

def count_age(bday):
    day = bday[:4]

    if 2017 - int(day) < 20:
        return 1

    elif 2017 - int(day) < 29 and 2017 - int(day) > 19:
        return 2

    elif 2017 - int(day) < 39 and 2017 - int(day) > 29:
        return 3

    else:
        return 4

def feature(data_y):
    title_new = ['Illegal or Unethical', 'Job Search', 'Finance and Banking', 'Alcohol', 'Entertainment', 'Nudity and Risque', 'Sports', 'Travel', 'Reference', 'Malicious Websites', 'Marijuana', 'Medicine', 'Child Abuse', 'Phishing', 'Sports Hunting and War Games', 'Gambling', 'Dating' , 'News and Media', 'Streaming Media and Download', 'Restaurant and Dining', 'Health and Wellness', 'AdvertisingArts and Culture', 'Weapons (Sales)', 'Internet Radio and TV', 'Explicit Violence', 'Drug Abuse', 'Extremist Groups', 'Dynamic DNS', 'Meaningless Content', 'Government and Legal Organizations', 'General Organizations', 'Personal Vehicles', 'Web-based Applications', 'Not Rated', 'Information Technology', 'Folklore', 'Information and Computer Security', 'Advocacy Organizations', 'Freeware and Software Downloads', 'Sex Education', 'Alternative Beliefs', 'Spam URLs', 'Tobacco', 'Web Chat', 'Domain Parking', 'Abortion', 'Global Religion', 'Web Hosting', 'Unclassified', 'Digital Postcards', 'Games', 'Society and Lifestyles', 'Discrimination', 'Internet Telephony', 'Hacking', 'Newsgroups and Message Boards', 'Social Networking', 'Lingerie and Swimsuit', 'Armed Forces', 'Personal Websites and Blogs', 'Arts and Culture', 'Proxy Avoidance', 'Business', 'Political Organizations', 'Child Education', 'Content Servers', 'Instant Messaging', 'File Sharing and Storage', 'Brokerage and Trading', 'Plagiarism', 'Personal Privacy', 'Search Engines and Portals' , 'Secure Websites', 'Other Adult Materials', 'Peer-to-peer File Sharing', 'Real Estate', 'Pornography', 'Education', 'Dynamic Content' , 'Freeware Downloads', 'Web-based Email', 'Shopping']
    title_feature = []
    feature_x = []

    for i in range(len(data_y)):
        feature = []
        title_feature = []
        for k in range(len(title_new)):
            title_feature.append(0.0)
        if data_y[i]["gender"] == 1:
            feature.append(1)
            feature.append(0)
            feature.append(0)

        elif data_y[i]["gender"] == 2:
            feature.append(0)
            feature.append(1)
            feature.append(0)

        else:
            feature.append(0)
            feature.append(0)
            feature.append(1)

        if data_y[i]["marr"] == 1:
            feature.append(1)
            feature.append(0)
            feature.append(0)

        elif data_y[i]["marr"] == 2:
            feature.append(0)
            feature.append(1)
            feature.append(0)

        else:
            feature.append(0)
            feature.append(0)
            feature.append(1)

        title_feature[title_new.index(data_y[i]["1st"])] = data_y[i]["1st_prop"]
        title_feature[title_new.index(data_y[i]["2nd"])] = data_y[i]["2nd_prop"]
        title_feature[title_new.index(data_y[i]["3rd"])] = data_y[i]["3rd_prop"]

        for j in title_feature:
            feature.append(j)

        age_result = count_age(data_y[i]["bday"])

        if age_result == 1:
            feature.append(1)
            feature.append(0)
            feature.append(0)
            feature.append(0)

        elif age_result == 2:
            feature.append(0)
            feature.append(1)
            feature.append(0)
            feature.append(0)

        elif age_result == 3:
            feature.append(0)
            feature.append(0)
            feature.append(1)
            feature.append(0)

        else:
            feature.append(0)
            feature.append(0)
            feature.append(0)
            feature.append(1)

        feature_x.append(feature)



    return feature_x


def main():
    #variable
    data_x = []
    data_y = []
    shop_x = []
    shop_y = []
    will_shopping = []
    shopping_avg = 0
    feature_x = []
    tr_x = []
    te_x = []
    tr_y = []
    te_y = []
    knn_tr_pred = []
    knn_te_pred = []
    svm_tr_pred = []
    svm_te_pred = []
    DT_tr_pred = []
    DT_te_pred = []
    log_tr_pred = []
    log_te_pred = []


    knn_tr_acc = []
    knn_te_acc = []
    svm_tr_acc = []
    svm_te_acc = []
    DT_tr_acc = []
    DT_te_acc = []
    log_tr_acc = []
    log_te_acc = []

    size_acc_svm_te = []
    size_acc_knn_te = []
    size_acc_DT_te = []
    size_acc_log_te = []
    knn_TF_one = 0
    knn_TF_two = 0
    knn_TF_three = 0
    knn_TF_four = 0
    svm_TF_one = 0
    svm_TF_two = 0
    svm_TF_three = 0
    svm_TF_four = 0

    svm_te_accuracy = 0
    svm_tr_accuracy = 0
    knn_te_accuracy = 0
    knn_tr_accuracy = 0
    DT_te_accuracy = 0
    DT_tr_accuracy = 0
    log_te_accuracy = 0
    log_tr_accuracy = 0


    svm_te_error_rate = 0
    svm_tr_error_rate = 0
    knn_te_error_rate = 0
    knn_tr_error_rate = 0
    #size = 0.9




    #main
    print("csv loading...")
    data_y, data_x, shop_y, shop_x = load_final_csv()
    shopping_avg, will_shopping = shopping_avg_count(shop_y, shop_x)

    # show numbers of increased and decreased
    increase_or_not(will_shopping)

    feature_x = feature(data_y)

    for size in range(9, 10, 1):
        size = size * 0.1
        knn_tr_acc = []
        knn_te_acc = []
        svm_tr_acc = []
        svm_te_acc = []
        DT_te_acc = []
        DT_tr_acc = []
        log_te_acc = []
        log_tr_acc = []


        for iter in range(20):
            #initialize

            knn_te_pred = []
            knn_tr_pred = []
            svm_te_pred = []
            svm_tr_pred = []
            DT_tr_pred = []
            DT_te_pred = []
            log_tr_pred = []
            log_te_pred = []
            svm_te_accuracy = 0
            svm_tr_accuracy = 0
            knn_te_accuracy = 0
            knn_tr_accuracy = 0
            DT_te_accuracy = 0
            DT_tr_accuracy = 0
            log_te_accuracy = 0
            log_tr_accuracy = 0

            tr_x, tr_y, te_x, te_y = data_split(feature_x, will_shopping, size)

            #knn_training
            knn = KNeighborsClassifier(n_neighbors=7)
            knn = knn.fit(tr_x, tr_y)

            #SVM
            clf_svm = svm.SVC(C = 1)
            clf_svm = clf_svm.fit(tr_x, tr_y)

            #DT
            clf_DT = tree.DecisionTreeClassifier()
            clf_DT = clf_DT.fit(tr_x, tr_y)

            #LOG
            clf_log = LogisticRegression()
            clf_log = clf_log.fit(tr_x, tr_y)

            #training
            for i in range(len(tr_x)):
                knn_tr_pred.append(knn.predict([tr_x[i]]))
                svm_tr_pred.append(clf_svm.predict([tr_x[i]]))
                DT_tr_pred.append(clf_DT.predict([tr_x[i]]))
                log_tr_pred.append(clf_log.predict([tr_x[i]]))

            #testing
            for i in range(len(te_x)):
                knn_te_pred.append(knn.predict([te_x[i]]))
                svm_te_pred.append(clf_svm.predict([te_x[i]]))
                DT_te_pred.append(clf_DT.predict([te_x[i]]))
                log_te_pred.append(clf_log.predict([te_x[i]]))

            if size == 0.9:
                for j in range(len(te_y)):
                    if knn_te_pred[j] == te_y[j]:
                        if knn_te_pred[j] == 1:
                            knn_TF_one += 1
                        else:
                            knn_TF_four += 1
                    else:
                        if knn_te_pred[j] == 1:
                            knn_TF_two += 1
                        else:
                            knn_TF_three += 1

                for k in range(len(te_y)):
                    if svm_te_pred[k] == te_y[k]:
                        if svm_te_pred[k] == 1:
                            svm_TF_one += 1
                        else:
                            svm_TF_four += 1
                    else:
                        if svm_te_pred[k] == 1:
                            svm_TF_two += 1
                        else:
                            svm_TF_three += 1



            knn_tr_acc.append(accuracy_score(tr_y, knn_tr_pred))
            knn_te_acc.append(accuracy_score(te_y, knn_te_pred))
            svm_tr_acc.append(accuracy_score(tr_y, svm_tr_pred))
            svm_te_acc.append(accuracy_score(te_y, svm_te_pred))
            DT_te_acc.append(accuracy_score(te_y, DT_te_pred))
            DT_tr_acc.append(accuracy_score(tr_y, DT_tr_pred))
            log_te_acc.append(accuracy_score(te_y, log_te_pred))
            log_tr_acc.append(accuracy_score(tr_y, log_tr_pred))



        for i in range(20):
            knn_tr_accuracy += knn_tr_acc[i]
            knn_te_accuracy += knn_te_acc[i]
            svm_tr_accuracy += svm_tr_acc[i]
            svm_te_accuracy += svm_te_acc[i]
            DT_tr_accuracy += DT_tr_acc[i]
            DT_te_accuracy += DT_te_acc[i]
            log_tr_accuracy += log_tr_acc[i]
            log_te_accuracy += log_te_acc[i]

        knn_tr_accuracy = knn_tr_accuracy / 20.0
        knn_te_accuracy = knn_te_accuracy / 20.0
        svm_tr_accuracy = svm_tr_accuracy / 20.0
        svm_te_accuracy = svm_te_accuracy / 20.0
        DT_tr_accuracy = DT_tr_accuracy / 20.0
        DT_te_accuracy = DT_te_accuracy / 20.0
        log_tr_accuracy = log_tr_accuracy / 20.0
        log_te_accuracy = log_te_accuracy / 20.0

        knn_tr_error_rate = 1 - knn_tr_accuracy
        knn_te_error_rate = 1 - knn_te_accuracy
        svm_tr_error_rate = 1 - svm_tr_accuracy
        svm_te_error_rate = 1 - svm_te_accuracy

        size_acc_svm_te.append("%.3f" % svm_te_accuracy)
        size_acc_knn_te.append("%.3f" % knn_te_accuracy)
        size_acc_DT_te.append("%.3f" % DT_te_accuracy)
        size_acc_log_te.append("%.3f" % log_te_accuracy)


    knn_TF_one = "%.2f" % (knn_TF_one / 20.0 / len(te_y))
    knn_TF_two = "%.2f" % (knn_TF_two / 20.0 / len(te_y))
    knn_TF_three = "%.2f" % (knn_TF_three / 20.0 / len(te_y))
    knn_TF_four = "%.2f" % (knn_TF_four / 20.0 / len(te_y))
    svm_TF_one = "%.2f" % (svm_TF_one / 20.0 / len(te_y))
    svm_TF_two = "%.2f" % (svm_TF_two / 20.0 / len(te_y))
    svm_TF_three = "%.2f" % (svm_TF_three / 20.0 / len(te_y))
    svm_TF_four = "%.2f" % (svm_TF_four / 20.0 / len(te_y))

    print("Accuracy: ")
    print("------ Training ------")
    print("knn_tr_accuracy: " + str("%.3f" % knn_tr_accuracy))
    print("svm_tr_accuracy: " + str("%.3f" % svm_tr_accuracy))
    print("DT_tr_accuracy: " + str("%.3f" % DT_tr_accuracy))
    print("log_tr_accuracy: " + str("%.3f" % log_tr_accuracy))
    print("")
    print("------ Testing ------")
    print("knn_te_accuracy: " + str("%.3f" % knn_te_accuracy))
    print("svm_te_accuracy: " + str("%.3f" % svm_te_accuracy))
    print("DT_te_accuracy: " + str("%.3f" % DT_te_accuracy))
    print("log_te_accuracy: " + str("%.3f" % log_te_accuracy))
    print("")

    print("")
    print("Traing data to accuracy")
    print("[ 50%, 70%, 90% ]")
    print("")
    print("knn")
    print(size_acc_knn_te)
    print("svm")
    print(size_acc_svm_te)
    print("DT")
    print(size_acc_DT_te)
    print("log")
    print(size_acc_log_te)


    #plot


    #ROC
    knn_te_pred = knn.predict_proba(te_x)[:,1]

    DT_te_pred = clf_DT.predict_proba(te_x)[:,1]
    log_te_pred = clf_log.predict_proba(te_x)[:,1]

    fpr, tpr, thresholds = roc_curve(te_y, log_te_pred, pos_label=2)
    roc_auc = auc(fpr, tpr)

    print("")
    print(tpr)
    print("")
    print(fpr)
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()





if __name__ == '__main__':
    main()
