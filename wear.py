import requests
from bs4 import BeautifulSoup
import pandas as pd

genre = {'ストリート系': 22016, '韓国ファッション': 34797, 'モード': 4249, '古着': 183, 'y2k': 433360, 'アメカジ': 424, 'グランジ': 6843, '90s': 10817, 'きれいめカジュアル': 5102}
url = 'https://wear.jp/coordinate/?tag_ids='

headers = ['genre', 'body', 'good', 'image']
df = pd.DataFrame(columns=headers)
df_index = 0
items_df = pd.DataFrame(columns=['id', 'brand', 'txt', 'buylink'])
for k, v in genre.items():
  response = requests.get(url + str(v))

  soup = BeautifulSoup(response.text, 'html.parser')
  main_box = soup.find(id='main_list')
  children = main_box.find_all(class_='like_mark')
  print(k)
  for c in children[:5]:
    try:
      c_url = 'https://wear.jp' + c.find(class_='over').get('href')
      image = 'https:' + c.find('img').get('data-original')
      good = c.find('span').text
      c_res = requests.get(c_url)
      c_soup = BeautifulSoup(c_res.text, 'html.parser')
      body = c_soup.find(class_='content_txt').text
      items_box = c_soup.find(id='item').find_all(class_='clearfix')
      items = []
      for item in items_box:
        try:
          item_main = item.find(class_='main')
          brand = item_main.find(class_='brand').text
          txt = item_main.find(class_='txt').text
          buylink = item_main.find(class_='buybtn').get('href')
          items_df = items_df.append({'id':df_index, 'brand':brand, 'txt':txt, 'buylink':buylink}, ignore_index=True)
        except Exception as e:
          print(f'itemでエラー出たよー: {e}')
      df.loc[df_index] = [k, body, good, image]
      df_index += 1
    except Exception as e:
      print(f'エラー出たよー: {e}')

print(df)
df.to_csv('./static/csv/wear.csv')
items_df.to_csv('./static/csv/items.csv')
