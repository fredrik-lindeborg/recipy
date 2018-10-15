from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from urllib.request import urlopen
import random


class Crawler(object):

    def _crawl(
        self, url, search, space_delimiter, recipe_tag,
        recipe_class, source, img_prefix,
        title_tag, title_class, img_class, results
    ):
        search = search.replace(" ", space_delimiter)
        search = quote_plus(search)
        url = url.replace("%search%", search)
        try:
            soup = BeautifulSoup(urlopen(url, timeout=5), 'html.parser')
        except:
            print(url, " FAILED TO LOAD")
            return
        else:
            print(url, " scanned")
        recipes = soup.find_all(recipe_tag, recipe_class)
        for recipe in recipes:
            result = {}

            if img_class:
                img = recipe.find('img', class_=img_class)
            else:
                img = recipe.find('img')
            if img:
                img_src = img.attrs.get('data-original-src')
                if not img_src:
                    img_src = img.attrs.get('data-src')
                if not img_src:
                    img_src = img.attrs.get('src')
                result['img'] = img_prefix + img_src
            if title_tag and title_class:
                title = recipe.find(title_tag, class_=title_class)
            else:
                title = recipe.find('h2')
                if not title:
                    title = recipe.find('h3')
            link = recipe.find('a')
            result['link'] = link.attrs['href']
            result['title'] = title.string
            result['source'] = source
            results.append(result)
        return results

    def fetch(self, search):
        results = []

        self._crawl(
            url='https://www.allrecipes.com/search/results/?wt=%search%&sort=re',
            search=search,
            space_delimiter="%20",
            recipe_tag="article",
            recipe_class="fixed-recipe-card",
            source="allrecipes.com",
            img_prefix="",
            title_tag="span",
            title_class="fixed-recipe-card__title-link",
            img_class="fixed-recipe-card__img",
            results=results
        )

        self._crawl(
            url='https://www.jamieoliver.com/search/?s=%search%',
            search=search,
            space_delimiter="+",
            recipe_tag="div",
            recipe_class="recipe",
            source="jamieoliver.com",
            img_prefix="",
            title_tag="",
            title_class="",
            img_class="img-responsive",
            results=results
        )

        random.shuffle(results)
        return results
