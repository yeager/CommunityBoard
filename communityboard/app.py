"""CommunityBoard - Huvudapplikation med GTK4/Adwaita UI."""

import sys

import gi
from communityboard.i18n import _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, Gtk

from communityboard.data import KATEGORIER, ladda_inlagg, skapa_inlagg


class InlaggsRad(Gtk.ListBoxRow):
    """En rad i anslagstavlan som visar ett inlägg."""

    def __init__(self, inlagg):
        super().__init__()
        self.inlagg = inlagg

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.set_margin_top(8)
        box.set_margin_bottom(8)
        box.set_margin_start(12)
        box.set_margin_end(12)

        # Övre rad: kategori-etikett + datum
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        kategori_label = Gtk.Label(label=inlagg["kategori"])
        kategori_label.add_css_class("caption")
        kategori_label.add_css_class("dim-label")
        header.append(kategori_label)

        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        header.append(spacer)

        datum_label = Gtk.Label(label=inlagg["datum"])
        datum_label.add_css_class("caption")
        datum_label.add_css_class("dim-label")
        header.append(datum_label)

        box.append(header)

        # Titel
        titel_label = Gtk.Label(label=inlagg["titel"], xalign=0)
        titel_label.add_css_class("heading")
        titel_label.set_wrap(True)
        box.append(titel_label)

        # Text
        text_label = Gtk.Label(label=inlagg["text"], xalign=0)
        text_label.set_wrap(True)
        text_label.add_css_class("body")
        box.append(text_label)

        # Kontakt
        if inlagg.get("kontakt"):
            kontakt_label = Gtk.Label(label=f"Kontakt: {inlagg['kontakt']}", xalign=0)
            kontakt_label.add_css_class("caption")
            box.append(kontakt_label)

        self.set_child(box)


