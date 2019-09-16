# -*- coding: utf-8 -*-

from datetime import timedelta, datetime

def daterange(st, ed):
    """ Yield a list of dates given the start and end point.
    
    Parameters
    ----------
    st : string
        start date of format %Y-%m-%d
    ed : string
        end date of format %Y-%m-%d
    """
    try:
        start_date = datetime.strptime(st, '%Y-%m-%d')
        end_date   = datetime.strptime(ed, '%Y-%m-%d')
    except:
        raise Exception('Incorrect date format!')
    
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def today_date():
    return datetime.now().strftime("%Y-%m-%d")

def yesterday_date():
    return (datetime.now() + timedelta(-1)).strftime("%Y-%m-%d")

def now_time():
    return datetime.now().strftime("%Y%m%dT%H%M")

def get_general_cat(text):
    """ Classify the given text to one of the 9 main categories:
    國內,論壇,生活,國際,藝文,娛樂,理財,科技,體育
    """
    cat_map = {
        '國內': ['焦點要聞','政治要聞','社會新聞','地方新聞','產業特刊','焦點新聞','政治','社會','軍事','要聞', '焦點', '人物', '地方','文教'],
        '論壇': ['時論廣場','話題觀察','論壇廣場','論壇與專欄', '評論'],
        '生活': ['生活新聞','時尚消費','生活','旅遊','副刊', '工商消息', '消費'],
        '國際': ['兩岸要聞','國際大事','兩岸新聞','國際','兩岸', '自由共和國','全球'],
        '藝文': ['藝文副刊','兩岸藝文', '文化週報','閱讀'],
        '娛樂': ['娛樂新聞','娛樂', '影視'],
        '理財': ['財經要聞','全球財經','金融．稅務','投資理財','產業財經','財經','地產','產經','股市','房市'],
        '科技': ['產業．科技','科技','數位'],
        '體育': ['體育','運動']
    }
    for cat, text_list in cat_map.items():
        if text in text_list:
            return cat
    
    return '其他'

def select_image(soup, selector):
    img_node = soup.select(selector)
    if img_node:
        if img_node[0].has_attr('src'):
            url = img_node[0]['src']
        elif img_node[0].has_attr('data-original'):
            url = img_node[0]['data-original']
            # From this weird page:
            # https://ent.ltn.com.tw/news/paper/1287155
        else:
            return None
        if url.startswith('//'):
            url = 'https:' + url
        return url
    return None
