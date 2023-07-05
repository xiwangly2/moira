import os
import re
import time
from urllib.parse import urlparse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def extract_image_urls_from_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用正则表达式提取图片URL
        image_urls = re.findall(r'!\[.*?\]\((.*?)\)', content)
        return image_urls

def save_images_from_markdown_directory(directory):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    chrome_options = Options()
    # 设置Chrome浏览器有界面模式，注释掉--headless
    # chrome_options.add_argument('--headless')
    # 指定Chrome浏览器驱动程序路径，请根据实际情况进行修改
    chrome_driver_path = 'E:\\Program Files (x86)\\chromedriver_win32\\chromedriver.exe'  # 将路径替换为实际的驱动程序路径

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                image_urls = extract_image_urls_from_markdown_file(file_path)
                image_dir = os.path.join(root, 'images')
                os.makedirs(image_dir, exist_ok=True)  # 创建保存图片的目录

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 创建浏览器实例
                driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)

                for url in image_urls:
                    # 检查URL是否以http://或https://开头
                    if url.startswith('http://') or url.startswith('https://'):
                        try:
                            # 使用Selenium打开网页
                            driver.get(url)
                            time.sleep(2)  # 等待页面加载完成，可根据实际情况调整等待时间

                            # 获取图片元素
                            img_element = driver.find_element_by_tag_name('img')

                            # 获取图片URL
                            image_url = img_element.get_attribute('src')

                            # 下载图片
                            response = requests.get(image_url, headers=headers)
                            if response.status_code == 200:
                                filename = os.path.basename(urlparse(image_url).path)
                                save_path = os.path.join(image_dir, filename)
                                with open(save_path, 'wb') as f:
                                    f.write(response.content)
                                print(f'Saved image: {save_path}')
                                # 替换Markdown文档中的URL为相对路径
                                relative_path = os.path.relpath(save_path, os.path.dirname(file_path))
                                content = content.replace(url, relative_path.replace("\\", "/"))
                                print(f'Replaced URL in Markdown: {url} -> {relative_path}')
                                time.sleep(5)  # 添加1秒的延迟
                            else:
                                print(f'Error downloading image: {url} - HTTP status code: {response.status_code}')
                        except Exception as e:
                            print(f'Error downloading image: {url}')
                            print(e)

                # 关闭浏览器
                driver.quit()

                # 将修改后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

# 设置Markdown文档所在的目录
markdown_directory = './docs/七政四餘星盤 天星擇日 占星盤 - Moira/'

save_images_from_markdown_directory(markdown_directory)