class CommunityBoardWindow(Adw.ApplicationWindow):
    """Huvudfönster för CommunityBoard."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs, title="CommunityBoard")
        self.set_default_size(600, 700)

        self.aktiv_kategori = None

        # Huvudlayout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Headerbar
        header = Adw.HeaderBar()
        header.set_title_widget(Adw.WindowTitle(
            title=_("CommunityBoard",
            subtitle=_("Anslagstavla för funktionshinderrörelsen",
        ))

        # Knapp för nytt inlägg
        ny_knapp = Gtk.Button(icon_name="list-add-symbolic")
        ny_knapp.set_tooltip_text(_("Nytt inlägg")
        ny_knapp.connect("clicked", self._visa_nytt_inlagg_dialog)
        header.pack_start(ny_knapp)

        main_box.append(header)

        # Sök
        self.sok_entry = Gtk.SearchEntry()
        self.sok_entry.set_placeholder_text(_("Sök inlägg...")
        self.sok_entry.set_margin_start(12)
        self.sok_entry.set_margin_end(12)
        self.sok_entry.set_margin_top(8)
        self.sok_entry.connect("search-changed", self._vid_sok)
        main_box.append(self.sok_entry)

        # Kategorifilter
        filter_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        filter_box.set_margin_start(12)
        filter_box.set_margin_end(12)
        filter_box.set_margin_top(8)
        filter_box.set_margin_bottom(4)

        alla_knapp = Gtk.ToggleButton(label=_("Alla")
        alla_knapp.set_active(True)
        alla_knapp.connect("toggled", self._vid_filter, None)
        self.filter_knappar = [alla_knapp]
        filter_box.append(alla_knapp)

        for kat in KATEGORIER:
            knapp = Gtk.ToggleButton(label=kat)
            knapp.set_group(alla_knapp)
            knapp.connect("toggled", self._vid_filter, kat)
            self.filter_knappar.append(knapp)
            filter_box.append(knapp)

        main_box.append(filter_box)

        # Inläggslista
        scrolled = Gtk.ScrolledWindow(vexpand=True)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.add_css_class("boxed-list")
        self.listbox.set_margin_start(12)
        self.listbox.set_margin_end(12)
        self.listbox.set_margin_top(8)
        self.listbox.set_margin_bottom(12)
        scrolled.set_child(self.listbox)
        main_box.append(scrolled)

        self.set_content(main_box)
        self._uppdatera_lista()

    def _uppdatera_lista(self):
        """Ladda om inlägg i listan."""
        # Ta bort alla rader
        while True:
            row = self.listbox.get_row_at_index(0)
            if row is None:
                break
            self.listbox.remove(row)

        sok_text = self.sok_entry.get_text().lower()
        for inlagg in ladda_inlagg():
            # Kategorifilter
            if self.aktiv_kategori and inlagg["kategori"] != self.aktiv_kategori:
                continue
            # Sökfilter
            if sok_text:
                sökbart = f"{inlagg['titel']} {inlagg['text']} {inlagg.get('kontakt', '')}".lower()
                if sok_text not in sökbart:
                    continue
            self.listbox.append(InlaggsRad(inlagg))

        # Visa meddelande om listan är tom
        if self.listbox.get_row_at_index(0) is None:
            tom_label = Gtk.Label(label=_("Inga inlägg hittades.")
            tom_label.add_css_class("dim-label")
            tom_label.set_margin_top(24)
            tom_label.set_margin_bottom(24)
            row = Gtk.ListBoxRow(selectable=False)
            row.set_child(tom_label)
            self.listbox.append(row)

    def _vid_sok(self, entry):
        self._uppdatera_lista()

    def _vid_filter(self, knapp, kategori):
        if knapp.get_active():
            self.aktiv_kategori = kategori
            self._uppdatera_lista()

    def _visa_nytt_inlagg_dialog(self, knapp):
        """Visa dialog för att skapa nytt inlägg."""
        dialog = Adw.Dialog()
        dialog.set_title("Nytt inlägg")
        dialog.set_content_width(400)
        dialog.set_content_height(500)

        toolbar_view = Adw.ToolbarView()
        dialog_header = Adw.HeaderBar()
        toolbar_view.add_top_bar(dialog_header)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(16)
        content.set_margin_bottom(16)
        content.set_margin_start(16)
        content.set_margin_end(16)

        # Titel
        titel_entry = Gtk.Entry()
        titel_entry.set_placeholder_text(_("Titel")
        content.append(Gtk.Label(label=_("Titel", xalign=0))
        content.append(titel_entry)

        # Kategori
        content.append(Gtk.Label(label=_("Kategori", xalign=0))
        kategori_dropdown = Gtk.DropDown.new_from_strings(KATEGORIER)
        content.append(kategori_dropdown)

        # Text
        content.append(Gtk.Label(label=_("Beskrivning", xalign=0))
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        text_view.set_vexpand(True)
        text_frame = Gtk.Frame()
        text_frame.set_child(text_view)
        content.append(text_frame)

        # Kontakt
        kontakt_entry = Gtk.Entry()
        kontakt_entry.set_placeholder_text(_("E-post eller telefon (valfritt)")
        content.append(Gtk.Label(label=_("Kontakt", xalign=0))
        content.append(kontakt_entry)

        # Spara-knapp
        spara_knapp = Gtk.Button(label=_("Publicera")
        spara_knapp.add_css_class("suggested-action")
        spara_knapp.set_margin_top(8)

        def _spara(btn):
            titel = titel_entry.get_text().strip()
            buf = text_view.get_buffer()
            text = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False).strip()
            if not titel or not text:
                return
            kategori = KATEGORIER[kategori_dropdown.get_selected()]
            kontakt = kontakt_entry.get_text().strip()
            skapa_inlagg(titel, text, kategori, kontakt)
            dialog.close()
            self._uppdatera_lista()

        spara_knapp.connect("clicked", _spara)
        content.append(spara_knapp)

        toolbar_view.set_content(content)
        dialog.set_child(toolbar_view)
        dialog.present(self)


class CommunityBoardApp(Adw.Application):
    """Huvudapplikation."""

    def __init__(self):
        super().__init__(
            application_id="se.communityboard.app",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

    def do_activate(self):
        win = CommunityBoardWindow(application=self)
        win.present()


def main():
    app = CommunityBoardApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
