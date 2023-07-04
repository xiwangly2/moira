import os
import re
import requests

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
                for url in image_urls:
                    # 检查URL是否以http://或https://开头
                    if url.startswith('http://') or url.startswith('https://'):
                        response = requests.get(url)
                        if response.status_code == 200:
                            filename = os.path.basename(url)
                            save_path = os.path.join(save_dir, filename)
                            with open(save_path, 'wb') as f:
                                f.write(response.content)
                            print(f'Saved image: {save_path}')
                        else:
                            print(f'Failed to download image: {url}')
                    else:
                        print(f'Skipped non-HTTP/HTTPS URL: {url}')

# 设置保存图片的目录
save_directory = 'saved_images'

# 创建保存图片的目录（如果不存在）
os.makedirs(save_directory, exist_ok=True)

# 遍历目录中的Markdown文档并保存其中的图片
markdown_directory = 'D:/Projects/xiwangly2/moira/docs/七政四餘星盤 天星擇日 占星盤 - Moira'
save_images_from_markdown_directory(markdown_directory, save_directory)
