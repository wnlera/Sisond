import random


def file_check_interface(file, mock=True):
    if mock:
        return mock_return()
    return check_file(file)



def mock_return():
    is_wrong = random.random() < 0.4
    res = [1 for x in range(5)]
    if is_wrong:
        for i in range(len(res)):
            if random.random() < 0.5:
                res[i] = 2
    return res

def check_file(file_path):
    with open(file_path, 'r') as file:
        print(file_path)

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    print(file_check_interface(file_path, mock=False))