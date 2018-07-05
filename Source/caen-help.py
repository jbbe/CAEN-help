import gi
import sys
import webbrowser
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

        # Establish a frame around the caen logo
        logoframe = Gtk.Frame()
        logoframe.set_shadow_type(0)
        logo = Gtk.Image.new_from_file('/home/drlamb/git/caen-help/Source/caen.png')
        logoframe.add(logo)

        # Create and define a Gtk.Grid
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        grid.set_halign(1)
        grid.set_valign(1)
        grid.attach(logoframe, 0, 0, 1, 1 )

        # Report Button
        reportbutton = Gtk.Button()
        reportbutton.set_label("Report a Problem")
        reportbutton.connect("clicked", self.report_problem)
        grid.attach(reportbutton, 0, 1, 1, 1)

        # FAQ Button
        faqbutton = Gtk.Button()
        faqbutton.set_label("Visit the FAQ")
        faqbutton.connect("clicked", self.visit_faq)
        grid.attach(faqbutton, 0, 2, 1, 1)

        # Attach grid to window and tell window to display everything attached
        window.add(grid)
        window.show_all()

    def visit_faq(faqbutton, data=None):
        webbrowser.open('http://caenfaq.engin.umich.edu/')

    def report_problem(reportbutton, data=None):
        print(f"hello")

if __name__ == '__main__':
    app = CaenHelp()
    app.run()