import requests
import io
import json
from bs4 import BeautifulSoup
from general import *

def init_company_category_files():
    projectName = 'ITVIEC'
    url = 'https://itviec.com/jobs-company-index'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    for link in soup.findAll('a', {'class':'link--darker'}):
        href = "https://itviec.com" + link.get('href')
        title = link.string
        fileName = projectName + '/' + title +'.json'
        create_data_file(fileName)

def format_title(title):
    rep_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|','.',',','(',')','{','}','[',']']

    for char in rep_chars:
        title = title.replace(char, '')
    return title

def get_company_by_category(url, projectName):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    for link in soup.findAll('a', {'class':'mkt-track skill-tag__link'}):
        href = "https://itviec.com" + link.get('href')
        title = link.string
        companyFileName = projectName + '/' + format_title(title) + '.json'
        get_info_company(href, companyFileName)
        #append to file
        # path = saveFile
        # data = {'link':href,'name':title}
        # # Write JSON file
        # with io.open(path, 'a', encoding='utf8') as outfile:
        #     str_ = json.dumps(data,
        #                       indent=4, sort_keys=True,
        #                       separators=(',', ': '), ensure_ascii=False)
        #     outfile.write(str_ + ',' + '\n')

def get_company_for_each_category():
    projectName = 'ITVIEC'
    string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    i = 0
    while i<len(string)-3:
        if(string[i] == 'S' or string[i] == 'W'):
            category = string[i] + string[i + 1] + string[i + 2] + string[i + 3]
            prefix = string[i].lower() +'-' + string[i+3].lower()
            i = i + 4
        else:
            category = string[i] + string[i + 1] + string[i + 2]
            prefix = string[i].lower()+'-'+string[i + 2].lower()
            i = i + 3

        if string[i-3] == 'A' and i<len(string)-4:
            url = 'https://itviec.com/jobs-company-index'
        else:
            url = 'https://itviec.com/jobs-company-index/' + prefix

        filePath = projectName + '/' + category + '.json'
        get_company_by_category(url, projectName)

def get_jobs_of_company(url):
    jobs = []
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    for job in soup.findAll('div', {'class':'job'}):
        nameTag = job.find('h4',{'class':'title'})
        nameLink = nameTag.find('a')
        link =  "https://itviec.com" + nameLink.get('href')
        name = nameLink.string
        descriptionTag = job.find('div',{'class':'description hidden-xs'})
        description = descriptionTag.text.replace('\n', '')
        skills = []
        for skillTag in job.findAll('a', {'class':'job__skill ilabel mkt-track'}):
            skill = skillTag.find('span')
            skills.append(skill.text.replace('\n',''))

        data = {'name': name, 'link': link, 'description': description, 'skills':skills}
        jobs.append(data)

    return jobs
        # # Write JSON file
        # with io.open(saveFile, 'a', encoding='utf8') as outfile:
        #     str_ = json.dumps(data, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
        #     outfile.write(str_ + ',' + '\n')


def get_info_company(url, saveFile):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    divHeader = soup.find('div', {'class':'headers visible-xs'})

    nameTag = divHeader.find('h1', {'class':'employer-name'})
    srcTag = divHeader.find('img')
    positionTag = divHeader.find('i', {'class':'fa fa-map-marker'})

    typeCompanyTag = divHeader.find('span', {'class':'gear-icon'})

    workingTimeTagCalender = divHeader.find('i', {'class':'fa fa-calendar'})
    workingTimeTag = None
    if workingTimeTagCalender is not None:
        workingTimeParentTag = workingTimeTagCalender.parent
        workingTimeTag = workingTimeParentTag.find('span')


    oTTagClock = divHeader.find('i', {'class':'fa fa-clock-o'})
    oTTag = None
    if oTTagClock is not None:
        oTTagParent = oTTagClock.parent
        oTTag = oTTagParent.find('span')

    name = nameTag.string.replace('\n','')
    src = srcTag.attrs['src']
    position = positionTag.nextSibling.replace('\n','')
    typeCompany = typeCompanyTag.string.replace('\n','')

    workingTime = None
    if workingTimeTag is not None:
        workingTime = workingTimeTag.string.replace('\n','')

    oT = None
    if oTTag is not None:
        oT = oTTag.string.replace('\n','')

    jobs = get_jobs_of_company(url)

    data = {'name':name, 'logo':src, 'position':position, 'company-type':typeCompany, 'working-time':workingTime, 'OT':oT, 'jobs':jobs}
    # Write JSON file
    with io.open(saveFile, 'a', encoding='utf8') as outfile:
        str_ = json.dumps(data, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
        outfile.write(str_ + ',' + '\n')

def get_detail_all_company():
    url = 'https://itviec.com/companies/adon'
    saveFile = 'adon.json'
    get_info_company(url, saveFile)
    # get_jobs_of_company(url, saveFile)

# get_detail_all_company()
get_company_for_each_category()

#init_company_category_files()
#get_company_by_category('DEF')

#craw_data_itViec()