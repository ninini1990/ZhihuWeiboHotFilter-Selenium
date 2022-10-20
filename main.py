# Author: 尼尼尼@知乎
# Author: 备份公众号： 尼尼尼不打拳
# HomePage: https://www.zhihu.com/people/nidaye2
# Version: 1.1

import os
import time
import webbrowser
# import requests
import json
# from requests_html import HTMLSession

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys


# 定义知乎和微博热榜页面地址
zhihuHotUrl = 'https://www.zhihu.com/hot'
# weiboHotUrl = 'https://weibo.com/ajax/statuses/hot_band'
# weiboHotUrl = 'https://weibo.com/hot/search' # 热搜动态刷新页面
weiboHotUrl = 'https://s.weibo.com/top/summary?cate=realtimehot'  #找到了热搜静态页面
jsonPath = 'config.json'

# 定义关键词数组
# keyWordList = ['男', '女', '儿', '婚', '孕', '彩礼', '嫁', '娶', '骚扰', '姑', '娘', '姐', '妹', '哥', '兄', '弟', '暴',
#                '偷拍', '妇', '夫', '妻', '父', '母', '爹', '妈', '婴', '童', '教授', '奸', '亵', '嫖', '孩',
#                '杨笠', '张桂梅', '卫生巾']


# 读取配置文件
def readJson(jsonPath):
    f = open(jsonPath, 'r', encoding='UTF-8')
    data = json.load(f)
    f.close()
    return data

# 获取系统用户目录名称
def getWinUserName():
    winUserHome = os.path.expanduser('~')
    winUserName =os.path.split(winUserHome)[-1]
    return winUserName


# 获取用户桌面路径, 输出结果"C:\Users\UserName\Desktop\"
def getWinDesktopPath():
    winUserName = getWinUserName()
    winDesktopPath = "C:\\Users\\" + winUserName + "\\Desktop\\"
    return winDesktopPath

# 报单独处理告文件名的时间戳
def getReportTimeStamp():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

# 设置Selenium浏览器参数(无头模式，模拟iPad Air)
def getBrowserOptions():
    mobileEmulation = {'deviceName': 'iPad Air'}
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_experimental_option('mobileEmulation', mobileEmulation)
    opts.add_experimental_option("excludeSwitches", ['enable-automation'])
    return opts

# 初始化浏览器
def initBrowser(url):
    print('开始初始化浏览器...')
    try:
        opts = getBrowserOptions()
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        browser.implicitly_wait(10)
        browser.get(url)
        time.sleep(5)
        print('浏览器初始化完成')
        return browser

    except Exception as e:
        print(e, '浏览器未启动, 或初始化失败')

# 字典去重
def deleteDuplicate(li):
    temp_list = list(set([str(i) for i in li]))
    li = [eval(i) for i in temp_list]
    return li

# 过滤话题
def filterLinks(list, keyWordList):
    tempList = []
    for item in list:
        title = item['title']
        for word in keyWordList:
            if word in title:
                tempList.append(item)
                continue
    li = deleteDuplicate(tempList)
    #li = deleteDuplicate(list)
    return li


# 过滤知乎热榜话题
def filterZhihuHot(keyWordList):
    print('开始获取知乎热榜')
    zhihuHotLinks = []
    driver = initBrowser(zhihuHotUrl)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # for i in range(5):
    #     driver.execute_script("window.scrollBy(0, 1000)")
    #     time.sleep(3)

    links = driver.find_elements(By.CSS_SELECTOR, "a[href ^= 'https://www.zhihu.com/question']")
    print(len(links))

    for item in links:
        link = item.get_property('href')
        titleNode = item.find_element(By.CSS_SELECTOR, "h1")
        title = titleNode.text
        temp = {'link': link, 'title': title}
        zhihuHotLinks.append(temp)
    filterZhihuList = filterLinks(zhihuHotLinks, keyWordList)
    print(len(filterZhihuList))
    print('知乎热榜过滤完成')
    return filterZhihuList


