/*
* ==============================================================================
*  Name        : helloworldbasicappui.cpp
*  Part of     : Helloworldbasic
*  Interface   : 
*  Description : 
*  Version     : 
*
*  Copyright (c) 2005-2006 Nokia Corporation.
*  This material, including documentation and any related 
*  computer programs, is protected by copyright controlled by 
*  Nokia Corporation.
* ==============================================================================
*/

// INCLUDE FILES
#include <avkon.hrh>
#include <aknnotewrappers.h>
#include <stringloader.h>
#include <HelloWorldBasic.rsg>
#include <f32file.h>
#include <s32file.h>

#include "HelloWorldBasic.pan"
#include "HelloWorldBasicAppUi.h"
#include "HelloWorldBasicAppView.h"
#include "HelloWorldBasic.hrh"

_LIT( KHelloFileName, "\\private\\A000017F\\Hello.txt" );
_LIT( KHelloText, "HELLO WORLD!");

// ============================ MEMBER FUNCTIONS ===============================


// -----------------------------------------------------------------------------
// CHelloWorldBasicAppUi::ConstructL()
// Symbian 2nd phase constructor can leave.
// -----------------------------------------------------------------------------
//
void CHelloWorldBasicAppUi::ConstructL()
    {
    // Initialise app UI with standard value.
    BaseConstructL(CAknAppUi::EAknEnableSkin);
// Here the Hello.txt file can be created, if it is not copied automatically.
/*
 	RFs fsSession;
	User::LeaveIfError(fsSession.Connect());            

    RFile file;
        
    // Create a file to write the text to       
   	if ( file.Replace(fsSession, KHelloFileName, EFileWrite ) != KErrNone )
    	{
   		return;
    	}
	CleanupClosePushL( file );            
	
 	RFileWriteStream outputFileStream( file );
   	CleanupClosePushL( outputFileStream );
	outputFileStream << KHelloText;

    CleanupStack::PopAndDestroy(2); // file, outputFileStream

	fsSession.Close();
*/

    // Create view object
    iAppView = CHelloWorldBasicAppView::NewL( ClientRect() );

    
    }
// -----------------------------------------------------------------------------
// CHelloWorldBasicAppUi::CHelloWorldBasicAppUi()
// C++ default constructor can NOT contain any code, that might leave.
// -----------------------------------------------------------------------------
//
CHelloWorldBasicAppUi::CHelloWorldBasicAppUi()
    {
    // No implementation required
    }

// -----------------------------------------------------------------------------
// CHelloWorldBasicAppUi::~CHelloWorldBasicAppUi()
// Destructor.
// -----------------------------------------------------------------------------
//
CHelloWorldBasicAppUi::~CHelloWorldBasicAppUi()
    {
    if ( iAppView )
        {
        delete iAppView;
        iAppView = NULL;
        }

    }

// -----------------------------------------------------------------------------
// CHelloWorldBasicAppUi::HandleCommandL()
// Takes care of command handling.
// -----------------------------------------------------------------------------
//
void CHelloWorldBasicAppUi::HandleCommandL( TInt aCommand )
    {
    switch( aCommand )
        {
        case EEikCmdExit:
        case EAknSoftkeyExit:
            Exit();
            break;

        case EHelloWorldBasicCommand1:
            {
            
            // Load a string from the resource file and display it
            HBufC* textResource = StringLoader::LoadLC( R_HEWB_COMMAND1_TEXT );
            CAknInformationNote* informationNote;

            informationNote = new ( ELeave ) CAknInformationNote;

            // Show the information Note with
            // textResource loaded with StringLoader.
            informationNote->ExecuteLD( *textResource);

            // Pop HBuf from CleanUpStack and Destroy it.
            CleanupStack::PopAndDestroy( textResource );
            }
            break;
		case EHelloWorldBasicCommand2:
			{
			
			RFs fsSession;
			RFile rFile;
			
			// Connects a client process to the fileserver
			User::LeaveIfError(fsSession.Connect());
			CleanupClosePushL(fsSession);
			
			//Open file where the stream text is
			User::LeaveIfError(rFile.Open(fsSession,KHelloFileName, EFileStreamText));//EFileShareReadersOnly));// EFileStreamText));
			CleanupClosePushL(rFile);
			
			// copy stream from file to RFileStream object
			RFileReadStream inputFileStream(rFile);
    		CleanupClosePushL(inputFileStream);
    		
    		// HBufC descriptor is created from the RFileStream object.
    		HBufC* fileData = HBufC::NewLC(inputFileStream, 32);

            CAknInformationNote* informationNote;

            informationNote = new ( ELeave ) CAknInformationNote;
            // Show the information Note
            informationNote->ExecuteLD( *fileData);			
			
			// Pop loaded resources from the cleanup stack
			CleanupStack::PopAndDestroy(4); // filedata, inputFileStream, rFile, fsSession
			fsSession.Close();
			}
			break;
        default:
            Panic( EHelloWorldBasicUi );
            break;
        }
    }
// -----------------------------------------------------------------------------
//  Called by the framework when the application status pane
//  size is changed.  Passes the new client rectangle to the
//  AppView
// -----------------------------------------------------------------------------
//
void CHelloWorldBasicAppUi::HandleStatusPaneSizeChange()
{
	iAppView->SetRect( ClientRect() );
	
} 

// End of File

