import time
import json
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 定义csv文件的列族
questions = []
answers = []
doc_infos = []
hospital_infos = []

# 选择断点续爬，并加载json文件
interrupt_point = input("是否断点续爬？ Y/N\n")
if interrupt_point.upper() == "Y":
    # 设置追加模式
    mode = "a"
    df = pd.read_csv("Depression_Unwashed.csv", encoding="utf-8")
    # 读取json文件
    URLS = json.load(open("BaiduHealth_urls.json", "r", encoding="utf-8"))["urls"][df.shape[0]:]
else:
    # 设置覆盖模式
    mode = "w"
    URLS = json.load(open("BaiduHealth_urls.json", "r", encoding="utf-8"))["urls"]

count = 0

# 设置无界面浏览器
option = webdriver.ChromeOptions()  # 创建一个配置对象
option.add_argument("--headless")  # 开启无界面模式
option.add_argument("--gpu")  # 禁用gpu
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不启用自动化工具
option.add_experimental_option('useAutomationExtension', False)  # 不使用自动化扩展

# 创建浏览器对象
browser = webdriver.Chrome(service=
                           Service(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'), options=option)

#  通过将 navigator.webdriver 的 get 方法重定义为返回 undefined，
#  可以欺骗网站的检测机制，让其认为浏览器不是通过自动化工具进行访问的，从而绕过一些反爬虫或反自动化的限制。
#  但似乎在百度上不起作用。
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                        {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})

# 创建显示等待对象
wait = WebDriverWait(browser, 30, poll_frequency=0.5)

print("开始爬取")
browser.get(URLS[0])
wait.until(EC.presence_of_element_located((By.ID, 'spread-fold')))
time.sleep(2)
for url in tqdm(URLS[1:]):
    try:
        count += 1
        # 每处理10条数据，写入一次CSV文件
        if count % 10 == 0:
            # 创建DataFrame对象
            data = {
                "问题": questions,
                "回答": answers,
                "医生信息": doc_infos,
                "医院信息": hospital_infos
            }
            # 空值用NaN填充
            df = pd.DataFrame(pd.DataFrame.from_dict(data, orient='index').values.T, columns=list(data.keys()))
            # 将DataFrame写入CSV文件
            df.to_csv('Depression_Unwashed.csv', sep=',', na_rep='', index=False, encoding="utf-8-sig", mode=mode)

        # 断点续爬为追加模式，需要清空列表
        if interrupt_point.upper() == "Y":
            questions, answers, doc_infos, hospital_infos = [], [], [], []

        # 标题
        title = browser.find_element(By.XPATH,
                                     "//div[@id='spread-fold']//p[@class='index_healthTitle__lpfdm hc-line-clamp2']")
        questions.append(title.text)

        # 回答
        content = browser.find_elements(By.XPATH,
                                        "//div[@id='spread-fold']//div[@class='index_textContent__CjNhL index_richText__OrVb1 index_richTextPc__IEcLL']/p")
        texts = "".join([i.text for i in content])
        answers.append(texts)

        # 医生信息
        doctor = browser.find_elements(By.XPATH,
                                       "//div[@id='spread-fold']//p[@class='index_nameInfo__9H6bC hc-line-clamp1']/span[position()<=2]")
        doc_info = "".join([i.text for i in doctor])
        doc_infos.append(doc_info)

        # 医院信息
        hospital_name = browser.find_element(By.XPATH,
                                             "//div[@id='spread-fold']//span[@class='index_hosName__EDr05 hc-line-clamp1']")
        hospital_level = browser.find_element(By.XPATH,
                                              "//div[@id='spread-fold']//div[@class='index_container__aTDkB']/span[position()=1]")
        hospital_infos.append(hospital_name.text + "\n" + hospital_level.text)

        # 下一页
        if url != URLS[-1]:
            browser.execute_script(f'window.open("{url}","_blank");')
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            wait.until(EC.presence_of_element_located((By.ID, 'spread-fold')))
            time.sleep(2)
        else:
            browser.close()
    # 针对部分AI医生的页面，没有医生信息和医院信息
    except NoSuchElementException as e:
        if url != URLS[-1]:
            browser.execute_script(f'window.open("{url}","_blank");')
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            wait.until(EC.presence_of_element_located((By.ID, 'spread-fold')))
            time.sleep(2)
        else:
            browser.close()
    # 针对百度反爬机制触发的情况，等待60s后重试
    except TimeoutException as e:
        time.sleep(60)
        if url != URLS[-1]:
            browser.execute_script(f'window.open("{url}","_blank");')
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            wait.until(EC.presence_of_element_located((By.ID, 'spread-fold')))
            time.sleep(3)
        else:
            browser.close()
print("爬取完成，共爬取{}条数据，成功{}条，失败{}条".format(count, len(questions), count - len(questions)))

if interrupt_point.upper() != "Y":
    # 创建DataFrame对象
    data = {
        "问题": questions,
        "回答": answers,
        "医生信息": doc_infos,
        "医院信息": hospital_infos
    }

    df = pd.DataFrame(pd.DataFrame.from_dict(data, orient='index').values.T, columns=list(data.keys()))
    # 将DataFrame写入CSV文件
    df.to_csv('Depression_Unwashed.csv', sep=',', na_rep='', index=False, encoding="utf-8-sig")
