import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Global list to store reviews (in-memory)
reviews = []

# Initialize the Tkinter window
window = tk.Tk()
window.title("Book Review System")
window.geometry("800x700")  # Set a reasonable window size

# Create a canvas widget for the background
canvas = tk.Canvas(window)
canvas.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas
content_frame = tk.Frame(canvas, bg="#f4f4f9")
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# --- Functions ---

# Update dropdown for selecting a review
def update_review_dropdown():
    menu = dropdown_reviews['menu']
    menu.delete(0, 'end')
    for i, rev in enumerate(reviews):
        display_text = rev['review'][:30].strip().replace('\n', ' ')
        menu.add_command(label=f"{i + 1}: {display_text}", command=lambda i=i: selected_review_index.set(i))

# Search book function
def search_books():
    search_query = entry_search.get()
    if not search_query:
        messagebox.showerror("Error", "Please enter a book title or author.")
        return

    url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["totalItems"] == 0:
            messagebox.showinfo("No Results", "No books found matching that query.")
            return
        
        book_info = data["items"][0]["volumeInfo"]
        title = book_info.get("title", "No title available")
        author = ', '.join(book_info.get("authors", ["No author available"]))
        image_url = book_info.get("imageLinks", {}).get("thumbnail", None)

        label_title.config(text=title)
        label_author.config(text=f"By: {author}")
        
        if image_url:
            img_response = requests.get(image_url)
            img_data = img_response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((150, 200))
            img_tk = ImageTk.PhotoImage(img)
            label_image.config(image=img_tk)
            label_image.image = img_tk
        else:
            label_image.config(image='')

        entry_review.delete(1.0, tk.END)
    else:
        messagebox.showerror("Error", "Failed to fetch book details. Try again later.")

# Submit review function
def submit_review():
    review = entry_review.get("1.0", tk.END).strip()
    rating = scale_rating.get()
    
    if not review:
        messagebox.showerror("Error", "Please write a review.")
        return

    reviews.append({'review': review, 'rating': rating})
    messagebox.showinfo("Review Submitted", f"Thank you for your review!\nRating: {rating}\nReview: {review}")

    entry_review.delete(1.0, tk.END)
    update_review_dropdown()
    canvas.config(scrollregion=canvas.bbox("all"))

# View reviews in a new window
def view_reviews():
    if not reviews:
        messagebox.showinfo("No Reviews", "No reviews available.")
        return

    reviews_window = tk.Toplevel(window)
    reviews_window.title("Book Reviews")
    reviews_window.geometry("500x400")
    reviews_window.configure(bg="#f4f4f9")
    
    tk.Label(reviews_window, text="Reviews", font=("Helvetica", 16, "bold"), bg="#f4f4f9", fg="#333").pack(pady=5)
    
    for index, review in enumerate(reviews):
        review_frame = tk.Frame(reviews_window, bg="#ffffff", padx=5, pady=5)
        review_frame.pack(fill="x", pady=3, padx=5)
        tk.Label(review_frame, text=f"Review {index + 1}: {review['review']}", font=("Arial", 12), bg="#ffffff", wraplength=450).pack(pady=5)
        tk.Label(review_frame, text=f"Rating: {review['rating']}", font=("Arial", 10), bg="#ffffff").pack(pady=2)

# Delete selected review
def delete_review():
    index = selected_review_index.get()
    if 0 <= index < len(reviews):
        deleted = reviews.pop(index)
        messagebox.showinfo("Review Deleted", f"Deleted review:\n{deleted['review']}")
        update_review_dropdown()
        entry_review.delete(1.0, tk.END)
    else:
        messagebox.showerror("Error", "Invalid review selection.")

# Edit selected review
def edit_review():
    index = selected_review_index.get()
    new_review_text = entry_review.get("1.0", tk.END).strip()
    if 0 <= index < len(reviews):
        reviews[index]['review'] = new_review_text
        reviews[index]['rating'] = scale_rating.get()
        messagebox.showinfo("Review Edited", "The review has been updated.")
        update_review_dropdown()
    else:
        messagebox.showerror("Error", "Invalid review selection.")

# --- GUI Elements ---

# Title Frame
title_frame = tk.Frame(content_frame, bg="#4CAF50", pady=20)
title_frame.pack(fill="x")
tk.Label(title_frame, text="Book Review System", font=("Arial", 24, "bold"), fg="white", bg="#4CAF50").pack()

# Search Section
search_frame = tk.Frame(content_frame, bg="#f4f4f9", pady=10)
search_frame.pack(fill="x", padx=30)
tk.Label(search_frame, text="Search for a Book:", font=("Helvetica", 14), bg="#f4f4f9").pack(pady=10)
entry_search = tk.Entry(search_frame, font=("Arial", 12), width=30, bd=2, relief="solid")
entry_search.pack(pady=5)
tk.Button(search_frame, text="Search", command=search_books, font=("Arial", 12), bg="#4CAF50", fg="white", width=20).pack(pady=10)

# Book Title and Image Section
details_frame = tk.Frame(content_frame, bg="#f4f4f9", pady=10)
details_frame.pack()
label_title = tk.Label(details_frame, text="", font=("Arial", 14, "bold"), bg="#f4f4f9", fg="#333")
label_title.pack()
label_author = tk.Label(details_frame, text="", font=("Arial", 12), bg="#f4f4f9", fg="#555")
label_author.pack(pady=5)
label_image = tk.Label(details_frame, bg="#f4f4f9")
label_image.pack(pady=10)

# Review Section
review_frame = tk.Frame(content_frame, bg="#f4f4f9", pady=20)
review_frame.pack(fill="x")
tk.Label(review_frame, text="Add your review:", font=("Arial", 12), bg="#f4f4f9", fg="#333").pack(pady=10)
entry_review = tk.Text(review_frame, width=40, height=5, font=("Arial", 12), bd=2, relief="solid")
entry_review.pack(pady=5)
scale_rating = tk.Scale(review_frame, from_=1, to=5, orient="horizontal", label="Rating (1-5)", bg="#f4f4f9", fg="#333")
scale_rating.pack(pady=5)
tk.Button(review_frame, text="Submit Review", command=submit_review, bg="#4CAF50", fg="white", width=20, height=2, font=("Arial", 12)).pack(pady=10)

# Dropdown to select review
selected_review_index = tk.IntVar(value=0)
dropdown_reviews = tk.OptionMenu(review_frame, selected_review_index, "")
dropdown_reviews.config(width=50)
dropdown_reviews.pack(pady=5)

# Buttons
button_frame = tk.Frame(content_frame, bg="#f4f4f9", pady=20)
button_frame.pack(fill="x", padx=30)
tk.Button(button_frame, text="View Reviews", command=view_reviews, bg="#2196F3", fg="white", width=20, height=2, font=("Arial", 12)).pack(side="left", padx=10)
tk.Button(button_frame, text="Edit Review", command=edit_review, bg="#FF9800", fg="white", width=20, height=2, font=("Arial", 12)).pack(side="left", padx=10)
tk.Button(button_frame, text="Delete Review", command=delete_review, bg="#F44336", fg="white", width=20, height=2, font=("Arial", 12)).pack(side="left", padx=10)

# Scroll region update
content_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Start main loop
window.mainloop()