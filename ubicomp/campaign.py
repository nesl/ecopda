import appuifw, dir_iter, time, base64, StringIO, httplib, urllib, time, e32, audio
from key_codes import EKeySelect, EKey1, EKey3, EKeyEdit, EKeyBackspace
import graphics

app_lock = e32.Ao_lock()

global user_name, demo_name, demo_auth, demo_affil
global num_vis, demo_rate, demo_comm, image_file
global image_dir, old_files, old_focus
user_name = u''

def exit_key_handler():
  app_lock.signal()

appuifw.app.exit_key_handler = exit_key_handler
oldtitle = appuifw.app.title
appuifw.app.title = u'UCLA\nUrbanCENS'

def get_files():
  global image_dir
  files = []
  for ii in range(len(image_dir.list_repr())):
    if os.path.isdir(image_dir.entry(ii)):
      image_dir.add(ii)
      for jj in range(len(image_dir.list_repr())):
        files.append(image_dir.entry(jj))
      image_dir.pop()
    
  return files

def image_focus(focus):
  if focus:
    global old_focus
    appuifw.app.focus = old_focus
    got_image()
  

def done():
  # reset the user name
  global user_name
  user_name = u''
  splash_screen()
  #exit_key_handler()

def not_done():
  init_app()

def continue_app():
  global user_name, demo_name, demo_auth, demo_affil
  global num_vis, demo_rate, demo_comm, image_file

  user_name = user_name.replace(',', '_')
  demo_name = demo_name.replace(',', '_')
  demo_auth = demo_auth.replace(',', '_')
  demo_affil = demo_affil.replace(',', '_')
  demo_comm = demo_comm.replace(',', '_')
  
  continueScreen = appuifw.Text()
  continueScreen.add(u'Are you done, ' + user_name + u'?')
  continueScreen.add(u'\n\nIf so, please return the equipment back to UrbanCENS.')
  continueScreen.add(u' If not, we will let you document another demo.')
  continueScreen.add(u'\n\n\nAre you done?')
  #pos = continueScreen.get_pos()
  continueScreen.add(u'\nYes (pencil) or No (c)')
  continueScreen.add(u'\nPress and hold the key.')
  #continueScreen.set_pos(pos)
  continueScreen.bind(EKeyEdit, done)
  continueScreen.bind(EKeyBackspace, not_done)

  datasentScreen = appuifw.Text()
  datasentScreen.add(u'Great job, ' + user_name + u'!')
  datasentScreen.add(u'\n\nPlease wait while we slog your data.')  

  appuifw.app.body = datasentScreen

  date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

  t1 = time.time()
  image_output = StringIO.StringIO()
  image_input = open(image_file, "rb")
  base64.encode(image_input, image_output)
  image_data = image_output.getvalue()
  t2 = time.time()

  #print 'Image Base 64 Time %0.3fms' % ((t2-t1)*1000.)
  datasentScreen.add(u'\n\nData encoded...')

  xml = '<?xml version="1.0" encoding="UTF-8"?>'
  xml += '<table>'
  xml += '<row>'
  xml += '<field name="User_Name">' + user_name + '</field>'
  xml += '<field name="Demo_Name">' + demo_name + '</field>'
  xml += '<field name="Demo_Author">' + demo_auth + '</field>'
  xml += '<field name="Affilliation">' + demo_affil + '</field>'
  xml += '<field name="Num_Of_Visitors">' + str(num_vis) + '</field>'
  xml += '<field name="Rate_Of_Demo">' + str(demo_rate) + '</field>'
  xml += '<field name="Comment">' + demo_comm + '</field>'
  xml += '<field name="Image">' + image_data + '</field>'
  #xml += '<field name="Image">' + 'abc' + '</field>'
  xml += '<field name="Date_Time">' + date_time + '</field>'
  xml += '</row>'
  xml += '</table>'

  params = {}
  params['email']='sasank@ee.ucla.edu'
  params['pw']='intel'
  params['data_string']=xml
  params['type']='xml'   
  params['project_id']="22"
  params['tableName']='demoData'

  t1 = time.time()
  params = urllib.urlencode(params)
  t2 = time.time()

  #print 'URL Encode Time %0.3fms' % ((t2-t1)*1000.)
  datasentScreen.add(u'\n\nXML encoded...')

  headers = {}
  headers['Content-type']='application/x-www-form-urlencoded'
  headers['Accept']='text/plain'

  t1 = time.time()
  conn = httplib.HTTPConnection("sensorbase.org")
  conn.request("POST", "/alpha/upload.php", params, headers)
  response = conn.getresponse()
  responseText = response.read()
  conn.close()
  t2 = time.time()

  #print 'HTTP Post Time %0.3fms' % ((t2-t1)*1000.)
  datasentScreen.add(u'\n\nHTTP POST...')
  e32.ao_sleep(1)

  #print responseText

  appuifw.app.body = continueScreen

