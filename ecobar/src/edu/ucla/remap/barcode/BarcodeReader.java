package edu.ucla.remap.barcode;

public class BarcodeReader {
	ImageData imageData;
	Profile profile;
	
	public BarcodeReader(ImageData imageData, Profile profile) {
		this.imageData = imageData;
		this.profile = profile;
	}
	public String recognize() {
		Barcode bc = ScanlineControl.recognize(imageData, profile);
		if(bc == null) {  // not sure if this is needed but lets be safe
			return null;
		}
		
		if(bc.isValid()) {
			return bc.toString();
		} else {
			return null;
		}
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
