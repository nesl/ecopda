package edu.ucla.remap.camera;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;

import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.midlet.MIDlet;

import edu.ucla.remap.barcode.BarcodeReader;
import edu.ucla.remap.barcode.ImageData;
import edu.ucla.remap.barcode.Profile;

public class ImageHandlerForm extends Form implements CommandListener {
	public static final String IMGFILE = "file:///E:/ecoBarTmp.bmp";

	private final Command exitCmd;
	private final Command recognizeCmd;
	private final Command saveCmd;
	private final Command backCmd;
	
	private MIDlet midlet;
	private ImageData imageData;
	private Profile profile;
	private CaptureForm captureForm;

	public ImageHandlerForm(MIDlet midlet, ImageData imageData, Profile profile, CaptureForm captureForm) {
		super("Image Handler");
		
		this.midlet = midlet;
		this.imageData = imageData;
		this.profile = profile;
		this.captureForm = captureForm;
		
		exitCmd = new Command("Exit", Command.EXIT, 1);
		backCmd = new Command("Back", Command.BACK, 1);
		recognizeCmd = new Command("Read Barcode", Command.OK, 1);
		saveCmd = new Command("Save Image", Command.OK, 1);
		
		addCommand(exitCmd);
		addCommand(backCmd);
		addCommand(recognizeCmd);
		addCommand(saveCmd);

		append("Image Captured\n");

		Display.getDisplay(midlet).setCurrent(this);

		setCommandListener(this);
	}

	public void writeResult(String result)
	{
		try {
			String blah = "0";
			FileConnection myfconn = (FileConnection)Connector.open("file:///E:/mylog.txt");
			if (!myfconn.exists())
			{
				myfconn.create();
			}
			DataOutputStream mystream = myfconn.openDataOutputStream();
			if (result != null)
			{
				mystream.writeChars(result);
			}
			else
			{
				mystream.writeChars(blah);
			}
			mystream.close();
			myfconn.close();
		}
		catch (Exception e) { }
		
	}
	public void commandAction(Command cmd, Displayable arg1) {
		if(cmd.equals(exitCmd)) {
			midlet.notifyDestroyed();
		} else if (cmd.equals(recognizeCmd)) {
			append("recognizing...\n");
			BarcodeReader br = new BarcodeReader(imageData, profile);
			String result = br.recognize();
			if(result == null) {
				append("Unable to recognize barcode\n");
			} else {
				append(result);
			}
			writeResult(result);
			
		} else if (cmd.equals(saveCmd)) {
			FileConnection fconn = null;
			try {
				fconn = (FileConnection)Connector.open(IMGFILE);
			} catch (IOException e) {
				CaptureForm.debugAlert(midlet, "Can't open file (bad URL):" + IMGFILE + "/n" + e);
				return;
			}
			if(fconn.exists()) {
				if(! fconn.canWrite()) {
					CaptureForm.debugAlert(midlet, "Can't write to existing file:" + IMGFILE);
				}
			} else {
				try {
					fconn.create();
				} catch (IOException e) {
					CaptureForm.debugAlert(midlet, "Can't create file:" + IMGFILE + "/n" + e);
					return;				
				}				
			}

			OutputStream outStream = null;
			try {
				outStream = fconn.openDataOutputStream();
			} catch (IOException e) {
				CaptureForm.debugAlert(midlet, "Can't open output stream for:" + IMGFILE + "/n" + e);
				return;				
			}
			try {
				outStream.write(imageData.pixel_data);
			} catch (IOException e) {
				CaptureForm.debugAlert(midlet, "Error while writing file:" + IMGFILE + "/n" + e);
				return;				
			}
			CaptureForm.debugAlert(midlet, "ImageHanderForm: file written");

			try {
				outStream.close();
			} catch (IOException e) {
				CaptureForm.debugAlert(midlet, "Error while closing stream:" + IMGFILE + "/n" + e);
				return;
			}
			CaptureForm.debugAlert(midlet, "file close");

			try {
				fconn.close();
			} catch (IOException e) {
				CaptureForm.debugAlert(midlet, "Error while closing file:" + IMGFILE + "/n" + e);
				return;
			}
			CaptureForm.debugAlert(midlet, "Image data written to " + IMGFILE);
			
			
			
			
		} else if (cmd.equals(backCmd)) {
			captureForm.wake();
		}
		
	}

}
