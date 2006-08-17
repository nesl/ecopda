# Need to show lat/lon even if there's not WLAN access.
# Exit only seems to work in Audio
# How to use gprs to get yahoo images?


# Copyright (c) 2006 Jurgen Scheible
# Application skeleton (no main loop)

import time
import appuifw
import e32
# for audio stuff
import audio
# for camera stuff
import camera
from key_codes import *
from graphics import *
# for BlueTooth GPS
import socket, location, urllib

### BT GPS App
class GPS:
	def __init__(self):
	    self.connect()
            self.displayUrl = None
            self.url = None
            self.running = 1
	def connect(self):
	    self.sock = socket.socket(socket.AF_BT,socket.SOCK_STREAM)
	    address,services = socket.bt_discover()
	    print "Discovered: %s, %s"%(address, services)
	    target = (address, services.values()[0])
            print "Connecting to " + str(target)
	    self.sock.connect(target)
	def close(self):
	    self.sock.close()
	def getPacket(self):
	    GPSPacket(self.sock).load()
        def getImage(self, lat, long):
            tempfile = "C:\\s60_py_gpsmap_api_cache"
            url = "http://api.local.yahoo.com/MapsService/V1/mapImage?appid=s60_py_gpsmap&latitude=%s&longitude=%s&image_height=145&image_width=176&zoom=3" % (lat,long)
            self.url = url
            urllib.urlretrieve( url, tempfile )
            f = open( tempfile, 'r' )
            mapinfo = f.read()
            f.close()
            startrestag = mapinfo.find( '<Result ' )
            endrestag = mapinfo.find( '>', startrestag )
            endrestag = endrestag + 1
            endrestext = mapinfo.find( '<', endrestag )
            imgurl = mapinfo[endrestag:endrestext]
            urllib.urlretrieve(imgurl, "C:\\ymap.png")
        def showLatLon(self, latitude, longitude):
            appuifw.app.body = appuifw.Text(u'GPS\nlat:' + str(latitude) + u'\nlon:' + str(longitude))
        def load(self):
            haveFix=0
            latitude_in=0
            longitude_in=0
            while self.running:
                  buffer=""
                  ch=self.sock.recv(1)
                  while (ch!='$'):
                        ch=self.sock.recv(1)
                  while 1:
                        if (ch=='\r'):
                           break
                        buffer+=ch
                        ch=self.sock.recv(1)
                  if (buffer[0:6]=="$GPGGA"):
                     try:
                         (GPGGA,utcTime,lat,ns,lon,ew,posfix,sats,hdop,alt,altunits,sep,sepunits,age,sid)=buffer.split(",")
                         latitude_in=float(lat)
                         longitude_in=float(lon)
                         haveFix=int(posfix)
                     except:
                            haveFix=0
                     if haveFix:

                        zoom=2
                        if ns == 'S':
                           latitude_in = -latitude_in
                        if ew == 'W':
                           longitude_in = -longitude_in
                        latitude_degrees = int(latitude_in/100)
                        latitude_minutes = latitude_in - latitude_degrees*100
                        longitude_degrees = int(longitude_in/100)
                        longitude_minutes = longitude_in - longitude_degrees*100
                        latitude = latitude_degrees + (latitude_minutes/60)
                        longitude = longitude_degrees + (longitude_minutes/60)
                        self.showLatLon(latitude, longitude)
                        try:
                            self.getImage( latitude, longitude )
                        except:
                            pass
                        if self.url!=self.displayUrl:
                           try:
                               id = appuifw.app.body.current()
                               content_handler = appuifw.Content_handler()
                               content_handler.open("C:\\ymap.png")
                           except IOError:
                                  appuifw.note(u"Could not fetch the map.",'info')
                           except Exception, E:
                                  appuifw.note(u"Could not open the map, %s"%E,'info')
                           self.displayUrl = self.url
                           self.running = 0
            e32.ao_sleep(0.2)

class GPSApp:
      def __init__(self):
          self.gps = GPS()
          self.gpspacket = None
          self.message = u''
#       def update(self):
#           appuifw.app.body = appuifw.Text(u'Waiting for update...')
#           self.packet = self.gps.getPacket()
#           appuifw.app.body = appuifw.Text(u'Lat:' + self.packet.lat + ' Lon:' + self.packet.lon)
      def update(self):
          self.gps.load()
      def switch_in(self):
          appuifw.app.menu = [(u"Update", self.update)]
          appuifw.app.title = u'GPS'
          appuifw.app.body = appuifw.Text(u'GPS')
      def switch_out(self):
          return

