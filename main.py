import logging
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import config
from mail import emailSendInfo
from log import console_logger, file_logger

### 读取中证800 PE-TTM
def getLixinger(website, usr_name, password):
    lixinger_usr_name = usr_name
    lixinger_password = password

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage') # 服务端需要加入此选项
    browser = webdriver.Chrome(options = chrome_options)
    browser.get(website)
    sleep(random.uniform(2, 3))

    ### 在主页面点击登录按钮，进入登录界面
    browser.find_element(By.XPATH,
                         '/html/body/div[3]/header/nav/ul[2]/li[2]/a').click()
    sleep(random.uniform(1, 2))
    ### 输入账号和密码
    browser.find_element(By.XPATH,
                         '/html/body/div[9]/div[1]/div/div/div[2]/div[1]/div/div/form/div[1]/input').send_keys(lixinger_usr_name)
    sleep(random.uniform(1, 2))
    browser.find_element(By.XPATH,
                         '/html/body/div[9]/div[1]/div/div/div[2]/div[1]/div/div/form/div[2]/input').send_keys(lixinger_password)
    ### 点击登录按钮
    browser.find_element(By.XPATH,
                         '/html/body/div[9]/div[1]/div/div/div[2]/div[1]/div/div/form/div[3]/div[2]/button').click()
    sleep(random.uniform(2, 3))

    ### 搜索框中输入中证800
    browser.find_element(By.XPATH,
                         '/html/body/div[4]/header/nav/form/div/div/div[2]').click()  # .send_keys("中证800")
    sleep(random.uniform(1, 2))
    browser.find_element(By.XPATH,
                         '/html/body/div[4]/header/nav/form/div/div/div[2]/input').send_keys("中证800")
    sleep(random.uniform(1, 2))
    browser.find_element(By.XPATH,
                         '/html/body/div[4]/header/nav/form/div/div/div[1]/span').click()
    sleep(random.uniform(1, 2))

    value = browser.find_element(By.XPATH,
                                 '/html/body/div[4]/div[1]/div[2]/div[5]/div/div[2]/div[2]/div[1]/div/div[1]/ul/li[1]/span[2]').text
    value = float(value)
    sleep(random.uniform(1, 2))
    browser.close()
    return value

### 读取macroview.club十年期国债收益率
def getBondYields(website):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options = chrome_options)
    browser.get(website)
    sleep(random.uniform(1, 2))

    value = browser.find_element(By.XPATH,
                         '/html/body/div[3]/div[2]/div[1]/div[2]/span[2]/em').text
    value = float(value)
    sleep(random.uniform(0, 1))
    browser.close()
    return value

### 获得集思录可转债中位数
def getConvertibleBond(website):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options = chrome_options)
    browser.get(website)
    sleep(random.uniform(1, 3))

    browser.find_element(By.XPATH,
                         '//*[@id="nav_data"]').click()
    sleep(random.uniform(1, 2))

    browser.find_element(By.XPATH,
                         '/html/body/div/div/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/a').click()
    sleep(random.uniform(1, 2))

    value = browser.find_element(By.XPATH,
                         '/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/span[6]').text
    value = value.split(' ')[-1]
    value = float(value)

    sleep(random.uniform(0, 1))
    browser.close()
    return value

### 基金推荐指数
def getFundClass(PE_TTM, bond_yields):
    level = 1.0 / PE_TTM / bond_yields * 100.0
    if level > 3.0:
        return "股市吸引力指数: {:.3f}, 粉钻机会".format(level)
    if level < 3.0 and level >= 2.5:
        return "股市吸引力指数: {:.3f}, 黄金机会".format(level)
    if level < 2.5 and level >= 2.0:
        return "股市吸引力指数: {:.3f}, 机会风险共存".format(level)
    if level < 2.0 and level >= 1.5:
        return "股市吸引力指数: {:.3f}, 风险较高".format(level)
    if level < 1.5 and level >= 0.0:
        return "股市吸引力指数: {:.3f}, 泡沫期".format(level)
    return "基金推荐指数数据出现异常"

### 可转债推荐指数
def getConvertibleClass(median):
    if median < 100.0:
        return "可转债吸引力指数: {:.3f}, 粉钻机会".format(median)
    if median < 110.0 and median >= 100.0:
        return "可转债吸引力指数: {:.3f}, 黄金机会".format(median)
    if median < 115.0 and median >= 110.0:
        return "可转债吸引力指数: {:.3f}, 机会风险共存".format(median)
    if median < 120.0 and median >= 115.0:
        return "可转债吸引力指数: {:.3f}, 风险较高".format(median)
    if median >= 120.0:
        return "可转债吸引力指数: {:.3f}, 泡沫期".format(median)
    return "可转债推荐指数数据出现异常"

def main():

    lixinger_website = config.lixinger_website
    lixinger_usr_name = config.lixinger_usr_name
    lixinger_password = config.lixinger_password

    investing_website = config.investing_website

    jisilu_website = config.jisilu_website

    pe_value = getLixinger(lixinger_website, lixinger_usr_name, lixinger_password)
    file_logger.info("中证800 PE-TTM: {}".format(pe_value))

    earning_ratio_value = getBondYields(investing_website)
    file_logger.info("中国十年期国债收益率: {}".format(earning_ratio_value))

    convert_value = getConvertibleBond(jisilu_website)
    file_logger.info("可转债中位数价格: {}".format(convert_value))

    ### 基金推荐指数
    fund_level_info = getFundClass(pe_value, earning_ratio_value)
    ### 可转债推荐指数
    convert_level_info = getConvertibleClass(convert_value)
    file_logger.info(fund_level_info)
    file_logger.info(convert_level_info)

    ### 邮件定期提醒基金和可转债星级推荐
    content = fund_level_info + '\n' + convert_level_info
    emailSendInfo('基金可转债星级指数', content)


### 定时启动
def timerSchedule():
    timer = threading.Timer(12*60*60, repeatTask)
    timer.start()

def repeatTask():
    main()
    timerSchedule()

if __name__ == '__main__':
    timerSchedule()





