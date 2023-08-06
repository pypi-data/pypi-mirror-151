#!/usr/bin/env python3
import os
import time
from urllib.parse import urljoin, quote

from .parsers import ImdbSearchParser, KinopoiskSearchParser, \
    KinopoiskParser, ImdbParser, KinopoiskSeriesParser, ImdbSeriesParser, \
    parser_run
from .utils import isallow, getd, getr, geth


class Film:
    def __init__(self, **kargs):
        for k, v in kargs.items():
            if v is not None:
                if isinstance(v, str) and v == "":
                    continue
                self.__dict__[k] = v
    
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return None
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
    def __str__(self):
        kargs = []
        title = ""
        
        for k, v in self.__dict__.items():
            if v is not None:
                if k == "title":
                    title = v
                else:
                    kargs.append(str(v))
        
        return f"{title} ({', '.join(kargs)})"
    
    def __repr__(self):
        kargs = []
        
        for k, v in self.__dict__.items():
            if v is not None:
                if isinstance(v, str) and v != "":
                    kargs.append(f"{k}='{v}'")
                else:
                    kargs.append(f"{k}={v}")
        
        return f"{self.__class__.__name__}({','.join(kargs)})"


class Series(Film):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.titles = {}
        self._s = {}
    
    def __str__(self):
        kargs = []
        
        if self._s:
            for k, v in self._s.items():
                kargs.append(f"{k}: {v}")
            
            return ", ".join(kargs)
        else:
            title = ""
            
            for k, v in self.__dict__.items():
                if v is not None and k not in ("titles", "_s"):
                    if k == "title":
                        title = v
                    else:
                        kargs.append(str(v))
            
            return f"{title} ({', '.join(kargs)})"
    
    def __repr__(self):
        kargs = []
        
        if self._s:
            for k, v in self._s.items():
                kargs.append(f"{k}: {v}")
            
            return repr(", ".join(kargs))
        else:
            for k, v in self.__dict__.items():
                if not v and k == "titles":
                    continue
                elif v is not None and k not in ("_s"):
                    if isinstance(v, str) and v != "":
                        kargs.append(f"{k}='{v}'")
                    else:
                        kargs.append(f"{k}={v}")
            
            return f"{self.__class__.__name__}({','.join(kargs)})"
    
    def add_season(self, season, episodes):
        if isinstance(episodes, dict) and isinstance(season, int):
            ep = {}
            
            for k, v in episodes.items():
                if isinstance(k, int) and isinstance(v, str):
                    ep[k] = v
            
            if ep:
                self.titles[season] = ep
    
    def amount_seasons(self):
        return len(self.titles)
    
    def amount_episodes(self, num=None):
        amount = 0
        
        if num is None:
            for k, v in self.titles.items():
                amount += len(v)
        else:
            try:
                num = int(num)
            except (TypeError, ValueError):
                amount = 0
            
            episodes = self.titles.get(num)
            
            if episodes is None:
                amount = 0
            else:
                amount = len(episodes)
        
        return amount
    
    def s(self, num):
        if not isinstance(num, int):
            num = int(num)
        
        if not self.titles:
            if not self.fetch_titles():
                return None
        
        if min(i for i in self.titles) <= num <= self.amount_seasons():
            self._s = self.titles[num]
            return self
        else:
            return None
    
    def ep(self, num):
        if not self._s:
            return None
        
        if not isinstance(num, int):
            num = int(num)
        
        ep = self._s.get(num)
        self._s = {}
        
        return ep
    
    def fetch_titles(self):
        try:
            url = self.url
        except KeyError:
            return False
        
        if not url.endswith("/"):
            url += "/"
            self.url = url
        
        if not isallow(url):
            return False
        
        if "kinopoisk" in url:
            parser = KinopoiskSeriesParser
        else:
            parser = ImdbSeriesParser
        
        html = geth(urljoin(url, "episodes/"))
        
        p = parser()
        parser_run(p, html)
        
        self.titles = p.titles
        
        if "imdb" in url:
            uj = urljoin(url, "episodes?season=")
            
            try:
                season_last = int(p._season)
            except ValueError:
                return True if self.titles else False
            
            for i in range(1, season_last):
                time.sleep(1)
                
                html = geth(uj + str(i))
                if not html:
                    continue
                
                ps = parser()
                parser_run(ps, html)
                
                self.titles.update(ps.titles)
        
        return True if self.titles else False


def new(url):
    if not url.endswith("/"):
        url += "/"
    
    if not isallow(url):
        return None
    
    if "kinopoisk" in url:
        p = KinopoiskParser()
    else:
        p = ImdbParser()
    
    html = geth(url)
    
    parser_run(p, html)
    
    keys = ("title", "alternate", "year", "time", "age", "url")
    values = (p.title, p.alternate, p.year, p.time, p.age, url)
    
    args = {k: v for k, v in zip(keys, values)}
    
    if p.isfilm:
        return Film(**args)
    else:
        return Series(**args)


def search(word):
    if len(word) < 1:
        return None
    
    key = quote(word.lower())
    
    result = []
    
    for url, parser in (
        ("https://www.imdb.com/find?q=", ImdbSearchParser),
        ("https://www.kinopoisk.ru/index.php?kp_query=", KinopoiskSearchParser)
    ):
        
        url += key
        
        r = getr(url)
        if not r:
            continue
        
        data = getd(r.read())
        html = data.decode("utf8", errors="ignore")
        
        if "kinopoisk" in url and ("film" in r.url or "series" in r.url):
                p = KinopoiskParser()
                parser_run(p, html)
                
                alternate = p.alternate
                if alternate:
                    alternate += " " 
                
                found = f"{p.title} ({p.year}) {alternate}[{r.url}]"
        else:
            p = parser()
            parser_run(p, html)
            
            found = p.found
            if found:
                found = os.linesep.join(found)
        
        if found:
            result.append(found)
        
    if result:
        return os.linesep.join(result)
    
    return None