# 过滤知乎热搜话题
# def filterZhihuHot():
#     links = []
#     zhihuHotLinks = []
#
#     print('获取知乎热搜Json数据')
#
#     # 知乎需要模拟请求头为移动端
#     hds = {
#       "Content-Type": "application/json;charset=UTF-8",
#       "Referer": "https://www.zhihu.com",
#       "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
#     }
#
#     response = requests.get(zhihuHotUrl, headers=hds, timeout=5)
#     # print(response.content)
#     print(response.text)
#
#     resDict = json.loads(response.text)
#     print(resDict)
#     hotDict = resDict['data']['band_list']
#     print(hotDict)
#
#     for item in hotDict:
#         link = ''
#         title = item['word']
#         temp = {'link': link, 'title': title}
#         zhihuHotLinks.append(temp)
#
#     filterWeiboList = filterLinks(zhihuHotLinks)
#     print('微博热搜过滤完成')
#
#     return zhihuHotLinks


# 过滤微博热搜话题
# 微博热搜是动态加载，需要滚动逐屏抓取 -- 抓不到，放弃
# 改用一个直接返回json数据的接口，但是里面只有标题没有链接，凑合看了。
# def filterWeiboHot():
#     links = []
#     weiboHotLinks = []
#
#     print('获取微博热搜Json数据')
#
#     response = requests.get(weiboHotUrl, timeout=5)
#     resDict = json.loads(response.text)
#     hotDict = resDict['data']['band_list']
#     print(hotDict)
#
#     for item in hotDict:
#         link = ''
#         title = item['word']
#         temp = {'link': link, 'title': title}
#         weiboHotLinks.append(temp)
#
#     filterWeiboList = filterLinks(weiboHotLinks)
#     print('微博热搜过滤完成')
#
#     return weiboHotLinks

# 微博热搜是动态加载，需要滚动逐屏抓取 -- 抓不到，放弃
# 改用一个直接返回json数据的接口，但是里面只有标题没有链接，凑合看了。
def filterWeiboHot(keyWordList):
    weiboHotLinks = []

    print('获取微博热搜数据')
    driver = initBrowser(weiboHotUrl)
    time.sleep(10)

    # hotButton = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="热搜榜"]'))
    # )

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # elements = driver.find_elements(By.CSS_SELECTOR, 'div[class="vue-recycle-scroller__item-view"]')
    #
    # for item in elements:
    #     linkNode = item.find_element(By.CSS_SELECTOR, "a")
    #     link = linkNode.get_property('href')
    #     titleNode = item.find_element(By.CSS_SELECTOR,'div[class="HotTopic_tit_eS4fv"]')
    #     title = titleNode.text
    #     temp = {'link': link, 'title': title}
    #     weiboHotLinks.append(temp)


    # 对于微博热搜动态页面

    # for i in range(10):
    #     elements = driver.find_elements(By.CSS_SELECTOR, 'div[class="vue-recycle-scroller__item-view"]')
    #
    #     for item in elements:
    #         linkNode = item.find_element(By.CSS_SELECTOR, "a")
    #         link = linkNode.get_property('href')
    #         titleNode = item.find_element(By.CSS_SELECTOR,'div[class="HotTopic_tit_eS4fv"]')
    #         title = titleNode.text
    #         temp = {'link': link, 'title': title}
    #         weiboHotLinks.append(temp)
    #
    #     driver.execute_script("window.scrollBy(0, 300)")
    #     time.sleep(10)


    # 对于微博热搜静态页面的处理
    elements = driver.find_elements(By.CSS_SELECTOR, 'ul[class="list_a"] > li')
    for item in elements:
        linkNode = item.find_element(By.CSS_SELECTOR, 'a')
        link = linkNode.get_property('href')
        titleNode = item.find_element(By.CSS_SELECTOR, 'span')
        title = titleNode.text
        temp = {'link': link, 'title': title}
        weiboHotLinks.append(temp)

    print(len(weiboHotLinks))
    filterWeiboList = filterLinks(weiboHotLinks, keyWordList)
    print('微博热搜过滤完成')
    print(len(filterWeiboList))

    # return weiboHotLinks
    return filterWeiboList

