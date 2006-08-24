//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
/** 
 *  Copyright (C) 2006 Robert Adelmann
 *   
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or (at your option) any later version.
 * 
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
 *  MA  02110-1301, USA  
 */
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

package edu.ucla.remap.barcode;

//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
/** 
 * <b>
 *  Significantly modified to run as commandline app EGM 8/16/06
 *  </b>
 *  <p>
 *   
 *   
 *  This class manages the recognition of a barcode, using several scanlines.
 *  It runs the recognition along several scanlines and combines the results of
 *  the different runs.
 *  <p>
 *  Central to the combination of the results of the different scanlines is a three dim. array,
 *  referenced as "possible_numbers", containing information about the occurence of a certain 
 *  digit at a specific position in the EAN13 code.
 *  <p>	         
 *  The first dimension has 13 entries and represents the position in the EAN13 code.
 *  The second dimension has 10 entries and works like a stack for the digits recognized
 *  at that position in the EAN13 code. <br>
 *  The third dimension has two elements: <br> 0 = specifies the digit itself (0..9), 
 *                                        <br> 1 = the amount of this digit's occurence  
 *                                                  at that position in the EAN13 code (0..#scanlines)
 *  <p><p>                                          
 *  Here is an example. Assume, we have 19 scanlines, and along these scanline the following 
 *  information is recognized: (This has been a quite blurry barcode image... :-)
 *  <p>
 *   Scanline 0 result: ????????????<br>
 *   Scanline 1 result: ????????????<br>
 *   Scanline 2 result: ????????????<br>
 *   Scanline 3 result: ????????????<br>
 *   Scanline 4 result: ????????????<br>
 *   Scanline 5 result: ????????????<br>
 *   Scanline 6 result: 3?6???3?????<br>
 *   Scanline 7 result: ????????????<br>
 *   Scanline 8 result: ?????4??????<br>
 *   Scanline 9 result: ????????????<br>
 *   Scanline 10 result: ????????????<br>
 *   Scanline 11 result: 612?97017840<br>
 *   Scanline 12 result: ???7????8???<br>
 *   Scanline 13 result: 6122970178?0<br>
 *   Scanline 14 result: ????????????<br>
 *   Scanline 15 result: ????????????<br>
 *   Scanline 16 result: ????????????<br>
 *   Scanline 17 result: ????????????<br>
 *   Scanline 18 result: ????????????<br>
 *   Scanline 19 result: ????????????<br>
 *   <p><p>
 *   The possible_numbers-array will contain the following information.
 *   (Index of third dim. = 0 => Here we see information about the recognized digits.)
 *   The array has already been sorted using the sortDigits() method. This means
 *   that the digits that have been detected most at a certain position are on top.
 *   <p>
 *   detected digits: possible_numbers[][][0]
 *   <p>
 *   0 :   6  1  2  7  9  7  0  1  7  8  4  0 <br> 
 *   1 :   3  x  6  2  x  4  3  x  8  x  x  x <br>
 *   2 :   x  x  x  x  x  x  x  x  x  x  x  x <br> 
 *   3 :   x  x  x  x  x  x  x  x  x  x  x  x <br> 
 *   4 :   x  x  x  x  x  x  x  x  x  x  x  x <br> 
 *   5 :   x  x  x  x  x  x  x  x  x  x  x  x <br> 
 *   6 :   x  x  x  x  x  x  x  x  x  x  x  x <br> 
 *   7 :   x  x  x  x  x  x  x  x  x  x  x  x <br> 
 *   8 :   x  x  x  x  x  x  x  x  x  x  x  x <br> 
 *   9 :   x  x  x  x  x  x  x  x  x  x  x  x <br> 
 *   <p>
 *   Index of third dim. = 1 => Here we see information about the occurence of the
 *   digits.
 *   <p>
 *   # of their occurence: possible_numbers[][][1]
 *   <p>
 *   0 :   2  2  2  1  2  2  2  2  2  2  1  2 <br>  
 *   1 :   1  0  1  1  0  1  1  0  1  0  0  0 <br> 
 *   2 :   0  0  0  0  0  0  0  0  0  0  0  0 <br> 
 *   3 :   0  0  0  0  0  0  0  0  0  0  0  0 <br> 
 *   4 :   0  0  0  0  0  0  0  0  0  0  0  0 <br> 
 *   5 :   0  0  0  0  0  0  0  0  0  0  0  0 <br> 
 *   6 :   0  0  0  0  0  0  0  0  0  0  0  0 <br> 
 *   7 :   0  0  0  0  0  0  0  0  0  0  0  0 <br> 
 *   8 :   0  0  0  0  0  0  0  0  0  0  0  0 <br> 
 *   9 :   0  0  0  0  0  0  0  0  0  0  0  0 <br> 
 *   <p> 
 *   Below is a run of the detectValidBarcode() method that tries to detect a valid
 *   barcode. If no code can be recognized directly, we are trying all possible
 *   combinations of the recognized digits starting with the "most likely" combination.
 *   This is intended as a last try. The need to try different combinations of the recognized digits
 *   should occur very seldom, or at least with only very few alternatives for 
 *   specific digits. As a prositive effect, we get the chance to recognize a barcode that
 *   couldn't be recognized before, as a negative consequence, we can get a EAN13 number
 *   that is correct, according to the checksum, but that doesn't match the 
 *   barcode on the image.
 *   <p>
 *   Trying to find a valid code: (detectValidBarcode()-method)
 *   <p>
 *   CHECK: 6 1 2 7 9 7 0 1 7 8 4 0  ckecksum_digit:5 <br>
 *   CHECK: 6 1 2 7 9 7 0 1 8 8 4 0  ckecksum_digit:2 <br>
 *   CHECK: 6 1 2 7 9 7 3 1 7 8 4 0  ckecksum_digit:6 <br>
 *   CHECK: 6 1 2 7 9 7 3 1 8 8 4 0  ckecksum_digit:3 <br>
 *   CHECK: 6 1 2 7 9 4 0 1 7 8 4 0  ckecksum_digit:8 <br>
 *   CHECK: 6 1 2 7 9 4 0 1 8 8 4 0  ckecksum_digit:5 <br>
 *   CHECK: 6 1 2 7 9 4 3 1 7 8 4 0  ckecksum_digit:9 <br>
 *   CHECK: 6 1 2 7 9 4 3 1 8 8 4 0  ckecksum_digit:6 <br>
 *   CHECK: 6 1 2 2 9 7 0 1 7 8 4 0  ckecksum_digit:0 <br>
 *   <p>
 *   RESULT: 612297017840                                                                         
 *   <p>            
 *   
 *  @author Robert Adelmann
 *  @version 1.0
 */
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
public class ScanlineControl {

