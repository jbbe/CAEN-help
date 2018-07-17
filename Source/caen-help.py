### CAEN Help Application ###
# Python3 and PyGObject
# http://lazka.github.io/pgi-docs/index.html
# Linux Version written by Dakota Lambert
# Linux v0.75

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
from pwd import getpwnam  

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

        # Get UserName of currently logged in user
        UserName = os.getlogin()
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
        space_buffer = Gtk.Frame()
        space_buffer.set_shadow_type(0)
        grid_left.attach(space_buffer, 0, 0, 1, 4)
        grid_left.attach(logo_frame, 0, 5, 1, 1)

        ### Right Grid Contents ###

        # Contact Info
        contact_info = Gtk.Label()
        contact_info.set_text(" (734) 764 2236" "\n" "caen@umich.edu")
        contact_frame = Gtk.Frame()
        contact_frame.set_shadow_type(3)
        contact_frame.set_label("Contact")
        contact_frame.set_border_width(0)
        #contact_frame.set_label_align(0.5,.5)
        contact_frame.add(contact_info)
        
        grid_right.attach(contact_frame, 0, 0, 1, 2)
        #grid_right.attach(contact_email, 0, 1, 1, 1)
        # Info field
        sys_info_frame = Gtk.Frame()
        sys_info_frame.set_shadow_type(3)
        sys_info_frame.set_label("System Info")
        #sys_info_frame.set_label_align(.5,.5)
        sys_info_frame.set_border_width(0)
        # Set the get_sys_info call to True to only display data
        sys_info = Gtk.Label(self.get_sys_info(True, UserName))
        #sys_info.set_justify(0)
        sys_info_frame.add(sys_info)
        grid_right.attach(sys_info_frame, 0, 2, 1, 2)

        # Report Problem Button
        report_button = Gtk.Button.new_with_label("Report a Problem")
        report_button.connect("clicked", self.report_problem, UserName)
        grid_right.attach(report_button, 0, 4, 1, 1)

        # FAQ Button
        faq_button = Gtk.Button.new_with_label("Visit the FAQ")
        faq_button.connect("clicked", self.visit_faq)
        grid_right.attach(faq_button, 0, 5, 1, 1)

        # Determine if the Chat button should be shown 
        # Currently set for summer hours
        now = datetime.datetime.now()
        if now.weekday() in range(0,4) and now.hour in range(8,17):
            # Helpdesk Button
            chat_button = Gtk.Button.new_with_label("Chat with the Helpdesk")
            chat_button.connect("clicked", self.start_chat)
            grid_right.attach(chat_button, 0, 6, 1, 1)

        # Attach the main grid to window and tell window to display everything attached
        window.add(grid)
        window.show_all()
    
    def get_sys_info(self, DisplayOnly, UserName):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        macaddr_hex = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = ':'.join(macaddr_hex[i:i + 2] for i in range(0, 11, 2))
        # Used for the system information field on the main window
        if DisplayOnly:
            return f'{hostname.split(".")[0]} \n IP: {ip}'
        # Submit has been pressed and it's time to collect the data
        else:
            # Get all user sessions
            active_sessions = call(["loginctl","list-sessions"])
            uid = getpwnam('%s' % UserName)[2]
            gid = getpwnam('%s' % UserName)[3]
            pts_grps = "test" #call(["pts","mem" "%s" % UserName])
            if os.path.exists("/home/%s" % UserName) and os.path.isdir("/home/%s" % UserName):
                has_homedir = True
            else:
                has_homedir = False
            process_list = call(["ps","-ef"])
            return ''.join(["Hostname: %s\n" % hostname.split(".")[0], "IP: ", "%s\n" % ip, "Username: %s\n" % UserName, "Active Sessions:\n %s\n" % active_sessions, "UID: %s\n" % uid, "GID: %s\n" % gid, "PTS Groups:\n %s\n" % pts_grps, "Has Homedir: %s\n" % has_homedir,"User Processes:\n %s\n" % process_list ])

    def start_chat(self, chat_button, data=None):
        webbrowser.open('https://caen.engin.umich.edu/contact/')
    def visit_faq(self, faq_button, data=None):
        webbrowser.open('http://caenfaq.engin.umich.edu/')
    def take_screenshot(self, screenshot_button, UserName):
        # Takes a screenshot of the entire screen and stores it in /tmp for later processing
        # The following sets a limit of 2 screenshots based on their mtime
        screenshot1 = Path("/tmp/caen-help-%s-1.png" % UserName)
        screenshot2 = Path("/tmp/caen-help-%s-2.png" % UserName)
        if screenshot1.is_file() and screenshot2.is_file():
            screenshot1_time = os.path.getmtime(screenshot1)
            screenshot2_time = os.path.getmtime(screenshot2)
            if screenshot2_time < screenshot1_time:
                call(["gnome-screenshot","-f","/tmp/caen-help-%s-2.png" % UserName])
                screenshot_button.set_label("Take another screenshot")
            else:
                call(["gnome-screenshot","-f","/tmp/caen-help-%s-1.png" % UserName])
                screenshot_button.set_label("Take another screenshot")
        elif screenshot1.is_file():
            call(["gnome-screenshot","-f","/tmp/caen-help-%s-2.png" % UserName])
            screenshot_button.set_label("Take another screenshot")
        else:
            call(["gnome-screenshot","-f","/tmp/caen-help-%s-1.png" % UserName])
            screenshot_button.set_label("Take another screenshot")
    def submit_data(self, submit_button, ThisComputer, IssueDescription, Attachment, UserName):
        # Convert the input buffer into text
        issue_description_input = IssueDescription.get_buffer()
        issue_description_bounds = issue_description_input.get_bounds()
        issue_description_text = issue_description_input.get_text(issue_description_bounds[0], issue_description_bounds[1], True)
    
        
        
        # Get status of whether or not the problem is with this computer
        # True an false are flipped due to Index. Yes is the desired first and default result
        this_computer_response = ThisComputer.get_active()
        # If No is selected: skip system info collection and just send input + other attachments
        if this_computer_response:
            print(f"%s is not the problem" % Attachment)
        # If Yes is selected: gather system info and compile it with the response
        else:
            report = self.get_sys_info(False, UserName)
            print(f"%s" % report)
            # Determine if there's an attachment
            if type(Attachment.get_filename()) is str:
                print(f"Issue Description:\n %s" % issue_description_text)
            # Attachment is NoneType
            else:
                print(f"Issue Description:\n %s" % issue_description_text)
        # Collect rest of system information for submission

    def report_problem(self,report_button, UserName):

        # Creates a separate window
        window = Gtk.ApplicationWindow()
        window.set_title("")
        window.set_position(1)
        window.set_resizable(0)
        window.set_border_width(10)
        window.props.destroy_with_parent = True

        # Creates a two column grid - questions on the left - answers on right
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        grid.set_halign(1)
        grid.set_valign(1)
        grid.props.column_homogeneous = True
        # Question and Answer 1 - This computer
        question1 = Gtk.Label("Is the problem with this computer?")
        question1.set_halign(1)
        this_computer_response = Gtk.ComboBoxText()
        this_computer_response.append_text("Yes")
        this_computer_response.append_text("No")
        this_computer_response.set_active(0)
        # Question and Answer 2 - Issue Description
        question2 = Gtk.Label("Please describe the issue:")
        question2.set_halign(1)
        issue_description = Gtk.TextView()
        issue_description.set_wrap_mode(2)
        issue_frame = Gtk.Frame()
        issue_frame.set_shadow_type(3)
        issue_frame.add(issue_description)
        # Question and Answer 3 - Attachment
        question3 = Gtk.Label("Attach any useful information:")
        question3.set_halign(1)
        file_attachment = Gtk.FileChooserButton("Select a file", 0)
        # Screenshot Hint
        screenshot_hint = Gtk.Label("While the button will continue to take screenshots,\nonly the two most recent screenshots are sent.")
        screenshot_hint.set_halign(1)
        screenshot_hint.set_line_wrap(True)
        screenshot_hint.set_line_wrap_mode(2)
       # screenshot_hint.props.wrap = True
        #screenshot_hint.set_width_chars(10)
        # Screenshot Button 
        screenshot_button = Gtk.Button.new_with_label("Take a screenshot")
        screenshot_button.connect("clicked", self.take_screenshot, UserName)

        submit_button = Gtk.Button.new_with_label("Submit")
        submit_button.connect("clicked", self.submit_data, this_computer_response, issue_description, file_attachment, UserName)

        # Attach every question and answer to the grid
        # 40 is set as the width for the text entry
        # Other widgets in the right column are placed at 40 to be right aligned
        grid.attach(question1, 0, 0, 1, 1)
        grid.attach(this_computer_response, 1, 0, 1, 1)

        grid.attach(question2, 0, 1, 1, 1)
        grid.attach(issue_frame, 1, 1, 1, 8)

        grid.attach(question3, 0, 9, 1, 1)
        grid.attach(file_attachment, 1, 9, 1, 1)
        grid.attach(screenshot_hint, 0, 10, 1, 1)
        grid.attach(screenshot_button, 1, 10, 1, 1)
        grid.attach(submit_button, 1, 11, 1, 15)
        # Add the grid to the window and tell the window to show all
        window.add(grid)
        window.show_all()

if __name__ == '__main__':
    app = CaenHelp()
    app.run()