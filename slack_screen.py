import curses
import os
import threading

class SlackTerminal(object):
    """
        Class for representing the  split screen needed to correctly display a real-time stream
        of messages and the input dialogue.

        This is done using curses to separate the terminal into a streaming window and an input window
    """
    _INPUT_ROW = None
    _INPUT_COL = None
    _MAX_MESSAGES = None
    _MESSAGE_CHAR_LIMIT = None

    def __init__(self):
        #Necessary curses setup
        self.stdscr = curses.initscr()
        self.height, self.width = self.stdscr.getmaxyx()
        curses.echo()
        curses.cbreak()
        #setup split-screens
        self.stream_win = curses.newwin(self.height-1, self.width, 0, 0)
        self.input_win = curses.newwin(1, self.width, self.height-1, 0)
        self._MESSAGE_CHAR_LIMIT = self.width
        self._MAX_MESSAGES = self.stream_win.getmaxyx()[0]
        self._INPUT_ROW = self.height-1
        self._INPUT_COL = self.width
        #Setup message list
        self._messages = []

    def _update_screen(self):
        """Redraws ALL messages to screen.  Should only be called AFTER a emssage has been added"""
        if len(self._messages) < self._MAX_MESSAGES:
            self.stream_win.addstr(len(self._messages)-1, 0, self._messages[-1])
        else:
            #display the most recent messages that will fit on screen
            for row, message in enumerate(self._messages[-self._MAX_MESSAGES:]):
                self.clear_row(row)
                self.stream_win.addstr(row, 0, message)
        self.stream_win.refresh()

    def add_message(self, user, message):
        self._messages.append('%s : %s' % (user, message))
        self._update_screen()

    def clear_row(self, row_num):
        self.stream_win.move(row_num, 0)
        self.stream_win.clrtoeol()

    def simulate_raw_input(self):
        curses.echo()
        while True:
            self.input_win.addstr('>>> ')
            self.input_win.refresh()
            input = self.input_win.getstr(0, 4, self._MESSAGE_CHAR_LIMIT)
            if input == 'quit' or input == 'q':
                break
            self.add_message('alex', input)
            self.input_win.clear()
        curses.nocbreak()
        self.stream_win.clear()
        self.input_win.refresh()
        self.stream_win.refresh()
        self.stdscr.keypad(0)
        curses.endwin()

SlackTerminal().simulate_raw_input()
os.system('reset')