	//---------------------------------------------------------------------------------------
	// VARIABLES
	//---------------------------------------------------------------------------------------
	private static boolean debug = false; // if set to true, additional debuggin information
                                          // is printed using System.out.println()

	//---------------------------------------------------------------------------------------
	// METHODS
	//---------------------------------------------------------------------------------------

	//---------------------------------------------------------------------------------------
	/** Is called from the a device object, if a recognition run should be performed.
	 *  
	 *  @param device Provides access to device specific functionality.
	 *  @param profile Contains all relevant recognition parameters. 
	 *  
	 *  @return The recognized Barcode. (All digits that could not be recognized
	 *          have a value of -1)
	 */
	//---------------------------------------------------------------------------------------
	public static Barcode recognize(ImageData imageData, Profile profile) {

		// PARAMETERS:
		int w = profile.getImage_width();
		int h = profile.getImage_height();
		int amount_scanlines = profile.getAmount_scanlines();

		// the array which will contain the result:
		int numbers[][] = new int[amount_scanlines][13];

		// temporary variables:
		int raw_path[][][];
		int x1, x2, y1, y2;

		Barcode_EAN13 temp_code;

		// generate and initialize the array that will contain all detected 
		// digits at a specific code position: 
		int possible_numbers[][][] = new int[10][13][2];
		for (int i = 0; i < 10; i++) {
			for (int j = 0; j < 13; j++) {
				possible_numbers[i][j][0] = -1;
				possible_numbers[i][j][1] = 0;
			}
		}

		// try to detect the barcode along scanlines:
		for (int i = 0; i < amount_scanlines; i++) {
			
			// set the position of the scanline:
			x1 = 0;
			y1 = (h / amount_scanlines) * i;
			x2 = w - 1;
			y2 = y1;

			//y1 = y2 = 240;

			// ensure that the scanline lies in the image:
			if (x1 < 0) x1 = 0;
			if (x1 > w - 1) x1 = w - 1;
			if (x2 < 0) x2 = 0;
			if (x2 > w - 1) x2 = w - 1;
			if (y1 < 0) y1 = 0;
			if (y1 > h - 1) y1 = w - 1;
			if (y2 < 0) y2 = 0;
			if (y2 > h - 1) y2 = w - 1;

			// get the RGB values along the line:
			raw_path = imageData.getPath(x1, y1, x2, y2, profile.getImage_width());

			// try to recognize a barcode along that path:
			temp_code = Scanline.recognize(raw_path, imageData, x1, y1, x2, y2, profile);

			if (temp_code != null) {
				numbers[i] = temp_code.getNumbers();

				// add the recognized digits to the array of possible numbers:
				addNumberToPossibleNumbers(numbers[i], possible_numbers);

				// show the information that has been recognized along the scanline:
				if (debug) System.out.println("Scanline " + i + " result: " + temp_code);
			}
		}

		// sort the detected digits at each code position, in accordance to the 
		// amount of their detection:
		sortDigits(possible_numbers);

		// print out the array that contains the possible digits at each code position, anf
		// the amount of their occurence/detection:
		if (debug) {
			System.out.println();
			System.out.println("detected digits:");
			printArray(possible_numbers, 0);
			System.out.println("# of their occurence:");
			printArray(possible_numbers, 1);

		}

		// try to find a valid code (one whose checksum is correct), from all possible
		// codes:
		if (debug) System.out.println("");
		if (debug) System.out.println("trying to find a valid code:");
		Barcode code = detectValidBarcode(possible_numbers, profile);
		if (debug) System.out.println("");

		// print out the result
		if (debug) System.out.println("RESULT: " + code);

		return code;

	}

