using Gtk;


class CaenHelpApp : Window {

    CaenHelpApp () {
        var header = new HeaderBar ();

        header.set_title("CAEN Help");
        header.show_close_button = true;
        
        this.window_position = WindowPosition.CENTER;
        set_titlebar(header);
        set_resizable(false);
        border_width = 10;

        var grid = new Grid();
        grid.column_spacing=5;
        grid.row_spacing=5;
        this.add(grid);

        var logoFrame = new Frame (null);
        logoFrame.set_shadow_type(NONE);
        var caenLogo = new Image ();
        caenLogo.set_from_file ("/home/drlamb/git/caen-help/Source/caen.png");
        logoFrame.add(caenLogo);
        grid.set_halign(CENTER);
        grid.set_valign(CENTER);
        grid.attach(logoFrame, 0, 0, 1, 1 );

        var reportButton = new Button.with_label("Report a Problem");
        reportButton.set_hexpand(true);
        reportButton.clicked.connect (() => {

        });
        grid.attach(reportButton, 0, 1, 1, 1);

        var faqButton = new Button.with_label("Visit the FAQ");
        faqButton.set_hexpand(true);
        faqButton.clicked.connect (() => {
            try {
                GLib.Process.spawn_command_line_async("firefox -foregound -new-window http://caenfaq.engin.umich.edu/");
            }  catch (SpawnError e) {
                Posix.openlog("caen-help", Posix.LOG_PID, Posix.LOG_USER);
                Posix.syslog(Posix.LOG_WARNING, "Caen-help failed to open firefox on ");
            }

        });
        grid.attach(faqButton, 0, 2, 1, 1);
    }
    static int main (string[] args) {
        init (ref args);

        var window = new CaenHelpApp ();
        window.destroy.connect (main_quit);
        window.show_all();

        Gtk.main ();
        return 0;
    }
    
}