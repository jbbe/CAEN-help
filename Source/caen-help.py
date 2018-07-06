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

        # Create and define a Gtk.Grid
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        grid.set_halign(1)
        grid.set_valign(1)

        # Establish a frame around the caen logo
        logoframe = Gtk.Frame()
        logoframe.set_shadow_type(0)
        logo = Gtk.Image.new_from_file('/home/drlamb/git/caen-help/Source/caen.png')
        logoframe.add(logo)
        grid.attach(logoframe, 0, 0, 1, 1 )

        # Info field
        infoframe = Gtk.Frame()
        infoframe.set_shadow_type(3)
        test = Gtk.Label(self.sysinfo())
        test.set_justify(0)
        infoframe.add(test)
        grid.attach(infoframe, 0, 1, 1, 1)

        # Report Button
        reportbutton = Gtk.Button.new_with_label("Report a Problem")
        reportbutton.connect("clicked", self.report_problem)
        grid.attach(reportbutton, 0, 2, 1, 1)

        # FAQ Button
        faqbutton = Gtk.Button.new_with_label("Visit the FAQ")
        faqbutton.connect("clicked", self.visit_faq)
        grid.attach(faqbutton, 0, 3, 1, 1)

        # Attach grid to window and tell window to display everything attached
        window.add(grid)
        window.show_all()

    def visit_faq(faqbutton, data=None):
        webbrowser.open('http://caenfaq.engin.umich.edu/')

    def report_problem(reportbutton, data=None):
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


        submit = Gtk.Button.new_with_label("Submit")

        grid.attach(question1, 0, 0, 1, 1)
        grid.attach(answer1, 1, 0, 1, 1)
        grid.attach(question2, 0, 1, 1, 1)
        grid.attach(answer2, 1, 1, 1, 1,)
        grid.attach(question3, 0, 2, 1, 1)
        grid.attach(submit, 1, 3, 1, 1)
        window.add(grid)
        window.show_all()

        
    @staticmethod
    def sysinfo():
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        macaddr_hex = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = ':'.join(macaddr_hex[i:i + 2] for i in range(0, 11, 2))
        return f'Hostname: {hostname.split(".")[0]} \nIP: {ip} \nMAC: {mac.upper()}'

if __name__ == '__main__':
    app = CaenHelp()
    app.run()