	//---------------------------------------------------------------------------------------
	/** Adds the given code digits to the array of possible digits,
	 *  if they are not already contained in it.
	 *  
	 *  @param number An array with 13 entries, containing the digits of a code, or
	 *                -1 for non recognized digits.
	 *  @param possible_numbers Three dim. array, containing information about 
	 *         the occurence of a certain digit at a certain position (1..13) and
	 *         the amount of its occurence.<p>
	 *         
     *         The first dimension has 13 entries and represents the position in the EAN13 code.
     *         The second dimension has 10 entries and works like a stack for the digits recognized
     *         at that position in the EAN13 code.<br>
     *         The third dimension has two elements: <br> 0 = specifies the digit itself (0..9), 
     *                                               <br> 1 = the amount of this digit's occurence  
     *                                            at that position in the EAN13 code (0..#scanlines)
	 *                                                                                                      
	 *  @see #printArray(int[][][], int)
	 *  @see #sortDigits(int[][][])                                                        
     */
	//---------------------------------------------------------------------------------------
	public static void addNumberToPossibleNumbers(int[] number, int[][][] possible_numbers) {

		int i;
		boolean digit_contained;
		for (int j = 0; j < 13; j++) {
			if (number[j] >= 0) {
				i = 0;
				digit_contained = false;
				while ((i < 10) && (possible_numbers[i][j][0] >= 0)) {
					if (possible_numbers[i][j][0] == number[j]) {
						digit_contained = true;
						possible_numbers[i][j][1]++;
						break;
					}
					i++;
				}
				if ((i < 10) && (!digit_contained)) {
					// add new digit:
					possible_numbers[i][j][0] = number[j];
					possible_numbers[i][j][1]++;
				}
			}
		}

	}

	//---------------------------------------------------------------------------------------
	/** Sorts the values contained in the specified  possible number array, dependent
	 *  on the amount of the digit's occurence. (So far simple bubble sort is used.)
	 *  The digits that occure most often will appear on top.
	 *  
	 *  @param possible_numbers Three dim. array, containing information about 
	 *         the occurence of a certain digit at a certain position (1..13) and
	 *         the amount of its occurence.              
	 */
	//---------------------------------------------------------------------------------------
	public static void sortDigits(int[][][] possible_numbers) {
		int i;
		int temp_value;
		int temp_occurence;
		boolean changes;

		for (int j = 0; j < 13; j++) {

			i = 1;
			changes = false;
			while (true) {

				if ((possible_numbers[i - 1][j][0] >= 0) && (possible_numbers[i][j][0] >= 0)) {
					if (possible_numbers[i - 1][j][1] < possible_numbers[i][j][1]) {
						temp_value = possible_numbers[i - 1][j][0];
						temp_occurence = possible_numbers[i - 1][j][1];
						possible_numbers[i - 1][j][0] = possible_numbers[i][j][0];
						possible_numbers[i - 1][j][1] = possible_numbers[i][j][1];
						possible_numbers[i][j][0] = temp_value;
						possible_numbers[i][j][1] = temp_occurence;

						changes = true;
					}
				}

				if ((possible_numbers[i][j][0] < 0) || (i >= 9)) {
					if (!changes) {
						break;
					} else {
						i = 1;
						changes = false;
					}
				} else {
					i++;
				}

			}
		}
	}

	//---------------------------------------------------------------------------------------
	/** Prints out the content of the given array. 
	 *  
	 *  @param array The three dim. array that should be printed. 
	 *         (e.g. the array containing information about the occurrence of digits.)
	 *  @param level index of the third dimension that sould be printed.
	 *  
	 *  @see #addNumberToPossibleNumbers(int[], int[][][])
	 *  @see #sortDigits(int[][][])
	 */
	//---------------------------------------------------------------------------------------
	public static void printArray(int[][][] array, int level) {

		for (int i = 0; i < array.length; i++) {
			System.out.print(i + " :   ");
			for (int j = 0; j < array[0].length; j++) {
				if (array[i][j][level] == -1) System.out.print("x  ");
				else System.out.print(array[i][j][level] + "  ");
			}
			System.out.println("");
		}
	}

