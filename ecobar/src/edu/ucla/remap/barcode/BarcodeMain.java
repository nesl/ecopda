package edu.ucla.remap.barcode;

import java.io.DataInputStream;
import java.io.IOException;
import java.util.Enumeration;
import java.util.Vector;

import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;

public class BarcodeMain {

	
	public static void main(String[] args) {
		if(args.length == 1) {
			FileConnection fconn = null;
			try {
				fconn = (FileConnection)Connector.open(args[0]);
			} catch (IOException e) {
				System.err.print(e.toString());
				System.out.print("");
				return;
			}
			
			if (! fconn.exists()) {
				System.err.print("File does not exits");
				System.out.print("");
				return;
			}
			
			DataInputStream inStream;
			try {
				inStream = fconn.openDataInputStream();
			} catch (IOException e) {
				System.err.print(e.toString());
				System.out.print("");
				return;
			}
			Vector v = new Vector();
			try {
				while(true) {
					Byte b = new Byte(inStream.readByte());
					v.addElement(b);
				}
			} catch (IOException e) { // just got to end of file
				
			}
			byte[] bmpImage = new byte[v.size()];
			Enumeration e = v.elements();
			int i = 0;
			while(e.hasMoreElements()) {
				bmpImage[i++] = ((Byte)e.nextElement()).byteValue();				
			}
			BarcodeReader br = new BarcodeReader(new ImageData(bmpImage), new Profile());
			String result = br.recognize();
			if(result == null) {
				System.err.print("Unable to read barcode");
				System.out.print("");
			} else {
				System.out.println(result);
			}
			try {
				fconn.close();
			} catch (IOException e1) {
			}
		}
	}

}
