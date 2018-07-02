using Gtk;

class CaenHelpApp : Window {

    CaenHelpApp () {
        var header = new HeaderBar ();

        header.set_title("CAEN Help");
        header.show_close_button = true;

        this.window_position = WindowPosition.CENTER;
        set_titlebar(header);
        set_default_size(400, 250);
        border_width = 15;

        var grid = new Grid();
        grid.column_spacing=5;
        grid.row_spacing=10;
        this.add(grid);

        var caenLogo = new Image ();
        caenLogo.set_hexpand(true);
        caenLogo.set_from_file ("/home/drlamb/git/caen-help/Source/caen.png");
        grid.attach(caenLogo, 0, 0, 1, 1 );

        var reportButton = new Button.with_label("Report a Problem");
        reportButton.clicked.connect (() => {

        });
        grid.attach(reportButton, 0, 1, 1, 1);

        var faqButton = new Button.with_label("Visit the FAQ");
        faqButton.clicked.connect (() => {

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