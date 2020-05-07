from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

base_url = 'https://www.wnsstamps.post' 

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp
    
    country_post = ''
    date_of_issue = ''
    primary_theme = ''
    subject = ''
    width = ''
    height = ''
    denomination = ''
    number_in_set = ''
    layout_format = ''
    perforations  = ''
    authority = ''
    printer = ''
    
    for info_item in html.select('.stamp_info th'):
        info_heading = info_item.get_text().strip()
        if info_item.find_next():
            info_value = info_item.find_next().get_text().strip()
            if info_heading == 'Country / Post':
                country_post = info_value 
            elif info_heading == 'Date of Issue':
                date_of_issue = info_value 
            elif info_heading == 'Primary theme':
                primary_theme = info_value        
            elif info_heading == 'Subject':
                subject = info_value 
            elif info_heading == 'Width':
                width = info_value   
            elif info_heading == 'Height':
                height = info_value 
            elif info_heading == 'Denomination':
                denomination = info_value                   
            elif info_heading == 'Number in set':
                number_in_set = info_value  
            elif info_heading == 'set list':
                set_list = info_value  
            elif info_heading == 'Layout/Format':
                layout_format = info_value  
                layout_img = ''
                try:
                    layout_img_href = info_item.find_next().select('a')[0].get('href')
                    if layout_img_href:
                        layout_img = base_url + layout_img_href
                except:
                    pass
            elif info_heading == 'Perforations':
                perforations = info_value                  
            elif info_heading == 'Stamp issuing authority':
                authority = info_value    
            elif info_heading == 'Printer':
                printer = info_value  
                
    stamp['country_/_post'] = country_post     
    stamp['date_of_issue'] = date_of_issue     
    stamp['primary_theme'] = primary_theme    
    stamp['subject'] = subject     
    stamp['width'] = width     
    stamp['height'] = height     
    stamp['denomination'] = denomination     
    stamp['number_in_set'] = number_in_set     
    stamp['layout_/_format'] = layout_format     
    stamp['perforations'] = perforations  
    stamp['authority'] = authority  
    stamp['printer'] = printer  
    
    try:
        wns = html.select('.stamp_info h1')[0].get_text().strip()
        stamp['wns'] = wns
    except:
        stamp['wns'] = None      
        
    set_list = []  

    # image_urls should be a list
    images = []                    
    try:
        image_href = html.select('.stamp_info center a')[0].get('href')
        img = base_url + image_href
        if img not in images:
           images.append(img)
                
        if layout_img and (layout_img not in images):
            images.append(layout_img)
           
    except:
        pass
    
    stamp['set_list'] = set_list
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = url
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):
    
    items = []
    next_url = ''
    
    try:
        html = get_html(url)
    except:
        return items
    
    try:
        for item in html.select('.wnsNumber a'):
            item_link = base_url + item.get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items

page_numbers = [x for x in range(1, 9925)]
shuffle(page_numbers)

for page_number in page_numbers:
    url = 'https://www.wnsstamps.post/en/stamps?page=' + str(page_number) + '&search%5Bauthority_id%5D=&search%5Bfreetext%5D=&search%5Bmonth%5D=&search%5Border_by%5D=asc&search%5Btheme_id%5D=&search%5Byear%5D=&utf8=%E2%9C%93'
    page_items = get_page_items(url)
    for page_item in page_items:
        stamp = get_details(page_item)