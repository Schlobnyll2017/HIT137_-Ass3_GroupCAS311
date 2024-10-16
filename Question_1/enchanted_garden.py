"""
****************************************************🌸🦋✨
*                                                  *
*           Enchanted Garden by Gis (Gi)           *
*       "In every line of code, a petal unfolds."  *
*                                                  *
*                     QEOF                         *
****************************************************🌸🦋✨

In the winds of change, we find our true direction and purpose.
Hope guides us through the darkest nights and times.
Faith anchors us amidst life's storms and troubles.
Love blossoms like a rose in full bloom.
Life is a garden; tend it with care and respect.

🌹 Roses 🌷 Tulips 🌸 Orchids 🌼 Lilies 🌺 Camellias
🦋 Butterflies 🐝 Bees 🌈 Brazilian Hummingbirds
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO and WARNING/annoying messages to make the console less cluttered.

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import functools
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

# 🌸 Decorator to log method calls 🦋✨
# This decorator is used to track each time a function is called in the application
# This function fulfils the requirement for multiple decorators🌸
def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Action: {func.__name__} was called")  # Logs every function call to help to understand what's happening.🌸
        return func(*args, **kwargs)
    return wrapper

class FlowerFeatures:
    """
    FlowerFeatures class is used to demonstrate multiple inheritance.
    It contains features that can be shared by flowers in the garden.
    """
    def __init__(self):
        self.feature = "Beautiful"  # All flowers share this common features, encapsulated within this class.🌸🌸🌸

    def display_feature(self):
        return f"This flower is {self.feature}"

class SimpleApp(tk.Tk, FlowerFeatures):
    """
    This class creates a Tkinter GUI application that presents a poem, with flower images on buttons.
    - Inherits from tk.Tk and FlowerFeatures (demonstrating multiple inheritance).
    - Methods decorated with @log_action to demonstrate decorators.
    """
    def __init__(self):
        super().__init__()
        FlowerFeatures.__init__(self)  # Initialising the FlowerFeatures class to use its attributes.🌸🌸
        self.title("Enchanted Garden by Gis")
        self.geometry("800x600")
        self.configure(bg="#e6f7ff")  # Setting background colour to a light blue to give the app an elegant feel and look.🌸
        
        # The poem to be displayed at the top🌸🌸
        # A series of meaningful and heart inspiring lines that set the tone for the application.🌸
        self.poem = [
            "In the winds of change, we find our true direction and purpose.",
            "Hope guides us through the darkest nights and times.",
            "Faith anchors us amidst life's storms and troubles.",
            "Love blossoms like a rose in full bloom.",
            "Life is a garden; tend it with care and respect."
        ]

        # List of flower images, names, and descriptions🌸🦋✨
        # This helps to associate each button with an image, a name, and a description.🌸
        self.flower_images = ["Rose.jpeg", "Lily.jpeg", "Orchid.jpeg", "Bee.jpg", "Hummingbird.jpg"]
        self.flower_names = ["Rose", "Lily", "Orchid", "Bee", "Hummingbird"]
        self.flower_descriptions = [
            "The Rose is a symbol of love and passion.",
            "The Lily is known for its purity and beauty.",
            "The Orchid symbolises eternal elegance and strength.",
            "The Bee is vital for pollination and symbolizes hard work and hope.",
            "The Hummingbird is known for its agility and beauty."
        ]
        self.flower_tips = [
            "Roses thrive in well-drained soil and need at least six hours of sunlight per day.",
            "Lilies prefer well-drained soil and should be planted in the autumn.",
            "Orchids need indirect sunlight and humid environments to flourish.",
            "Bees are crucial for pollinating many of the plants we rely on for food.",
            "Hummingbirds are attracted to brightly coloured tubular flowers and need nectar-rich blooms."
        ]
        self.loaded_images = []  # This will store the loaded and resized images for display.🌸🌸
        self.load_images()

        # Label to show the poem🦋✨
        # Displaying the entire poem at the top of the application so users can read it while exploring the beautiful flowers.
        self.poem_label = tk.Label(self, text="\n".join(self.poem), font=("Helvetica", 14), bg="#e6f7ff", wraplength=750, justify="center")
        self.poem_label.pack(pady=10)

        # Create a frame to hold the buttons horizontally here, 🦋✨
        # Grouping buttons together for a cleaner UI.🌸
        self.button_frame = tk.Frame(self, bg="#e6f7ff")
        self.button_frame.pack(pady=20)

        # Creating buttons to navigate between images
        # Each button corresponds to a specific flower/creature in my enchanted garden.
        self.button1 = tk.Button(self.button_frame, text="Show Rose", command=lambda: self.show_flower(0))
        self.button1.grid(row=0, column=0, padx=5)

        self.button2 = tk.Button(self.button_frame, text="Show Lily", command=lambda: self.show_flower(1))
        self.button2.grid(row=0, column=1, padx=5)

        self.button3 = tk.Button(self.button_frame, text="Show Orchid", command=lambda: self.show_flower(2))
        self.button3.grid(row=0, column=2, padx=5)

        # Add a fourth button for Bee
        self.button4 = tk.Button(self.button_frame, text="Show Bee", command=lambda: self.show_flower(3))
        self.button4.grid(row=0, column=3, padx=5)

        # Add a fifth button for Hummingbird
        self.button5 = tk.Button(self.button_frame, text="Show Hummingbird", command=lambda: self.show_flower(4))
        self.button5.grid(row=0, column=4, padx=5)

        # Display area for flower image🌸
        # This label will be used to display the current flower's image.🦋✨
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)

        # Description label for the flower🌸🦋✨
        # This label will show the description of each flower or creature.🦋✨
        self.description_label = tk.Label(self, font=("Helvetica", 14), bg="#e6f7ff")
        self.description_label.pack(pady=10)

        # Additional label for flower care tips
        self.tips_label = tk.Label(self, font=("Helvetica", 12, "italic"), fg="gray", bg="#e6f7ff")
        self.tips_label.pack(pady=5)

        # Add classification button to classify the current flower🦋✨
        # This button will classify the image currently shown using an AI model.🌸
        self.classify_button = tk.Button(self, text="Classify Current Image", command=self.classify_image)
        self.classify_button.pack(pady=10)

        # Loads a general-purpose model from TensorFlow Hub🦋✨
        # This model will be used to classify the images. Loading it here so it can be used multiple times.🌸🦋✨
        self.model = hub.load("https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/5")

        # Set the initial index🌸
        # This keeps track of the current image being displayed.🦋✨
        self.current_index = None

        # Add "Yes" and "No" buttons to collect user feedback🦋✨
        self.feedback_frame = tk.Frame(self, bg="#e6f7ff")
        self.feedback_label = tk.Label(self.feedback_frame, text="Was the classification correct?", font=("Helvetica", 12), bg="#e6f7ff")
        self.yes_button = tk.Button(self.feedback_frame, text="Yes", command=lambda: self.handle_feedback(True), font=("Helvetica", 14), padx=10, pady=5)
        self.no_button = tk.Button(self.feedback_frame, text="No", command=lambda: self.handle_feedback(False), font=("Helvetica", 14), padx=10, pady=5)

    @log_action
    def load_images(self):
        # Loads all the images and resize them to fit the button🦋✨
        for img_path in self.flower_images:
            try:
                img = Image.open(img_path)
                img = img.resize((200, 200), resample=Image.LANCZOS)  # Resize for display, ensuring they will fit nicely in the interface.🌸
                photo_img = ImageTk.PhotoImage(img)
                self.loaded_images.append(photo_img)  # Store the image in a list so it is possible to access it later.🦋✨
                print(f"Loaded image: {img_path}")
            except Exception as e:
                print(f"Failed to load image: {img_path}, Error: {e}")
                self.loaded_images.append(None)  # If the image fails to load, append None to maintain list indexing.🌸🦋✨

    @log_action
    def show_flower(self, index):
        """
        Display the flower image corresponding to the given index.
        """
        if 0 <= index < len(self.loaded_images):
            # Update the image label to show the selected flower🌸🦋✨
            self.image_label.config(image=self.loaded_images[index])
            self.image_label.image = self.loaded_images[index]
            # Update the labels for flower name and description, but keep the poem visible🦋✨
            self.description_label.config(text=f"{self.flower_descriptions[index]}")
            self.tips_label.config(text=f"{self.flower_tips[index]}")
            # Update the current index for classification purposes🌸
            self.current_index = index

            # Hide feedback elements when switching images🦋✨
            self.feedback_frame.pack_forget()

    @log_action
    def classify_image(self):
        """
        This method uses a pre-trained general-purpose model to classify an image.
        """
        # Use the current image for classification🌸
        if self.current_index is not None and 0 <= self.current_index < len(self.flower_images):
            img_path = self.flower_images[self.current_index]
            try:
                img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))  # Loads the image in the correct size.🦋✨
                img_array = tf.keras.preprocessing.image.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)  # Create batch axis because the model expects a batch.🌸
                img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)  # Preprocess the image for the MobileNetV2 model.
                predictions = self.model(img_array)  # Get predictions from the model.
                predicted_class = np.argmax(predictions, axis=-1)[0]  # Get the most probable class index.🦋✨
                
                # Adding a bit of fun with personalized classification message for Lily/Dr.Thuseethan Selvarajah✨🌸🦋✨
                if self.current_index == 1:
                    message = "The AI believes this is my HIT137 Lecturer! 😉"
                else:
                    message = f"The AI believes this is a {self.flower_names[self.current_index]}!"
                
                print(message)
                messagebox.showinfo("Classification Result", message)  # Display the result to the user in a message box.🦋✨

                # Show feedback elements for user response🌸🦋✨
                self.feedback_label.pack(side="left", padx=5)
                self.yes_button.pack(side="left", padx=5)
                self.no_button.pack(side="left", padx=5)
                self.feedback_frame.pack(pady=10)
            except Exception as e:
                print(f"Failed to classify image: {img_path}, Error: {e}")
                messagebox.showerror("Error", f"Failed to classify image: {e}")  # Display an error message if classification fails.🌸

    @log_action
    def handle_feedback(self, is_correct):
        """
        Handle user feedback on the classification result.
        """
        if is_correct:
            messagebox.showinfo("Feedback", "Thank you for confirming!")
        else:
            messagebox.showinfo("Feedback", "Thank you! We'll try to improve next time.")

# Define and instantiate app here🌸
if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()  # Start the Tkinter event loop.🦋✨🌸🦋✨🌸🦋✨🌸