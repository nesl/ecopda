//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
/** 
 *  This class represents an EAN13 barcode.
 * 
 *  @author Robert Adelmann
 *  @version 1.0
 */
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

package edu.ucla.remap.barcode;

//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
/** 
 *  This class represents an EAN13 barcode.
 * 
 *  @author Robert Adelmann
 *  @version 1.0
 */
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
public class Barcode_EAN13 implements Barcode {

	//---------------------------------------------------------------------------------------
	// VARIABLES
	//---------------------------------------------------------------------------------------
	private int numbers[] = new int[13];

	//---------------------------------------------------------------------------------------
	// CONSTRUCTOR
	//---------------------------------------------------------------------------------------
	public Barcode_EAN13(int numbers[]) {
		for (int i = 0; i < 13; i++) this.numbers[i] = -1;
		if (numbers == null) return;
		if (numbers.length != 13) return;
		for (int i = 0; i < 13; i++) this.numbers[i] = numbers[i];
	}

	public Barcode_EAN13(String code) {
		for (int i = 0; i < 13; i++) this.numbers[i] = -1;
		if (code.length() != 13) return;
		char[] code_chars = code.toCharArray();
		for (int i = 0; i < 13; i++) this.numbers[i] = Integer.valueOf("" + code_chars[i]).intValue();
	}

	//---------------------------------------------------------------------------------------
	// METHODS
	//---------------------------------------------------------------------------------------

	//---------------------------------------------------------------------------------------
	/** Converts this Barcode_EAN13 object to a String. 
	 * 
	 *  @return this Code as a String.
	 */
	//---------------------------------------------------------------------------------------
	public String toString() {
		String s = "";
		for (int i = 0; i < numbers.length; i++) {
			if (numbers[i] >= 0) s = s + String.valueOf(numbers[i]); else s = s + "?";
		}
		return s;
	}

	//---------------------------------------------------------------------------------------
	/** Checks if the contained barcode is a valid EAN13 barcode.
	 *  (So far, the checksum is not tested.)
	 *  
	 *  @return true, if the code is a valid EAN13 code.
	 */
	//---------------------------------------------------------------------------------------
	public boolean isValid() {
		for (int i = 0; i < numbers.length; i++) {
			if ((numbers[i] < 0) || (numbers[i] > 9)) return false;
		}
		return true;
	}

	//---------------------------------------------------------------------------------------
	// GET/SET METHODS
	//---------------------------------------------------------------------------------------
	public int[] getNumbers() {
		return numbers;
	}

	public int getSystemCode() {
		return numbers[0];
	}

	public int getNumber(int index) {
		if ((index < 0) || (index > 12)) return -1;
		return numbers[index];
	}

}