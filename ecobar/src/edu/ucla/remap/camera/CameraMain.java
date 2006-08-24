package edu.ucla.remap.camera;

import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;

public class CameraMain extends MIDlet  {
	CaptureForm captureForm = null;

	protected void startApp() throws MIDletStateChangeException {
		if(captureForm == null) {
			captureForm = new CaptureForm(this);
		} else {
			captureForm.wake();
		}

	}

	protected void pauseApp() {
		captureForm.pause();

	}

	protected void destroyApp(boolean arg0) throws MIDletStateChangeException {
		captureForm.quit();
	}
}
