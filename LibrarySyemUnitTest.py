import unittest
import tkinter as tk
from LibrarySystem import LibraryManagementGUI, Book

class TestLibraryManagementGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.gui = LibraryManagementGUI(self.root)

    def testSearchBooks(self):
        # Insert test books into the libraries inventory to test user interactions
        book1 = Book("Percy Jackson and the Lightning Thief", "Rick Riordan", "06-05-2005", "111")
        book2 = Book("Percy Jackson and the Sea of Monsters", "Rick Riordan", "04-01-2006", "222")
        self.gui.book_inventory.addBook(book1)
        self.gui.book_inventory.addBook(book2)

        # Pretends to be a user searching certain portions of the title or author
        self.gui.searchbytitleentry.insert(0, "Percy Jackson")
        self.gui.SearchByAuthorEntry.insert(0, "Rick Riordan")
        # Pretends the user clicks a button to search for the books
        self.gui.searchBooks()

        # Checks to see if the search list populates and is greater than 0
        self.assertTrue(self.gui.searchList.size() > 0)

    def testBorrowBook(self):
        # Putting in another test book
        book = Book("Percy Jackson and the Lightning Thief", "Rick Riordan", "06-05-2005", "111")
        self.gui.book_inventory.addBook(book)

        #Pretends to be a user putting in a memberid and then searching for a book
        self.gui.memberIdEntry.insert(0, "12345")
        self.gui.searchList.insert(tk.END, "Percy Jackson and the Lightning Thief")
        # Pretends to have the user click to borrow the book
        self.gui.borrowBook()

        # checks to see if the book borrowed shows up in the list of borrowed books
        self.assertIn("Percy Jackson and the Lightning Thief", self.gui.listForBorrowedBooks.get(0, tk.END))


if __name__ == '__main__':
    unittest.main()