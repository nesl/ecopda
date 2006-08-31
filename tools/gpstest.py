import appuifw, e32, sys

sys.path.append("E:\\Python")
print sys.path
import gpsmod

def exit_key_pressed():
        going = 0
        appuifw.ap.exit_key_handler = None

appuifw.app.screen='normal'
appuifw.app.title=u'GPS Test Module'
appuifw.app.exit_key_handler = exit_key_pressed

going = 1
gpsThread = gpsmod.gpsModule('00:08:1B:C1:75:F2')
e32.ao_sleep(5)

while going:
	gpsValues = gpsThread.getGPSvalues()
	appuifw.note(unicode(gpsValues), 'info')
	e32.ao_sleep(5)