	//---------------------------------------------------------------------------------------
	/** Trys to detect a valid barcode from the data collected by the different scanlines. 
	 *  
	 *  (Has been implemented so far non recursively with counters, 
	 *  in order to save the overhead time of the recursive calls. 
	 *  Would probably be clearer if it is implented recursively.)
	 *  
	 *  @param array The three dim. array that should be printed. 
	 *         (e.g. the array containing information about the occurrence of digits.) 
	 *  @param profile A Profile object specifying the parameters to use. (In this case,
	 *         the max. number of combinations to try, if different digits have been
	 *         recognized at certain barcode positions.) 
	 */
	//---------------------------------------------------------------------------------------
	public static Barcode detectValidBarcode(int[][][] possible_numbers, Profile profile) {

		Barcode_EAN13 code = null;

		// create and initialize the temporary variables:
		int[] temp_code = new int[13];
		for (int i = 0; i < 13; i++)
			temp_code[i] = possible_numbers[0][i][0];

		int alternative_amount = 0;

		int[] counter = new int[13];
		int counter_nr = 11;

		// check if there is at least one complete code present:
		for (int i = 0; i < 13; i++) {
			// exit and return the "most likely" code parts:
			if (temp_code[i] < 0) return new Barcode_EAN13(temp_code);
		}

		// if there is at least one complete node, try to detect a valid barcode:
		while (alternative_amount < profile.getMax_amount_of_considered_possible_codes()) {

			// fill the temporary code array with one possible version:
			for (int i = 0; i < 13; i++)
				temp_code[i] = possible_numbers[counter[i]][i][0];

			alternative_amount++;

			// check if this version represents a valid code:
			if (isValid(temp_code)) {
				code = new Barcode_EAN13(temp_code);
				return code;
			}

			// increment the counters:
			if ((counter[counter_nr] < 9) && (possible_numbers[counter[counter_nr] + 1][counter_nr][0] >= 0)) {
				// increment the actual counter.
				counter[counter_nr]++;
			} else {

				// check if we have reached the end and no valid barcode has been found:
				if (counter_nr == 1) {
					// exit and return the "most likely" code parts:
					for (int i = 0; i < 13; i++)
						temp_code[i] = possible_numbers[0][i][0];
					return new Barcode_EAN13(temp_code);
				} else {

					// reset the actual counter and increment the next one(s):
					counter[counter_nr] = 0;

					while (true) {
						if (counter_nr > 2) {
							counter_nr--;
						} else {
							for (int i = 0; i < 13; i++)
								temp_code[i] = possible_numbers[0][i][0];
							return new Barcode_EAN13(temp_code);
						}
						if (counter[counter_nr] < 9) {
							counter[counter_nr]++;
							if (possible_numbers[counter[counter_nr]][counter_nr][0] < 0) {
								counter[counter_nr] = 0;
							} else {
								break;
							}
						} else {
							counter[counter_nr] = 0;
						}
					}
					counter_nr = 12;
				}

			}
		}

		for (int i = 0; i < 13; i++)
			temp_code[i] = possible_numbers[0][i][0];
		return new Barcode_EAN13(temp_code);

	}

	//---------------------------------------------------------------------------------------
	/** Return true if the given numbers represent a valid barcode. The barcode
	 *  is valid, if the checksum is correct.
	 *  
     *  @param Array containing 13 digits that represent the recognizd digits of
	 *         the EAN13 code. If a digit was not recognized, a value of -1 is set
	 *         for that one.
	 */
	//---------------------------------------------------------------------------------------
	public static boolean isValid(int[] numbers) {

		// calculate the checksum of the barcode:
		int sum1 = numbers[0] + numbers[2] + numbers[4] + numbers[6] + numbers[8] + numbers[10];
		int sum2 = 3 * (numbers[1] + numbers[3] + numbers[5] + numbers[7] + numbers[9] + numbers[11]);
		int checksum_value = sum1 + sum2;
		int checksum_digit = 10 - (checksum_value % 10);
		if (checksum_digit == 10) checksum_digit = 0;

		if (debug) {
			System.out.print("CHECK:");
			for (int i = 0; i < 13; i++)
				System.out.print(" " + numbers[i]);
			System.out.println("  ckecksum_digit:" + checksum_digit);
		}

		return (numbers[12] == checksum_digit);
	}

}
