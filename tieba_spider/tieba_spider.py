import requests
from retrying import retry
from lxml import etree
import json


class tieba_spider(object):
    def __init__(self, tieba_name):
        self.headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                                      "(KHTML, like Gecko)"
                                      " Version/9.0 Mobile/13B143 Safari/601.1"}
        self.start_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/m?kw={}&lp=5011&lm=&pn=20".format(
            tieba_name)
        self.url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/"
        self.tieba_name = tieba_name

    @retry(stop_max_attempt_number=4)
    def _parse_url(self, url):
        """解析url"""
        response = requests.get(url, self.headers)
        assert response.status_code == 200
        return response.content

    def parse_url(self, url):
        try:
            html = self._parse_url(url)
        except Exception as e:
            html = None
        return html

    def get_content_list(self, html):
        """获取信息列表"""
        content_list = []
        # print(html)
        html = etree.HTML(html)
        div_list = html.xpath("//*[contains(@class,'i')]")  # 每一个帖子都被一个div包裹
        for div in div_list:
            item = {}
            title = div.xpath('./a/text()')[0] if len(div.xpath("./a/text()")) > 0 else None  # 选取当前帖子的标题
            href = self.url + div.xpath('./a/@href')[0] if len(div.xpath("./a/@href")) > 0 else None  # 获取当前帖子链接
            item['title'] = title
            item['href'] = href
            content_list.append(item)
        next_url_temp = html.xpath("//*[text()='下一页']/@href") if len(html.xpath("//*[text()='下一页']/@href")) > 0 else None
        next_url = self.url + next_url_temp[0]  # 下一页帖子url
        print(next_url)
        return content_list, next_url

    def get_image_list(self, href):
        try:
            html_detail = self.parse_url(href)
            print("图片"+str(html_detail))
            print(type(html_detail))
            html_detail = etree.HTML(html_detail)
            image_list = html_detail.xpath('//*[@class="BDE_Image"]/@src')  # 获取图片链接
            image_list = [requests.utils.unquote(i).split("src=")[-1] for i in image_list]  # requests.utils.unquote对url链接进行解码
        except:
            image_list = None
        return image_list

    def save_content(self, content_list):
        """保存"""
        with open(self.tieba_name+'.txt', 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
                f.write("\n")
        print('保存成功')

    def run(self):
        next_url = self.start_url
        while next_url is not None:
            html = self.parse_url(next_url)  # 解析url
            content_list, next_url = self.get_content_list(html)
            for content in content_list:
                href = content['href']  # 获取到帖子中的图片
                content['img'] = self.get_image_list(href)
            self.save_content(content_list)  # 保存


if __name__ == '__main__':
    tieba_spider = tieba_spider('海贼王')
    tieba_spider.run()
