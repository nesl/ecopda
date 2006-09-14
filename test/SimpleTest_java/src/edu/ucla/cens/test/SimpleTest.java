package edu.ucla.cens.test;

//import javax.microedition.lcdui.Command;
//import javax.microedition.lcdui.CommandListener;
//import javax.microedition.lcdui.Displayable;
//import javax.microedition.midlet.MIDlet;
//import javax.microedition.midlet.MIDletStateChangeException;


import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.InputStream;
import java.util.Vector;

import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;
import javax.microedition.lcdui.*;
import javax.microedition.midlet.*;
import javax.microedition.media.*;
import javax.microedition.media.control.*;

public class SimpleTest extends MIDlet implements CommandListener {
	byte[] output = null; 
	Vector power = new Vector();
	private HelloCanvas myCanvas;
	private Form myForm;
	private Gauge myGauge;
	private TextField textField;
	private Command backCommand = new Command("Back", Command.BACK, 1);
	private Command messageCommand = new Command("Message", Command.SCREEN,1);
	private Command displayCommand = new Command("Display Message", Command.SCREEN,1);
	private Command exitCommand = new Command("Exit", Command.EXIT, 1);
	private Command showCommand = new Command("Show Levels", Command.SCREEN, 1);
	private Command recordCommand = new Command("Record", Command.SCREEN, 1);
	private Command playCommand = new Command("Play", Command.SCREEN,1);
	public SimpleTest(){
		myCanvas = new HelloCanvas(this);
		myCanvas.addCommand(backCommand);
		myCanvas.addCommand(messageCommand);
		myCanvas.addCommand(playCommand);
		myCanvas.addCommand(recordCommand);
		myForm = new Form("Gauge level");
		myGauge = new Gauge("Value", true, 120, 10);
		textField = new TextField("Enter number", "", 3, TextField.NUMERIC);
		myForm.append(myGauge);
		myForm.append(textField);
		myForm.addCommand(showCommand);
		myForm.addCommand(displayCommand);
		myForm.addCommand(exitCommand);
		myCanvas.setCommandListener(this);
		myForm.setCommandListener(this);
	}
		
	protected void destroyApp(boolean arg0) throws MIDletStateChangeException {
	}

	protected void pauseApp() {
	}

	protected void startApp() throws MIDletStateChangeException {
		Display.getDisplay(this).setCurrent(myCanvas);
		myCanvas.start();
	}

	public void commandAction(Command c, Displayable d) {
		if (c == exitCommand){
			notifyDestroyed();
		}
		if (c == messageCommand){
			myCanvas.newMessage();
		}
		if (c == backCommand){	
			Display.getDisplay(this).setCurrent(myForm);
		}	
		if (c== displayCommand){
			Display.getDisplay(this).setCurrent(myCanvas);
			myCanvas.start();
		}
		if (c==showCommand){
			String valueString = textField.getString();
			int value = 0;
			if (!valueString.equals("")) { 
				value = Integer.parseInt(valueString);
			}
			myGauge.setValue(value);
		}
		if (c==recordCommand) {
			recordCallback2(); 
		}
		if (c==playCommand) {
			playCallback2();
		}
	}
	
	private FileConnection createFC(String arg, boolean write)
	{
		FileConnection fconn = null;
		try {
			fconn = (FileConnection)Connector.open(arg);
		} catch (IOException e) {
			this.alertError("Can't open file (bad URL):" + arg + "/n" + e);
			return null;
		}
		if(write) {
			if(fconn.exists()) {
				if(! fconn.canWrite()) {
					this.alertError("Can't write to existing file:" + arg);
				}
			} else {
				try {
					fconn.create();
				} catch (IOException e) {
					this.alertError("Can't create file:" + arg + "/n" + e);
					return null;				
				}				
			}
		}
		return fconn;
	}
	
	public void recordCallback2()
	{
		try
		{
			Player p = Manager.createPlayer("capture://audio?encoding=pcm");
			p.realize();
			RecordControl rc = (RecordControl)p.getControl("RecordControl");
			ByteArrayOutputStream tempoutput = new ByteArrayOutputStream();
			rc.setRecordStream(tempoutput);
			rc.startRecord();
			p.start();
			Thread.sleep(2000);
			rc.commit();
			p.close();
			this.output = tempoutput.toByteArray();
			tempoutput.close();
			double noiseLevel = this.getNoiseLevel();
			if (this.power.size() > 20)
			{
				this.power.removeAllElements();
			}
			this.power.addElement(new Double(noiseLevel));
			this.alertError("Done recording:"+String.valueOf(noiseLevel));
		} catch (IOException ioe) {
			
		} catch (MediaException me) {
			
		} catch (InterruptedException ie) {
			
		}
		
	}
	
