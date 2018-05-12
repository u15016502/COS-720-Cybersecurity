"""
Functions for Exploratory Data Analysis

Script containing functions used for performing
exploratory data analysis on the cleaned headers.

"""
import numpy as np
import matplotlib.pyplot as plt
import operator
import progressbar
import sys
from wordcloud import WordCloud, STOPWORDS

sys.path.append('src/python')
import util


def analyze_basic(headers):
    """ Perform basic analysis on the email data set """
    util.log_print("Performing Basic Analysis")
    # Check how many people sent emails to themselves
    sent_to_self_count = len(list(filter(lambda header: header["From"][0] in header["To"][0], headers)))
    sent_to_self_percentage = round(sent_to_self_count / len(headers) * 100, 2)
    print("{0} Emails ({1}%) were sent from the senders to themselves"
          .format(sent_to_self_count, sent_to_self_percentage))

    # Check how many emails were sent from the same domain
    valid_headers = list(filter(lambda h: len(h["From"][0].split("@")) == 2, headers))
    same_domain_count = len(list(filter(lambda d: d["From"][0].split("@")[1].split(".")[0]
                            in " ".join(d["To"]), valid_headers)))
    same_domain_percentage = round(same_domain_count / len(headers) * 100, 2)
    print("{0} Emails ({1}%) were sent from the same domain".format(same_domain_count, same_domain_percentage))

    # Check how many emails were sent to more than one recipient
    multiple_recipient_count = len(list(filter(lambda q: len(q["To"]) > 1, headers)))
    multiple_recipient_percentage = round(multiple_recipient_count / len(headers) * 100, 2)
    print("{0} Emails ({1}%) were sent to more than one recipient"
          .format(multiple_recipient_count, multiple_recipient_percentage))

    # Check how many emails were sent to a single recipient
    single_recipient_count = len(list(filter(lambda q: len(q["To"]) == 1, headers)))
    single_recipient_percentage = round(single_recipient_count / len(headers) * 100, 2)
    print("{0} Emails ({1}%) were sent to only one recipient"
          .format(single_recipient_count, single_recipient_percentage))


def analyze_subjects(headers, words_to_strip):
    """ Creates a word cloud of all subjects"""
    util.log_print("Running Subject Analysis")
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
    plt.imsave("res/images/sub.png", word_cloud)


