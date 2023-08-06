#!/usr/bin/env python3
import json
import html
from urllib.parse import urljoin
from html.parser import HTMLParser


class StopParsing(Exception): pass


class BaseParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.alternate = None
        self.year = None
        self.time = None
        self.age = None
        self.isfilm = True


class ImdbParser(BaseParser):
    def __init__(self):
        super().__init__()
        self._script = False
        self._span = False
        self._spanRuntime = False
        self._spanEnd = False
        self._tagAfterSpan = ""
    
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            for n, v in attrs:
                if n == "type" and v == "application/ld+json":
                    self._script = True
        elif tag == "span":
            for n, v in attrs:
                if n == "class" and "label" in v:
                    self._span = True
        elif self._spanEnd:
            self._tagAfterSpan = tag
    
    def handle_data(self, data):
        if self._script:
            j = json.loads(data.strip())
            
            self.title = html.unescape(j["name"])
            
            alternate = j.get("alternateName", "")
            if alternate:
                self.alternate = alternate
            
            year = j.get("datePublished", "")
            if year:
                try:
                    self.year = int(year.split("-")[0])
                except (ValueError, TypeError):
                    pass
            
            time = j.get("duration", "")
            if time:
                self.time = self._calc_time(time)
            else:
                self.time = ""
            
            age = j.get("contentRating", "")
            if age:
                self.age = age
            
            self.isfilm = True if j["@type"] == "Movie" else False
        elif self._span and data == "Runtime":
            self._spanRuntime = True
        elif self._tagAfterSpan:
            self.time += data

    def handle_endtag(self, tag):
        if tag == "script" and self._script:
            self._script = False
            if self.time:
                raise StopParsing()
        elif tag == "span" and self._span and self._spanRuntime:
            self._span = False
            self._spanRuntime = False
            self._spanEnd = True
        elif tag == self._tagAfterSpan:
            self.time = self._calc_time(self.time)
            raise StopParsing()
            
    
    def _calc_time(self, s):
        if "hour" in s:
            time_split = s.strip().lower().split("hour")
        else:
            time_split = s.strip().lower().split("h")
        
        if len(time_split) == 1:
             time = "".join(i for i in time_split[0] if i.isdigit())
             try:
                return int(time)
             except (ValueError, TypeError):
                pass
        else:
            hours = "".join(i for i in time_split[0] if i.isdigit())
            minutes = "".join(i for i in time_split[1] if i.isdigit())
            
            if not minutes:
                minutes = 0
            try:
                return int(hours) * 60 + int(minutes)
            except (ValueError, TypeError):
                pass
        
        return None


class KinopoiskParser(BaseParser):
    def __init__(self):
        super().__init__()
        self._script = False
        self._a = False
        self._span = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            for n, v in attrs:
                if n == "type" and v == "application/ld+json":
                    self._script = True
        elif tag == "a":
            for n, v in attrs:
                if not self.age and n == "class" and "restrictionLink" in v:
                    self._a = True
        elif tag == "span" and self._a:
            self._span = True
    
    def handle_data(self, data):
        if self._script:
            j = json.loads(data.strip())
            
            self.title = j["name"]
            
            alternate = j.get("alternateName", "")
            if alternate:
                self.alternate = html.unescape(alternate)
            
            try:
                self.year = int(j["datePublished"])
            except (ValueError, TypeError):
                pass
            
            try:
                self.time = int(j["timeRequired"])
            except (ValueError, TypeError):
                pass
            
            self.isfilm = True if j["@type"] == "Movie" else False
            self._script = False
        elif self._span:
            if "+" in data:
                self.age = data.strip()

    def handle_endtag(self, tag):
        if self._span:
            raise StopParsing()


class BaseSeriesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.titles = {}
        self._season = None
        self._episode = None
    
    def _update_titles(self, season, episode, title):
        if not self.titles.get(season):
            self.titles[season] = {}
        e = self.titles[season]
        if not e.get(episode):
            self.titles[season].update({episode: title})
        else:
            t = e.get(episode)
            t += "/" + title
            self.titles[season].update({episode: t})


class ImdbSeriesParser(BaseSeriesParser):
    def __init__(self):
        super().__init__()
        self._option = False
        self._meta_episodes = 0
        self._div_eplist = False
        self._div_list_item = False
        self._meta = False
        self._strong = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "option" and not self._option:
            for n, v in attrs:
                if n == "selected" and v == "selected":
                    self._option = True
                    continue
                if n == "value" and self._option:
                    self._season = int(v)
                    return
        if tag == "div":
            for n, v in attrs:
                if n == "class" and "eplist" in v:
                    self._div_eplist = True
                    return
                if n == "class" and "list_item" in v and self._div_eplist:
                    self._div_list_item = True
                    return
        if tag == "meta":
            ep_num = False
            q = False
            for n, v in attrs:
                if n == "itemprop" and v == "episodeNumber" and \
                   self._div_list_item:
                    ep_num = True
                if n == "itemprop" and v == "numberofEpisodes" and \
                   self._meta_episodes == 0:
                    q = True
            for n, v in attrs:
                if n == "content" and q:
                    self._meta_episodes = int(v)
                    q = False
                    return
                if n == "content" and ep_num:
                    self._episode = int(v)
                    self._meta = True
                    ep_num = False
                    return
        if tag == "strong" and self._meta:
            self._strong = True
            return
    
    def handle_data(self, data):
        if self._strong:
            name = data.strip()
            if name:
                self._update_titles(self._season, self._episode, name)
    
    def handle_endtag(self, tag):
        if self._strong:
            self._strong = False
            self._meta = False
            self._div_list_item = False
            if len(self.titles[self._season]) == self._meta_episodes:
                raise StopParsing()


