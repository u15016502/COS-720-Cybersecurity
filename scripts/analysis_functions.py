"""
Functions for Exploratory Data Analysis

Script containing functions used for performing
exploratory data analysis on the cleaned headers.

"""
import numpy as np
import time
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import operator
from wordcloud import WordCloud, STOPWORDS
import progressbar


def analyze_subjects(headers, words_to_strip):
    """ Creates a word cloud of all subjects"""
    # Map headers to subjects
    subjects = list(map(lambda h: h["Subject"][0], headers))
    text = " ".join(subjects)

    # Strip specified words from subjects
    for word in words_to_strip:
        text = text.replace(word, " ")

    # Generate and save world cloud
    word_cloud = WordCloud(width=1000, height=500, stopwords=set(STOPWORDS)).generate(text)
    plt.figure(figsize=(15, 8))
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()
    plt.imsave("../data/images/res.png", word_cloud)


def analyze_content_types(headers, is_charset):
    if is_charset:
        content_types = list(map(lambda h: h["Content-Type"][1].split("=")[1], headers))
    else:
        content_types = list(map(lambda h: h["Content-Type"][0], headers))

    unique_types = list(set(content_types))
    counts = []
    for t in unique_types:
        counts.append(unique_types.count(t))
    chart, ax1 = plt.subplots()
    ax1.pie(counts, labels=unique_types, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig("../data/images/content" + str(is_charset) + ".png")
    plt.show()


def analyze_days(headers):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    email_days = list(map(lambda x: x["Date"][0].split(",")[0], headers))
    day_counts = []
    for day in days_of_week:
        day_counts.append(email_days.count(day))

    # Configure bar chart
    num_days = len(days_of_week)
    ind = np.arange(num_days)
    bar_width = 0.6
    chart, ax = plt.subplots()
    rectangles = ax.bar(ind, day_counts, bar_width, color='r', alpha=0.6)
    ax.set_ylabel("Number of emails")
    ax.set_xlabel("Day")
    ax.set_title("Number of emails per day")
    ax.set_xticks(ind + bar_width / 20)
    ax.set_xticklabels(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"))

    for rect in rectangles:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1 * height,
                '%d' % int(height),
                ha='center', va='bottom')
    plt.savefig("../data/images/days.png")
    plt.show()


def analyze_months(headers):
    months_of_year = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    email_months = list(map(lambda x: x["Date"][0].split(" ")[2], headers))
    month_counts = []
    for month in months_of_year:
        month_counts.append(email_months.count(month))

    # Configure bar chart
    num_days = len(months_of_year)
    ind = np.arange(num_days)
    bar_width = 0.6
    chart, ax = plt.subplots()
    rectangles = ax.bar(ind, month_counts, bar_width, color='b', alpha=0.6)
    ax.set_ylabel("Number of emails")
    ax.set_xlabel("Month")
    ax.set_title("Number of emails per month")
    ax.set_xticks(ind + bar_width / 20)
    ax.set_xticklabels(months_of_year)

    for rect in rectangles:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1 * height,
                '%d' % int(height),
                ha='center', va='bottom')
    plt.savefig("../data/images/months.png")
    plt.show()


def analyze_years(headers):
    email_years = list(map(lambda x: x["Date"][0].split(" ")[3]
                           .replace("2000", "x")
                           .replace("000", "200")
                           .replace("x", "2000"), headers))
    unique_years = list(set(email_years))
    unique_years.sort()
    year_counts = []
    for year in unique_years:
        year_counts.append(email_years.count(year))
    # Configure line chart
    unique_years = list(map(int, unique_years))
    plt.plot(unique_years, year_counts, color='r', alpha=0.6)
    plt.xlim(1979, 2044)
    plt.ylabel('Number of Emails')
    plt.xlabel('Year')
    plt.title('Number of emails per year')
    plt.savefig("../data/images/years.png")
    plt.show()


def analyze_times(headers):
    hours = list(map(lambda x: int(x["Date"][0].split(" ")[4].split(":")[0]), headers))
    unique_hours = list(set(hours))
    unique_hours.sort()
    hours_count = []
    for hour in unique_hours:
        hours_count.append(hours.count(hour))
    # Configure line chart
    plt.plot(unique_hours, hours_count, color='g', alpha=0.6)
    plt.xlim(0, 24)
    plt.ylabel('Number of Emails')
    plt.xlabel('Hour of Day')
    plt.title('Number of emails per hour')
    plt.savefig("../data/images/hours.png")
    plt.show()


def get_max_senders(headers, top):
    email_addresses = list(map(lambda h: h["From"][0].split("@")[0], headers))
    unique_addresses = list(set(email_addresses))
    address_counts = {}
    counter = 0
    with progressbar.ProgressBar(max_value=len(unique_addresses)) as bar:
        for address in unique_addresses:
            address_counts[address] = email_addresses.count(address)
            bar.update(counter)
            counter += 1
    sorted_address_counts = sorted(address_counts.items(), key=operator.itemgetter(1))
    sorted_address_counts.reverse()

    graph_emails = []
    graph_counts = []
    for x in range(top):
        graph_emails.append(sorted_address_counts[x][0])
        graph_counts.append(sorted_address_counts[x][1])
    print(graph_emails)
    print(graph_counts)

    # Configure bar chart
    num_emails = len(graph_emails)
    ind = np.arange(num_emails)
    bar_width = 0.6
    chart, ax = plt.subplots()
    rectangles = ax.bar(ind, graph_counts, bar_width, color='r', alpha=0.6)
    ax.set_ylabel("Number of emails")
    ax.set_xlabel("Sender")
    ax.set_title("Number of emails per sender")
    ax.set_xticks(ind + bar_width / 20)
    ax.set_xticklabels(graph_emails)
    plt.xticks(rotation=90)

    plt.savefig("../data/images/senders.png")
    plt.show()
