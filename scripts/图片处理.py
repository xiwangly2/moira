import os
import re
from time import sleep
import requests
from urllib.parse import urlparse

def extract_image_urls_from_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用正则表达式提取图片URL
        image_urls = re.findall(r'\!\[.*?\]\((.*?)\)', content)
        return image_urls

def save_images_from_markdown_directory(directory, save_dir):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                image_urls = extract_image_urls_from_markdown_file(file_path)
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                for url in image_urls:
                    # 检查URL是否以http://或https://开头
                    if url.startswith('http://') or url.startswith('https://'):
                        # 太快了会被拦截
                        sleep(5)
                        response = requests.get(url)
                        if response.status_code == 200:
                            filename = os.path.basename(urlparse(url).path)
                            save_path = os.path.join(save_dir, filename)
                            with open(save_path, 'wb') as f:
                                f.write(response.content)
                            print(f'Saved image: {save_path}')
                            # 替换Markdown文档中的URL为相对路径
                            relative_path = os.path.relpath(save_path, os.path.dirname(file_path))
                            content = content.replace(url, relative_path.replace("\\", "/"))
                            print(f'Replaced URL in Markdown: {url} -> {relative_path}')

                # 将修改后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)


# 设置保存图片的目录
save_directory = 'docs/七政四餘星盤 天星擇日 占星盤 - Moira/images'

# 创建保存图片的目录（如果不存在）
os.makedirs(save_directory, exist_ok=True)

# 遍历目录中的Markdown文档并保存其中的图片
markdown_directory = 'docs/七政四餘星盤 天星擇日 占星盤 - Moira'
save_images_from_markdown_directory(markdown_directory, save_directory)
