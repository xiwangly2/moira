import os
import re
import time
import requests
from urllib.parse import urlparse

def extract_image_urls_from_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用正则表达式提取图片URL
        image_urls = re.findall(r'!\[.*?\]\((.*?)\)', content)
        return image_urls

def save_images_from_markdown_directory(directory):
    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8',
'Cache-Control': 'no-cache',
'Dnt': '1',
'Pragma': 'no-cache',
'Referer': 'https://sites.google.com/',
'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
'Sec-Ch-Ua-Mobile': '?0',
'Sec-Ch-Ua-Platform': "Windows",
'Sec-Fetch-Dest': 'image',
'Sec-Fetch-Mode': 'no-cors',
'Sec-Fetch-Site': 'cross-site',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
'X-Client-Data': 'CJC2yQEIprbJAQipncoBCOmBywEIlqHLAQiLq8wBCJz+zAEIhZPNAQiFoM0BCO2zzQEI2rTNAQi/tc0BCNy9zQEIu77NAQilv80BCP6/zQE='
    }

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

                for url in image_urls:
                    # 检查URL是否以http://或https://开头
                    if url.startswith('http://') or url.startswith('https://'):
                        try:
                            response = requests.get(url, headers=headers)
                            if response.status_code == 200:
                                filename = os.path.basename(urlparse(url).path)
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

                # 将修改后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

# 设置Markdown文档所在的目录
markdown_directory = './docs/七政四餘星盤 天星擇日 占星盤 - Moira/'

save_images_from_markdown_directory(markdown_directory)