class KinopoiskSeriesParser(BaseSeriesParser):
    def __init__(self):
        super().__init__()
        self._div_season_item = False
        self._a = False
        self._a_s = False
        self._table = False
        self._td = False
        self._span = False
        self._b = False
        self._span_original = False
        self._seasons = []
    
    def handle_starttag(self, tag, attrs):
        if tag == "div" and not self._div_season_item:
            for n, v in attrs:
                if n == "class" and v == "season_item":
                    self._div_season_item = True
                    return
        if tag == "a" and self._div_season_item:
            for n, v in attrs:
                if n == "href" and v.startswith("#"):
                    self._a = True
                    season = v[2:]
                    self._seasons.append(season)
                    self._a = False
                    return
        if tag == "a":
            for n, v in attrs:
                if n == "name" and v[1:] in self._seasons:
                    s = v[1:]
                    self._seasons.remove(s)
                    self._season = int(s)
                    self._a_s = True
                    return
        if tag == "table" and self._a_s:
            self._table = True
            return
        if tag == "td" and self._table:
            self._td = True
            return
        if tag == "span" and self._td:
            if not self._span:
                self._span = True
                return
            else:
                for n, v in attrs:
                    if n == "class" and v == "episodesOriginalName":
                        self._span_original = True
                        return
        if tag == "b" and self._span:
            self._b = True
            return
    
    def handle_data(self, data):
        if self._div_season_item:
            self._div_season_item = False
        elif self._b or self._span_original:
            name = data.strip()
            if name:
                self._update_titles(self._season, self._episode, name)
        elif self._span and not self._b:
            episode = data.strip()
            if "Эпизод" in episode:
                ep = episode.split()[-1]
                self._episode = int(ep)
    
    def handle_endtag(self, tag):
        if tag == "b" and self._b:
            self._b = False
        if tag == "span" and self._span_original:
            self._td = False
            self._span = False
            self._span_original = False
        if tag == "table" and self._table:
            self._table = False
            self._a_s = False
            if not self._seasons:
                raise StopParsing()


class BaseSearch(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []
        self._name = ""
        self._link = ""


class ImdbSearchParser(BaseSearch):
    def __init__(self):
        super().__init__()
        self._root_url = "https://www.imdb.com/"
        self._table = False
        self._td = False
        self._a = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "table" and not self._table:
            for n, v in attrs:
                if n == "class" and v == "findList":
                    self._table = True
        elif tag == "td" and self._table:
            for n, v in attrs:
                if n == "class" and v == "result_text":
                    self._td = True
        elif tag == "a" and self._td:
            for n, v in attrs:
                if n == "href":
                    self._link = v.split("?")[0]
                    self._a = True
    
    def handle_data(self, data):
        data = data.strip()
        if data:
            if self._a:
                self._name = data
            elif self._td:
                self._name += " " + data
    
    def handle_endtag(self, tag):
        if tag == "a" and self._a:
            self._a = False
        elif tag == "td" and self._td:
            if self._name and self._link:
                url = urljoin(self._root_url, self._link)
                name = f"{self._name} [{url}]"
                self.found.append(name)
            self._name = ""
            self._link = ""
            self._td = False
        elif tag == "table" and self._table:
            raise StopParsing()


class KinopoiskSearchParser(BaseSearch):
    def __init__(self):
        super().__init__()
        self._root_url = "https://www.kinopoisk.ru/"
        self._p = False
        self._a = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "p":
            for n, v in attrs:
                if n == "class" and v == "name":
                    self._p = True
        elif tag == "a" and self._p:
            for n, v in attrs:
                if n == "href" and "film" in v:
                    self._link = v if v.endswith("/") else v + "/"
                    self._a = True
        elif tag == "div":
            for n, v in attrs:
                if n == "class" and v == "search_gray":
                    raise StopParsing()
    
    def handle_data(self, data):
        data = data.strip()
        if data:
            if self._a:
                self._name = data
            elif self._p:
                self._name += " (" + data + ")"
    
    def handle_endtag(self, tag):
        if tag == "a" and self._a:
            self._a = False
        elif tag == "p" and self._p:
            self._p = False
            if self._name and self._link:
                url = urljoin(self._root_url, self._link)
                name = f"{self._name} [{url}]"
                self.found.append(name)
                self._name = ""
                self._link = ""


def parser_run(parser, data):
    try:
        parser.feed(data)
    except StopParsing:
        pass
    finally:
        parser.reset()
        parser.close()
