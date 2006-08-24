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
 *  This interface represents a Barcode.
 *  
 *  @author Robert Adelmann
 *  @version 1.0
 */
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
public interface Barcode {

	//---------------------------------------------------------------------------------------
	/** Converts the given EAN13 to a String.
	 *  
	 *  @return this Code as a String
	 */
	//---------------------------------------------------------------------------------------
	public String toString();
	
	//---------------------------------------------------------------------------------------
	/** Checks if the contained barcode is a valid EAN13 barcode.
	 * 
	 *  @return true, if the code is a valid EAN13 code
	 */
	//---------------------------------------------------------------------------------------
	public boolean isValid();

}
