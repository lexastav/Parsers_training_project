from bs4 import BeautifulSoup

with open('blank/index.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

# title = soup.title
#
# print(title.string)
#
# page_div = soup.find_all('div')
#
# for item in page_div:
#     print(item.text)

# user_name = soup.find('div', class_="user__name")
# print(user_name.text.strip())

# user_name = soup.find('div', class_="user__name").find('span').text
# print(user_name)

# user_name = soup.find('div', {"class": "user__name"}).find('span').text
# print(user_name)


# span_tags = soup.find(class_="user__info").find_all('span')
#
# for item in span_tags:
#     print(item.text)

# social_links = soup.find(class_="social__networks").find('ul').find_all('a')
# for item in social_links:
#     item_text = item.text
#     item_url = item.get('href')
#     print(f'{item_text}: {item_url}')


# post_div = soup.find(class_="post__text").find_parent()
# print(post_div)

# post_div = soup.find(class_="post__text").find_parents('div', 'user__post')
# print(post_div)

# next_el = soup.find(class_='post__title').next_element.next_element
# print(next_el.text)

# next_el = soup.find(class_='post__title').find_next().text
# print(next_el)

next_sib = soup.find(class_="post__title").find_next_sibling().text
print(next_sib)