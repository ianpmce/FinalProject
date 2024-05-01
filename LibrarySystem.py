##***************************************************************
##* Name : LibrarySystem.py
##* Author: Ian McElderry
##* Created : 4/16/2024
##* Course: CIS 152 - Data Structure
##* Version: 1.0
##* OS: Windows
##* IDE:PyCharm
##* Copyright : This is my own original work
##* based on specifications issued by our instructor
##* Description : An app for creation of a library management system using elements in the required final project submission to create a system in which users can check in and out books and keep an eye on the inventory of the library and update it needed for both member and non membership users.
##*            Input: User input to work with functionality
##*            Ouput: An application resembling that of a checking in and out books from a library
##*            BigO: O(n)
##* I have not used unauthorized source code, either modified or
##* unmodified. I have not given other fellow student(s) access
##* to my program.
##***************************************************************

import tkinter as tk
from tkinter import messagebox


# Node class for linked list instead of binary search tree for keeping track of book objects and borrowed books
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# linked list class created to use for keeping track of the book objects and borrowed books
class LinkedList:
    def __init__(self):
        self.head = None

    def addBook(self, book):
        newNode = Node(book)
        if not self.head:
            self.head = newNode
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = newNode

    def displayBooks(self):
        current = self.head
        while current:
            print(current.data.title)
            current = current.next


# Class created for the GUI or the interface that users will use added buttons for return or borrowing books as well
# as functionality for members Also adds a search function for both author and Book Title I found adding for ISBN or
# Pub date to be a bit much and will instead add a list item to show all books available
class LibraryManagementGUI:
    def __init__(self, root):
        # Library Management Title of Gui
        self.root = root
        self.root.title("Library Management System")

        self.lTitle = tk.Label(root, text="Welcome to the Library!")
        self.lTitle.grid(row=0, column=0, columnspan=2)

        # Search Section of GUi
        self.SearchByTitle = tk.Label(root, text="Search by Title:")
        self.SearchByTitle.grid(row=1, column=0, sticky="e")
        self.searchbytitleentry = tk.Entry(root)
        self.searchbytitleentry.grid(row=1, column=1)

        self.SearchByAuthor = tk.Label(root, text="Search by Author:")
        self.SearchByAuthor.grid(row=2, column=0, sticky="e")
        self.SearchByAuthorEntry = tk.Entry(root)
        self.SearchByAuthorEntry.grid(row=2, column=1)

        self.SearchButton = tk.Button(root, text="Search", command=self.searchBooks)
        self.SearchButton.grid(row=3, column=0, columnspan=2)

        self.showFullLibraryButton = tk.Button(root, text="Show Full Library", command=self.showFullLibrary)
        self.showFullLibraryButton.grid(row=4, column=0, columnspan=2)

        self.searchList = tk.Listbox(root, width=40, height=10)
        self.searchList.grid(row=5, column=0, columnspan=2)

        # Member ID Section of GUI
        self.memberIdLabel = tk.Label(root, text="Member ID:")
        self.memberIdLabel.grid(row=6, column=0, sticky="e")
        self.memberIdEntry = tk.Entry(root)
        self.memberIdEntry.grid(row=6, column=1)

        self.signInButton = tk.Button(root, text="Sign In", command=self.signIn)
        self.signInButton.grid(row=7, column=0, columnspan=2)

        self.signedInLabel = tk.Label(root, text="")
        self.signedInLabel.grid(row=8, column=0, columnspan=2)

        # Borrow and Return Section of GUI
        self.BorrowButton = tk.Button(root, text="Borrow a Book", command=self.borrowBook)
        self.BorrowButton.grid(row=9, column=0, columnspan=2)

        self.ReturnButton = tk.Button(root, text="Return a Book", command=self.returnBook)
        self.ReturnButton.grid(row=10, column=0, columnspan=2)

        self.listForBorrowedBooks = tk.Listbox(root, width=40, height=10)
        self.listForBorrowedBooks.grid(row=11, column=0, columnspan=2)

        # Create an instance of LinkedList to hold the book inventory
        self.book_inventory = LinkedList()

    # Function to sign in user with validation to make sure the user id is submitted correctly
    def signIn(self):
        member_id = self.memberIdEntry.get()
        if member_id:
            self.signedInLabel.config(text=f"Signed in as Member ID: {member_id}")
        else:
            messagebox.showerror("Error:", "Please enter a valid Member ID.")

    # Function created to search for books within the linked list
    def searchBooks(self):
        # Delete any previous search results from user
        self.searchList.delete(0, tk.END)

        # Get the search queries of user searches as well as set it to lower case and strips it for easier searching
        titleQuery = self.searchbytitleentry.get().strip().lower()
        authorQuery = self.SearchByAuthorEntry.get().strip().lower()

        # Search for books matching the queries of the users intended search
        current = self.book_inventory.head
        while current:
            if (titleQuery and titleQuery in current.data.title.lower()) or (
                    authorQuery and authorQuery in current.data.author.lower()):
                # Check if the current books title is not already in the search list
                if current.data.title not in self.searchList.get(0, tk.END):
                    # If the title is not already present add it at the end of the search list
                    self.searchList.insert(tk.END, current.data.title)
            current = current.next

    # Function created to show full library of books offered
    def showFullLibrary(self):
        # Deletes any previous searches from the user
        self.searchList.delete(0, tk.END)

        # Display all books in the library for the user
        current = self.book_inventory.head
        while current:
            self.searchList.insert(tk.END, current.data.title)
            current = current.next

    # grabs the book and member information from the entries of the GUI
    def borrowBook(self):
        # Get the selected book and member ID of the user
        bookTitle = self.searchList.get(tk.ACTIVE)
        memberID = self.memberIdEntry.get()

        # Validate member ID and selected book of user entry
        if not memberID:
            messagebox.showerror("Error:", "Please enter a Member ID.")
            return
        if not bookTitle:
            messagebox.showerror("Error:", "Please select a book to borrow.")
            return

        # Check if the book is available and update its status in the GUI
        current = self.book_inventory.head
        while current:
            if current.data.title == bookTitle:
                if not current.data.checkedOut:
                    current.data.checkedOut = True
                    current.data.checkedOutBy = memberID
                    messagebox.showinfo("Book Borrowed:", f"{bookTitle} has been borrowed.")
                    self.listForBorrowedBooks.insert(tk.END, bookTitle)
                    self.searchList.delete(tk.ACTIVE)
                    break
                else:
                    messagebox.showerror("Error:", "Book is already checked out.")
                    return
            current = current.next

    # Function created to handle the check in for books when users checks in a book back to the system
    def returnBook(self):
        # Get the index of the selected book in the listbox of borrowed books
        index = self.listForBorrowedBooks.curselection()
        if index:
            # Get the title of the book to return
            book_title = self.listForBorrowedBooks.get(index)

            # Find the book in the book inventory linked list
            current = self.book_inventory.head
            prev = None
            while current:
                if current.data.title == book_title:
                    # Set the book's status to checked in
                    current.data.checkedOut = False
                    current.data.checkedOutBy = None

                    # Remove the book from the listbox of borrowed books
                    self.listForBorrowedBooks.delete(index)

                    # Display a message indicating successful check in
                    messagebox.showinfo("Book Returned:", f"{book_title} has been returned successfully.")

                    # Add the book back to the library list of available books for borrowing
                    self.searchList.insert(tk.END, book_title)

                    break
                prev = current
                current = current.next


