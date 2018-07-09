### CAEN Help Application ###
# Python3 and PyGObject
# http://lazka.github.io/pgi-docs/index.html

import gi
import sys
import webbrowser
import socket
import uuid
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

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

        #Gtk.Grid
        # attach(child, left, top, width, height)

        # Create and define a Gtk.Grid
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
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

        # Attach the two grids to the initial
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

        # Report Button
        report_button = Gtk.Button.new_with_label("Report a Problem")
        report_button.connect("clicked", self.report_problem)
        grid_right.attach(report_button, 0, 2, 1, 1)

        # Helpdesk Button
        chat_button = Gtk.Button.new_with_label("Chat with the Helpdesk")
        chat_button.connect("clicked", self.start_chat)
        grid_right.attach(chat_button, 0, 3, 1, 1)

        # FAQ Button
        faq_button = Gtk.Button.new_with_label("Visit the FAQ")
        faq_button.connect("clicked", self.visit_faq)
        grid_right.attach(faq_button, 0, 4, 1, 1)

         # Right Grid Spacing Buffer
        #buffer = Gtk.Label()
        #grid_right.attach(buffer, 0, 0, 1, 1)

        # Attach grid to window and tell window to display everything attached
        window.add(grid)
        window.show_all()
    
    def start_chat(chat_button, data=None):
        webbrowser.open('https://caen.engin.umich.edu/contact/')
    def visit_faq(faq_button, data=None):
        webbrowser.open('http://caenfaq.engin.umich.edu/')

    def report_problem(report_button, data=None):
        # Creates a separate window
        window = Gtk.ApplicationWindow()
        window.set_title("")
        window.set_position(1)
        window.set_resizable(0)
        window.set_border_width(10)

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
        answer2 = Gtk.Entry()

        question3 = Gtk.Label("Screenshot(s) of issue or other useful information:")
        file1 = Gtk.FileChooserButton("Select a file", 0)
        file2 = Gtk.FileChooserButton("Select another file", 0)
       


        submit = Gtk.Button.new_with_label("Submit")

        grid.attach(question1, 0, 0, 1, 1)
        grid.attach(answer1, 1, 0, 1, 1)
        grid.attach(question2, 0, 1, 1, 1)
        grid.attach(answer2, 1, 1, 1, 1,)
        grid.attach(question3, 0, 2, 1, 1)
        grid.attach(file1, 1, 2, 1, 1)
        grid.attach(file2, 1, 3, 1, 1)
        grid.attach(submit, 1, 4, 1, 1)
        window.add(grid)
        window.show_all()

        
    @staticmethod
    def get_sys_info():
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        macaddr_hex = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = ':'.join(macaddr_hex[i:i + 2] for i in range(0, 11, 2))
        return f'Hostname: {hostname.split(".")[0]} \nIP: {ip} \nMAC: {mac.upper()}'

if __name__ == '__main__':
    app = CaenHelp()
    app.run()