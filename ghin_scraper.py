from bs4 import BeautifulSoup
from html.parser import HTMLParser
import csv
import time
from selenium import webdriver
from copy import copy

def xpath_soup(element):
    # https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
    # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
    """
    Generate xpath from BeautifulSoup4 element.
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str
    Usage
    -----
    >>> import bs4
    >>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    >>> import bs4
    >>> xml = '<doc><elm/><elm/></doc>'
    >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    >>> xpath_soup(soup.doc.elm.next_sibling)
    '/doc/elm[2]'
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def handle_regular(s):
    score = s.find('div', attrs={'class':"card__cell esc-score"})
    date = s.find('div', attrs={'class':"card__cell date"})
    rating = s.find('div', attrs={'class':"card__cell rating-slope"})
    pcc = s.find('div', attrs={'class':"card__cell pcc"})
    diff = s.find('div', attrs={'class':"card__cell differential"})
    course = s.find('div', attrs={'class':"card__cell course"})
    #stats = s.find('div', attrs={'class':"card__cell stats"})
    return score, date, rating, pcc, diff, course

def handle_combined(combined_button):
    path = xpath_soup(combined_button)
    button = browser.find_elements_by_xpath(path)[0]
    button.click()

    html_combined = browser.page_source
    time.sleep(2)
    parsed_html_combined = BeautifulSoup(html_combined, features="html.parser")
    cscores = parsed_html_combined.findAll('div', attrs={'class':"stats__column combined-score"})
    score1_info_list = cscores[0].findAll('div', attrs={'class':"combined-score-info"})
    score2_info_list = cscores[1].findAll('div', attrs={'class':"combined-score-info"})
    score1 = score1_info_list[0].find(text=True, recursive=False)
    course1 = score1_info_list[1].find(text=True, recursive=False)
    date1 = score1_info_list[2].find(text=True, recursive=False)
    score2 = score2_info_list[0].find(text=True, recursive=False)
    course2 = score2_info_list[1].find(text=True, recursive=False)
    date2 = score2_info_list[2].find(text=True, recursive=False)

    close = browser.find_element_by_class_name("modal_close")
    close.click()
    return score1, course1, date1, score2, course2, date2

browser = webdriver.Firefox()
browser.get("https://www.ghin.com")

input("Login and navigate to the page with the scores you want to export. Then press Enter to continue...")

html = browser.page_source
time.sleep(2)

parsed_html = BeautifulSoup(html, features="html.parser")
scores = parsed_html.findAll('div', attrs={'class':"card"})

row = {}
rows = []
combined_row = {}
combined_rows = []
combined_count = 0
for s in scores:
    combined_id = 0
    score,date,rating,pcc,diff,course = handle_regular(s)

    combined_score = score.find('button')
    if combined_score is not None:
        combined_count = combined_count + 1
        combined_id = copy(combined_count)
        score1,course1,date1,score2,course2,date2 = handle_combined(combined_score)
        combined_row = {'ID': combined_id, 'Score1': score1.strip(), 'Course1': course1.strip(), 'Date1': date1.strip(), 'Score2': score2.strip(), 'Course2': course2.strip(), 'Date2': date2.strip()}
        combined_rows.append(combined_row)

    row = {'Score': score.text, 'Date': date.text, 'Rating': rating.text, 'PCC': pcc.text, 'Diff': diff.text, 'Course': course.text.strip(), 'Combined ID': combined_id}
    rows.append(row)

output_file = input("Enter an output file name (must have .csv extension):")

with open(output_file, 'w+') as f:
    writer = csv.DictWriter(f, fieldnames=['Score', 'Date', 'Rating', 'PCC', 'Diff', 'Course', 'Combined ID'])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

    combined_writer = csv.DictWriter(f, fieldnames=['ID', 'Score1', 'Course1', 'Date1', 'Score2', 'Course2', 'Date2'])
    combined_writer.writeheader()
    for cr in combined_rows:
        combined_writer.writerow(cr)

browser.close()
exit(0)

