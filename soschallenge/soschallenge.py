# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import cgi
import datetime
import time
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Quiz(db.Model):
  author = db.StringProperty()
  level = db.StringProperty()
  passcode = db.StringProperty()
  content = db.TextProperty()
  date = db.DateTimeProperty(auto_now_add=True)

def retry(req):
  req.response.out.write("""
      <h1>답을 잘못입력했네요.</h1>
    <a href="javascript:history.back()">답 다시 입력하기.</a>      
    """)

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
    <img src="http://piny.cc/_static/piny_slogan.png">
    <div>
    안녕하세요. SOS 문제은행에 오신것을 축하드립니다.
    각 단계의 문제에 답을 하면 다음 단계를 넘어갈 수 있습니다.
    <br/><br/>
    자 그럼 문제를 풀어 볼까요?
    </div>
    <br/>    
    <div>
    <b> 문제</b>: 여러분의 이름은?
    </div>
    <br>
          <form action="/p" method="post">
            <div><input name="name" cols="60"></input></div>                      
            <div><input type="hidden" name="level" value=1 cols="60"></input></div>
            <div><input type="hidden" name="passcode" value=0 cols="60"></input></div>            
            <br/>
            <div><input type="submit" value="다음"></div>
          </form>
     """)
#    goto_start(self)


class p(webapp.RequestHandler):
  def __init__(self):
    self.p_passcode = None
    
  def post(self):
    _level = self.request.get('level').encode("utf-8")
    _passcode = self.request.get('passcode')

    query = Quiz().all()
    if _level != '1':
      pquiz = query.filter('level =', str(int(_level)-1)).fetch(1)[0]
      self.p_passcode = pquiz.level.encode('utf-8')
    query = Quiz().all()      
    quiz = query.filter('level =', _level).fetch(1)[0]
    content = quiz.content.encode('utf-8')
    level = quiz.level.encode('utf-8')
    passcode = quiz.passcode.encode('utf-8')

    if _passcode  == '0' or  _passcode == self.p_passcode :
      self.response.out.write(content)
      self.response.out.write("""
      <form action="/p" method="post">
      <div><input name="passcode" cols="60"></input></div>      
      <div><input type="hidden" name="level" value=%s cols="60"></input></div>
      <br/>
      <div><input type="submit" value="다음"></div>
      </form>
      """ % (str(int(level)+1)))
      self.response.out.write("""
      <a href="/">처음으로 </a>
      """)

      self.p_passcode = passcode
#      self.response.out.write(self.p_passcode      )
    else:
      retry(self)
    

class MakingQuiz(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    quizs = db.GqlQuery("SELECT * FROM Quiz ORDER BY level LIMIT 10")

    for quiz in quizs:
      content = quiz.content.encode('utf-8')
      level = quiz.level.encode('utf-8')
      passcode = quiz.passcode.encode('utf-8')            
      self.response.out.write('<blockquote>level: %s passcode: %s content: %s</blockquote>' % (level, passcode, content ))
      self.response.out.write("""
      <form action="/admin/delete" method="post">
      <input type="hidden" name="level" value="%s">
      <div><input type="submit" value="지우기"></div>
      </form>""" % level)

      self.response.out.write('<hr><br/>')
    
    self.response.out.write("""
    <form action="/admin" method="post">
    <div>Level: <input name="level"></input></div>
    <div>Passcode: <input name="passcode"></input></div>        
    <div>Content <textarea name="content" rows="10" cols="60"> <h1>1단계 </h1> </textarea></div>
    <div><input type="submit" value="문제내기"></div>
    </form>
    </body>
    </html>""")
    
  def post(self):
    quiz = Quiz()
    quiz.content = self.request.get('content')
    quiz.level = self.request.get('level')
    quiz.passcode = self.request.get('passcode')    
    quiz.put()
    self.redirect('/admin')

class DeleteQuiz(webapp.RequestHandler):
  def post(self):
    level = self.request.get('level')
    q = db.GqlQuery("SELECT __key__ FROM Quiz WHERE level = :1", level)
    results = q.fetch(1)
    db.delete(results)
    self.redirect('/admin')    


application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/p', p),
  ('/admin', MakingQuiz),
  ('/admin/delete', DeleteQuiz),              
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
