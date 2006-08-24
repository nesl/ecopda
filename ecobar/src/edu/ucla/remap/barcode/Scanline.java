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
 *  This class encapsulates the recognition of a barcode along one scanline.  
 *  
 *  @author Robert Adelmann
 *  @version 1.0
 */
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
public class Scanline {

	//---------------------------------------------------------------------------------------
	// VARIABLES
	//---------------------------------------------------------------------------------------
	static boolean debug = false; // if set to true, additional debuggin information is 
	                              // printed using System.out.println()

	//---------------------------------------------------------------------------------------
	// METHODS
	//---------------------------------------------------------------------------------------

	//---------------------------------------------------------------------------------------
	/** Method is called from the ScanlineControl class, if a recognition run should be 
	 *  performed along a path.
	 *  
	 *  @param raw_path Contains the RGB values of pixels along that path.
	 *  @param device Provides access to device specific functionality, e.g. to display some information.
	 *  @param profile Contains the recognition parameters that should be used.
	 *  <p>
	 *  @param x1 x-value of the scanline start point
	 *  @param y1 y-value of the scanline start point
	 *  @param x2 x-value of the scanline end point
	 *  @param y2 y-value of the scanline end point
	 *  <p>
	 *  @return The recognized barcode. Digits that have not been recognized correctly
	 *          are marked using -1.
	 */
	//---------------------------------------------------------------------------------------
	public static Barcode_EAN13 recognize(int[][][] raw_path, ImageData imgageData, int x1, int y1, int x2, int y2, Profile profile) {

		//int numbers[] = {1,2,3,4,5,6,7,8,9,2,3,4,5};	
		//return new Barcode_EAN13(numbers);

		// convert the given path into a string of black and white pixels:
		int string[] = transformPathToBW(raw_path, profile);

		// convert the string of black&white pixels into a list, containing
		// information about the black and white fields
		// first indes = field nr.
		// second index: 0 = color of the field
		//               1 = field length
		int fields[][] = extractFieldInformation(string);

		// try to extract the encoded information from the field series:
		int numbers[] = decode(fields, 0, fields.length, profile);

		// Draw a red scanline on the screen:
//		NokiaS60Device n_device = ((NokiaS60Device) device);
//		Graphics g = n_device.getScreenGraphics();
//		int s_w = g.getClipWidth();
//		int s_h = g.getClipHeight();
//		int i_w = profile.getImage_width();
//		int i_h = profile.getImage_height();
//		float fw = (s_w / (float) i_w);
//		float fh = (s_h / (float) i_h);
//		g.setColor(255, 0, 0);
//		g.drawLine((int) (x1 * fw), (int) (y1 * fh), (int) (x2 * fw), (int) (y2 * fh));
//		n_device.updateScreen();

		// return the results:
		return new Barcode_EAN13(numbers);

	}

