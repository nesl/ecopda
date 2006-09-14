package edu.ucla.cens.test;

import javax.microedition.lcdui.*;

public class HelloCanvas extends Canvas {
	boolean myCanvasTXT = true;
	SimpleTest midlet = null;
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
		// TODO Auto-generated method stub
		int w = getWidth();
		int h = getHeight();
		g.setColor(0xffff00);
		g.fillRect(0, 0, w, h);
//		display the message
		if(myCanvasTXT){
			Font font = g.getFont();
			int fontHeight = font.getHeight();
			int fontWidth = font.stringWidth("CANVAS FONT");
			//set the text color
			g.setColor(0x00ff0000);
			g.setFont(font);
			//write the strings in the center of the screen
			g.drawString("CANVAS FONT !!!", (w-fontWidth)/2, (h-fontHeight)/2, Graphics.TOP | Graphics.LEFT);
		}	
	}
}
