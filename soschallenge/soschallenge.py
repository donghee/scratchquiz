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
import os
import glob
import random

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Quiz(db.Model):
  author = db.StringProperty()
  level = db.StringProperty()
  passcode = db.StringProperty()
  content = db.TextProperty()
  date = db.DateTimeProperty(auto_now_add=True)

def retry(req):
  template_values = {
    }
  path = os.path.join(os.path.dirname(__file__), 'templates','retry.html')
  req.response.out.write(template.render(path, template_values))

def end(req):
  req.response.out.write("""
      <h1>미션 완료.</h1>
    """)

class MainPage(webapp.RequestHandler):

  def __init__(self):
    self.p_passcode = None
    self.template_path = os.path.join(os.path.dirname(__file__), 'templates','index.html')
    self.imagepath=os.path.join(os.path.dirname(__file__), 'images')
    self.imagefiles = ["addList.gif","addVariable.gif",
                    "allMotorsOff.gif","allMotorsOn.gif",
                    "and.gif","answer.gif","append_toList_.gif",
                    "backgroundIndex.gif", "bounceOffEdge.gif","broadcastHat.gif",
                    "broadcast_.gif","changeGraphicEffect_by_.gif",
                    "changePenHueBy_.gif","changePenShadeBy_.gif",
                    "changePenSizeBy_.gif","changeSizeBy_.gif",
                    "changeTempoBy_.gif","changeVolumeBy_.gif",
                    "changeXposBy_.gif","changeYposBy_.gif",
                    "clearPenTrails.gif","color_sees_.gif",
                    "comeToFront.gif","computeFunction_of_.gif",
                    "concatenate_with_.gif","contentsOfList_.gif",
                    "costumeIndex.gif","deleteLine_ofList_.gif",
                    "deleteList.gif","deleteVariable.gif",
                    "distanceTo_.gif","divide.gif",
                    "doAsk.gif","doBroadcastAndWait.gif",
                    "doForever.gif","doForeverIf.gif",
                    "doIf.gif","doIfElse.gif",
                    "doPlaySoundAndWait.gif","doRepeat.gif",
                    "doReturn.gif","doUntil.gif",
                    "doWaitUntil.gif","drum_duration_elapsed_from_.gif",
                    "equals.gif","filterReset.gif",
                    "forward_.gif","getAttribute_of_.gif",
                    "getLine_ofList_.gif","glideSecs_toX_y_elapsed_from_.g",
                    "goBackByLayers_.gif","gotoSpriteOrMouse_.gif",
                    "gotoX_y_.gif","greaterThan.gif",
                    "heading.gif","heading_.gif",
                    "hide.gif","hideVariable_.gif",
                    "images","index.html",
                    "insert_at_ofList_.gif","isLoud.gif",
                    "keyHat.gif","keyPressed_.gif",
                    "lessThan.gif","letter_of_.gif",
                    "lineCountOfList_.gif","list_contains_.gif",
                    "lookLike_.gif","midiInstrument_.gif",
                    "minus.gif","mod.gif",
                    "motorOnFor_elapsed_from_.gif","mousePressed.gif",
                    "mouseX.gif","mouseY.gif",
                    "mouseclickHat.gif","nextBackground.gif",
                    "nextCostume.gif","not.gif",
                    "noteOn_duration_elapsed_from_.g","or.gif",
                    "penColor_.gif","penSize_.gif",
                    "playSound_.gif","plus.gif",
                    "pointTowards_.gif","putPenDown.gif",
                    "putPenUp.gif","randomFrom_to_.gif",
                    "rest_elapsed_from_.gif","rounded.gif",
                    "say_.gif","say_duration_elapsed_from_.gif",
                    "scale.gif","sensorPressed_.gif",
                    "sensor_.gif","setGraphicEffect_to_.gif",
                    "setLine_ofList_to_.gif","setMotorDirection_.gif",
                    "setPenHueTo_.gif","setPenShadeTo_.gif",
                    "setSizeTo_.gif","setTempoTo_.gif",
                    "setVolumeTo_.gif","show.gif",
                    "showBackground_.gif","showVariable_.gif",
                    "soundLevel.gif","stampCostume.gif",
                    "startHat.gif","startMotorPower_.gif",
                    "stopAll.gif","stopAllSounds.gif",
                    "stringLength_.gif","tempo.gif",
                    "think_.gif","think_duration_elapsed_from_.gi",
                    "timer.gif","timerReset.gif",
                    "times.gif","touchingColor_.gif",
                    "touching_.gif","turnLeft_.gif",
                    "turnRight_.gif","variable.gif",
                    "variableChangeBy.gif","variableSet.gif",
                    "volume.gif","wait_elapsed_from_.gif",
                    "xpos.gif","xpos_.gif",
                    "ypos.gif","ypos_.gif"]

    
  
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
          <form action="/" method="post">
            <div><input name="name" cols="60"></input></div>                      
            <div><input type="hidden" name="nextlevel" value=1 cols="60"></input></div>
            <div><input type="hidden" name="passcode" value=0 cols="60"></input></div>
            <div><input type="hidden" name="skipnext" value=True cols="60"></input></div>            
            <br/>
            <div><input type="submit" value="다음"></div>
          </form>
     """)
#    goto_start(self)

  def post(self):
    _level = self.request.get('nextlevel').encode("utf-8")
    _passcode = self.request.get('passcode').encode("utf-8")
    isSkip = self.request.get('skipnext').encode("utf-8")    

    query = Quiz().all()
    if _level != '1':
      pquiz = query.filter('level =', str(int(_level)-1)).fetch(1)[0]
      self.p_passcode = pquiz.passcode.encode('utf-8')

    query = Quiz().all()
    try:
      quiz = query.filter('level =', _level).fetch(1)[0]
    except IndexError:
      end(self)
      return

    content = quiz.content.encode('utf-8')
    level = quiz.level.encode('utf-8')
    passcode = quiz.passcode.encode('utf-8')

#    print self.template_path
#    print os.path.join(os.path.dirname(__file__), 'images')
#    imagefiles = glob.glob(self.imagepath+os.sep+'*.gif')
#    print imagefiles
    imagefile = random.choice(self.imagefiles)
    

    if isSkip  == 'True' or  _passcode == self.p_passcode :
      template_values = {
        'headerimage' : imagefile,                
        'level' : level,        
        'content' : content,
        'nextlevel' : str(int(level)+1)
        }
      self.response.out.write(template.render(self.template_path, template_values))      
      self.p_passcode = passcode
    else:
      retry(self)
    

class MakingQuiz(webapp.RequestHandler):
  def __init__(self):
    self.template_path = os.path.join(os.path.dirname(__file__), 'templates','admin.html')

    
  def get(self):
    self.response.out.write('<html><body>')
    quizs = db.GqlQuery("SELECT * FROM Quiz ORDER BY level LIMIT 10")
    template_values = {
      'quizs' : quizs
      }
    self.response.out.write(template.render(self.template_path, template_values))      

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
  ('/admin', MakingQuiz),
  ('/admin/save', MakingQuiz),  
  ('/admin/delete', DeleteQuiz),
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