	//---------------------------------------------------------------------------------------
	/** Takes information about a series of alternating black&white fields and tries to detect 
	 *  an EAN13 barcode in between the fields with index start_i and end_i, using
	 *  the recognition parameters specified in the provided Profile object.
	 *  
	 *  It trys to detect a EAN13 barcode in the field data.
	 *  If a EAN 13 barcode is found, it is returned. If not,
	 *  at least the digits of it that could be recognized will be returned. All other
	 *  digits will contain a -1 value. 
	 *  
	 *  @param fields Array containing a series of alternating black&white fields.
	 *  @param start_i Index of field at which the search for an EAN13 code should be 
	 *         started. (usually 0)
	 *  @param end_i Index of field at which the search for an EAN13 code should be 
	 *         stopped. (usually fields.length-1)
	 *  @param profile Contains the recognition parameters that should be used.
	 *  
	 *  @returns Array containing 13 digits that represent the recognizd digits of
	 *           the EAN13 code. If a digit was not recognized, a value of -1 is set
	 *           for that one.  
	 */
	//---------------------------------------------------------------------------------------
	private static int[] decode(int[][] fields, int start_i, int end_i, Profile profile) {

		// start sentinel detection parameters:
		int max_start_sentry_bar_differences = profile.getMax_start_sentry_bar_differences();
		int max_unit_length = profile.getMax_unit_length();
		int min_unit_length = profile.getMin_unit_length();

		// consistency checks:
		if (fields.length <= 0) return null;
		if (start_i > end_i - 3) return null;
		if (end_i - start_i < 30) return null; // (just a rough value)

		// relevant indexes: 
		int start_sentinel_i;
		int end_sentinel_i;
		int left_numbers_i;
		int middle_guard_i;
		int right_numbers_i;

		// relevant parameters:
		float unit_length;
		int[] comparison_lengths = new int[5];

		// results:
		int[] numbers = new int[13];

		// determine the relevant positions:

		// Try to detect the start sentinel (a small black-white-black serie):
		start_sentinel_i = -1;
		for (int i = start_i; i < end_i - 56; i++) {

			if ((fields[i][0] == 0) && (fields[i + 1][0] == 255) && (fields[i + 2][0] == 0)) {
				if ((fields[i][1] >= min_unit_length) && (fields[i][1] <= max_unit_length)) {
					if ((Math.abs(fields[i][1] - fields[i + 1][1]) <= max_start_sentry_bar_differences)
							&& (Math.abs(fields[i][1] - fields[i + 2][1]) <= max_start_sentry_bar_differences)) {
						start_sentinel_i = i;
						break;
					}
				}
			}

		}

		if (debug) System.out.println("start_sentinal_index: " + start_sentinel_i);
		if (start_sentinel_i < 0) return null;

		// calculate the other positions:
		left_numbers_i = start_sentinel_i + 3;
		middle_guard_i = left_numbers_i + 6 * 4;
		right_numbers_i = middle_guard_i + 5;
		end_sentinel_i = right_numbers_i + 6 * 4;

		if (debug) System.out.println("end_sentinel " + end_sentinel_i + " end_i " + end_i);
		if (end_sentinel_i + 3 > end_i) return null;

		// calculate the average (pixel) length of a bar that is one unit wide:
		// (a complete  barcode consists out of 95 length units)
		int temp_length = 0;
		int field_amount = (end_sentinel_i - start_sentinel_i + 3);
		for (int i = start_sentinel_i; i < start_sentinel_i + field_amount; i++)
			temp_length = temp_length + fields[i][1];
		unit_length = (float) ((float) temp_length / (float) 95);

		// calculate the lenght_units used for the classification of bars, in dependence of their width:
		for (int i = 0; i < 4; i++)
			comparison_lengths[i + 1] = round(((3 + (i * 2)) * unit_length) / 2);
		comparison_lengths[0] = -1;

		// print out some debugging information:
		if (debug) {
			System.out.println("unit_width: " + unit_length);
			System.out.println("unit_lenghts: " + comparison_lengths[0] + " " + comparison_lengths[1] + " " + comparison_lengths[2] + " "
					+ comparison_lengths[3] + " " + comparison_lengths[4]);
		}
		int[][] current_number_field = new int[4][2];

		if (left_numbers_i + 1 > end_i) return null;

		//check if we start from the left side, or the right side:
		//(this information is not used so far, but can be used to be able to detect 
		// barcodes that are upside-down in the image)
		//boolean is_left_side;
		//if (fields[left_numbers_i + 1][0] == 255) is_left_side = true; else is_left_side = false;

		MatchMakerResult matchMakerResult;

		boolean[] parity_pattern = new boolean[6]; // true = even, false = odd

		// try to recognize the left numbers:
		int counter = 1;
		for (int i = left_numbers_i; i < left_numbers_i + 24; i = i + 4) {
			for (int j = 0; j < 4; j++) {
				current_number_field[j][0] = fields[i + j][0];
				current_number_field[j][1] = fields[i + j][1];
			}
			matchMakerResult = MatchMaker.recognizeNumber(current_number_field, comparison_lengths, true);
			numbers[counter] = matchMakerResult.getDigit();
			parity_pattern[counter - 1] = matchMakerResult.isEven();
			if (debug) System.out.println("left_number " + (counter - 1) + " : " + numbers[counter]);
			counter++;
		}

		// try to determine the system code:
		matchMakerResult = MatchMaker.recognizeSystemCode(parity_pattern);
		numbers[0] = matchMakerResult.getDigit();

		// try to recognize the right numbers:
		counter = 0;
		for (int i = right_numbers_i; i < right_numbers_i + 24; i = i + 4) {
			for (int j = 0; j < 4; j++) {
				current_number_field[j][0] = fields[i + j][0];
				current_number_field[j][1] = fields[i + j][1];
			}
			matchMakerResult = MatchMaker.recognizeNumber(current_number_field, comparison_lengths, false);
			numbers[counter + 7] = matchMakerResult.getDigit();
			if (debug) System.out.println("right_number " + counter + " : " + numbers[counter + 7]);
			counter++;
		}

		return numbers;

	}