def got_image():
  global image_file
  global old_files
  new_files = get_files()
  for file in old_files:
    try:
      new_files.remove(file)
    except ValueError:
      print u'Huh?'
    
  if len(new_files) == 0:
    get_image()
  else:
    if len(new_files) > 1:
      index = appuifw.selection_list(map(unicode, new_files))
    else:
      index = 0
    image_file = new_files[index]
    
    continue_app()
  

def get_image():
  global user_name
  global image_dir, old_files, old_focus
  imageScreen = appuifw.Text()
  imageScreen.add(u'Hi ' + user_name + ',\n')
  imageScreen.add(u'  Great job collecting that information.')
  imageScreen.add(u' Now please take a representative image of the demo that shows its uniqueness or value.')
  imageScreen.add(u'\n\nPress and hold the camera button to start capture.')
  image_dir = dir_iter.Directory_iter([u'e:\\Images',])
  image_dir.add(0)
  old_files = get_files()
  
  old_focus = appuifw.app.focus
  appuifw.app.focus = image_focus
  appuifw.app.body = imageScreen
  

def start_app():
  global user_name, demo_name, demo_auth, demo_affil
  global num_vis, demo_rate, demo_comm, image_file
  
  yname = u'Your Name'
  dname = u'Demo Name'
  dauth = u'Demo Author'
  daff  = u'Demo Affiliation'
  nvis  = u'Number of Visitors'
  drate = u'Demo Rating'
  comm  = u'One Word Comment'
  demoList = [yname, dname, dauth, daff, nvis, drate, comm]
  
  if user_name:
    demoList.pop(0)
  
  def edit():
    global user_name, demo_name, demo_auth, demo_affil
    global num_vis, demo_rate, demo_comm, image_file
    current = questListBox.current()
    curr = demoList[current]
    if curr == yname:
      user_name = appuifw.query(u'What is your name?', 'text')
      if user_name <> None:
        demoList.pop(current)
        if len(demoList):
          questListBox.set_list(demoList)
        
      
    elif curr == dname:

      demo_name_list = [u'DietGame', u'CoCoa', u'UbiREAL', u'AudioIndex', u'RedTacton', u'MASTABA']
      demo_name_list = demo_name_list + [u'UbiCommunity', u'Barcode', u'WiRope', u'Pileus', u'BiblioRoll', u'LINC', u'AnonComm']
      demo_name_list = demo_name_list + [u'Push!Photo', u'UrbanCENS', u'HumanState', u'SpaceTracer', u'RWAttention', u'Flood']
      demo_name_list = demo_name_list + [u'Jetcam', u'Hullabaloo', u'IPoi', u'TinyObj', u'MedAware', u'SmartFuroshiki', u'WonderWall']
      demo_name_list = demo_name_list + [u'MicroLearning', u'Spinal', u'Haggle', u'Crossroads', u'Other']
    
      demo_name_list.sort()
 
      demo_name_index = appuifw.popup_menu(demo_name_list, u"Select the demo name and press ok.")
      if(demo_name_index in range(0, 31)):
        demo_name = demo_name_list[demo_name_index]
        demoList.pop(current)
        if len(demoList):
          questListBox.set_list(demoList)

      #demo_name_index = appuifw.selection_list(choices=demo_name_list, search_field=1)

      #demo_name = appuifw.query(u'What is the name of the demo?', 'text')
      #if demo_name <> None:
      #  demoList.pop(current)
      #  if len(demoList):
      #    questListBox.set_list(demoList)
        
      
    elif curr == dauth:
      demo_auth = appuifw.query(u'Who is the author of the demo?', 'text')
      if demo_auth <> None:
        demoList.pop(current)
        if len(demoList):
          questListBox.set_list(demoList)
        
      
    elif curr == daff:
      demo_affil = appuifw.query(u'What is the demo affiliation?', 'text')
      if demo_affil <> None:
        demoList.pop(current)
        if len(demoList):
          questListBox.set_list(demoList)
        
      
    elif curr == nvis:
      num_vis = appuifw.query(u'How many visitors are there?', 'number')
      if num_vis <> None:
        demoList.pop(current)
        if len(demoList):
          questListBox.set_list(demoList)
        
      
    elif curr == drate:
      demo_rate = 11
      while demo_rate < 1 or demo_rate > 10:
        demo_rate = appuifw.query(u'What is the rating of the demo? (1-10)', \
                                    'number', 1)
        if demo_rate == None:
          break
      if demo_rate <> None:
        demoList.pop(current)
        if len(demoList):
          questListBox.set_list(demoList)
        
      
    elif curr == comm:
      demo_comm = u'a a'
      while len(demo_comm.split(u' ')) > 1:
        demo_comm = appuifw.query(u'Give a one word comment.', 'text')
        if demo_comm == None:
          break
      if demo_comm <> None:
        demoList.pop(current)
        if len(demoList):
          questListBox.set_list(demoList)
        
      
    if not len(demoList):
      get_image()
    
  
  questListBox = appuifw.Listbox(demoList)
  questListBox.bind(EKeySelect, edit)
  appuifw.app.body = questListBox

