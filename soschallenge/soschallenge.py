# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright 2010 PINY.
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


# DB
class Quiz(db.Model):
  author = db.StringProperty()
  level = db.StringProperty() # TODO: integer로 수정
  passcode = db.TextProperty()  
  subject = db.TextProperty()  
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
      <a href="/"> 처음으로 </a>      
    """)

class MainPage(webapp.RequestHandler):

  def __init__(self):
    self.p_passcode = None
    template_path = os.path.join(os.path.dirname(__file__), 'templates')
    self.index_template_path = os.path.join(template_path ,'index.html')
    self.quiz_template_path = os.path.join(template_path ,'quiz.html')    
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
    template_values = {}
    self.response.out.write(template.render(self.index_template_path, template_values))

#    goto_start(self)

  def post(self):
    _level = self.request.get('level').encode("utf-8")
    _passcode = self.request.get('passcode').encode("utf-8")
    isSkip = self.request.get('skipnext').encode("utf-8")    

    query = Quiz().all()
    if _level != '0':
      pquiz = query.filter('level =', _level).get()
      self.p_passcode = pquiz.passcode.encode('utf-8')

    query = Quiz().all()
    quiz = query.filter('level >', _level).order('level').get()
    imagefile = random.choice(self.imagefiles)

    if isSkip  == 'True' or  _passcode == self.p_passcode :
      if quiz == None:
        end(self)
        return

      subject = quiz.subject.encode('utf-8')
      content = quiz.content.encode('utf-8')
      level = quiz.level.encode('utf-8')
      passcode = quiz.passcode.encode('utf-8')

      template_values = {
        'headerimage' : imagefile,                
        'subject' : subject,       
        'content' : content,
        'level' : level
        }
      self.response.out.write(template.render(self.quiz_template_path, template_values))      
      self.p_passcode = passcode
    else:
      retry(self)
    

class ManageQuiz(webapp.RequestHandler):
  def __init__(self):
    self.template_path = os.path.join(os.path.dirname(__file__), 'templates','admin.html')
    
  def get(self):
    quizs = db.GqlQuery("SELECT * FROM Quiz ORDER BY level LIMIT 20")
    template_values = {
      'quizs' : quizs
      }
    self.response.out.write(template.render(self.template_path, template_values))

class SaveQuiz(webapp.RequestHandler):
  def post(self):
    quiz = Quiz()
    quiz.subject = self.request.get('subject')    
    quiz.content = self.request.get('content')
    quiz.level = self.request.get('level')
    quiz.passcode = self.request.get('passcode')    
    quiz.put()
    self.redirect('/admin')

class ModifyQuiz(webapp.RequestHandler):
  def post(self):
    level = self.request.get('level')
    q = db.GqlQuery("SELECT __key__ FROM Quiz WHERE level = :1", level)
    quiz = q.get()
    quiz.level = self.request.get('level')
    quiz.passcode = self.request.get('passcode')
    quiz.subject = self.request.get('subject')
    quiz.content = self.request.get('content')
#    quiz.put()
#    db.put(quiz)
#    print type(quiz)
#    print dir(quiz)
    self.redirect('/admin')

class DeleteQuiz(webapp.RequestHandler):
  def post(self):
    level = self.request.get('level')
    q = db.GqlQuery("SELECT __key__ FROM Quiz WHERE level = :1", level)
    results = q.get()
    db.delete(results)
    self.redirect('/admin')    


application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/admin', ManageQuiz),
  ('/admin/save', SaveQuiz),
  ('/admin/modify', ModifyQuiz),    
  ('/admin/delete', DeleteQuiz),
], debug=True)

def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
# GAE_PATH = "C:\\Program Files\\Google\\google_appengine"

# EXTRA_PATHS = [
#   GAE_PATH,
#   os.path.join(GAE_PATH, 'lib', 'antlr3'),
#   os.path.join(GAE_PATH, 'lib', 'django'),
#   os.path.join(GAE_PATH, 'lib', 'ipaddr'),
#   os.path.join(GAE_PATH, 'lib', 'webob'),
#   os.path.join(GAE_PATH, 'lib', 'yaml', 'lib'),
#   ]
# SCRIPT_DIR = os.path.join(GAE_PATH, 'google', 'appengine', 'tools')
# sys.path = EXTRA_PATHS + [SCRIPT_DIR] + sys.path 

  main()
