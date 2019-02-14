### CAEN Help Application ###
# Linux v0.98 - Fall 2018
# Written by Dakota Lambert
#############################

import gi
import sys
import os
import webbrowser
import socket
import uuid
import time
import datetime
import smtplib
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from subprocess import Popen, PIPE # Run cannot be used in rhel 7 due to python 3.4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import email.encoders
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
        UserName = os.getlogin()]
        # UserName = "josh"
        
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
        caen_logo = Gtk.Image.new_from_file('/home/josh/caen-help/Source/Linux/caen.png')
        logo_frame.add(caen_logo)
        grid_left.attach(logo_frame, 0, 0, 1, 1)

        ###########################

        ### Right Grid Contents ###

        # Contact Info
        contact_info = Gtk.Label()
        contact_info.set_text(" (734) 764 2236" "\n" "caen@umich.edu")
        contact_info.set_xalign(.5)
        contact_frame = Gtk.Frame()
        contact_frame.set_shadow_type(3)
        contact_frame.set_label("Contact")
        contact_frame.set_border_width(0)
        contact_frame.add(contact_info)
        grid_right.attach(contact_frame, 0, 0, 1, 2)

        # System Info field
        sys_info_frame = Gtk.Frame()
        sys_info_frame.set_shadow_type(3)
        sys_info_frame.set_label("System Info")
        sys_info_frame.set_border_width(0)
        # Set the get_sys_info call to True to only display data rather than collect
        sys_info = Gtk.Label(self.get_sys_info(True, UserName))
        sys_info.set_xalign(.5)
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

        ### Determine if the Chat button should be shown ###############################
        ### Currently set for summer 2018 hours ########################################
        #TODO
        # Perhaps link to google caledar for live status of the hotline chat
        # Would need api access key
        now = datetime.datetime.now()
        if now.weekday() in range(0,4) and now.hour in range(8,20):
        ################################################################################
            # Helpdesk Button
            chat_button = Gtk.Button.new_with_label("Chat with the Helpdesk")
            chat_button.connect("clicked", self.start_chat)
            grid_right.attach(chat_button, 0, 6, 1, 1)

        ################################################################################

        # Attach the main grid to window and tell window to display everything attached
        window.add(grid)
        window.show_all()
    
    # Function to get system information ###############################################
    # DisplayOnly - bool to control wether or not system information is collected
    # UserName - username of current user
    def get_sys_info(self, DisplayOnly, UserName):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        macaddr_hex = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = ':'.join(macaddr_hex[i:i + 2] for i in range(0, 11, 2))
        # Used for the system information field on the main window
        if DisplayOnly:
            # Return the hostname striped of the .engin.umich.edu and the IP
            return "{hostname} \n IP: {ip}".format(hostname=hostname.split(".")[0], ip=ip)
        # Submit has been pressed and it's time to collect the data
        else:
            # Get all user sessions
            active_sessions = Popen(["loginctl","list-sessions"]).communicate()[0]
            uid = getpwnam('%s' % UserName)[2]
            gid = getpwnam('%s' % UserName)[3]
            pts_grps = "test" #call(["pts","mem" "%s" % UserName]) ##TODO
            if os.path.exists("/home/{username}".format(username=UserName)) and os.path.isdir("/home/{username}".format(username=UserName)):
                has_homedir = True
            else:
                has_homedir = False
            # Save process list to local file because popen with PIPE results in escape characters being stripped
            process_list = open("/tmp/caen-help-{username}-process-list".format(uid=uid,username=UserName), "w+")
            # Pipe stdout to process_list file
            Popen(['ps', '-ef'], stdout=process_list).communicate()[0]
            # Reopen the file for reading, in read only mode for no particular reason. 
            process_list = open("/tmp/caen-help-{username}-process-list".format(username=UserName), "r")
            report = open("/tmp/caen-help-{username}-report".format(username=UserName), "w+")
            report.write(''.join(["Hostname: {hostname}\n".format(hostname=hostname.split(".")[0]), "IP: ", "{ip}\n".format(ip=ip), "Username: %s\n" % UserName, "Active Sessions:\n {active_sessions}".format(active_sessions=active_sessions), "UID: {uid}\n".format(uid=uid), "GID: {gid}\n".format(gid=gid), "PTS Groups:\n {pts_grps}\n".format(pts_grps=pts_grps), "Has Homedir: {has_homedir}\n".format(has_homedir=has_homedir), "User Process List:\n {process_list}s\n".format(process_list=process_list.read())]))
            return
    #####################################################################################
    # Function to start chat. Intentionally not combined with the faq buttons and both actions might evolve over time as new services are evaluated
    # Perhaps direct link to liveengage?
    def start_chat(self, chat_button, data=None):
        webbrowser.open('https://caen.engin.umich.edu/contact/')
    # Function to open FAQ ##############################################################
    # Perhaps link into future FAQ platform's API
    def visit_faq(self, faq_button, data=None):
        webbrowser.open('http://caenfaq.engin.umich.edu/')
    # Function to take screenshots ######################################################
    # Writes over the same two files in /tmp based on username
    def take_screenshot(self, screenshot_button, UserName):
        # The following sets a limit of 2 screenshots based on their mtime
        screenshot1 = Path("/tmp/caen-help-{username}-1.png".format(username=UserName))
        screenshot2 = Path("/tmp/caen-help-{username}-2.png".format(username=UserName))
        if screenshot1.is_file() and screenshot2.is_file():
            screenshot1_time = os.path.getmtime(str(screenshot1))
            screenshot2_time = os.path.getmtime(str(screenshot2))
            if screenshot2_time < screenshot1_time:
                Popen(["gnome-screenshot", "-f","/tmp/caen-help-{username}-2.png".format(username=UserName)])
                screenshot_button.set_label("Take another screenshot")
            else:
                Popen(["gnome-screenshot", "-f","/tmp/caen-help-{username}-1.png".format(username=UserName)])
                screenshot_button.set_label("Take another screenshot")
        elif screenshot1.is_file():
            Popen(["gnome-screenshot", "-f","/tmp/caen-help-{username}-2.png".format(username=UserName)])
            screenshot_button.set_label("Take another screenshot")
        else:
            Popen(["gnome-screenshot", "-f","/tmp/caen-help-{username}-1.png".format(username=UserName)])
            screenshot_button.set_label("Take another screenshot")


    # Function to remove all temporary files #############################################
    # Writes a "receipt" to the $XDG_RUNTIME_DIR that submit_data() checks for to ensure 
    # that two reports cannot be sent within 5 minutes of each other to avoid abuse
    def do_cleanup(self, UserName):
        #call(['rm /tmp/caen-help-%s-*' % UserName])
        # Add rm with wildcard to delete temp files
        uid = getpwnam("{username}".format(username=UserName))[2]
        receipt = open(("/run/user/{uid}/caen-help-{username}-receipt").format(uid=uid,username=UserName), "w+")
        receipt.close()
        # Kill the report window
        # I want to eventually add a green submitted button or some other form of feedback

        
    # Function to gather up and submit the data for further filtering ####################
    # Checks if receipt file exists - need to implement some form of warning to the user #TODO
    # Currently submits data via email. Future solutions might include hooking directly into Jira's or X's api for reporting issues 
    # Takes:
    # ThisComputer - (bool) - reversed due to Gtk.ComboBox() index. 0 indicates the problem is with this machine
    # IssueDescription - raw input buffer that has to be processed
    # Attachment - file selected in the report window. If no file is selected this object with be a None type 
    # UserName - username of current user
    # Window - the problem report window. Used here to close the window upon confirming submission, also quits CAEN Help
    #
    #TODO As we discussed during the meeting, the email/attachment system needs to be rewritten/reimplemented, preferably with smtplib as
    # that is what the Windows version uses. 
    def submit_data(self, submit_button, ThisComputer, IssueDescription, Attachment, UserName, Window):
        """Check whether user has submitted a report in the last 5 minutes and if not submit an email explaining their issue. """
	# Check whether or not report has been sent in the last 5 minutes Todo?
        # i changed to my usrname
        uid = getpwnam("{username}".format(username=UserName))[2]
        
	# Generate default email flags  
        mail_flags = ''.join(["-s ", "\"CAEN Problem Report from {username}\"".format(username=UserName)])
        attachments= ""

     	# Convert the input buffer into text
        issue_description_input = IssueDescription.get_buffer()
        issue_description_bounds = issue_description_input.get_bounds()
        issue_description_text = issue_description_input.get_text(issue_description_bounds[0], issue_description_bounds[1], True)
        
	# Set screen shot path names
        screen_shot_1 = "/tmp/caen-help-{username}-1.png".format(username=UserName)
        screen_shot_2 = "/tmp/caen-help-{username}-2.png".format(username=UserName)


	# Initialize email message and server
        SERVER = "mx1.a.mail.umich.edu"
        send_email = MIMEMultipart()
        send_email['From'] = "{username}@umich.edu".format(username=UserName) 
        send_email['To'] = "jbbe@umich.edu"
        send_email['Subject'] = "CAEN Issue Report from {username}".format(username=UserName)
        message = issue_description_text
        send_email.attach(MIMEText(message, 'plain'))
        smtp = smtplib.SMTP()
        smtp.connect(SERVER)

        # Check if screen shot 1 & 2 and attachment exist
	# If they exist attach to send_email object
        if os.path.exists(screen_shot_1):
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(screen_shot_1, "rb").read())
            email.encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={filename}'.format(filename = screen_shot_1))
            send_email.attach(part)
        
        if os.path.exists(screen_shot_2):
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(screen_shot_2, "rb").read())
            email.encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={filename}'.format(filename = screen_shot_2))
            send_email.attach(part)

        if type(Attachment.get_filename()) is str:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(Attachment.get_filename(), "rb").read())
            email.encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={filename}'.format(filename = screen_shot_1))
            send_email.attach(part)

        # Get status of whether or not the problem is with this computer
        # True and false are flipped due to Index. Yes (0) is the desired first and default result
	# If false then attach info doc from tmp/ dir
        data_collection_is_off = ThisComputer.get_active()
        if not data_collection_is_off: 
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open("/tmp/caen-help-{username}-report".format(username=UserName), "rb").read())
            email.encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={filename}'.format(filename = screen_shot_1))
            send_email.attach(part)

        smtp.sendmail(send_email['From'], send_email['To'], send_email.as_string())
        smtp.quit()

        # Submission success check 
        # Submission confirmation Popup #TODO
        submitted = Gtk.Dialog()
        # set_transient_for is used to avoid warning because submitted doesn't have a parent
        submitted.set_transient_for(Window)
        submitted.add_buttons(Gtk.STOCK_OK, 1)
        label = Gtk.Label('Your issue has been sucessfully reported. Press OK to close CAEN Help.')
        label.show()
        submitted.vbox.pack_start(label, False, False, 0)
        answer = submitted.run()
        submitted.destroy()
        # Delete temporary files and write the receipt
        self.do_cleanup(UserName)
        # Closes the report a problem window
        Window.close()
        # Quits the CAEN Help application itself
        self.quit()

    # Function to open the second window to collect issue description ###################
    def report_problem(self,report_button, UserName):

        # Creates a separate window
        window = Gtk.ApplicationWindow()
        window.set_title("Problem Reporting")
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
        data_collection_is_off = Gtk.ComboBoxText()
        data_collection_is_off.append_text("Yes")
        data_collection_is_off.append_text("No")
        data_collection_is_off.set_active(0)
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
        screenshot_hint = Gtk.Label("Press this button to take a screenshot of the entire screen.\nOnly the two most recent screenshots are sent.")
        screenshot_hint.set_halign(1)
        # Screenshot Button 
        screenshot_button = Gtk.Button.new_with_label("Take a screenshot")
        screenshot_button.connect("clicked", self.take_screenshot, UserName)
        submit_button = Gtk.Button.new_with_label("Submit")
        submit_button.connect("clicked", self.submit_data, data_collection_is_off, issue_description, file_attachment, UserName, window)

        # Attach every question and answer to the grid
        grid.attach(question1, 0, 0, 1, 1)
        grid.attach(data_collection_is_off, 1, 0, 1, 1)

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
