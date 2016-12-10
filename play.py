import curses
import time
import random


def refresh_gameboard(placement):
    gameboard = \
"""
 1 | 2 | 3          {0} | {1} | {2} 
---+---+---        ---+---+---
 4 | 5 | 6          {3} | {4} | {5}
---+---+---        ---+---+---
 7 | 8 | 9          {6} | {7} | {8}
"""
    stdscr.refresh()
    stdscr.addstr(0, 0, gameboard.format(*placement))


def set_ai_choices(user,opts,in_use, ai_choice):
    if len(user) == 3:
        ai_choice.append(0)
    elif len(user) == 2:
        for item in opts:
            if item not in user and item not in in_use:
                ai_choice.append(item)
    elif set(opts) < set(in_use) and len(user) == 0:
        ai_choice.append(-1)
    

def do_thinking(in_use_by_user, in_use):

    ai_choice = []
    
    col1 = [1, 4, 7]
    ucol1 = []
    col2 = [2, 5, 8]
    ucol2 = []
    col3 = [3, 6, 9]
    ucol3 = []
    row1 = [1, 2, 3]
    urow1 = []
    row2 = [4, 5, 6]
    urow2 = []
    row3 = [7, 8, 9]
    urow3 = []
    diag1 = [1, 5, 9]
    udiag1 = []
    diag2 = [3, 5, 7]
    udiag2 = []

    for item in in_use_by_user:
        if item == 1:
            ucol1.append(item)
            urow1.append(item)
            udiag1.append(item)
        if item == 2:
            ucol2.append(item)
            urow1.append(item)
        if item == 3:
            ucol3.append(item)
            urow1.append(item)
            udiag2.append(item)
        if item == 4:
            ucol1.append(item)
            urow2.append(item)
        if item == 5:
            ucol2.append(item)
            urow2.append(item)
            udiag1.append(item)
            udiag2.append(item)
        if item == 6:
            ucol3.append(item)
            urow2.append(item)
        if item == 7:
            ucol1.append(item)
            urow3.append(item)
            udiag2.append(item)
        if item == 8:
            ucol2.append(item)
            urow3.append(item)
        if item == 9:
            ucol3.append(item)
            urow3.append(item)
            udiag1.append(item)

    set_ai_choices(ucol1, col1, in_use, ai_choice)
    set_ai_choices(ucol2, col2, in_use, ai_choice)
    set_ai_choices(ucol3, col3, in_use, ai_choice)
    set_ai_choices(urow1, row1, in_use, ai_choice)
    set_ai_choices(urow2, row2, in_use, ai_choice)
    set_ai_choices(urow3, row3, in_use, ai_choice)
    set_ai_choices(udiag1, diag1, in_use, ai_choice)
    set_ai_choices(udiag2, diag2, in_use, ai_choice)

    return ai_choice


if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.cbreak()

    play_again = True
    while play_again:
        available = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        placement = [" "," "," "," "," "," "," "," "," "]
        in_use_by_user = []
        in_use = []
        refresh_gameboard(placement)
        try:
            for i in range(9):
               
                # User's turn
                if i % 2 == 0:
                    turn = "X" 
                    next_move = 0
                    usr_input = ""
                    while next_move not in in_use:
                        stdscr.addstr(7,0, "Choose a position:  ")
                        stdscr.refresh()
                        stdscr.clrtoeol()
                        try:
                            usr_input = stdscr.getstr(7, 19)[0]
                            next_move = int(usr_input)
                            if next_move != 0 and next_move not in in_use:
                                stdscr.clrtoeol()
                                in_use.append(next_move)
                                in_use_by_user.append(next_move)
                                available.remove(next_move)
                            else:
                                stdscr.addstr(8,0, str(next_move) + " is already in use")
                                next_move = 0
                        except:
                            if usr_input.lower().startswith("q"):
                                raise TypeError("Quitting now...")

                # AI's turn
                else:
                    turn = "O"
                    ai_choice = do_thinking(in_use_by_user, in_use)
                    
                    if len(ai_choice) == 0:
                        next_move = random.choice(available)
                        in_use.append(next_move)
                        available.remove(next_move)
                    else:
                        if 0 in ai_choice:
                            stdscr.addstr(0, 0, "           You win!")
                            stdscr.refresh()
                            break
                        next_move = random.choice(ai_choice)
                        in_use.append(next_move)
                        available.remove(next_move)
    
                placement[next_move - 1] = turn
                refresh_gameboard(placement)
                
                ai_choice = do_thinking(in_use_by_user, in_use)
                if -1 in ai_choice:
                    stdscr.addstr(0, 0, "           You lose")
                    break
                    
                
                time.sleep(0.5)
            stdscr.addstr(7, 0, "Would you like to play again? (y/n) ")
            stdscr.refresh()
            stdscr.clrtoeol()
            continue_playing = stdscr.getstr(7, 37)[0]

            if continue_playing != "y":
                play_again = False
        except TypeError as e:
            stdscr.addstr(9, 0, str(e))
            stdscr.refresh()
            time.sleep(1)
        finally:
            curses.nocbreak()
            curses.endwin()
