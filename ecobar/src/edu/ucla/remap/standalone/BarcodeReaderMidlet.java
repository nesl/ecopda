package edu.ucla.remap.standalone;

import java.io.DataOutputStream;
import java.io.IOException;

import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;

import edu.ucla.remap.barcode.BarcodeReader;
import edu.ucla.remap.barcode.ImageData;
import edu.ucla.remap.barcode.Profile;
import edu.ucla.remap.camera.CaptureForm;
//import edu.ucla.remap.camera.ImageHandlerForm;

public class BarcodeReaderMidlet extends MIDlet {
	public static String CODEFILE = "file:///E:/ecoCodeTmp.txt";


	protected void destroyApp(boolean arg0) throws MIDletStateChangeException {
		
	}
	
	public void writeTextFile(String s) {
		
		
		CaptureForm.debugAlert(this, "Writing:" + s);
		FileConnection fconn = null;
		try {
			fconn = (FileConnection)Connector.open(CODEFILE);
		} catch (IOException e) {
			CaptureForm.debugAlert(this, "Can't open file (bad URL):" + CODEFILE+ "/n" + e);
			return;
		}
		if(fconn.exists()) {
			if(! fconn.canWrite()) {
				CaptureForm.debugAlert(this, "Can't write to existing file:" +CODEFILE);
			}
		} else {
			try {
				fconn.create();
			} catch (IOException e) {
				CaptureForm.debugAlert(this, "Can't create file:" + CODEFILE + "/n" + e);
				return;				
			}				
		}

		DataOutputStream outStream = null;
		try {
			outStream = fconn.openDataOutputStream();
		} catch (IOException e) {
			CaptureForm.debugAlert(this, "Can't open output stream for:" + CODEFILE + "/n" + e);
			return;				
		}
		try {
			outStream.writeChars(s);
		} catch (IOException e) {
			CaptureForm.debugAlert(this, "Error while writing file:" + CODEFILE + "/n" + e);
			return;				
		}


		try {
			outStream.close();
		} catch (IOException e) {
			CaptureForm.debugAlert(this, "Error while closing stream:" + CODEFILE + "/n" + e);
			return;
		}
		//CaptureForm.debugAlert(this, "file close");

		try {
			fconn.close();
			//CaptureForm.debugAlert(this, "BarcodeReaderMidlet: file writen");
		} catch (IOException e) {
			CaptureForm.debugAlert(this, "Error while closing file:" + CODEFILE+ "/n" + e);
			return;
		}
		//CaptureForm.debugAlert(this, "Barcode number written to " + CODEFILE);
		
	}

	protected void startApp() throws MIDletStateChangeException {
		
		try {
			CaptureForm.debugAlert(this, "Trying to write to file.");
			FileConnection myfconn = (FileConnection)Connector.open("file:///E:/mylog.txt");
			if (!myfconn.exists())
			{
				myfconn.create();
			}
			DataOutputStream mystream = myfconn.openDataOutputStream();
			mystream.writeChars("HI");
			mystream.close();
			myfconn.close();
		}
		catch (Exception e) { }
		byte[] pix = CaptureForm.loadImage(this);
		if(pix != null) {
			ImageData id = new ImageData(pix);
			BarcodeReader br = new BarcodeReader(id, new Profile());
			String result = br.recognize();
			if(br == null) {
				writeTextFile("-1");
			} else {
				writeTextFile(result);
			}
		}
			
		
		notifyDestroyed();
		
	}

	protected void pauseApp() {
		// TODO Auto-generated method stub
		
	}

}
