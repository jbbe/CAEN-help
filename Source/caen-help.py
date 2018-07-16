### CAEN Help Application ###
# Python3 and PyGObject
# http://lazka.github.io/pgi-docs/index.html
# Linux Version written by Dakota Lambert
# Linux v0.5

import gi
import sys
import os
import webbrowser
import socket
import uuid
import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from subprocess import call
from pathlib import Path


class CaenHelp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        # Configure the initial window
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("CAEN Help")
        window.set_position(1)
        window.set_resizable(0)
        window.set_border_width(10)

        # Get Username of currently logged in user
        username = os.getlogin()
        # Gtk.Grid
        # attach(child, left, top, width, height)

        # This application is configured as three grids. One two column grid with each of its two columns containing another grid. 

        # Create and define the main Gtk.Grid
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        # Sets vertical and horizontal alignment on the grid within each allocated space. Needed on all grid otherwise some weird spacing issues can occur.
        grid.set_halign(1)
        grid.set_valign(1)

        # Define the left grid that will hold the CAEN logo
        grid_left = Gtk.Grid()
        grid_left.set_column_spacing(5)
        grid_left.set_row_spacing(5)
        grid_left.set_halign(1)
        grid_left.set_valign(1)

        # Define the right grid that will hold the buttons
        grid_right = Gtk.Grid()
        grid_right.set_column_spacing(5)
        grid_right.set_row_spacing(5)
        grid_right.set_halign(1)
        grid_right.set_valign(1)

        # Attach the two grids to the initial one
        grid.attach(grid_left, 0, 0, 1, 1)
        grid.attach(grid_right, 1, 0, 1, 1)

        ### Left Grid Contents ###

        # Establish a frame around the caen logo
        logo_frame = Gtk.Frame()
        logo_frame.set_shadow_type(0)
        caen_logo = Gtk.Image.new_from_file('/home/drlamb/git/caen-help/Source/caen.png')
        logo_frame.add(caen_logo)
        grid_left.attach(logo_frame, 0, 0, 1, 1)


        ### Right Grid Contents ###

        # Info field
        sys_info_frame = Gtk.Frame()
        sys_info_frame.set_shadow_type(3)
        sys_info_frame.set_label("System Information")
        sys_info_frame.set_label_align(.5,1.0)
        sys_info_frame.set_border_width(0)
        sys_info = Gtk.Label(self.get_sys_info())
        sys_info.set_justify(0)
        sys_info_frame.add(sys_info)
        grid_right.attach(sys_info_frame, 0, 0, 1, 2)

        # Report Problem Button
        report_button = Gtk.Button.new_with_label("Report a Problem")
        report_button.connect("clicked", self.report_problem, username)
        grid_right.attach(report_button, 0, 2, 1, 1)

        # FAQ Button
        faq_button = Gtk.Button.new_with_label("Visit the FAQ")
        faq_button.connect("clicked", self.visit_faq)
        grid_right.attach(faq_button, 0, 3, 1, 1)

        # Determine if the Chat button should be shown 
        # Currently set for summer hours
        now = datetime.datetime.now()
        if now.weekday() in range(0,4) and now.hour in range(8,17):
            # Helpdesk Button
            chat_button = Gtk.Button.new_with_label("Chat with the Helpdesk")
            chat_button.connect("clicked", self.start_chat)
            grid_right.attach(chat_button, 0, 4, 1, 1)

        # Attach the main grid to window and tell window to display everything attached
        window.add(grid)
        window.show_all()
    
    def get_sys_info(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        macaddr_hex = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = ':'.join(macaddr_hex[i:i + 2] for i in range(0, 11, 2))
        return f'Hostname: {hostname.split(".")[0]} \nIP: {ip} \nMAC: {mac.upper()}'

    def start_chat(self, chat_button, data=None):
        webbrowser.open('https://caen.engin.umich.edu/contact/')
    def visit_faq(self, faq_button, data=None):
        webbrowser.open('http://caenfaq.engin.umich.edu/')
    def take_screenshot(self, screenshot_button, username):
        # Takes a screenshot of the entire screen and stores it in /tmp for later processing
        # The following sets a limit of 2 screenshots
        screenshot1 = Path("/tmp/caen-help-%s-1.png" % username)
        screenshot2 = Path("/tmp/caen-help-%s-2.png" % username)
        if screenshot1.is_file():
            call(["gnome-screenshot","-f","/tmp/caen-help-%s-2.png" % username])
            screenshot_button.set_label("Take another screenshot")
        elif screenshot2.is_file():
            call(["gnome-screenshot","-f","/tmp/caen-help-%s-1.png" % username])
            screenshot_button.set_label("Take another screenshot")
        else:
            call(["gnome-screenshot","-f","/tmp/caen-help-%s-1.png" % username])
            screenshot_button.set_label("Take another screenshot")
    def submit_data(self, submit_button, TextView):
        # The conversion of what the user types to a local file
        user_input = TextView.get_buffer()
        user_input_bounds = user_input.get_bounds()
        response = user_input.get_text(user_input_bounds[0], user_input_bounds[1], True)
        print("%s" % response)
        # Collect rest of system information for submission

    def report_problem(self,report_button, username):

        # Creates a separate window
        window = Gtk.ApplicationWindow()
        window.set_title("")
        window.set_position(1)
        window.set_resizable(0)
        window.set_border_width(10)
        window.props.destroy_with_parent = True

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        grid.set_halign(1)
        grid.set_valign(1)

        question1 = Gtk.Label("Is the problem with this computer?")
        answer1 = Gtk.ComboBoxText()
        answer1.append_text("Yes")
        answer1.append_text("No")
        answer1.set_active(0)

        question2 = Gtk.Label("Please describe the issue:")
        answer2 = Gtk.TextView()
        answer2.set_wrap_mode(2)

        question3 = Gtk.Label("Attach any useful information:")
        file1 = Gtk.FileChooserButton("Select a file", 0)
       

        screenshot_button = Gtk.Button.new_with_label("Take a screenshot")
        screenshot_button.connect("clicked", self.take_screenshot, username)
        submit_button = Gtk.Button.new_with_label("Submit")
        submit_button.connect("clicked", self.submit_data, answer2)

        grid.attach(question1, 0, 0, 1, 1)
        grid.attach(answer1, 40, 0, 1, 1)

        grid.attach(question2, 0, 1, 1, 1)
        grid.attach(answer2, 1, 1, 40, 8)

        grid.attach(question3, 0, 9, 1, 1)
        grid.attach(file1, 40, 9, 1, 1)

        grid.attach(screenshot_button, 40, 10, 1, 1)
        grid.attach(submit_button, 40, 11, 1, 10)
        window.add(grid)
        window.show_all()

if __name__ == '__main__':
    app = CaenHelp()
    app.run()