	public void recordCallback()
	{
		try 
		{
			String SNDFILE = "file:///E:/audio.wav";
			FileConnection fconn = null;
			OutputStream outStream = null;
			Player p = null;
			RecordControl rc = null;
			
			// create a datasource that captures live audio
			p = Manager.createPlayer("capture://audio");
			p.realize();
			rc = (RecordControl)p.getControl("RecordControl");
			fconn = this.createFC(SNDFILE, true);
			if (fconn == null)
			{
				this.alertError("fconn was null");
				return;
			}
						
			try {
				outStream = fconn.openDataOutputStream();
			} 
			catch (IOException e) {
				this.alertError("Can't open output stream for:" + SNDFILE + "/n" + e);
				return;				
			}

			rc.setRecordStream(outStream);
			rc.startRecord();
			p.start();
			Thread.sleep(5000);
			p.stop();
			rc.stopRecord();
			rc.commit();


			try {
				outStream.close();
			} catch (IOException e) {
				this.alertError("Error while closing stream:" + SNDFILE + "/n" + e.getMessage());
				return;
			}

			try {
				fconn.close();
			} catch (IOException e) {
				this.alertError("Error while closing file:" + SNDFILE + "/n" + e);
				return;
			}
			this.alertError("Acoustic data written to " + SNDFILE);
		} catch (IOException e) {
			this.alertError("IOException: " + e.getMessage());
		} catch(MediaException e) {
			this.alertError("MediaException: " + e.getMessage());
		} catch(InterruptedException e) {
			this.alertError("InterruptedException: " + e.getMessage());
		}
	}

	public void playCallback2()
	{
		try
		{
			ByteArrayInputStream is = new ByteArrayInputStream(this.output);
			Player p = Manager.createPlayer(is, "audio/x-wav");
			p.start();
		}
		catch (MediaException me) {}
		catch (IOException io) {}
	}
	
	public void playCallback()
	{
		String SNDFILE = "file:///E:/audio.wav";
		FileConnection fconn = null;
		InputStream inStream = null;
		Player p = null;		
		fconn = this.createFC(SNDFILE, false);
		if (fconn == null)
		{
			this.alertError("fconn was null");
			return;
		}		
		try {
			inStream = fconn.openDataInputStream();
		} 
		catch (IOException e) {
			this.alertError("Can't open input stream for:" + SNDFILE + "/n" + e);
			return;				
		}
		try
		{
			// create a datasource that captures live audio
			p = Manager.createPlayer(inStream, "audio/X-wav");
			p.start();
		} catch (IOException e) {
			this.alertError("IOException in createPlayer:" + e.getMessage());
		} catch (MediaException e) {
			this.alertError("MediaException in createPlayer:" + e.getMessage());
		}
	}
	
	public void alertError(String message)
    {
        Alert alert = new Alert("Error", message, null, AlertType.ERROR);
        Display display = Display.getDisplay(this);
        Displayable current = display.getCurrent();
        if (!(current instanceof Alert))
        {
            // This next call can't be done when current is an Alert
            display.setCurrent(alert, current);
        }
    }
	
	public double getNoiseLevel()
	{
		long sum = 0;
		try {
			//FileConnection fc = this.createFC("file:///E:/soundfile.txt", true);
			//OutputStream os = fc.openOutputStream();
			//os.write(output);
			for (int i = 44; i < this.output.length; i += 2)
			{
				//String currentByte = String.valueOf(output[i]) + "\n";
				//os.write(currentByte.getBytes());
				//sum +=  java.lang.Math.abs(this.output[i] - 128);
				short val = SimpleTest.byteArrayToShort(this.output, i);
				//String currentInt = String.valueOf(val) + "\n";
				//os.write(currentInt.getBytes());
				sum += val * val;
			}
			//os.close();
			//fc.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return (1.0 * sum)/this.output.length;
	}
	 /**
     * Convert the byte array to an int starting from the given offset.
     *
     * @param b The byte array
     * @param offset The array offset
     * @return The integer
     */
    public static int byteArrayToInt(byte[] b, int offset) {
        int value = 0;
        for (int i = 0; i < 4; i++) {
            //int shift = (bytewidth - 1 - i) * 8;
        	int shift = i * 8;
            value += (b[i + offset] & 0x000000FF) << shift;
        }
        return value;
    }
    public static short byteArrayToShort(byte[] b, int offset) {
        short value = 0;
        for (int i = 0; i < 2; i++) {
        	int shift = i * 8;
            value += (b[i + offset] & 0x000000FF) << shift;
        }
        return value;
    }
}