def splash_screen():

  appuifw.app.body = c = appuifw.Canvas()
  im = graphics.Image.open('E:\\Python\\splash.jpg')

  c.blit(im, target=(5,23), scale=0)
  #sf = audio.Sound.open('E:\\Sounds\\gb.m4a')
  #sf.play()
  #e32.ao_sleep(16)
  c.bind(EKeySelect, init_app)

def init_app():
  global user_name, demo_name, demo_auth, demo_affil
  global num_vis, demo_rate, demo_comm, image_file

  demo_name = u''
  demo_auth = u''
  demo_affil = u''
  num_vis = 0
  demo_rate = 1
  demo_comm = u''
  image_file = u''
  
  title = u'UCLA UrbanCENS'
  if (user_name == u''):
    intro = u'Welcome.'
  else:
    intro = u'Welcome back, ' + user_name + u'.'
  intro += u' Today, our campaign is to document other Ubicomp demos.'
  intro += u' Your input will be used to find the best demos, most popular demos, and document comments about each demo.'
  cont = u'Press the center joystick button to start.'
  
  textScreen = appuifw.Text()
  
  plainStyle = textScreen.style
  textScreen.font = 'title'
  textScreen.style = appuifw.STYLE_BOLD
  textScreen.add(title + '\n\n')
  textScreen.font = 'normal'
  textScreen.style = plainStyle
  textScreen.add(intro + '\n\n')
  textScreen.add(cont)
  
  textScreen.bind(EKeySelect, start_app)

  appuifw.app.body = textScreen

#init_app()
splash_screen()
app_lock.wait()
appuifw.app.title = oldtitle
appuifw.app.body = None
