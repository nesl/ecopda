package edu.ucla.remap.nokias60.util;

import java.io.IOException;
import java.util.Enumeration;

import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;
import javax.microedition.io.file.FileSystemRegistry;
import javax.microedition.lcdui.Alert;
import javax.microedition.lcdui.AlertType;
import javax.microedition.lcdui.ChoiceGroup;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Item;
import javax.microedition.lcdui.ItemStateListener;
import javax.microedition.midlet.MIDlet;

public class FileBrowser extends Form implements CommandListener, ItemStateListener {
	int type;
	String filename;
	String filter;
	MIDlet midlet;
	ChoiceGroup dirChoiceGroup;

	
	private final Command cancelCmd;
	private final Command loadSaveCmd;
	private final Command selectCmd;
	private final Command backCmd;
	
	//Vector directory = new Vector();

	public static final class FileBrowserType  {
		public static final int SAVE = 0;
		public static final int LOAD = 1;
	}
	
	
	public FileBrowser(String name, int type, MIDlet midlet,  String filename) {
		super(name);
		
		this.midlet = midlet;
		type = this.type;
		

		backCmd = new Command("Up", Command.BACK, 1);
		cancelCmd = new Command("Cancel", Command.CANCEL, 2);

		selectCmd = new Command("Select", Command.ITEM, 1);

		if(type == FileBrowserType.LOAD) {
			loadSaveCmd = new Command("Load", Command.ITEM, 2);
		} else {
			loadSaveCmd = new Command("Save", Command.ITEM, 2);
		}

		dirChoiceGroup = new ChoiceGroup(filename,ChoiceGroup.EXCLUSIVE);

		addCommand(backCmd);
		addCommand(cancelCmd);
		addCommand(selectCmd);
		addCommand(loadSaveCmd);

		
		
		if(filename == null) {
			this.filename = null;
			displayRoots();
		} else {
			this.filename = filename;
			displayFiles();
		}
		
		append(dirChoiceGroup);

		Display.getDisplay(midlet).setCurrent(this);
		setCommandListener(this);
		setItemStateListener(this);

	}
	
	public void alert(String msg) {
		Alert a = new Alert(msg);
		a.setType(AlertType.ERROR);
		a.setTimeout(Alert.FOREVER);
		a.addCommand(Alert.DISMISS_COMMAND);
		Display.getDisplay(midlet).setCurrent(a);
	}
	public void displayFiles() {
		
			try {
				FileConnection fconn = (FileConnection)Connector.open(filename);
				 setDirChoiceGroup(fconn);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	}
	
	private void setDirChoiceGroup(FileConnection fconn) {
		try {
			if(fconn.exists()) {
				if(fconn.isDirectory()) {
					dirChoiceGroup.setLabel(filename);

					Enumeration e = fconn.list();
					while(e.hasMoreElements()) {
						dirChoiceGroup.append((String) e.nextElement(), null);
					}
					fconn.close();
				} else {
					fconn.setFileConnection("..");
					filename = fconn.getPath();
					setDirChoiceGroup(fconn);
				}
			} 
		} catch (IOException e) {

		}
	}

	public void  displayRoots() {
		Enumeration e = FileSystemRegistry.listRoots();
		dirChoiceGroup.setLabel("Roots");

		while(e.hasMoreElements()) {
			dirChoiceGroup.append((String) e.nextElement(), null);
		}
		
	}
	public void commandAction(Command arg0, Displayable arg1) {
//		midlet.notifyDestroyed();
		
	}


	public void itemStateChanged(Item item) {
		if(dirChoiceGroup.equals(item)) {
			String nextSelection = dirChoiceGroup.getString(dirChoiceGroup.getSelectedIndex());
			dirChoiceGroup.deleteAll();
			if(filename == null) {
				filename =nextSelection;
			} else {
				filename += "/" + nextSelection;
			}
			displayFiles();
		}
		
	}



}
