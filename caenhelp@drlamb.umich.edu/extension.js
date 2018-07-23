const St = imports.gi.St;
const Main = imports.ui.main;
const Lang = imports.lang;
const Clutter = imports.gi.Clutter;
const PanelMenu = imports.ui.panelMenu;
const Util = imports.misc.util;

const CaenHelpShortcut = new Lang.Class({
  Name: 'CaenHelpShortcut',
  Extends: PanelMenu.Button,

  _init: function () {
    this.parent(0.0, "Caen Help Shortcut", true);
    this.buttonText = new St.Label({
      text: _("CAEN Help"),
      y_align: Clutter.ActorAlign.CENTER
    });
    this.actor.add_actor(this.buttonText);
    this.actor.connect('button-press-event',Lang.bind(this, function() {
        Util.spawn(['gnome-boxes'])
    }));
  },
  }
);

let chShortcut;

function init() {
    
}

function enable() {
	chShortcut = new CaenHelpShortcut;
	Main.panel.addToStatusArea('ch-indicator', chShortcut);
}

function disable() {
	chShortcut.stop();
	chShortcut.destroy();
}