# Class creation with attributes for title author, publication date and the ISBN of the book also added a checkedout
# attribute and checked out by who for further development to keep track of book inventory
class Book:
    def __init__(self, title, author, pub_date, isbn):
        self.title = title
        self.author = author
        self.pub_date = pub_date
        self.isbn = isbn
        self.checkedOut = False
        self.checkedOutBy = None


# Class creation for Members, so they are able to borrow books with the attribute of their member ID and their name
class Member:
    def __init__(self, memberID, name):
        self.memberID = memberID
        self.name = name


# Class creation to keep track of borrowed books and whether the book borrowed is being checked in our checked out
class BorrowBook:
    def __init__(self, book, member, checkedInorCheckedOut):
        self.book = book
        self.member = member
        self.checkedInorCheckedOut = checkedInorCheckedOut


def main():
    # Create the main Tkinter window
    root = tk.Tk()

    # Create an instance of the LibraryManagementGUI class
    app = LibraryManagementGUI(root)

    # Adding book objects into the library system
    book1 = Book("Percy Jackson and the Lightning Thief", "Rick Riordan", "06-05-2005", "111")
    book2 = Book("Percy Jackson and the Sea of Monsters", "Rick Riordan", "04-01-2006", "222")
    book3 = Book("Percy Jackson and the Titans Curse", "Rick Riordan", "04-07-2007", "333")
    book4 = Book("Percy Jackson and the Battle for the Labrynth", "Rick Riordan", "05-06-2008", "444")
    book5 = Book("Percy Jackson and the Last Olympian", "Rick Riordan", "05-05-2009", "555")
    book6 = Book("The Traitor Baru Cormorant", "Seth Dickinson", "09-15-2015", "666")
    book7 = Book("Cirque Du Freak A living Nightmare", "Darren O'Shaughnessy", "01-01-2000", "777")
    book8 = Book("Cirque Du Freak The Vampires Assistant", "Darren O'Shaughnessy", "05-30-2000", "888")
    book9 = Book("Cirque Du Freak Tunnels of Blood", "Darren O'Shaughnessy", "11-06-2000", "999")
    book10 = Book("Cirque Du Freak Vampire Mountain", "Darren O'Shaughnessy", "01-01-2001", "000")
    app.book_inventory.addBook(book1)
    app.book_inventory.addBook(book2)
    app.book_inventory.addBook(book3)
    app.book_inventory.addBook(book4)
    app.book_inventory.addBook(book5)
    app.book_inventory.addBook(book6)
    app.book_inventory.addBook(book7)
    app.book_inventory.addBook(book8)
    app.book_inventory.addBook(book9)
    app.book_inventory.addBook(book10)
    # Run the Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
