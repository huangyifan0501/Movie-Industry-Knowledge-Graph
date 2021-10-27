from xml.dom.minidom import parse
import xml.dom.minidom
import re
import os
import shutil
from tqdm import tqdm
import mwparserfromhell

# 提取某个指定页面的信息并返回字典（若为无效页面则返回-1）
def page_extract(page_path):
    extracted_data={}

    DOMTree = xml.dom.minidom.parse(page_path)
    collection = DOMTree.documentElement
    try:
        page = collection.getElementsByTagName("page")[0]
        title = page.getElementsByTagName('title')[0].childNodes[0].data
        entity_id = page.getElementsByTagName('id')[0].childNodes[0].data
        text = page.getElementsByTagName('text')[0].childNodes[0].data
    except IndexError:
        return - 1
    else:
        extracted_data['title']=title
        extracted_data['id']=entity_id
        extracted_data['text']=text

        return extracted_data


# 提取text中的Category信息并返回列表
def re_category(text):
    category=[]

    pattern=r'(?<=Category:).*?(?=(]]))'
    carry=re.finditer(pattern, text)
    for item in carry:
        category.append(item.group())

    return category


# 根据key_words列表将满足要求的page放入分类文件夹下
def filter(key_words):
    number={}
    out_path={}
    classes=key_words.keys()
    for c in classes:
        number[c]=0
        out_path[c]='../filtered_data/'+c
        os.mkdir(out_path[c])
    
    pbar = tqdm(total=3682195)
    pbar.set_description("Processing pages")

    for f in os.listdir('../data'):
        f_path = os.path.join('../data', f)
        page = page_extract(f_path)
        pbar.update(1)

        if page != -1:         
            category = re_category(page['text'])

            for c in classes:
                signal=False
                ykey=key_words[c][0]
                nkey=key_words[c][1]

                for item in category:
                    item_signal=True
                    for y in ykey:
                        if y not in item:
                            item_signal=False
                            break
                    for n in nkey:
                        if n in item:
                            item_signal=False
                            break
                    signal=item_signal
                    
                    if signal: 
                        shutil.copy(f_path, out_path[c])
                        number[c] += 1
                        break

    pbar.close()
    print(number)


# 利用categories信息对某个页面进行type inference
def type(page_path, key_words):
    page = page_extract(page_path)
    classes = key_words.keys()
    result = set()
    
    if page != -1:         
        category = re_category(page['text'])

        for c in classes:
            signal=False
            ykey=key_words[c][0]
            nkey=key_words[c][1]

            for item in category:
                item_signal=True
                for y in ykey:
                    if y not in item:
                        item_signal=False
                        break
                for n in nkey:
                    if n in item:
                        item_signal=False
                        break
                signal=item_signal
                
                if signal: 
                    result.add(c)

    return list(result)


# 提取text中的infobox信息并返回列表（若不存在任意infobox则返回-1）
def infobox_extract(text):
    properties=[]
    wiki = mwparserfromhell.parse(text)
    matches = wiki.filter_templates()
    pattern = r'(Infobox|艺人)'
    infobox_matches = [match for match in matches if re.match(pattern, str(match.name)) is not None]
    if len(infobox_matches) >= 1:
        properties = [{param.name.strip_code().strip(): param.value.strip_code().strip() 
                        for param in match.params
                        if param.value.strip_code().strip()} for match in infobox_matches]

    return properties