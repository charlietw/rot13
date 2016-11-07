# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class MainPage(Handler):
    def rot13(self,s):
        rotcode_lc = ["a","b","c","d","e","f","g",
                      "h","i","j","k","l","m","n",
                      "o","p","q","r","s","t","u",
                      "v","w","x","y","z"]
        rotcode_uc = ["A","B","C","D","E","F","G",
                      "H","I","J","K","L","M","N",
                      "O","P","Q","R","S","T","U",
                      "V","W","X","Y","Z"]

        rot_return = ""

        for e in s:
            #check to see if it's a letter, then if uc or lc
            if e in rotcode_lc or e in rotcode_uc:
                if e.islower():
                    rotcode = rotcode_lc
                else:
                    rotcode = rotcode_uc
                #find the location of the letter in the alphabet and add/subtract
                first_instance = rotcode.index(e)
                if first_instance < 13:
                    return_instance = first_instance + 13
                else:
                    return_instance = first_instance - 13
                return_char = rotcode[return_instance]
            else:
                return_char = e
            #add to the return value
            rot_return += return_char
        return rot_return

    def get(self):
        self.render("rot13.html")

    def post(self):
        text = self.request.get("text")
        self.render("rot13.html", text=self.rot13(text))




# class FizzBuzzHandler(Handler):
#     def get(self):
#         n = self.request.get('n',0)
#         n = n and int(n) #same as saying ''if n', n =int(n)'
#         self.render('fizzbuzz.html',n = n)



app = webapp2.WSGIApplication([
    ('/', MainPage),
    #('/fizzbuzz', FizzBuzzHandler),
], debug=True)
