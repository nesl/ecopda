package edu.ucla.remap.camera;

import java.io.IOException;
import java.io.InputStream;

import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;
import javax.microedition.lcdui.Alert;
import javax.microedition.lcdui.AlertType;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Item;
import javax.microedition.media.Manager;
import javax.microedition.media.MediaException;
import javax.microedition.media.Player;
import javax.microedition.media.control.VideoControl;
import javax.microedition.midlet.MIDlet;

import edu.ucla.remap.barcode.ImageData;
import edu.ucla.remap.barcode.Profile;


public class CaptureForm extends Form implements CommandListener {
	private final Command exitCommand;
	private final Command captureCommand;
	private final Command loadImgCmd;
	private MIDlet midlet;
	private Player player = null;
	private VideoControl videoController;
	private Profile profile = new Profile();
	
	protected CaptureForm(MIDlet midlet) {
		super("Barcode Capture");
		
		this.midlet = midlet;
		
		captureCommand = new Command("Capture1", Command.OK, 2);
		loadImgCmd = new Command("Load Image1", Command.BACK, 2);
		exitCommand = new Command("Exit1", Command.EXIT, 1);
		

		addCommand(captureCommand);
		addCommand(loadImgCmd);
		addCommand(exitCommand);

		setCommandListener(this);
		
		if(player == null) {
			try {
				player = Manager.createPlayer("capture://video");
				player.realize();
			} catch (IOException e) {
				append("IOException creating player" + e.toString() + "\n");
				return;
			} catch (MediaException e) {
				append("MediaException creating player" + e.toString() + "\n");
				return;
			}
		} 
		
		if(videoController == null) {		
			videoController = (VideoControl)player.getControl("VideoControl");
			if(videoController == null) {
				this.append("Unable to get VideoControl\n");
				return;
			}
			append((Item) videoController.initDisplayMode(VideoControl.USE_GUI_PRIMITIVE, null));
			wake();
		}
		
		
	}
	
	public void pause() 
	{
		if(player != null) {
			try {
				player.stop();
			} catch (MediaException e) {
				append("Unable to stop/pause player\n" + e);
			}
		}
		if(videoController != null) {
			videoController.setVisible(false);
		}
	}
	public void wake() {
		if(player != null) {
			try {
				player.start();
			} catch (MediaException e) {
				append("MediaException starting player" + e.toString() + "\n");
				return;
			}
		}
		if(videoController != null) {
			videoController.setVisible(true);
		}
		Display.getDisplay(midlet).setCurrent(this);

	}
	
	public void quit() {
		//if(player != null) {
		//	player.deallocate();
		//}
	}
	
	public static byte[] loadImage(MIDlet midlet) {
		FileConnection fconn = null;
		try {
			fconn = (FileConnection)Connector.open(ImageHandlerForm.IMGFILE);
		} catch (IOException e) {
			CaptureForm.debugAlert(midlet, "Can't open file (bad URL):" + ImageHandlerForm.IMGFILE + "/n" + e);
			return null;
		}
		if(! fconn.exists()) {
				CaptureForm.debugAlert(midlet, "File nonexistant:" + ImageHandlerForm.IMGFILE );
				return null;
		}
		if(! fconn.canRead()) {
			CaptureForm.debugAlert(midlet, "can't read file:" + ImageHandlerForm.IMGFILE );
			return null;			
		}
		

		InputStream instream = null;
		try {
			instream = fconn.openDataInputStream();
		} catch (IOException e) {
			CaptureForm.debugAlert(midlet, "Can't open input stream for:" + ImageHandlerForm.IMGFILE + "/n" + e);
			return null;				
		}
		
		byte[] pixelData = null;
		try {
			pixelData = new byte[(int) fconn.fileSize()];
		} catch (IOException e1) {
			CaptureForm.debugAlert(midlet, "unable to filesize");			
			return null;
		}
		
		if(pixelData == null) {
			CaptureForm.debugAlert(midlet, "unable to allocate memory to read image file");			
			return null;
		}
		
		try {
			instream.read(pixelData);
		} catch (IOException e) {
			CaptureForm.debugAlert(midlet, "Error while reading file:" + ImageHandlerForm.IMGFILE + "/n" + e);
			return null;				
		}
		CaptureForm.debugAlert(midlet, "CaptureForm: file read.");

		try {
			instream.close();
		} catch (IOException e) {
			CaptureForm.debugAlert(midlet, "Error while closing stream:" + ImageHandlerForm.IMGFILE  + "/n" + e);
			return pixelData;
		}
		CaptureForm.debugAlert(midlet, "file close");

		try {
			fconn.close();
		} catch (IOException e) {
			CaptureForm.debugAlert(midlet, "Error while closing file:" + ImageHandlerForm.IMGFILE  + "/n" + e);
			return pixelData;
		}
		
		CaptureForm.debugAlert(midlet, "Image data read from" + ImageHandlerForm.IMGFILE );
		return pixelData;
		
		
	}

	public void recognizeImage(ImageData img) {
		pause();
		new ImageHandlerForm(midlet, img, profile, this);
	}
	public static void debugAlert(MIDlet midlet, String msg) {
		Alert a = new Alert(msg);
		a.setType(AlertType.INFO);
		a.setTimeout(Alert.FOREVER);
		a.addCommand(Alert.DISMISS_COMMAND);
		Display.getDisplay(midlet).setCurrent(a);		
	}
	
	
	
	public void commandAction(Command cmd, Displayable arg1) {
		//System.out.println("Command received" + c);

		if (cmd.equals(exitCommand)) {
			midlet.notifyDestroyed();
		} else if (cmd.equals(loadImgCmd)) {
			byte[] pix = loadImage(midlet);
			if(pix != null) {
				recognizeImage(new ImageData(pix));				
			}
		} else {
			try {
				byte[] bmpImage = videoController.getSnapshot(profile.getImage_encoding());
				recognizeImage(new ImageData(bmpImage));
			} catch (MediaException e) {
				Alert a = new Alert(e.toString());
				a.setType(AlertType.ERROR);
				a.setTimeout(Alert.FOREVER);
				a.addCommand(Alert.DISMISS_COMMAND);
				Display.getDisplay(midlet).setCurrent(a);
				
			}
		}
	}

/*
	public void loadFile(String s) {
		Display.getDisplay(midlet).setCurrent(this);
		debugAlert(midlet,"save:\n" + s);
		
	}

	public void saveFile(String s) {
		Display.getDisplay(midlet).setCurrent(this);
		debugAlert(midlet, "save:\n" + s);
		
	}
	*/

}
