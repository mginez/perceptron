import customtkinter as ctk
from PIL import Image
import tkinter.filedialog as fd

# Initialize appearance
ctk.set_appearance_mode("System")  # Modes: "Light", "Dark", "System"
ctk.set_default_color_theme("view/themes/violet.json")  # Themes: "violet", "cherry"

class PerceptronUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Perceptron Interface")
        self.geometry("525x600")
        self.minsize(525, 600)
        self._run_callback = lambda bias, vectors, weights, activation: None
        self._vector_frames = []
        self._weight_entries = []
        self._build_ui()

    def _build_ui(self):
        # Transparent scrollable frame covering the entire window
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # Title
        ctk.CTkLabel(container, text="Perceptron", font=("Roboto", 24)).pack(pady=(40, 10))

        # Separator
        ctk.CTkFrame(container, height=2, fg_color="#444444").pack(padx=20, pady=10)

        # Activation selector
        select_container = ctk.CTkFrame(container, fg_color="transparent")
        select_container.pack(pady=5)
        ctk.CTkLabel(select_container, text="Activation Function:").pack(side="left", padx=(0, 15))
        self.activation_function = ctk.StringVar(value="sigmoid")
        ctk.CTkOptionMenu(select_container, variable=self.activation_function, values=["sigmoid", "heaviside"]).pack(side="left", padx=(0, 5))
        
        # Bias input frame
        self.bias_frame = ctk.CTkFrame(select_container, fg_color="transparent")
        self.bias_frame.pack(side="left", padx=(0, 5))
        ctk.CTkLabel(self.bias_frame, text="Bias:").pack(side="left", padx=(10, 5))
        self.bias_entry = ctk.CTkEntry(self.bias_frame, placeholder_text="bias", width=50)
        self.bias_entry.pack(side="right", padx=(5, 0))

        # Weights input frame
        self.weight_frame = ctk.CTkFrame(container)
        self.weight_frame.pack(padx=30, pady=10, fill="x")
        ctk.CTkLabel(self.weight_frame, text="Weights:").pack(side="left", padx=(10, 5))
        # Horizontal scrollable frame for weights
        self.weights_scroll_frame = ctk.CTkScrollableFrame(self.weight_frame, orientation="horizontal", width=150, height=40, fg_color="transparent")
        self.weights_scroll_frame.pack(side="left", fill="x", expand=True)
        # Buttons to add/remove weight entries
        w_btn_frame = ctk.CTkFrame(self.weight_frame, fg_color="transparent")
        w_btn_frame.pack(side="right", padx=5)
        ctk.CTkButton(w_btn_frame, text='+', width=25, command=lambda cf=self.weights_scroll_frame: self._add_weight_entry(cf)).pack(side="left")
        ctk.CTkButton(w_btn_frame, text='-', width=25, command=lambda cf=self.weights_scroll_frame: self._remove_weight_entry(cf)).pack(side="left", padx=(5,0))
        
        # Container for all vector panels inside the scrollable frame
        self.vectors_container = ctk.CTkFrame(container)
        self.vectors_container.pack(padx=30, pady=10, fill="x")

        # Initial vector panel
        self._add_vector_panel()

        # Vector controls
        ctrl = ctk.CTkFrame(container, fg_color="transparent")
        ctrl.pack(pady=10)
        ctk.CTkButton(ctrl, text="Add Vector", command=self._add_vector_panel).grid(row=0, column=0, padx=5)
        ctk.CTkButton(ctrl, text="Remove Vector", command=self._remove_vector_panel).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(ctrl, text="or Upload").grid(row=0, column=2, padx=5)
        #Clickable upload image to load vectors from file
        upload_image = ctk.CTkImage(light_image=Image.open("view/images/upload_icon3.png"), size=(20, 20))
        ctk.CTkButton(ctrl, text="", image=upload_image, command=self.load_file, width=20).grid(row=0, column=3, padx=1)
        
        # Separator
        ctk.CTkFrame(container, height=2, fg_color="#444444").pack(padx=20, pady=5)

        # Run button
        ctk.CTkButton(container, text="Run Perceptron", command=self._handle_run).pack(pady=15)

        # Results
        self.result_label = ctk.CTkLabel(container, text="Result will appear here.", wraplength=450, justify="left")
        self.result_label.pack(pady=10)
    
    def set_load_file_callback(self, fn):
        #Callback for loading files
        self._load_file_callback = fn

    def load_file(self):
        #Pass to the controller
        if self._load_file_callback:
            self._load_file_callback()

    def clear_vectors(self):
        #Clear all vector panels.
        for panel, _ in self._vector_frames:
            panel.destroy()
        self._vector_frames.clear()

    def add_vector(self, values):
        #Add a vector panel with given values.
        self._add_vector_panel()
        _, comp_frame = self._vector_frames[-1]
        for child in comp_frame.winfo_children():
            child.destroy()
        for val in values:
            e = ctk.CTkEntry(comp_frame)
            e.pack(side="left", padx=5, pady=5)
            e.insert(0, val)

    def update_bias(self, bias):
        #Update the bias entry in the UI.
        self.bias_entry.delete(0, "end")
        self.bias_entry.insert(0, str(bias))

    def update_weights(self, weights):
        #Update the weight entries in the UI.
        for entry in self._weight_entries:
            entry.destroy()
        self._weight_entries.clear()
        for weight in weights:
            self._add_weight_entry(self.weights_scroll_frame)
            self._weight_entries[-1].insert(0, str(weight))

    def set_load_file_callback(self, fn):
        #Callback for loading files.
        self._load_file_callback = fn
    
    def load_file(self):
        #Pass file loading to the controller.
        if self._load_file_callback:
            self._load_file_callback()

    def _add_weight_entry(self, weight_frame):
        # Add a new weight entry to the scrollable frame
        entry = ctk.CTkEntry(weight_frame, placeholder_text="weight")
        entry.pack(side="left", padx=5, pady=5)
        self._weight_entries.append(entry)

    def _remove_weight_entry(self, weight_frame):
        # Remove the last weight entry from the scrollable frame
        if self._weight_entries:
            entry = self._weight_entries.pop()
            entry.destroy()

    def _add_vector_panel(self):
        # Create a new vector panel with components
        idx = len(self._vector_frames) + 1
        panel = ctk.CTkFrame(self.vectors_container)
        panel.pack(fill="x", pady=5, padx=5)

        # Label for vector index
        ctk.CTkLabel(panel, text=f"v{idx}:").pack(side="left", padx=(25,20))

        # Horizontal scrollable frame for components
        comp_frame = ctk.CTkScrollableFrame(panel, orientation="horizontal", width=200, height=40, fg_color="transparent")
        comp_frame.pack(side="left", fill="x", expand=True)

        # Initial component entry (2 by default)
        self._add_component(comp_frame)
        self._add_component(comp_frame)

        # Buttons to add/remove components
        btn_frame = ctk.CTkFrame(panel, fg_color="transparent")
        btn_frame.pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text='+', width=25, command=lambda cf=comp_frame: self._add_component(cf)).pack(side="left")
        ctk.CTkButton(btn_frame, text='-', width=25, command=lambda cf=comp_frame: self._remove_component(cf)).pack(side="left", padx=(5,0))

        self._vector_frames.append((panel, comp_frame))

    def _remove_vector_panel(self):
        # Remove the last vector panel
        if not self._vector_frames:
            return
        panel, _ = self._vector_frames.pop()
        panel.destroy()

    def _add_component(self, comp_frame):
        # Add a new component entry to the vector panel
        entry = ctk.CTkEntry(comp_frame, placeholder_text="component")
        entry.pack(side="left", padx=5, pady=5)

    def _remove_component(self, comp_frame):
        # Remove the last component entry from the vector panel
        children = comp_frame.winfo_children()
        if children:
            children[-1].destroy()

    def show_error_popup(self, message):
        #Display a CTkToplevel window with an error message.
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x250")
        error_window.resizable(False, False)

        # Vincular la ventana de error a la ventana principal
        error_window.transient(self)

        # Error message
        ctk.CTkLabel(error_window, text="An Error Occurred", font=("Roboto", 18)).pack(pady=(20, 10))
        ctk.CTkLabel(error_window, text=message, wraplength=250, justify="center").pack(pady=(0, 20))

        # Close button
        ctk.CTkButton(error_window, text="Close", command=error_window.destroy).pack(pady=10)

    
    def set_run_callback(self, fn):
        #Callback for running the perceptron.
        self._run_callback = fn

    def _handle_run(self):
        # Collect data from the UI and validate it to then run the perceptron.
        vectors = [] # List of vectors
        weights = [] # List of weights
        bias = 0
        invalid_entry = False

        # Collect vector components and weights
        # Iterate through each vector frame and collect entries
        for _, comp_frame in self._vector_frames:
            vals = []
            for entry in comp_frame.winfo_children():
                try:
                    vals.append(float(entry.get()))
                except:
                    pass
                    invalid_entry = True
                
            if vals:
                vectors.append(vals)
        for entry in self._weight_entries:
            try:
                weights.append(float(entry.get()))
            except:
                pass
                invalid_entry = True

        # Validate bias entry 
        try:
            bias = float(self.bias_entry.get())
        except:
            pass
            invalid_entry = True

        # Raise window for data validation
        if invalid_entry:
            self.show_error_popup(f"Invalid input.")
            return
        # Validate number of weights matches number of vector components
        for vector in vectors:
            if len(weights) != len(vector):
                self.show_error_popup(
                    f"Mismatch: Number of weights ({len(weights)}) must match the number of components in each vector ({len(vector)})."
                )
                return

        self._run_callback(bias, vectors, weights, self.activation_function.get())

    def show_results(self, vectors, results):
        # Display the results in the result label
        lines = [f"{v} → {r:.3f}" for v, r in zip(vectors, results)]
        self.result_label.configure(text="\n".join(lines))

if __name__ == "__main__":
    ui = PerceptronUI()
    ui.mainloop()
