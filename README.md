# scriptlessPy
This is Alpha V3.0 which is built on Java +selenium +Python
Please follow below steps to leverage the framework or contribute.

Step 1:	 After installing python, execute below commands.

		pip install --user -U nltk
		pip install --user -U openpyxl
		pip install --user -U xlrd
		pip install --user -U pandas
Step 4: Below are the functions available in framework

		Method Name									Purpose										Parameter

		alertAccept						:		To accept a single alert					  	Element								
		alertDismiss					:		To reject a single alert					  	Element		
		clear							:		to clear the content of an input webelement		Element
		click							:		To click on any element							Element
		clickAftermouseHover			:		To click on any element after mouseHover		Element, Text Value of click element
		jsClick							:       To Click on any element via jsClick				Element				
		doubleClick						:		To double click on any webelement				Element		
		jsDragAndDrop					:		To Drag and drop of element via JS				Element
		DragAndDrop						:		Drag and drop of one element  					Element, source position, target position
		dropDownByMouseHover			:		Mouse hover on any dropdown						Element
		enterText						:		Entering text on any input element				Element, text to be entered		
		isDisplayed						:		To check if the element is displayed or not		Element
		isEnabled						:		To check if the element is enabled or not		Element		
		moveToNextPage					:		Navigate to next page							Driver
		moveToPreviousPage				:		Navigate to back page							Driver
		jsMouseHover					:		Mouse Hover via JS								Driver, Element
		navigateToURL					:		Navigate to a given URL							Driver, URL
		readText						:		To get the text associated with the element		Element		
		readTitleOfPage					:		To get the title of the page					Driver					
		scrollElementIntoView			:		Scroll to a particular element					Element			
		selectDate						:		Select a Date value								Element
		selectDateFromCalendar			:		Select a Calendar value							Element
		selectDropDown					:		Select a dropdown by its Index value			Element, Index/Text/Value		
		selectFromListDropDown			:		Select one Value from a list					Element, Value to be selected		
		singleMouseHover				:		Mouse hover on element							Element		
		submit							:		Submit the action								Element
		switchOutOfFrame				:		Switch back to parent frame						Driver, Frameid
		switchToChildWindow				:		Switch to child window							Driver
		switchToFrame					:		Switch to Frame 								Driver, FrameID
		switchToParentWindow			:		Switch back to parent Window 					Driver
		verifyAfterClick				:		Verify Text After clicking 						Element, Text value
		verifyalertText					:		Verify alert Text value							Element
		verifyAllCheckBoxNotSelected	:		Verify if all check boxes NOT selected			Element
		verifyAllCheckBoxSelected		:		Verify  all check boxes  Selected				Element
		verifyCheckBoxSelected			:		Verify if the check box selected				Element
		verifyPageUrl					:		To verify the current URL						Driver			
		verifyText						:		Verify the Text value							Element
		verifyTextFieldData				:		Verify the text field Data 						Element
		verifyTitleOfPage				:		Verify Page title								Element
		verifyTableData	                :       Verify if given text is present in webtable     Element, Text value
		wait							:		Wait for milisec								Time in mili sec
		waitForElement					:		Wait for an element to be visible				Element
		readWebTable					:		Read data of an webtable						Element
-------------------------------------------------------------------------------------------------------------------------------------------------------
Step 5: Open the excel sheet "TestCase.xlsx" present in src/test/resources

Step 6: in the above Excel open TestCaseSheet. This sheet contains step wise information about the manual test cases.

	TestCaseName	: Can be any name. Recommended is TC00<n> 
	Page	        : The URL where the test will be performed
	StepNo		    : Test Step No 	
	Test Step Name	: Test Step Description, Step needs to perform
	ActionType	    : No Need to fill anything. AI/ML will take care of it.
	Element Locator : Type of Element locator on which that step will be performed(XPATH/ID/CSS)	
	onFail	        : What is output you expect if the test case failed
	data	        : if performing any search operation then the data calue need to be mentioned here
	
	
	Fill the TestCaseName and page details in the above sheet. 

Step 7: Open "Regression Suite" sheet add the above newly added test case name to it with value as "YES" and save the excel file

Step 8: Open command prompt and navigate to the project location and type "mvn test -Ptestcreator". This will map the correct Action Type for each test steps and generate the xpath for the given website and put in captured objects sheet. You can also use any other xpath finder browser extensions for the same.
Note: This will work only for the URL given under "Page" column in "TestCaseSheet".

Step 9: Now open the CapturedObjectProperties sheet. You will find below informations in that sheet.

	URL             : Website under test
	Property        : Identifier proerties for that particular element e.g (ID/ XPATH/ CSS/NAME)	
	Value			: The value of that identifier (ID Value/XPATH Value)
	Combined Locator: Combined locator is the value of (property : value) in one cell.

Step 10: Now you can copy the combined locator  from "CapturedObject" sheet and paste them under "Element Locator" column respectively in 		"TestCaseSheet". Once its done for all the test steps save and close the excel file.