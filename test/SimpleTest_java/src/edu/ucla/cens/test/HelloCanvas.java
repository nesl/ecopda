package edu.ucla.cens.test;

import javax.microedition.lcdui.*;

public class HelloCanvas extends Canvas {
	boolean myCanvasTXT = true;
	SimpleTest midlet = null;
	private double ave = 0;
	private double peak = 0;
	HelloCanvas(SimpleTest midlet)
	{
		this.midlet = midlet;
	}
	
	void start(){
		repaint();
	}
	
	public void newMessage(){
		myCanvasTXT = !myCanvasTXT;
		repaint();
	}
	
	protected void paint(Graphics g) {
		int w = getWidth();
		int h = getHeight();
		g.setColor(0xffff00);
		g.fillRect(0, 0, w, h);
		this.pointHistogram(g);
//		display the message
//		if(myCanvasTXT){
		Font font = g.getFont();
		int fontHeight = font.getHeight();
		int fontWidth = font.stringWidth("CANVAS FONT");
//			//set the text color
		g.setColor(0x00ff0000);
		g.setFont(font);
//			//write the strings in the center of the screen
		double ave = 0;
		double peak = 0;
		g.drawString("Ave: " + this.ave + "\nPeak: " + this.peak, (w-fontWidth)/2, (h-fontHeight)/2, Graphics.TOP | Graphics.LEFT);
//		g.drawString("Elements:" + this.midlet.power.size(), (w-fontWidth)/2, (h-fontHeight)/2, Graphics.TOP | Graphics.LEFT);
//		}	
	}
	private void pointHistogram(Graphics g)
	{
		int MYSIZE = 30;
		//g.setColor(0xff000000);
		//g.fillRect(50, 50, 100, 100);
		g.setColor(0x0000ff00);
		int w = getWidth();
		if (midlet.power.size() > 0)
		{
			 Double foo = new Double((1.0*w) / (1.0* MYSIZE));
			 w = foo.intValue();
		}
		int h = getHeight();
		double max = 0;
		double sum = 0;
		for (int i = 0; i < midlet.power.size(); ++i)
		{
			double val = ((Double)midlet.power.elementAt(i)).doubleValue();
			val = java.lang.Math.sqrt(val);
			if (val > max)
			{
				max = val;
			}
			sum += val;
		}
		for (int i = 0; i < midlet.power.size(); ++i)
		{
			double val = ((Double)midlet.power.elementAt(i)).doubleValue();
			val = java.lang.Math.sqrt(val) * ((1.0*h) / max);
			Double dval = new Double(val);
			g.fillRect(i * w,h - dval.intValue(),w, dval.intValue());
		}
		this.ave = sum / midlet.power.size();
		this.peak = max;
		g.setColor(0xfff);
		Double dave = new Double(h - ave * ((1.0*h)/max));
		g.fillRect(0, dave.intValue(), getWidth(), 3);
	}
}
