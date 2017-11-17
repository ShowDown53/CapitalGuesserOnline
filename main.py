#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
import random
import sys

reload(sys)

sys.setdefaultencoding("utf-8")


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class Country(object):
    name = ""
    capital = ""
    image = ""

    def __init__(self, name, capital, image):
        self.name = name
        self.capital = capital
        self.image = image

def get_countries():
    slo = Country("Slovenija", "Ljubljana", "assets/images/ljubljana.jpg")
    hrv = Country("Hrvaška", "Zagreb", "assets/images/zagreb.jpg")
    ita = Country("Italija", "Rim", "assets/images/rim.jpg")

    return [slo,hrv,ita]

class MainHandler(BaseHandler):
    def get(self):
        countries = get_countries()
        index = random.randint(0,2)
        country = countries[index]
        params = {"country": country.name, "image": country.image}

        return self.render_template("main.html", params=params)

class ResultHandler(BaseHandler):
    def post(self):
        capital = self.request.get("capital")
        country = self.request.get("country")

        countries = get_countries()

        params = {}

        for c in countries:
            if c.name == country:
                if c.capital.lower() == capital.lower():
                    result = True
                else:
                    result = False

                params = {"result": result, "c": c}

                return self.render_template("result.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
], debug=True)
