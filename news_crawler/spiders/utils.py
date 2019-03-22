# -*- coding: utf-8 -*-

from datetime import timedelta

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_general_cat(text):
    cat_map = {
        '國內': ['焦點要聞','政治要聞','社會新聞','地方新聞','產業特刊','焦點新聞','政治','社會', '軍事', '要聞'],
        '論壇': ['時論廣場','話題觀察','論壇廣場', '論壇與專欄'],
        '生活': ['生活新聞', '時尚消費', '生活', '旅遊', '副刊'],
        '國際': ['兩岸要聞', '國際大事', '兩岸新聞', '國際', '兩岸'],
        '藝文': ['藝文副刊', '兩岸藝文'],
        '娛樂': ['娛樂新聞', '娛樂'],
        '理財': ['財經要聞', '全球財經', '金融．稅務', '投資理財', '產業財經', '財經', '地產'],
        '科技': ['產業．科技', '科技'],
        '體育': ['體育']
    }
    for cat, text_list in cat_map.items():
        if text in text_list:
            return cat
    
    return '其他'