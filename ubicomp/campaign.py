import appuifw, dir_iter, time, base64, StringIO, httplib, urllib, time, e32, audio
from key_codes import EKeySelect, EKey1, EKey3, EKeyEdit, EKeyBackspace
import graphics

app_lock = e32.Ao_lock()

global user_name, demo_name, demo_novel, demo_new
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
  init_app()
  #splash_screen()
  #exit_key_handler()

def not_done():
  init_app()

def continue_app():
  global user_name, demo_name, demo_novel, demo_new
  global num_vis, demo_rate, demo_comm, image_file

  datasentScreen = appuifw.Text()
  datasentScreen.add(u'Great job, ' + user_name + u'!')
  datasentScreen.add(u'\n\nWe will slog your data now.')  
  datasentScreen.add(u'\n\nThis might take a couple of mins.')
  datasentScreen.add(u'\nData will be encoded, wrapped in xml, and sent.')

  appuifw.app.body = datasentScreen

  user_name_filtered  = user_name.replace(',', '_')
  demo_name_filtered  = demo_name.replace(',', '_')
  demo_novel_filtered = demo_novel.replace(',', '_')
  demo_new_filtered   = demo_new.replace(',', '_')
  demo_comm_filtered  = demo_comm.replace(',', '_')

  for chr in user_name_filtered:
	if ord(chr) not in range(0, 128):
		user_name_filtered = user_name_filtered.replace(chr, '_')

  for chr in demo_name_filtered:
        if ord(chr) not in range(0, 128):
                demo_name_filtered = demo_name_filtered.replace(chr, '_')

  for chr in demo_novel_filtered:
        if ord(chr) not in range(0, 128):
                demo_novel_filtered = demo_novel_filtered.replace(chr, '_')

  for chr in demo_new_filtered:
        if ord(chr) not in range(0, 128):
                demo_new_filtered = demo_new_filtered.replace(chr, '_')

  for chr in demo_comm_filtered:
        if ord(chr) not in range(0, 128):
                demo_comm_filtered = demo_comm_filtered.replace(chr, '_')

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

  date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

  image_output = StringIO.StringIO()
  image_input = open(image_file, "rb")
  base64.encode(image_input, image_output)
  image_data = image_output.getvalue()

  #print 'Image Base 64 Time %0.3fms' % ((t2-t1)*1000.)
  datasentScreen.add(u'\n\nData encoded...')

  xml = '<?xml version="1.0" encoding="UTF-8"?>'
  xml += '<table>'
  xml += '<row>'
  xml += '<field name="User_Name">' + user_name_filtered + '</field>'
  xml += '<field name="Demo_Name">' + demo_name_filtered + '</field>'
  xml += '<field name="Demo_Novel">' + demo_novel_filtered + '</field>'
  xml += '<field name="Demo_New">' + demo_new_filtered + '</field>'
  xml += '<field name="Num_Of_Visitors">' + str(num_vis) + '</field>'
  xml += '<field name="Rate_Of_Demo">' + str(demo_rate) + '</field>'
  xml += '<field name="Comment">' + demo_comm_filtered + '</field>'
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
  params['project_id']="39"
  params['tableName']='ubicompDemo'

  params = urllib.urlencode(params)

  #print 'URL Encode Time %0.3fms' % ((t2-t1)*1000.)
  datasentScreen.add(u'\nXML encoded...')

  headers = {}
  headers['Content-type']='application/x-www-form-urlencoded'
  headers['Accept']='text/plain'

  conn = httplib.HTTPConnection("sensorbase.org")
  conn.request("POST", "/alpha/upload.php", params, headers)
  response = conn.getresponse()
  responseText = response.read()
  conn.close()

  #print 'HTTP Post Time %0.3fms' % ((t2-t1)*1000.)
  datasentScreen.add(u'\nHTTP POST...')
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
  imageScreen.add(u'Hi ' + user_name + '.\n\n')
  imageScreen.add(u'Great job collecting that information.\n\n')
  imageScreen.add(u'Now please take a representative image of the demo that shows its uniqueness or value.')
  imageScreen.add(u'\n\nPress and hold the camera button to start capture.')
  image_dir = dir_iter.Directory_iter([u'e:\\Images',])
  image_dir.add(0)
  old_files = get_files()
  
  old_focus = appuifw.app.focus
  appuifw.app.focus = image_focus
  appuifw.app.body = imageScreen
  

def start_app():
  global user_name, demo_name, demo_novel, demo_new
  global num_vis, demo_rate, demo_comm, image_file
  
  yname = u'Your Name'
  dname = u'Demo Name'
  dnovel = u'Novel Attribute'
  dnew  = u'New Knowledge'
  nvis  = u'Number of Visitors'
  drate = u'Interest Rating'
  comm  = u'One Word Tag'
  demoList = [yname, dname, dnovel, dnew, nvis, drate, comm]
  
  if user_name:
    demoList.pop(0)
  
  def edit():
    global user_name, demo_name, demo_novel, demo_new
    global num_vis, demo_rate, demo_comm, image_file
    current = questListBox.current()
    curr = demoList[current]
    if curr == yname:
      user_name = appuifw.query(u'Please tell us your name.', 'text')
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

    elif curr == dnovel:
      demo_novel = appuifw.query(u'Tell us what is novel about the demo.', 'text')
      if demo_novel <> None:
        demoList.pop(current)
        if len(demoList):
          questListBox.set_list(demoList)
        
      
    elif curr == dnew:
      demo_new = appuifw.query(u'Tell us something new you learned from talking to the author.', 'text')
      if demo_new <> None:
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
        demo_rate = appuifw.query(u'How interesting is the demo? [ 1 - not, \n 5 - moderate, 10 - very ]', \
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
        demo_comm = appuifw.query(u'Please give us a one word descriptive tag for the demo.', 'text')
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
  global user_name, demo_name, demo_novel, demo_new
  global num_vis, demo_rate, demo_comm, image_file

  demo_name = u''
  demo_novel = u''
  demo_new = u''
  num_vis = 0
  demo_rate = 1
  demo_comm = u''
  image_file = u''
  
  title = u'UCLA UrbanCENS'
  if (user_name == u''):
    intro = u'Welcome.'
    intro += u'Today, our campaign is to document other Ubicomp demos.'
    intro += u'\n\nIn the process, we hope to:\n'
    intro += u'\n- encourage interaction with authors'
    intro += u'\n- get user perspectives on demos'
    intro += u'\n- show partisans in action'
  else:
    intro = u'Welcome back, ' + user_name + u'.\n'
    intro += u'Thanks for documenting that last demo. '
    intro += u'When you are ready, lets document another.'

  cont = u'Press the center joystick to start.'
  
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

init_app()
#splash_screen()
app_lock.wait()
appuifw.app.title = oldtitle
appuifw.app.body = None
