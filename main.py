import os
import requests
from bs4 import BeautifulSoup
from markdowngenerator import MarkdownGenerator

# 來源
BLOG = 'https://blog.xuite.net/[帳號]/wretch'


def start():
    # 取得頁面數量
    source_url = BLOG
    page = requests.get(source_url)
    soup = BeautifulSoup(page.content, "html.parser")
    page_count = soup.select("div.page a")[-1]["href"].split('?&p=')[1]

    # 檢查目錄是否存在
    if not os.path.isdir('./result'):
        os.mkdir('./result')

    os.chdir('./result')

    # 輸出結果
    processing = 1

    while processing < (int(page_count) + 1):
        source_url = BLOG + '?&p=' + str(processing)
        page = requests.get(source_url)
        soup = BeautifulSoup(page.content, "html.parser")
        post_href = soup.select("span.titlename a")

        print('第 ' + str(processing) + ' 頁／共 ' + str(page_count) + ' 頁')

        for s in post_href:
            post_url = 'https:' + s["href"]
            post = BeautifulSoup(requests.get(post_url).content, "html.parser")
            post_title = post.select_one("div#content span.titlename").text.replace('/', '_')
            post_time = post.select_one("span.titledate-year").text + '-' + post.select_one("span.titledate-month").text + '-' + post.select_one("span.titledate-day").text
            post_content = post.select_one("div#content div#content_all").get_text(separator="\n").replace('\n', '  \n')
            print('☑️ ' + post_time + ' ' + post_title)

            with MarkdownGenerator(
                    filename=post_time + ' ' + post_title + ".md", enable_write=False
            ) as doc:
                doc.addHeader(1, post_title)
                doc.writeTextLine(post_content)

        processing = processing + 1

start()