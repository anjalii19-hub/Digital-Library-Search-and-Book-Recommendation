"""Command-line interface for the Digital Library Search and Book Recommendation project."""
from library import Library, load_books

DATA_PATH = "data/books.json"


def print_books(books):
    if not books:
        print("No books found.")
        return
    print("-" * 78)
    for b in books:
        print(f"ID: {b['id']} | {b['title']} — {b['author']}")
        print(f"   Category: {b['category']} | Reading time: {b['reading_time']} min")
        print(f"   Keywords: {', '.join(b['keywords'])}")
    print("-" * 78)


def main():
    library = Library(load_books(DATA_PATH))
    while True:
        print("\n=== DIGITAL LIBRARY ===")
        print("1. Display all books")
        print("2. Search by title or author")
        print("3. Browse by category")
        print("4. Find related books (BFS)")
        print("5. Explore related books (DFS)")
        print("6. Shortest relationship path (Dijkstra)")
        print("7. Recommend within reading-time limit (Knapsack)")
        print("8. Compare two titles (LCS similarity)")
        print("9. Balanced recommendations by category")
        print("10. Show all-pairs shortest paths (Floyd-Warshall)")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Thank you for using the Digital Library!")
            break
        elif choice == "1":
            print_books(library.books)
        elif choice == "2":
            query = input("Enter title/author/keyword: ").strip()
            print_books(library.search(query))
        elif choice == "3":
            print("Categories:", ", ".join(library.categories()))
            category = input("Enter category: ").strip()
            print_books(library.by_category(category))
        elif choice in ("4", "5"):
            book_id = input("Enter a book ID (e.g. B1): ").strip().upper()
            if choice == "4":
                print("BFS related-book discovery:")
                print_books(library.related_bfs(book_id))
            else:
                print("DFS related-book exploration:")
                print_books(library.related_dfs(book_id))
        elif choice == "6":
            start = input("Start book ID: ").strip().upper()
            end = input("Destination book ID: ").strip().upper()
            result = library.dijkstra(start, end)
            if result is None:
                print("No path found (or an invalid book ID was entered).")
            else:
                cost, path = result
                print(f"Path: {' -> '.join(path)} | Relationship cost: {cost}")
        elif choice == "7":
            try:
                limit = int(input("Maximum reading time in minutes: "))
                print_books(library.recommend_knapsack(limit))
            except ValueError:
                print("Please enter a whole number.")
        elif choice == "8":
            a = input("First book ID: ").strip().upper()
            b = input("Second book ID: ").strip().upper()
            result = library.compare_titles(a, b)
            if result is None:
                print("Invalid book ID.")
            else:
                length, score = result
                print(f"LCS token count: {length}; simplified similarity: {score:.1%}")
        elif choice == "9":
            try:
                slots = int(input("Number of recommendation slots: "))
                print_books(library.resource_allocation(slots))
            except ValueError:
                print("Please enter a whole number.")
        elif choice == "10":
            print("All-pairs shortest relationship costs:")
            for source, distances in library.floyd_warshall().items():
                print(source, ":", distances)
        else:
            print("Invalid option. Please choose one of the listed options.")


if __name__ == "__main__":
    main()
