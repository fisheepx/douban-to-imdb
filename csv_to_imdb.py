import os
import sys
import time
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException  


def login():
    driver = webdriver.Chrome()
    driver.get('https://www.imdb.com/registration/signin')
    element = driver.find_element_by_id('signin-perks')
    driver.execute_script("arguments[0].setAttribute('style', 'color: red;font-size: larger; font-weight: 700;')", element)
    driver.execute_script("arguments[0].innerText = '请登录自己的IMDB账号, 程序将等待至登录成功。'", element)
    current_url = driver.current_url
    while True:
        WebDriverWait(driver, 600).until(EC.url_changes(current_url))
        new_url = driver.current_url
        if new_url == 'https://www.imdb.com/?ref_=login':
            break
    print('IMDB登录成功')
    return driver

def mark(is_unmark = False, rating_ajust = -1):
    driver = login()
    success_marked = 0
    success_unmarked = 0
    can_not_found = []
    already_marked = []
    never_marked = []
    file_name = os.path.dirname(os.path.abspath(__file__)) + '/movie.csv'
    with open(file_name, 'r') as file:
        content = csv.reader(file, lineterminator='\n')
        for line in content:
            # 如果只标记为看过并没有过分则略过
            if not line[1]:
                continue
            movie_name = line[0]
            movie_rate = int(line[1]) * 2 + rating_ajust
            imdb_id = line[2]
            if not imdb_id or not imdb_id.startswith('tt'):
                can_not_found.append(movie_name)
                print('无法在IMDB上找到：', movie_name)
                continue

            driver.find_element_by_name('q').send_keys(imdb_id)
            driver.find_element_by_name('q').submit()
            time.sleep(3)
            try:
                if is_unmark:
                    driver.find_element_by_class_name('star-rating-button')
                else:
                    driver.find_element_by_class_name('star-rating-text')
            except NoSuchElementException:
                if is_unmark:
                    never_marked.append(f'{movie_name}({imdb_id})')
                    print(f'并没有在IMDB上打过分：{movie_name}({imdb_id})')
                else:
                    already_marked.append(f'{movie_name}({imdb_id})')
                    print(f'已经在IMDB上打过分：{movie_name}({imdb_id})')
            else:
                if is_unmark:
                    driver.find_element_by_class_name('star-rating-button').click()
                    driver.find_element_by_css_selector(f"[title^='Delete']").click()
                    print(f'电影删除打分成功：{movie_name}({imdb_id})')
                    success_unmarked += 1
                else:
                    driver.find_element_by_class_name('star-rating-text').click()
                    driver.find_element_by_css_selector(f"[title^='Click to rate: {movie_rate}']").click()
                    print(f'电影打分成功：{movie_name}({imdb_id})')
                    success_marked += 1
            time.sleep(1)
    driver.close()

    print('***************************************************************************')
    if is_unmark:
        print(f'成功删除了 {success_unmarked} 部电影的打分')
        print(f'有 {len(can_not_found)} 部电影没能在IMDB上找到：', can_not_found)
        print(f'有 {len(never_marked)} 部电影并没有在IMDB上打过分：', never_marked)
    else:
        print(f'成功标记了 {success_marked} 部电影')
        print(f'有 {len(can_not_found)} 部电影没能在IMDB上找到：', can_not_found)
        print(f'有 {len(already_marked)} 部电影已经在IMDB上打过分：', already_marked)
    print('***************************************************************************')


if __name__ == '__main__':
    if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/movie.csv'):
        print('未能找到CSV文件，请先导出豆瓣评分，请参照：',
        'https://github.com/fisheepx/douban-to-imdb')
        sys.exit()
    if len(sys.argv) > 1 and sys.argv == 'unmark':
        mark(True)
    elif len(sys.argv) > 1:
        if sys.argv[1] not in ['-2', '-1', '0', '1', '2']:
            print('分数调整范围不能超过±2分(默认 -1分)，请参照：',
            'https://github.com/fisheepx/douban-to-imdb')
            sys.exit()
        else:
            mark(False, sys.argv[1])
    else:
        mark()


