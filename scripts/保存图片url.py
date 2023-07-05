import os
import re

def extract_image_urls_from_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Use regular expressions to extract image URLs
        image_urls = re.findall(r'!\[.*?\]\((.*?)\)', content)
        return image_urls

def save_urls_to_file(urls, file_path):
    with open(file_path, 'a+', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')

def save_urls_from_markdown_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                image_urls = extract_image_urls_from_markdown_file(file_path)
                urls_file_path = os.path.join(root, 'image_urls.txt')

                save_urls_to_file(image_urls, urls_file_path)

# Set the directory of the Markdown documents
markdown_directory = './docs/七政四餘星盤 天星擇日 占星盤 - Moira/'

save_urls_from_markdown_directory(markdown_directory)
