#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json


def get_movies():
    movies = {"movies": []}
    
    original_url = "https://movie.douban.com/top250"
    headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:62.0) Gecko/20100101 Firefox/62.0",
                "Host": "movie.douban.com"
              }
    for i in range(10):
        url = original_url + "?start=" + str(i * 25)
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "lxml")
        items = soup.find_all("div", class_="item")
        
        for item in items:
            movie = OrderedDict()
            
            pic_tag = item.find("div", class_="pic")
            img_num = int(pic_tag.em.string)
            img_url = pic_tag.a.img.get("src")

            hd_tag = item.find("div", class_="info").find("div", class_="hd")
            movie_name = hd_tag.a.span.string
            
            bd_tag = item.find("div", class_="info").find("div", class_="bd")
            movie_rating_num = float(bd_tag.find("div", class_="star").find("span", class_="rating_num").string)
            movie_quote = bd_tag.find("p", class_="quote").span.string
            
            movie["num"] = img_num
            movie["name"] = movie_name
            movie["img"] = img_url
            movie["rating_num"] = movie_rating_num
            movie["quote"] = movie_quote
            movies["movies"].append(movie)
    
    return movies

def download_img(num, name, url):
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:62.0) Gecko/20100101 Firefox/62.0"}
    r = requests.get(url, headers=headers, timeout=20)
    
    with open("./img/"+str(num)+"_"+name+".jpg", "wb") as f:
        f.write(r.content)

        
def generate_json_file(name, value):
    with open(name+".json", "w", encoding="utf-8") as f:
        f.write(json.dumps(value))

def generate_txt_file(name, movies):
    with open(name+".txt", "w", encoding="utf-8") as f:
        for movie in movies["movies"]:
            for v in movie.values():
                f.write(str(v)+"\t")
            f.write("\n")
            
def sort_movies(movies, reverse=False):
    movies["movies"].sort(key=lambda movie: movie["rating_num"], reverse=reverse)

if __name__ == "__main__":
    movies = get_movies()
    generate_json_file("movies", movies)
    generate_txt_file("movies", movies)
    for movie in movies["movies"]:
#         for v in movie.values():
#             print(v, end="  ")
#         print()
        download_img(movie["num"], movie["name"], movie["img"])
        
    sort_movies(movies, reverse=True)
    generate_txt_file("movies_sorted_by_rating", movies)
    print("DONE.")
