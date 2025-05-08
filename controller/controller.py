from model.perceptron import Perceptron
from view.ui import PerceptronUI
import os
from tkinter import filedialog as fd

class PerceptronController:
    def __init__(self):
        self.model = Perceptron()
        self.view = PerceptronUI()
        # Callback
        self.view.set_run_callback(self.on_run)
        self.view.set_load_file_callback(self.load_file)

        # Load configuration at the start
        self.load_config("config.txt")

    def load_file(self):
        #Load vectors and weights from a file
        path = fd.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not path:
            return
        try:
            # Clear existing vectors in the UI
            self.view.clear_vectors()

            # Load all non-blank lines
            with open(path) as f:
                lines = [line.strip() for line in f if line.strip()]
            if not lines:
                return

            # Fill vectors in the UI
            for line in lines:
                try:
                    parts = [float(p.strip()) for p in line.split(',') if p.strip()]
                    if not parts:
                        continue
                    self.view.add_vector(parts)
                except ValueError:
                    # Handle the case where conversion to float fails
                    self.view.show_error_popup(f"Invalid format in line: '{line}'")
                    return

        except Exception as e:
            self.view.show_error_popup(f"Failed to load file: {e}")

    def load_config(self, file_path):
        #Load bias and weights from a configuration file.
        if not os.path.exists(file_path):
            self.view.show_error_popup(f"Configuration file '{file_path}' not found.")
            return

        try:
            with open(file_path, "r") as f:
                # Read the first line
                line = f.readline().strip()
                if not line:
                    self.view.show_error_popup("Configuration file is empty.")

                # Split values by commas
                try:
                    parts = [float(value.strip()) for value in line.split(",")]
                except ValueError:
                    # Handle the case where conversion to float fails
                    self.view.show_error_popup("Invalid format in configuration file.")
                    return
                
                # First value is the bias, the rest are weights
                bias = parts[0] 
                weights = parts[1:]

                # Set the model's bias and weights
                self.model.set_bias(bias)
                self.model.set_weights(weights)

                # Update the UI with the loaded values
                self.view.update_bias(bias)
                self.view.update_weights(weights)

        except Exception as e:
            self.view.show_error_popup(f"Failed to load configuration: {e}")

    def on_run(self, bias, vectors, weights, activation_name):
        # Set the perceptron's bias, weights, and activation function
        self.model.set_activation_function(activation_name)
        self.model.set_weights(weights)
        self.model.set_bias(bias)
        # Get predictions
        outputs = self.model.get_output(vectors)
        # Push to the UI
        self.view.show_results(vectors, outputs)

    def run(self):
        self.view.mainloop()