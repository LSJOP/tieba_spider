import requests

# 1.找到url规律，构造url list
# 2. 遍历url list ，发送请求，获取响应
# 3.提取html str，
# 4.保存


class Tieba_Spider(object):
    """贴吧爬虫"""
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.headers = {"User - Agent": "Mozilla/5.0(WindowsNT 10.0; Win64; x64)" 
                        "AppleWebKit / 537.36(KHTML,like Gecko) Chrome / 61.0.3163.100 Safari / 537.36"}

    def get_url_list(self):
        """构造url"""
        # https://tieba.baidu.com/f?kw=海贼王&ie=utf-8&pn=50
        url_list = []
        for i in range(1000):
            url_temp = "https://tieba.baidu.com/f?kw="+self.tieba_name+"&ie=utf-8&pn={}".format(i*50)
            url_list.append(url_temp)
        return url_list

    def parse_url(self, url):
        """发送请求"""
        response = requests.get(url, headers=self.headers)
        html_str = response.content.decode("utf8")
        return html_str

    def save_html(self, html_str, page_number):
        """保存提取的html"""
        file_path = 'html/'+self.tieba_name+'第'+str(page_number)+'页.html'
        with open(file_path, 'w', encoding='utf-8')as f:
            f.write(html_str)

    def run(self):
        url_list = self.get_url_list()  # 构造url
        for url in url_list:
            html_str = self.parse_url(url)  # 发送请求
            page_number = url_list.index(url) + 1
            self.save_html(html_str, page_number)     # 保存提取的html

if __name__ == '__main__':
    tieba_spider = Tieba_Spider('海贼王')
    tieba_spider.run()



