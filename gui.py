import customtkinter
import tkinter.filedialog as filedialog
import lib.bbsoft as bbsoft
import lib.model_checker as model_checker
import lib.quantity_takeoff as qto
from threading import Thread


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #
        # Setup
        #

        # Variables
        self.filename = None
        self.checks_var = customtkinter.StringVar(value="on")
        self.qto_var = customtkinter.StringVar(value="off")

        # Window
        self.geometry("400x400")

        #
        # Widgets
        #

        # File selection
        self.file_button = customtkinter.CTkButton(
            self, text="IFC-Datei auswählen", command=self.on_select_file
        )
        self.file_button.pack(padx=20, pady=5)

        # File name label
        self.file_label = customtkinter.CTkLabel(master=self, text="")
        self.file_label.pack()

        # Run button
        self.run_button = customtkinter.CTkButton(
            self,
            text="Datei verarbeiten",
            state="disabled",
            command=self.on_start_file_processing,
        )
        self.run_button.pack(padx=20, pady=5)

        # Progress bar
        self.progress_bar = customtkinter.CTkProgressBar(self, mode="indeterminate")

        # Check box if to perform checks
        self.checks_checkbox = customtkinter.CTkCheckBox(
            self,
            text="Modellprüfung durchführen?",
            variable=self.checks_var,
            onvalue="on",
            offvalue="off",
        )
        self.qto_checkbox = customtkinter.CTkCheckBox(
            self,
            text="Mengenermittlung durchführen?",
            variable=self.qto_var,
            onvalue="on",
            offvalue="off",
        )

    #
    # Callbacks
    #
    def on_select_file(self):
        self.filename = filedialog.askopenfilename(
            title="Bitte eine Datei auswählen", filetypes=[("IFC", "*.ifc")]
        )
        self._update_filename_label()
        self.checks_checkbox.pack(padx=20, pady=5)
        self.qto_checkbox.pack(padx=20, pady=5)
        self.run_button.configure(state="normal")

    def on_start_file_processing(self):
        if not self.filename:
            self.show_error("Keine Datei ausgewählt")
            return
        self._update_progress_bar("start")
        self.update_idletasks()  # Force update to show progress bar
        Thread(target=self._run_processing).start()

    def on_checkbox_change(self, checkbox: customtkinter.CTkCheckBox):
        value = checkbox.get()
        checkbox.set("on" if value == "off" else "off")

    def on_closing(self):
        # TODO kill running processing threads
        self.destroy()

    #
    # Helper functions
    #
    def _update_filename_label(self):
        if self.filename:
            if not hasattr(self, "file_label"):  # Create label if it doesn't exist
                self.file_label = customtkinter.CTkLabel(master=self, text="")
                self.file_label.pack()
            self.file_label.configure(text=f"Ausgewählte Datei:\n{self.filename}")
        else:
            if hasattr(self, "file_label"):  # Remove label if filename is cleared
                self.file_label.destroy()
                del self.file_label

    def _update_progress_bar(self, operation: str):
        # check if progress bar is already packed
        if not self.progress_bar.winfo_ismapped():
            self.progress_bar.pack()
        if operation == "start":
            self.progress_bar.start()
        elif operation == "stop":
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

    def _run_processing(self):
        processed_file_path = bbsoft.process(self.filename)
        print(self.checks_var.get(), self.qto_var.get())
        if self.checks_var.get() == "on":
            model_checker.run(processed_file_path)
        if self.qto_var.get() == "on":
            qto.get(processed_file_path)
        self._update_progress_bar("stop")


app = App()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()
