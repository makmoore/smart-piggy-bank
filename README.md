# Project Title: Smart Piggy Bank

## Brief description of the project idea: 
This project was designed as a smart financial traking system for children. Our goal was to implement basic budgetting functionalities to promote financial literacy to children from a young age. Using GUI and physical components, we created a Smart Piggy Bank to teach children to manage their money responsibly using the 3 jar system. The 3 jar system utilizes three categories - give, save, and spend - to help teach healthy financial habits. There is also the option to set a savings goal to encourage saving money long-term for things the child really wants. This program can be used through use of an intuitive GUI or through the sole use of the buttons on the Piggy Bank itself to enter money.

Team Member Names: Makenzie Moore and Hallie Burgess

## Resources Used
### External Python Libraries:
- tkinter, tkinter.messagebox, tkinter.ttk		(for tkinter GUI)
- os.path						(for file management)
- rpi_lcd						(for LCD display)
- RPi.GPIO						(for GPIO buttons)
- time						(also for GPIO buttons)

### Resources:
- https://www.geeksforgeeks.org/python-tkinter-tutorial/?ref=lbp
  - used for referencing proper use of tkinter widgets
- https://www.fultonbank.com/Education-Center/Saving-and-Budgeting/Teach-your-kids-about-budgeting-with-the-3-jar-money-system
  - used for research about ways of budgetting for kids
- https://www.forbes.com/sites/ericbrotman/2021/09/21/the-three-jar-method-raising-financially-responsible-kids-and-building-savings-habits-early/
  - also used to research the 3 jar system
- https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/
  - for referencing button library & code
- https://github.com/bogdal/rpi-lcd
  - for importing and using the rpi_lcd library for the LCD display



## Instructions
### Version 1: GUI
1. Start the program at `1352SmartBankGUI.py`
2. Select deposit to add money or withdraw to subtract money
3. Put money in the box & click corresponding button on the GUI (changes shown in panel to the left)
4. New balance is shown bellow in green if positive and red if negative & also on LCD display
5. To clear the changes you've made so far, click the "Clear" button on the bottom middle
6. Click the "Budget" button in the bottom left to view budgetting information
7. Once Budget window has openned, view the amount in each category (give, save, spend)
8. Below that is the Saving Goal Progress Bar to show the amount of savings you have that are put toward a goal (default $5)
9. To change this goal, click "Adjust Goal" in the bottom left corner
10. Enter new goal and click "Confirm"
11. When finished, close the Budget Window and click "Save" on the main window to save your changes & close

### Version 2: Physical Piggy Bank
1. Start the program at `independentSmartBank.py`
2. Enter dollar/coin in the correctly labelled slot
3. Press the button by that slot to indicate the coin you entered
4. The new total & most recent addition will be shown on the LCD display
5. Type Ctrl + C to save the program & new total
** To remove any amount, open the GUI program and select withdraw and the amount

 

## Problems Encountered
1. The original plan was to use a camera and OpenCV to automatically detect different types of coins. While doing research we tried several things but discovered that the OpenCV technique was a bit above our current skill level. Instead of OpenCV, we switched to using different buttons corresponding to different coin amounts. While this was less efficient, it allowed us to show more accurately what we actually knew rather than copying a code we didn't understand from the internet with OpenCV.
2. The second major problem we came across was that the buttons weren't able to be run at the same time as the GUI due to them both using continuous loops. We attempted to use threading to solve this issue but unfortunately the threading we tried didn't work and we ran out of time. As a solution, we created two separate files or "modes" that each respectively had the GUI and the physical buttons.
3. A minor problem we had throughout was that the text file used for saving and reading amounts would occasionally not save for some reason. If the number was negative it would save but wouldn't be read at all. However this isn't so much a problem because you wouldn't have a negative amount in a Piggy Bank anyway.
                
 

## Final Comments
Overall this project was incredibly helpful in developing and refining basic python skills through hands-on experience. The project was a lot of fun to work on. If there had been more time there is a lot we could have added to make it even better such as a parental control system, a more robust budgetting system that allows modification of each allotted percentage, and/or different accounts for if there are more than one children (like siblings for example). We are both very happy with how it turned out though and are now much more confident in our computer programming skills.       
                                  
 
 