### Audio App

class AudioApp:
      def __init__(self):
          self.S = None
          self.body = appuifw.Text(u'Audio')
          self.filename_prefix = u'e:\\Sounds\obs_'
          self.filename = u''
      def recording(self):
          self.filename = self.filename_prefix + str(int(time.time())) + u'.wav'
          self.S = audio.Sound.open(self.filename)
          self.S.record()
          appuifw.note(u"Recording to " + self.filename)
      def playing(self):
        try:
            self.S = audio.Sound.open(self.filename)
            self.S.play()
            appuifw.note(u"Playing " + self.filename)
        except:
               appuifw.note(u"Record something first.")
      def closing(self):
          self.S.stop()
          self.S.close()
          appuifw.note(u"Stopped.")
      def switch_in(self):
          appuifw.app.menu =[(u"play", self.playing),
                           (u"record", self.recording),
                           (u"stop", self.closing)]
          appuifw.app.title = u'Audio'
          appuifw.app.body = self.body
      def switch_out(self):
          return

### Image App

class Keyboard(object):
  def __init__(self,onevent=lambda:None):
      self._keyboard_state={}
      self._downs={}
      self._onevent=onevent
  def handle_event(self,event):
      if event['type'] == appuifw.EEventKeyDown:
          code=event['scancode']
          if not self.is_down(code):
              self._downs[code]=self._downs.get(code,0)+1
          self._keyboard_state[code]=1
      elif event['type'] == appuifw.EEventKeyUp:
          self._keyboard_state[event['scancode']]=0
      self._onevent()
  def is_down(self,scancode):
      return self._keyboard_state.get(scancode,0)
  def pressed(self,scancode):
      if self._downs.get(scancode,0):
          self._downs[scancode]-=1
          return True
      return False

# 1280x960, 800x600, 640x480
# N80 screen is 352x416
class ImageApp:
      def __init__(self):
          self.save_picture_flag = 0
          self.keyboard = Keyboard()
          self.screen_picture = camera.take_photo(size = (640,480))
          self.img = Image.new((176,208))
          self.canvas = appuifw.Canvas(event_callback=self.keyboard.handle_event,
                      redraw_callback=self.handle_redraw)
          self.filename_prefix = u'e:\\Images\obs_'
          self.filename = u''
      def handle_redraw(self,rect):
          self.img.blit(self.screen_picture, target=(8,10, 168, 130), scale=1)
          self.canvas.blit(self.img)
      def save_picture(self):
          self.save_picture_flag = 1
          appuifw.note(u"Standby...","info")
      def switch_in(self):
          appuifw.app.body = self.canvas
          appuifw.app.menu =[(u"Save Image", self.save_picture)]
          appuifw.app.title = u'Image'
          self.screen_picture = camera.take_photo(size = (640,480))
          self.running = 1
          while self.running:
                if self.save_picture_flag:
                   self.running = 0
                   try:
                       self.screen_picture = camera.take_photo(size = (1280,960))
                       self.filename = self.filename_prefix + str(int(time.time())) + u'.jpg'
                       self.screen_picture.save(self.filename)
                       appuifw.note(u"Picture saved to " + self.filename, "conf")
                   except:
                          pass
                else:
                     try:
                         self.screen_picture = camera.take_photo(size = (640,480))
                     except:
                            pass
                self.handle_redraw(())
                e32.ao_yield()
          self.handle_redraw(())
      def switch_out(self):
          self.running = 0
          return

################################
### Main part of application

def exit_key_handler():
    app_lock.signal()

# Create a table handler that switches the application based on what tab is selected:
def handle_tab(index):
    audioapp.switch_out()
    imageapp.switch_out()
    gpsapp.switch_out()
    if index == 0:
       imageapp.switch_in()
    elif index == 1:
       audioapp.switch_in()
    elif index == 2:
         gpsapp.switch_in()
#     if index == 2:
#        appuifw.app.body = app_tags

# Create Application Objects
audioapp = AudioApp()
imageapp = ImageApp()
gpsapp = GPSApp()

# Create an Active Object
app_lock = e32.Ao_lock()

# Create the tabs with its names in unide as a list, include the tab handler
appuifw.app.set_tabs([u"Image", u"Audio", u"GPS"], handle_tab)

appuifw.app.exit_key_handler = exit_key_handler

# Set app.body to app1 (for start of script)
handle_tab(0)

app_lock.wait()
