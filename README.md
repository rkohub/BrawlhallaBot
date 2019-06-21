# BrawlhallaBot
Trying_To_Make_A_Script_Play_The_Game_Brawlhalla

This is just a fun project that I started to work on earlier, but then I decided that I should keep it on github for organizational and protfolio reasons. So if it looks like the project started half done, thats because it is... Well not nearly half, but some ways ion.

My plan
- Process the screen by taking pictues using the screencapture terminal command. That is run using os.system()
- Once I take the picture, use the PIL library to open it.
- Then convert it into a giant array of 3d array of the rows, columns, and the rgb value of each pixel. With Numpy
- Then I again use numpys efficiant array processing methods to process the image
- Once I get all the data I need from the picture, I use the library pyautogui to contorl the character and move it around the screen.
- I also use the python opencv library for testing in order to be able to visualise what the bot is seeing.

Currently the bot will feature no machine learning, but that is a field that I want to investigate so I want to leave the project open for that change.

List of goals

* Have a script identify where a character is within a still image -DONE!
* Have the script track itself in a pre-recorded video -Just Finished! (At the time of putting the project on Github)
* Have the bot consistantly move itself back onto the stage in response to an attack
* Finally have the bot beat one of the games AI's
* Then maybe make it learn how to play better.

I know that there will be errors in the program, as with any program, i will work to fix them as they come up.