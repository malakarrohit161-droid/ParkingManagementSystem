import tkinter as tk


def main():
    root = tk.Tk()

    root.title("Parking Management System")
    root.geometry("1000x650")
    root.minsize(800, 550)

    title = tk.Label(
        root,
        text="Parking Management System",
        font=("Arial", 26, "bold")
    )
    title.pack(pady=40)

    subtitle = tk.Label(
        root,
        text="TQM-Based Parking Management",
        font=("Arial", 14)
    )
    subtitle.pack()

    root.mainloop()


if __name__ == "__main__":
    main()