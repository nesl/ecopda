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
 *  Objects of this class are used in order to represent the parameters used for a 
 *  recognition run.
 *  
 *  @author Robert Adelmann
 *  @version 1.0
 */
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
public class Profile {

	//---------------------------------------------------------------------------------------
	// VARIABLES
	//---------------------------------------------------------------------------------------
	
	private String image_encoding = "encoding=bmp&width=640&height=480";
	private int image_width = 640;              
	private int image_height = 480;            

	// scanline management:
	private int amount_scanlines = 30;                // standard 20

	// combination of the scanline results:
	private int max_amount_of_considered_possible_codes = 1000;

	// scanline transformation to black&white:
	private double use_area_illumination = 0.5;       // standard 0.5
	private int black_white_border = -5;              // standard -5

	// code recognition:
	private int max_start_sentry_bar_differences = 3; // standard 3
	private int max_unit_length = 6;                  // standard 6
	private int min_unit_length = 1;                  // standard 1

	//---------------------------------------------------------------------------------------
	// GET/SET METHODS
	//---------------------------------------------------------------------------------------

	public String getImage_encoding() {
		return image_encoding;
	}

	public void setImage_encoding(String image_encoding) {
		this.image_encoding = image_encoding;
	}

	public int getAmount_scanlines() {
		return amount_scanlines;
	}

	public void setAmount_scanlines(int amount_scanlines) {
		this.amount_scanlines = amount_scanlines;
	}

	public int getBlack_white_border() {
		return black_white_border;
	}

	public void setBlack_white_border(int black_white_border) {
		this.black_white_border = black_white_border;
	}

	public int getImage_height() {
		return image_height;
	}

	public void setImage_height(int image_height) {
		this.image_height = image_height;
	}

	public int getImage_width() {
		return image_width;
	}

	public void setImage_width(int image_width) {
		this.image_width = image_width;
	}

	public int getMax_start_sentry_bar_differences() {
		return max_start_sentry_bar_differences;
	}

	public void setMax_start_sentry_bar_differences(int max_start_sentry_bar_differences) {
		this.max_start_sentry_bar_differences = max_start_sentry_bar_differences;
	}

	public int getMax_unit_length() {
		return max_unit_length;
	}

	public void setMax_unit_length(int max_unit_length) {
		this.max_unit_length = max_unit_length;
	}

	public int getMin_unit_length() {
		return min_unit_length;
	}

	public void setMin_unit_length(int min_unit_length) {
		this.min_unit_length = min_unit_length;
	}

	public double getUse_area_illumination() {
		return use_area_illumination;
	}

	public void setUse_area_illumination(double use_area_illumination) {
		this.use_area_illumination = use_area_illumination;
	}

	public int getMax_amount_of_considered_possible_codes() {
		return max_amount_of_considered_possible_codes;
	}

	public void setMax_amount_of_considered_possible_codes(int max_amount_of_considered_possible_codes) {
		this.max_amount_of_considered_possible_codes = max_amount_of_considered_possible_codes;
	}

}