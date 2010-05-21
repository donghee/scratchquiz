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

# class Greeting(db.Model):
#   author = db.UserProperty()
#   content = db.StringProperty(multiline=True)
#   date = db.DateTimeProperty(auto_now_add=True)

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
    안녕하세요. 파이니 문제은행에 오신것을 축하드립니다.
    각 단계의 문제에 답을 하면 다음 단계를 넘어갈 수 있습니다.
    <br/><br/>
    자 그럼 문제를 풀어 볼까요?
    </div>
    <br/>    
    <div>
    <b> 문제</b>: 파이니의 영어 이름은? (소문자로..) 
    </div>
    <br>
          <form action="/p1" method="post">
            <div><input name="content" cols="60"></input></div>
            <br/>
            <div><input type="submit" value="다음"></div>
          </form>
     """)
#    goto_start(self)


class p1(webapp.RequestHandler):
  def post(self):
    # greeting = Greeting()

    # if users.get_current_user():
    #   greeting.author = users.get_current_user()

#    greeting.content = self.request.get('content')

    if self.request.get('content') == 'piny':
      self.response.out.write("""
      <h1>스크래치 다운로드 받기 </h1>
      <h3>힌트: 아래 클릭.</h3>
      <a href="http://scratch.mit.edu">새창으로 열기</a>
      <br/>
      <br/>
      </div>
    <b> 문제</b>: 현재 스크래치 프로그램의 버전은 (소수점 찍을것. 총3글자)?
    </div>
          <form action="/p2" method="post">
            <div><input name="content" cols="60"></input></div>
            <br/>
            <div><input type="submit" value="다음"></div>
          </form>
          """)
      self.response.out.write("""
      <a href="/">처음으로 </a>
      """)
      
    else:
      retry(self)

class p2(webapp.RequestHandler):
  def post(self):
    if self.request.get('content') == '1.4':
      self.response.out.write("""
      <h1>스크래치 설치하기</h1>
      스크래치를 설치해 봅시다.
      다운로드 받은 ScratchInstaller1.4.exe 파일을 설치하여 봅시다.
      스크래치를 설치하면 C:\Program Files\Scratch 이곳 폴더에 설치가 됩니다.
<div>
<object width="425" height="344"><param name="movie" value="http://www.youtube.com/v/64vsI3nmjbk&hl=ko_KR&fs=1&color1=0xe1600f&color2=0xfebd01"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/64vsI3nmjbk&hl=ko_KR&fs=1&color1=0xe1600f&color2=0xfebd01" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="425" height="344"></embed></object>
</div>
<br>
      <div>
    <b> 문제</b>: 스크래치를 대표하는 동물은? (설치를 하고 실행해보면 알 수 있습니다.)
    </div>

          <form action="/p3" method="post">
            <div><input name="content" cols="60"></input></div>
            <br/>
            <div><input type="submit" value="다음"></div>
          </form>
      
          """)
      self.response.out.write("""
      <a href="/">처음으로 </a>
      """)
      
    else:
      retry(self)      

class p3(webapp.RequestHandler):
  def post(self):
    if self.request.get('content').encode("utf-8") == '고양이':
      self.response.out.write("""
      <h1>스크래치 도움말</h1>
      <br/>
    313호 piny 사무실의 박준표님 책상 아래 있습니다.
    한부씩만 가져가세요. 
      <br/>
      <br/>
      <div>
    <b> 문제</b>: "Getting Started with SCRATCH" 문서는 총 몇장인가요?  (숫자만입력)</b>
    </div>
          <form action="/p4" method="post">
            <div><input name="content" cols="60"></input></div>
            <br/>
            <div><input type="submit" value="다음"></div>
          </form>
      
          """)
      self.response.out.write("""
      <a href="/">처음으로 </a>
      """)
      
    else:
#      self.response.out.write(self.request.get('content') )
      retry(self)      

class p4(webapp.RequestHandler):
  def post(self):
    if self.request.get('content') == '13':
      self.response.out.write("""
      <h1>잠깐 쉬는 시간... </h1>
      <div>
      <object width="425" height="344"><param name="movie" value="http://www.youtube.com/v/mhMQjOYhb7U&hl=ko_KR&fs=1&color1=0xe1600f&color2=0xfebd01"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/mhMQjOYhb7U&hl=ko_KR&fs=1&color1=0xe1600f&color2=0xfebd01" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="425" height="344"></embed></object>
      </div>
      <div>
    <b> 문제</b>: 이 동영상에 나오는 손은 누구의 손 일까요? (답은 보기의 숫자로 입력)
    </div>
    <div>
    1. 김승범 2. 박동희 3. 박영준 4. 박준표 5. 아이유
    </div>
          <form action="/p5" method="post">
            <div><input name="content" cols="60"></input></div>
            <br/>
            <div><input type="submit" value="다음"></div>
          </form>""")
      self.response.out.write("""
      <a href="/">처음으로 </a>
      """)
      
      
    else:
#      self.response.out.write(self.request.get('content') )
      retry(self)      

class p5(webapp.RequestHandler):
  def post(self):
    if self.request.get('content') == '1':
      self.response.out.write("""
      <h1>"Getting Started with SCRATCH" 따라하기 </h1>
      "Getting Started with SCRATCH" 문서를 보고 10번까지 따라 합니다.
      문서를 읽고 다음을 답하세요.
      <div>
    <b> 문제</b>: 스크래치에 있는 객체를 뭐라고 부를까요? (힌트: 5글자)
    </div>
          <form action="/p6" method="post">
            <div><input name="content" cols="60"></input></div>
            <br/>
            <div><input type="submit" value="다음"></div>
          </form>    
      """)
      self.response.out.write("""
      <a href="/">처음으로 </a>
      """)
      
    else:
      retry(self)      

class p6(webapp.RequestHandler):
  def post(self):
    if self.request.get('content').encode('utf-8') == '스프라이트':
      self.response.out.write("""
      <h1>삼각형 그리기</h1>
      스크래치를 사용하여 삼격형을 그려 봅시다.
      "Getting Started with SCRATCH" 문서를 참고하세요.

      <div>
      <img src="/images/triangle.png">
      </div>
      <br/>
      <div>
      문제를 풀면 프로젝트를 "팀이름.sb" 으로 저장하고 저장된 프로젝트를 이메일(
      dongheepark@gmail.com ) 로 첨부하여 보내주세요.

      답신에서 다음 단계 링크를 알려드리겠습니다.
      </div>
      """)
      self.response.out.write("""
      <a href="/">처음으로 </a>
      """)
      
    else:
      retry(self)            

class p7(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
    <h1>오늘은 여기까지 입니다. 아래꺼 보면서 좀 쉬시죠.. </h1>
    
    <object width="425" height="344"><param name="movie" value="http://www.youtube.com/v/VMc-2pPvur0&hl=ko_KR&fs=1&color1=0xe1600f&color2=0xfebd01"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/VMc-2pPvur0&hl=ko_KR&fs=1&color1=0xe1600f&color2=0xfebd01" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="425" height="344"></embed></object>
    <br/>
    <br/>
    <div>
    처음 모였던 3층 회의실로 모여주세요.
    </div>
     """)
    self.response.out.write("""
      <a href="/">처음으로 </a>
      """)
    

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/p1', p1),
  ('/p2', p2),
  ('/p3', p3),
  ('/p4', p4),
  ('/p5', p5),
  ('/p6', p6),
  ('/p7', p7),            
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