def analyze_content_types(headers, is_charset):
    """ Creates a pie chart of all content types or charsets"""
    if is_charset:
        util.log_print("Running Charset Analysis")
        content_types = list(map(lambda h: h["Content-Type"][1].split("=")[1], headers))
    else:
        util.log_print("Running Content Type Analysis")
        content_types = list(map(lambda h: h["Content-Type"][0], headers))

    unique_types = list(set(content_types))
    counts = []
    for t in unique_types:
        counts.append(unique_types.count(t))
    chart, ax1 = plt.subplots()
    ax1.pie(counts, labels=unique_types, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig("res/images/content" + str(is_charset) + ".png")
    plt.show()


def analyze_days(headers):
    """ Creates a bar chart showing the number of emails sent per day"""
    util.log_print("Running Day of Week Analysis")
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    email_days = list(map(lambda x: x["Date"][0].split(",")[0], headers))
    day_counts = []
    for day in days_of_week:
        day_counts.append(email_days.count(day))

    # Display statistics
    util.display_stats(day_counts, "Statistics for days on which emails are set:")

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
    plt.savefig("res/images/days.png")
    plt.show()


def analyze_months(headers):
    """ Creates a bar chart showing the number of emails sent per month """
    util.log_print("Running Month Analysis")
    months_of_year = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    email_months = list(map(lambda x: x["Date"][0].split(" ")[2], headers))
    month_counts = []
    for month in months_of_year:
        month_counts.append(email_months.count(month))

    # Display statistics
    util.display_stats(month_counts, "Statistics for months in which emails are sent:")

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
    plt.savefig("res/images/months.png")
    plt.show()


def analyze_years(headers):
    """ Creates a line chart showing the number of emails sent per year """
    util.log_print("Running Year Analysis")
    email_years = list(map(lambda x: x["Date"][0].split(" ")[3]
                           .replace("2000", "x")
                           .replace("000", "200")
                           .replace("x", "2000"), headers))
    unique_years = list(set(email_years))
    unique_years.sort()
    year_counts = []
    for year in unique_years:
        year_counts.append(email_years.count(year))

    # Display statistics
    util.display_stats(year_counts, "Statistics for years in which emails are sent:")

    # Configure line chart
    unique_years = list(map(int, unique_years))
    plt.plot(unique_years, year_counts, color='r', alpha=0.6)
    plt.xlim(1979, 2044)
    plt.ylabel('Number of Emails')
    plt.xlabel('Year')
    plt.title('Number of emails per year')
    plt.savefig("res/images/years.png")
    plt.show()


def analyze_times(headers):
    """ Creates a line chart showing the number of emails sent per hour """
    util.log_print("Running Time Analysis")
    hours = list(map(lambda x: int(x["Date"][0].split(" ")[4].split(":")[0]), headers))
    unique_hours = list(set(hours))
    unique_hours.sort()
    hours_count = []
    for hour in unique_hours:
        hours_count.append(hours.count(hour))

    # Display statistics
    util.display_stats(hours_count, "Statistics for hours in which emails are sent:")

    # Configure line chart
    plt.plot(unique_hours, hours_count, color='g', alpha=0.6)
    plt.xlim(0, 24)
    plt.ylabel('Number of Emails')
    plt.xlabel('Hour of Day')
    plt.title('Number of emails per hour')
    plt.savefig("res/images/hours.png")
    plt.show()


def analyze_domains(headers, top):
    """ Creates a horizontal bar chart showing the number of emails sent by the top domains """
    util.log_print("Running Domain Analysis")
    valid_headers = list(filter(lambda h: len(h["From"][0].split("@")) == 2, headers))
    domains = list(map(lambda h: h["From"][0].split("@")[1].split(".")[0], valid_headers))
    unique_domains = set(domains)
    domain_counts = {}
    counter = 0
    bar = util.ProgressBar(len(unique_domains), 'Analyzing domains', 72)
    for domain in unique_domains:
        domain_counts[domain] = domains.count(domain)
        bar.update(counter)
        counter += 1
    bar.clean()
    sorted_domain_counts = sorted(domain_counts.items(), key=operator.itemgetter(1))
    sorted_domain_counts.reverse()
    chart_domains = []
    chart_domain_counts = []
    print("Top {0} domains that sent emails:".format(top))
    for x in range(top):
        chart_domains.append(sorted_domain_counts[x][0])
        chart_domain_counts.append(sorted_domain_counts[x][1])
        # Print results
        print("{0}. {1} - {2} emails sent".format(x+1, sorted_domain_counts[x][0], sorted_domain_counts[x][1]))
    # Draw horizontal bar chart
    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = np.arange(len(chart_domains))
    ax.barh(y_pos, chart_domain_counts, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(chart_domains)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of emails sent')
    ax.set_title('Emails Sent per Domain')

    plt.savefig("res/images/domainsA.png")
    plt.show()


def get_max_senders(headers, top):
    """ Creates a bar chart showing the number of emails sent by the top senders """
    print("Running Max Senders Analysis")
    email_addresses = list(map(lambda h: h["From"][0].split("@")[0], headers))
    unique_addresses = list(set(email_addresses))
    address_counts = {}
    counter = 0
    bar = util.ProgressBar(len(unique_addresses), 'Analyzing uniqueness', 71)
    for address in unique_addresses:
        address_counts[address] = email_addresses.count(address)
        bar.update(counter)
        counter += 1
    bar.clean()
    sorted_address_counts = sorted(address_counts.items(), key=operator.itemgetter(1))
    sorted_address_counts.reverse()

    graph_emails = []
    graph_counts = []
    for x in range(top):
        graph_emails.append(sorted_address_counts[x][0])
        graph_counts.append(sorted_address_counts[x][1])

    # Display statistics
    util.display_stats(graph_counts, "Statistics for emails sent per person:")

    # Configure bar chart
    plt.tight_layout()
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

    plt.savefig("res/images/senders.png")
    plt.show()

