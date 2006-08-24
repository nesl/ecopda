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

/**
 *  This class is used in order to translate a set of four bars with known lengths
 *  into a digit. This is done in accordance to the EAN13 encoding.
 *  
 *  @author Robert Adelmann
 *  @version 1.0
 */
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

public class MatchMaker {

	//---------------------------------------------------------------------------------------
	// VARIABLES
	//---------------------------------------------------------------------------------------

	static int[][] l_code_odd = { { 3, 2, 1, 1 }, 
			                      { 2, 2, 2, 1 }, 
			                      { 2, 1, 2, 2 }, 
			                      { 1, 4, 1, 1 }, 
			                      { 1, 1, 3, 2 }, 
			                      { 1, 2, 3, 1 }, 
			                      { 1, 1, 1, 4 }, 
			                      { 1, 3, 1, 2 },
			                      { 1, 2, 1, 3 }, 
			                      { 3, 1, 1, 2 } };

	static int[][] l_code_even = { { 1, 1, 2, 3 }, 
			                       { 1, 2, 2, 2 }, 
			                       { 2, 2, 1, 2 }, 
			                       { 1, 1, 4, 1 }, 
			                       { 2, 3, 1, 1 }, 
			                       { 1, 3, 2, 1 }, 
			                       { 4, 1, 1, 1 }, 
			                       { 2, 1, 3, 1 },
			                       { 3, 1, 2, 1 }, 
			                       { 2, 1, 1, 3 } };

	static int[][] r_code = { { 3, 2, 1, 1 }, 
			                  { 2, 2, 2, 1 }, 
			                  { 2, 1, 2, 2 }, 
			                  { 1, 4, 1, 1 }, 
			                  { 1, 1, 3, 2 }, 
			                  { 1, 2, 3, 1 }, 
			                  { 1, 1, 1, 4 }, 
			                  { 1, 3, 1, 2 },
			                  { 1, 2, 1, 3 }, 
			                  { 3, 1, 1, 2 } };
	
	static boolean parity_pattern_list[][] = { 
		{ false, false, false, false, false, false },
        { false, false, true, false, true, true },
        { false, false, true, true, false, true },
        { false, false, true, true, true, false },
        { false, true, false, false, true, true },
        { false, true, true, false, false, true },
        { false, true, true, true, false, false },
        { false, true, false, true, false, true },
        { false, true, false, true, true, false },
        { false, true, true, false, true, false }};
	
	static boolean debug = false;

	//---------------------------------------------------------------------------------------
	// METHODS
	//---------------------------------------------------------------------------------------

