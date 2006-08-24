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
 *  An object of this class is used to represent the result of a run performed by MatchMaker.
 *  
 *  @author Robert Adelmann
 *  @version 1.0
 */
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
public class MatchMakerResult {

	//---------------------------------------------------------------------------------------
	// VARIABLES
	//---------------------------------------------------------------------------------------
	boolean even; // specifies if the recognized digit has an even or odd encoding
	int digit;    // the recognized digit
	float confidence; // an optional confidence value, specifying the confidence of the result
	                  // (so far alway 1.0)

    //---------------------------------------------------------------------------------------
	// CONSTRUCTOR
	//---------------------------------------------------------------------------------------
	public MatchMakerResult(boolean even, int digit, float confidence) {
        this.even = even;
		this.digit = digit;
		this.confidence = confidence;
	}

    //---------------------------------------------------------------------------------------
	// METHODS
	//---------------------------------------------------------------------------------------
    
	//---------------------------------------------------------------------------------------
	/** Returns the confidence value that specifying the confidence of the result.
	 *  (So far always 1.0 is returned.)
	 *  
	 *  @return The confidence of the result. 8A Value between 0.0 = min. confidence 
	 *          and 1.0 = maxs confidence.)
	 */
	//---------------------------------------------------------------------------------------
	public float getConfidence() {
		return confidence;
	}

	public void setConfidence(float confidence) {
		this.confidence = confidence;
	}
	
	//---------------------------------------------------------------------------------------
	/** Returns the recognized digit.
	 *  
	 *  @return The recognized digit. (And -1 if no digit has been recognized)
	 */
	//---------------------------------------------------------------------------------------
	public int getDigit() {
		return digit;
	}

	public void setDigit(int digit) {
		this.digit = digit;
	}
	
	//---------------------------------------------------------------------------------------
	/** Returns the encoding of the recognized digit.
	 *  
	 *  @return Encoding of the recognized digit.
	 */
	//---------------------------------------------------------------------------------------
	public boolean isEven() {
		return even;
	}

	public void setEven(boolean even) {
		this.even = even;
	}
	
	
}