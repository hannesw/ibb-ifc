import customtkinter
from customtkinter import filedialog
import os
from PIL import ImageTk

from ibb_ifc.lib import bbsoft
from ibb_ifc.lib import quantity_takeoff as qto

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # data setup
        self.ifc_file_path = ""

        # ui setup
        self.title("IBB IFC-Verarbeitung")
        self.geometry("400x240")
        # Icon disabled due to probelms with pyinstaller and --add-data flag
        # self.iconpath = ImageTk.PhotoImage(
        # file=os.path.join(".", "assets", "logo-ibb.png"))
        # self.wm_iconbitmap()
        # self.iconphoto(False, self.iconpath)

        # build ui
        # Use CTkButton instead of tkinter Button
        self.button = customtkinter.CTkButton(
            master=self, text="IFC-Datei auswählen", command=self._select_file)
        self.button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    def _process_ifc_file(self):
        # Show loading indicator on button
        self.progressbar = customtkinter.CTkProgressBar(
            self, orientation="horizontal", mode="indeterminate")
        self.progressbar.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)
        self.progressbar.start()

        self.update()  # Update the UI to show the progress bar
        self.update_idletasks()  # Force an immediate update of the UI

        processed_file_path = bbsoft.process(self.ifc_file_path)
        qto.get(processed_file_path)

        self.progressbar.stop()
        self.progressbar.destroy()
        # Show message box
        self.label = customtkinter.CTkLabel(
            master=self, text="Die IFC-Datei wurde erfolgreich verarbeitet.")
        self.label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

    def _select_file(self):
        self.ifc_file_path = filedialog.askopenfilename(
            filetypes=[("IFC-Dateien", ".ifc")])
        if self.ifc_file_path:
            self._process_ifc_file()


if __name__ == "__main__":
    app = App()
    app.mainloop()