	//---------------------------------------------------------------------------------------
	/** Converts the given path into one containing only black&white pixels.
	 * 
	 * @param path Three dim. array containig the RGB color information along a path.      
	 *        (Three dim., because the path can in general be wider than one pixel) 
	 *         Index 1 has a size that correlates to the length of the path and 
	 *         specifies the position along the path.
	 *         Index 2 has a size that correlates with the width of the path. (usually size 1) 
	 *         Index 3 has size three and specifies the color as RGB values. 
	 * @param profile A Profile object specifying the recognition parameters to use.          
	 *             
	 * @return A one-dim. array containing a series of black and white pixels.
	 *         (0 represents a black pixel, 255 a white one)
	 *         Its size is equal to the size of the first field of the specified
	 *         color value array and equals the apth length.                     
	 */
	//---------------------------------------------------------------------------------------
	public static int[] transformPathToBW(int[][][] path, Profile profile) {

		// PARAMETERS:
		double use_area_illumination = profile.getUse_area_illumination();
		int black_white_border = profile.getBlack_white_border();

		int w = path.length;
		int h = path[0].length;
		int gray[][][] = convertToGray(path);

		// reduce the information to one string, if the specified path was broader then one pixel.
		int string[] = new int[w];
		for (int x = 0; x < w; x++) {
			string[x] = 0;
			for (int y = 0; y < h; y++) {
				string[x] = string[x] + gray[x][y][0];
			}
			string[x] = string[x] / h;
		}

		// determine the average illumination in the whole sting:
		int avera_image_illumination = 0;
		for (int x = 0; x < w; x++) {
			avera_image_illumination = avera_image_illumination + string[x];
		}
		avera_image_illumination = avera_image_illumination / w;

		// calculate the average area illumination around each pixel:
		int area_ill[] = new int[w];
		int ill_value;
		int temp_value;
		for (int x = 0; x < w; x++) {
			ill_value = 0;
			for (int i = x - 40; i < x + 40; i = i + 4) {
				if ((i >= 0) && (i < w)) temp_value = string[i];
				else if (i < 0) temp_value = string[0];
				else temp_value = string[w - 1];

				ill_value = ill_value + temp_value;
			}
			ill_value = ill_value / 20;

			if ((x <= 1)) {
				area_ill[x] = ill_value;
			} else {
				area_ill[x] = (area_ill[x - 2] + area_ill[x - 1] + ill_value) / 3;
			}
		}

		// adjust the average illumination values: (soften them in order to avoid extremes):
		// This is done by shifting them towards the global string average value,
		// dependent on the fact if the value is darker or lighter than the average:
		for (int x = 0; x < w; x++) {
			area_ill[x] = new Float(area_ill[x] - (area_ill[x] - avera_image_illumination) * (1.0 - use_area_illumination)).intValue();
		}

		// calculate the bw values:
		int diff;
		for (int x = 0; x < w; x++) {
			diff = string[x] - area_ill[x];

			if (diff < black_white_border) string[x] = 0;
			else string[x] = 255;

			//string[x] = 128 + diff * 10;

			if (string[x] < 0) string[x] = 0;
			if (string[x] > 255) string[x] = 255;

		}

		// filter the values: (remove too small fields)
		for (int x = 1; x < w - 1; x++) {
			if ((string[x] != string[x - 1]) && (string[x] != string[x + 1])) string[x] = string[x - 1];
		}

		return string;

	}

	//---------------------------------------------------------------------------------------
	/** Transforms information about the black and white pixels in the given array
	 *  into a two.dim array, containing information about black and white fields.  
	 *  
	 *  @param bwpixels A one-dim. array containing a series of black and white pixels.
	 *         (0 represents a black pixel, 255 a white one)
	 *         Its size is equal to the size of the first field of the specified
	 *         color value array and equals the apth length. 
	 *         
	 *  @return Two.dim array, containing information about black and white fields
	 *          (First indes = field nr. 
	 *          Second index: 0 = color of the field, 1 = field length in pixels.)
	 *  
	 *  @see Scanline#transformPathToBW(int[][][], Profile)
	 */
	//---------------------------------------------------------------------------------------
	public static int[][] extractFieldInformation(int[] bwpixels) {

		int[][] temp_fields = new int[bwpixels.length][2];

		if (bwpixels.length == 0) return new int[0][1];

		int field_counter = 0;
		int last_value = bwpixels[0];
		int last_fields = 1;
		for (int i = 1; i < bwpixels.length; i++) {
			if ((bwpixels[i] == last_value) && (i < bwpixels.length - 1)) {
				last_fields++;
			} else {

				// create new field entry:
				temp_fields[field_counter][0] = last_value;
				temp_fields[field_counter][1] = last_fields;

				last_value = bwpixels[i];
				last_fields = 0;
				field_counter++;
			}
		}

		int[][] fields = new int[field_counter][2];
		for (int i = 0; i < field_counter; i++) {
			fields[i][0] = temp_fields[i][0];
			fields[i][1] = temp_fields[i][1];
		}
		return fields;
	}

	
    //---------------------------------------------------------------------------------------
	/** Converts the given image data (3d pixel array) to gray values.
	 * 
	 *  @param pixels Three dim. array, containing the image data as RGB values.
	 *  
	 *  @return Three dim. array, containing the image data as RGB values, but now
	 *          the image is gray. (The values for red, green, blue of a pixel
	 *          all equal the arithmetic mean of the given RGB values of that pixel.)
	 *  
	 *  @see Device#getPath(int, int, int, int, int)
	 */
	//---------------------------------------------------------------------------------------
	public static int[][][] convertToGray(int[][][] pixels) {
		int w = pixels.length;
		int h = pixels[0].length;
		int gray[][][] = new int[w][h][1];

		for (int x = 0; x < w; x++) {
			for (int y = 0; y < h; y++) {
				gray[x][y][0] = (pixels[x][y][0] + pixels[x][y][1] + pixels[x][y][2]) / 3;
			}
		}
		return gray;
	}
	
	//---------------------------------------------------------------------------------------
	/** Rounds the given float value. 
	 * 
	 *  @param f Float value to be rounded
	 *  
	 *  @return Rounde value as Int.
	 */
	//---------------------------------------------------------------------------------------
	private static int round(double f) {
		int i = (int) f;
		f = f - i;
		if (f >= 0.5) i = i + 1;
		return i;
	}

}