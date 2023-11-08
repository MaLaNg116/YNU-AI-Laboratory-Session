from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
import json

URLS = []
num = 500  # 爬取的数据量
count = 0
page_element = None
last = False
service = Service(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')

# 设置无界面浏览器
option = webdriver.ChromeOptions()  # 创建一个配置对象
option.add_argument("--headless")  # 开启无界面模式
option.add_argument("--gpu")  # 启用gpu
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不启用自动化工具
option.add_experimental_option('useAutomationExtension', False)  # 不使用自动化扩展

browser = webdriver.Chrome(service=service, options=option)

#  通过将 navigator.webdriver 的 get 方法重定义为返回 undefined，
#  可以欺骗网站的检测机制，让其认为浏览器不是通过自动化工具进行访问的，从而绕过一些反爬虫或反自动化的限制。
#  但似乎在百度上不起作用。
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                        {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})

browser.get("https://www.baidu.com")
wait = WebDriverWait(browser, 5, poll_frequency=0.5)
search = wait.until(EC.presence_of_element_located((By.ID, 'kw')))
# 限制检索内容为百度健康
search.send_keys('抑郁 inurl:health.baidu.com')
search.send_keys(Keys.ENTER)

while True:
    # 等待页面加载完成
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    # mu属性为百度健康的原链接，ar为文章形式
    result = browser.find_elements(By.XPATH,
                                   "//div[@id='content_left']/div[starts-with(@mu,'https://health.baidu.com/m/detail/ar')]")
    result_urls = [i.get_attribute('mu') for i in result]
    for i in result_urls:
        URLS.append(i)
    # 爬取数据量达到num时停止
    if len(URLS) >= num:
        break

    # 预防StaleElementReferenceException, ElementClickInterceptedException
    temp = 0
    while temp < 2:
        try:
            # 下一页
            page_element = browser.find_elements(By.XPATH,
                                                 "//div[@id='page']/div[@class='page-inner_2jZi2']/strong/following-sibling::a[1]")
            if len(page_element) == 0:
                last = True
                # 无下一页，则退出循环
                print("已是最后一页")
                # 关闭浏览器
                browser.close()
                break
            else:
                page_element[0].click()
                browser.implicitly_wait(5)
            break
        except StaleElementReferenceException:
            temp += 1
            continue
        except ElementClickInterceptedException:
            temp += 1
            continue
    if not last:
        print(f"当前页{int(page_element[0].text) - 1}, 当前爬取了{len(URLS)}条数据")
    else:
        break
print(f"爬取完成！共爬取了{len(URLS)}条数据")

data = {
    "urls": URLS
}

# 将urls写入json文件
with open("BaiduHealth_urls.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