# 组装展示结果
def assembleResult(listZhihu, listWeibo, saveToDesktop):
    # 组装html
    htmlHeader = '<!DOCTYPE html><html lang="cn"><head><meta charset="utf-8"></head><body>'

    summary = '<div><b>可能感兴趣的热榜话题</b><p><table>'

    table = '<th align="left">知乎列表</th>'

    # 填充报告页面
    if (len(listZhihu) != 0):
        for item in listZhihu:
            link = '<a href=' + item['link'] + ' target = "_blank">' + item['title'] + '</a>'
            cell = '<tr><td>' + link + '</td></tr>'
            table = table + cell

    table = table + '<p><tr align="left"><td><b>微博列表<b></td></tr>'

    if (len(listWeibo) != 0):
        for item in listWeibo:
            link = '<a href=' + item['link'] + ' target = "_blank">' + item['title'] + '</a>'
            cell = '<tr><td>' + link + '</td></tr>'
            table = table + cell

    htmlFoot = '</table></div></body></html>'
    reportPage = htmlHeader + summary + table + htmlFoot

    reportFileName = 'hot_report_' + getReportTimeStamp() + '.html'

    # 根据用户设置判断是否保存到桌面，如果不为1则保存到同一路径下
    if saveToDesktop == 1:
        reportFilePath = getWinDesktopPath() + reportFileName
    else:
        reportFilePath = reportFileName

    try:
        f = open(reportFilePath, 'w', encoding="utf-8")
        f.write(reportPage)
        f.close()
        print("生成报告文件成功:  {0}".format(reportFilePath))
        return reportFilePath
    except Exception as e:
        print(e, "生成报告文件失败")

# 邮件发送函数

# 主流程函数
def main():

    # 读取用户设置
    data = readJson(jsonPath)
    keyWordList = data['keyWordList'].split(',')
    saveToDesktop = int(data['saveToDesktop'])
    autoOpenResult = int(data ['autoOpenResult'])



    listZhihu =filterZhihuHot(keyWordList)
    #listZhihu = []
    listWeibo= filterWeiboHot(keyWordList)
    # listWeibo = []
    reportPath = assembleResult(listZhihu, listWeibo, saveToDesktop)

    # 根据用户设置判断是否自动打开结果文件
    if autoOpenResult == 1:
        webbrowser.open(reportPath)

    # 根据用户设置判断是否发送邮件, 为1时发送
    sendMail = int(data['sendMail'])
    if sendMail == 1:
        # 邮件设置
        mail_host = data['mail_host']
        mail_port = data['mail_port']
        mail_user = data['mail_user']
        mail_pass = data['mail_pass']
        sender = data['sender']
        receiver = data['receiver']

        # 组装邮件内容
        msg = MIMEMultipart()
        msg['From'] = formataddr(['话题通知', sender])
        msg['To'] = formataddr(['', receiver])
        msg['Subject'] = '知乎、微博热榜兴趣话题 ' + getReportTimeStamp()
        # 邮件正文内容
        file = open(reportPath, 'rb')
        htmlText = file.read()
        file.close()
        msg.attach(MIMEText(htmlText, _subtype='html',  _charset='utf-8'))

        # 构造附件
        # xlsxpart = MIMEApplication(open(reportPath, 'rb').read())
        # filename表示邮件中显示的附件名
        # xlsxpart.add_header('Content-Disposition', 'attachment', filename='%s' % reportPath)
        # msg.attach(xlsxpart)

        # SMTP服务器
        server = smtplib.SMTP_SSL(mail_host, mail_port, timeout=10)
        # 登录账户
        server.login(mail_user, mail_pass)
        # 发送邮件
        server.sendmail(sender, [receiver, ], msg.as_string())
        # 退出账户
        server.quit()
        print('发送通知邮件成功')

    print('执行完毕')
    input('按回车键退出...')

# 主函数入口
main()
