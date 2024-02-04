import customtkinter
from customtkinter import filedialog
import os
from PIL import ImageTk

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
        self.iconpath = ImageTk.PhotoImage(
            file=os.path.join(".", "assets", "logo-ibb.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        # build ui
        # Use CTkButton instead of tkinter Button
        button = customtkinter.CTkButton(
            master=self, text="IFC-Datei auswählen", command=self._select_file)
        button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    def _select_file(self):
        self.ifc_file_path = filedialog.askopenfilename(
            filetypes=[("IFC-Dateien", ".ifc")])
        print(self.ifc_file_path)


if __name__ == "__main__":
    app = App()
    app.mainloop()
