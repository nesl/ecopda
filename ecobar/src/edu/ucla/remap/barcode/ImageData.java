package edu.ucla.remap.barcode;

public class ImageData {
	public byte pixel_data[];
	
	public ImageData(byte pixel_data[]) {
		this.pixel_data = pixel_data;
	}
//	---------------------------------------------------------------------------------------
	/** Extracts color values from the class's 
     *  pixel data array along a specified path.
     *
	 *  @param x1 x-Pos of path starting point
	 *  @param y1 y-Pos of path starting point
	 *  @param x2 x-Pos of path end point
	 *  @param y2 y-Pos of path end point
	 *  @param w  path width
	 *  
	 *  @return A two three dim. array, containing the RGB values along the specified path.
	 *  (Three dim., because the path can in general be wider than one pixel.But currently
	 *  the path width is set to 1.) <p>
	 *  Index 1 has a size that correlates to the length of the path and 
	 *  specifies the position along the path.<br>
	 *  Index 2 has a size that correlates with the width of the path. (usually size 1)<br> 
	 *  Index 3 has size three and specifies the color as RGB values. <br>
	 */
	//---------------------------------------------------------------------------------------
	public int[][][] getPath(int x1, int y1, int x2, int y2, int w) {
		if (pixel_data == null) return null;
		return getPathFromBMPData(pixel_data, w, x1, y1, x2, y2);
	}

	//---------------------------------------------------------------------------------------
	/** Extracts color values from the image along a specified path.
	 * 
	 *  @param bmp_data array, containing the image data in the bmp format
	 *  @param x1 x-Pos of path starting point
	 *  @param y1 y-Pos of path starting point
	 *  @param x2 x-Pos of path end point
	 *  @param y2 y-Pos of path end point
	 *  @param width  image width
	 *  
	 *  @return A two three dim. array, containing the RGB values along the specified path. 
	 *  <br>
	 *  (Three dim., because the path can in general be wider than one pixel. But currently
	 *  the path width is set to 1.) 
	 */
	//---------------------------------------------------------------------------------------
	private int[][][] getPathFromBMPData(byte[] bmp_data, int width, int x1, int y1, int x2, int y2) {

		// all distances are measured in "pixels"
		float dx = Math.abs(x2 - x1);
		float dy = Math.abs(y2 - y1);

		int distance = new Float(Math.sqrt(dx * dx + dy * dy)).intValue();
		int[][][] path = new int[distance][1][3];

		float factor, px, py;
		int px_i, py_i;
		int pos;

		// collect the color information:
		for (int i = 0; i < distance; i++) {
			factor = ((float) i / distance);
			px = x1 + dx * factor;
			py = y1 + dy * factor;
			px_i = new Float(px).intValue();
			py_i = new Float(py).intValue();

			pos = 54 + (py_i * width + px_i) * 3;
			path[i][0][2] = getIntValue(bmp_data[pos]);
			path[i][0][1] = getIntValue(bmp_data[pos + 1]);
			path[i][0][0] = getIntValue(bmp_data[pos + 2]);

			//System.out.println(pos+" -> "+path[i][0][0]+" "+path[i][0][1]+" "+path[i][0][2]);
		}
		return path;
	}

	private static int getIntValue(byte byte_value) {
		if (byte_value >= 0) {
			int value = byte_value;
			return value;
		} else {
			int value = 255 + byte_value;
			return value;
		}
	}
}
