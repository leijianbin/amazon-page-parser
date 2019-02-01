# -*- coding: utf-8 -*-

# All rights reserved.
# @Author: hyan15
# @Email: qwang16@olivetuniversity.edu

class DetailParser(object):
    def __init__(self, text, type='html', namespace=None, root=None, base_url=None):
        self.selector = Selector(
            text, type=type, namespace=namespace, root=root, base_url=base_url)

    def parse(self):
        return {
            'title': self.parse_title(),
            'author': self.parse_author(),
            'feature_bullets': self.parse_feature_bullets(),
            'book_description': self.parse_book_description(),
            'product_description': self.parse_product_description(),
            'images': self.parse_images(),
            'star': self.parse_star(),
            'reviews': self.parse_reviews(),
            'rank': self.parse_rank(),
            'categories': self.parse_categories(),
            'details': self.parse_details()
        }

    def parse_title(self):
        raw_title = self.selector.xpath('//[@id="productTitle"]/text()').get()
        return raw_title.strip() if raw_title else ''

    def parse_feature_bullets(self):
        return self.selector.xpath(
            '//*[@id="feature-bullets"]/ul/li/span[contains(@class, "a-list-item")]/text()').getall()

    def parse_book_description(self):
        noscript_elems = self.selector.xpath('//*[@id="bookDescription_feature_div"]/noscript')
        return ''.join([s.strip() for s in noscript_elems.xpath('.//text()').getall()])

    def parse_product_description(self):
        try:
            product_description = ''.join(
                [s.strip() for s in self.selector..xpath('//*[@id="productDescription"]//text()')])
        except:
            product_description = ''

        return product_description

    def parse_images(self):
        thumb_urls = []

        bottom_thumb_elems = self.selector.xpath(
            '//*[@id="imageBlockThumbs"]//div[contains(@class, "imageThumb")]/img')
        bottom_thumb_urls = bottom_thumb_elems.xpath('./@src').getall()
        thumb_urls.extend(bottom_thumb_urls)

        side_thumb_elems = self.selector.xpath(
            '//*[@id="altImages"]//li[contains(@class, "item")]/img')
        side_thumb_urls = side_thumb_elems.xpath('./@src').get()
        thumb_urls.extend(side_thumb_urls)

        if len(thumb_urls) <= 0:
            front_img_data = self.selector.xpath(
                '//img[@id="imgBlkFront"]/@data-a-dynamic-image').get()
            if front_img_data:
                try:
                    front_img_dict = json.loads(front_img_data)
                    raw_front_img_urls = front_img_dict.keys()
                    if len(raw_front_img_urls) > 0:
                        thumb_urls.append(raw_front_img_urls.pop(0))
                except:
                    pass

        return thumb_urls

    def parse_star(self):
        stars = 0
        stars_str = self.selector.xpath('//*[@id="acrPopover"]/@title').get()
        try:
            stars = float(stars_str.strip().split().pop(0))
        except:
            pass

        return stars

    def parse_reviews(self):
        reviews = 0
        reviews_str = self.selector.xpath(
            '//*[@id="acrCustomerReviewText"]/text()').get()
        try:
            reviews = int(reviews_str.strip().split().pop(0))
        except:
            pass

        return reviews

    def parse_details(self):
        details = dict()

        details_elems = self.selector.xpath(
            '//*[@id="productDetailsTable"]/tr/td/div[@class="content"]/ul/li[not(@id="SalesRank")]')
        for details_elem in details_elems:
            key = details_elem.xpath('./b/text()').get()
            key = key.strip().strip(':') if key else ''
            value = details_elem.xpath('./text()').get()
            value = value.strip() if value else ''
            if key and value:
                details[key] = value

        details_elems = self.selector.xpath(
            '//*[@id="detailBullets_feature_div"]/ul/li/span[@class="a-list-item"]')
        for details_elem in details_elems:
            key = details_elem.xpath('./span[@class="a-text-bold"]/text()').get()
            key = key.strip().strip(':') if key else ''
            value = details_elem.xpath(
                    './span[not(@class="a-text-bold")]/text()').get()
            value = value.strip() if value else ''
            if key and value:
                details[key] = value

        details_elems = self.selector.xpath(
            '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr')
        for details_elem in details_elems:
            key = details_elem.xpath('./th/text()').get()
            key = key.strip().strip(':') if key else ''
            value = details_elem.xpath('./td/text()').get()
            value = value.strip() if value else ''
            if key and value:
                details[key] = value

        return details

    def parse_specifications(self):
        pass

    def parse_categories(self):
        category_elems = self.selector.xpath(
            '//*[@id="SalesRank"]/ul[@class="zg_hrsr"]/li[1]/span[@class="zg_hrsr_ladder"]//a')
        if category_elems:
            categories = '>'.join(category_elems.xpath('./text()').get())
        else:
            xpath_str = '//*[@id="prodDetails"]//table/tbody/tr/'
            common_xpath_str = 'th[contains(@class, "prodDetSectionEntry") and '
            common_xpath_str += 'contains(./text(), "Best Sellers Rank")]'
            common_xpath_str += '/following-sibling::td/span/span[2]/a'
            category_elems = self.selector.xpath(xpath_str + common_xpath_str)

            additional_xpath_str = '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr'
            category_elems.extend(response.xpath(additional_xpath_str + common_xpath_str))

            if category_elems:
                categories = '>'.join(
                    [cs.strip() for cs in category_elems.xpath('./text()').get()])
            else:
                categories = ''

        return categories

    def parse_rank(self):
        sales_rank_str = ''.join(self.selector.xpath('//*[@id="SalesRank"]/text()').get()).strip()
        if sales_rank_str:
            try:
                rank = int(sales_rank_str.split().pop(0).strip('#').replace(',', ''))
            except:
                rank = 0
        else:
            xpath_str = '//*[@id="prodDetails"]//table/tbody/tr/'
            common_xpath_str = 'th[contains(@class, "prodDetSectionEntry") and '
            common_xpath_str += 'contains(./text(), "Best Sellers Rank")]'
            common_xpath_str += '/following-sibling::td/span/span/text()'
            sales_rank_str = ''.join(
                self.selector.xpath(xpath_str + common_xpath_str).get()).strip()

            additional_xpath_str = '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr'
            sales_rank_str += ''.join(
                self.selector.xpath(additional_xpath_str + common_xpath_str).get()).strip()
            if sales_rank_str:
                try:
                    rank = int(sales_rank_str.split().pop(0).strip('#').strip(','))
                except:
                    rank = 0
            else:
                rank = 0

        return rank