	//---------------------------------------------------------------------------------------
	/** Takes information about four black & white fields and information 
	 *  about the min&max lengths of all four bar types in EAN13 codes and uses this 
	 *  information, together with the information if the digit is encoded even or odd, to
	 *  determine and return the digit that is encoded by this series of black&white fields.
	 *  
	 *  @param fields A 2-dim array, containing information about a series of alternating
	 *                black and white fields. The first index specifies the field number,
	 *                while the second one specifies the field color (0=black, 255 = white), 
	 *                and the field length in pixels.<br>
	 *                E.g. <br>fields[5][0] = color of field (0 or 255)
	 *                     <br>fields[5][1] = length of this field in pixels.
	 *                <p>
	 *   @param v An array with four elements, containing the length necessary to classify
	 *          a black or white fields. <br>
	 *          E.g. v = [2, 5, 10, 15] means, that all fields
	 *          with a length x, where x >= 2 and x < 5 will be classified of as a bar
	 *          of one unit width, and so on.
	 *          <p>
	 *   @param left_side Specifies if the given black and white fields are located on the
	 *          right or left part of the code.                  
     */
	//---------------------------------------------------------------------------------------
	public static MatchMakerResult recognizeNumber(int[][] fields, int[] v, boolean left_side) {

		// convert the black&white fields into four digits, representing the bar types.
		// 1 = 1 unit wide bar, 2 = 2 unit wide bar,... 4 = 4 unit wide bar
		int b[] = { getBarSize(fields[0][1], v), getBarSize(fields[1][1], v), getBarSize(fields[2][1], v), getBarSize(fields[3][1], v) };
	
        // we can try to detect and correct obviously wrong estimated bar types:
		if (left_side) {
			//if (b[1] == 4) b[1] = 3;
			//if (b[3] == 4) b[3] = 3;
		} else {
			if (b[0] == 4) b[0] = 3;
			if (b[2] == 4) b[2] = 3;
		}
		
		// since the sum of all bar width is always 7,
		// we can perform some consistency checks
		// and try to "fix" the bar types...
		// (since 4 is quite unlikely, reduce a four to a three)
		int sum = b[0] + b[1] + b[2] + b[3];
		if (sum > 7) {
			for (int i = 0; i < 4; i++) if (b[i] >= 4) b[i] = 3;
		}
		
		// print some debugging information:
		if (debug) {
		   System.out.println("Recognize Number (left_side: " + left_side + "):");
		   System.out.println("lengths: " + fields[0][1] + " " + fields[1][1] + " " + fields[2][1] + " " + fields[3][1]);
		   System.out.println("bartype: " + b[0] + " " + b[1] + " " + b[2] + " " + b[3]);
		}
			
		// try to detect the digit that is encoded by the set of four bar types:
		// (here an extension would be possible, in order to return at least the digit,
		// whose code is "closest" to the determined four bar types if no digit is found
		// whose code resembles the four bar types exactly...)
		if (left_side) {
			// search in the even_group:
			for (int i = 0; i < 10; i++) if ((b[0] == l_code_even[i][0]) && (b[1] == l_code_even[i][1]) && (b[2] == l_code_even[i][2]) && (b[3] == l_code_even[i][3])) return new MatchMakerResult(true,i,1.0f);
			// search in the odd group:
			for (int i = 0; i < 10; i++) if ((b[0] == l_code_odd[i][0]) && (b[1] == l_code_odd[i][1]) && (b[2] == l_code_odd[i][2]) && (b[3] == l_code_odd[i][3])) return new MatchMakerResult(false,i,1.0f);
		} else {
			for (int i = 0; i < 10; i++) if ((b[0] == r_code[i][0]) && (b[1] == r_code[i][1]) && (b[2] == r_code[i][2]) && (b[3] == r_code[i][3])) return new MatchMakerResult(false,i,1.0f);
		}
		
		return new MatchMakerResult(false,-1,1.0f);
	}

    //---------------------------------------------------------------------------------------
	/** Tries to determine the system code, given the parities of the already recognized 
	 *  12 numers.
	 * 
	 *  @param parity_patter Array with twelve fields, vontaining the parities of the 
	 *         already recognized code numbers.
	 */
	//---------------------------------------------------------------------------------------
	public static MatchMakerResult recognizeSystemCode(boolean[] parity_pattern) {
	    
		// search for a fitting parity pattern:
	    boolean fits = false;
		for (int i = 0; i < 10; i++) {
	    	fits = true;
	    	for (int j = 0; j < 6; j++){
	    	   if (parity_pattern_list[i][j] != parity_pattern[j]) fits = false;	
	    	}
	    	if (fits) return new MatchMakerResult(false,i,1.0f);
	    }
		return new MatchMakerResult(false,-1,1.0f);
	}
	
	//---------------------------------------------------------------------------------------
	/** Classifies a given length as beeing one, two, three or four units wide,
	 *  dependent on the classification intervals given in the v array.
	 *  
	 *  @param length The length of the bar that should be classified.
	 *  <p>
	 *  @param v an array with four elements, containing the length necessary to classify
	 *         a black or white fields. <br>
	 *         E.g. v = [2, 5, 10, 15] means, that all fields
	 *         with a length x, where x >= 2 and x < 5 will be classified of as a bar
	 *         of one unit width, and so on.
	 */
	//---------------------------------------------------------------------------------------
	private static int getBarSize(int length, int[] v) {

		int number = 4;
		if ((length > v[0]) && (length <= v[1])) number = 1;
		if ((length > v[1]) && (length <= v[2])) number = 2;
		if ((length > v[2]) && (length <= v[3])) number = 3;
		if ((length > v[3]) && (length <= v[4])) number = 4;

		return number;
	}

}