# Binary-Puzzle-Solver
This is a python based solver for Binary Puzzles that can solve all below size 8x8.
It interfaces with the website 0hh1.com to play online.
It uses computer vision to dectect the starting grid and the mouse to play the game.
If running this understand the pixel locations of the square may be different and should be updated.

#### How to Use:
- GetMouseLocation.py can be used to find the pixel locations of the rows and columns on the website.  These need to be changed in Game.py file 6x6 and 8x8 for a 1080 screen have been included.  
- Show Hint icon must be set to **No** on 0hh1
- Run Play.py after setting the number of games to play making sure program can get focus onto website

#### Possible Future Improvements:
- Expand to solve larger than 8x8
- Improve mouse location calibration
  - Make computer edit a save file, instead of human editting code
- Make it easier for human to cancel program early
- Improve general user experience
  - Remove need for coding editting
