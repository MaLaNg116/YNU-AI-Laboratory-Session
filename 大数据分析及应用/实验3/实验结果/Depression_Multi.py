import json
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.common.exceptions import NoSuchElementException, TimeoutException

questions = []
answers = []
doc_infos = []
hospital_infos = []
success_num = 0
fail_num = 0

MAX_WORKERS = 10
service = Service(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
URLS = json.load(open('BaiduHealth_urls.json', 'r'))["urls"][400:]

# 设置无界面浏览器
option = webdriver.ChromeOptions()  # 创建一个配置对象
option.add_argument("--headless")  # 开启无界面模式
option.add_argument("--gpu")  # 启用gpu
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不启用自动化工具
option.add_experimental_option('useAutomationExtension', False)  # 不使用自动化扩展


def start_browser():
    browser = webdriver.Chrome(service=service, options=option)
    return browser


def browser_task(browser: webdriver.Chrome, idx: int):
    global success_num, fail_num
    wait = WebDriverWait(browser, 5, poll_frequency=0.5)
    try:
        if idx <= 5:
            browser.get(URLS[idx])
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.ID, 'spread-fold')))
        else:
            # 为下一页创建新的标签页
            browser.execute_script(f'window.open("{URLS[idx]}","_blank");')
            # 关闭当前标签页
            browser.close()
            # 切换到新标签页
            browser.switch_to.window(browser.window_handles[-1])
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.ID, 'spread-fold')))

        title = browser.find_element(By.XPATH,
                                     "//div[@id='spread-fold']//p[@class='index_healthTitle__lpfdm hc-line-clamp2']")
        questions.append(title.text)

        content = browser.find_elements(By.XPATH,
                                        "//div[@id='spread-fold']//div[@class='index_textContent__CjNhL index_richText__OrVb1 index_richTextPc__IEcLL']/p")
        texts = "".join([i.text for i in content])
        answers.append(texts)

        doctor = browser.find_elements(By.XPATH,
                                       "//div[@id='spread-fold']//p[@class='index_nameInfo__9H6bC hc-line-clamp1']/span[position()<=2]")
        doc_info = "".join([i.text for i in doctor])
        doc_infos.append(doc_info)

        hospital_name = browser.find_element(By.XPATH,
                                             "//div[@id='spread-fold']//span[@class='index_hosName__EDr05 hc-line-clamp1']")
        hospital_level = browser.find_element(By.XPATH,
                                              "//div[@id='spread-fold']//div[@class='index_container__aTDkB']/span[position()=1]")
        hospital_infos.append(hospital_name.text + "\n" + hospital_level.text)
        success_num += 1
        if idx % 20 == 0:
            print(f"当前爬取了{idx}条数据")
        if idx >= len(URLS) - MAX_WORKERS:
            return "Done!"
        else:
            browser_task(browser, idx + MAX_WORKERS)
    except NoSuchElementException:
        if idx >= len(URLS) - MAX_WORKERS:
            fail_num += 1
            return "Done!"
        else:
            fail_num += 1
            browser_task(browser, idx + MAX_WORKERS)
    except TimeoutException:
        if idx >= len(URLS) - MAX_WORKERS:
            fail_num += 1
            return "Done!"
        else:
            fail_num += 1
            browser_task(browser, idx + MAX_WORKERS)
    except IndexError:
        return "Done!"


def main():
    global URLS
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    ths = list()
    for idx in range(5):
        time.sleep(2)
        browser = start_browser()
        th = executor.submit(browser_task, browser, idx=idx)
        ths.append(th)

    for future in as_completed(ths):
        print(future.result())


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    data = {
        "问题": questions,
        "回答": answers,
        "医生信息": doc_infos,
        "医院信息": hospital_infos
    }
    df = pd.DataFrame(pd.DataFrame.from_dict(data, orient='index').values.T, columns=list(data.keys()))

    # 将DataFrame写入CSV文件
    df.to_csv('BaiduHealth_Depression_Threadpool.csv', sep=',', na_rep='', index=False, encoding="utf-8-sig")
    print("总耗时：{:.2f}".format(end - start))
    print(f"应爬取{len(URLS)}条数据，成功{success_num}条，失败{fail_num}条")
