# Project Documentation
## Digital Library Search and Book Recommendation

### 1. Introduction
A digital library catalogue can become difficult to browse when users do not know the exact title of a book. This project demonstrates a small Python-based system that lets users search a sample catalogue, browse categories, explore related books, and generate reading-time-aware recommendations.

### 2. Objectives
- Search books using title, author, category, and keywords.
- Model related books as a graph.
- Demonstrate BFS, DFS, Dijkstra, and Floyd–Warshall.
- Use LCS to compare ordered title/keyword tokens.
- Apply 0/1 Knapsack to select books under a reading-time limit.
- Demonstrate simple category-wise resource allocation.

### 3. Scope
This is an educational command-line prototype using a local JSON file. It demonstrates algorithms on a small sample dataset. It is not a production-scale or experimentally validated recommender.

### 4. Technology
- Python 3
- JSON for sample catalogue data
- Python standard library (`json`, `re`, `collections`, `heapq`, `unittest`)
- Visual Studio Code can be used as the editor

### 5. System Design
Each book record contains an ID, title, author, category, keyword list, and estimated reading time. The graph uses book IDs as vertices. Two books are linked when they share a category or keyword. The edge weight is a small positive cost based on shared terms/category; lower cost represents a closer relationship in this demo model.

### 6. Algorithms Applied
**Graph / adjacency list:** stores neighboring books without allocating a full matrix for the main graph.

**Breadth-First Search (BFS):** explores graph neighbors level by level to find books connected to the starting book.

**Depth-First Search (DFS):** explores a branch of related-book links before backtracking.

**Dijkstra:** computes a lowest-cost route between two books in the weighted graph. All edge weights are non-negative.

**Floyd–Warshall:** computes shortest costs between all pairs of books. It uses O(V³) time and O(V²) space.

**Longest Common Subsequence (LCS):** compares token sequences formed from titles and keywords. The resulting count is converted to a simplified score by dividing by the longer sequence length. This is only one similarity feature.

**0/1 Knapsack:** reading time is the weight, demo recommendation utility is the value, and the user-provided time limit is the capacity. Each book can be selected at most once. The implementation uses O(NW) time and space.

**Resource allocation DP:** a dynamic-programming table allocates a limited number of recommendation slots among categories. Each category may contribute zero or more books, and the first book from a category receives a small diversity bonus. This is a transparent demo objective, not a validated measure of user preference.

### 7. How to Run
1. Open the project folder in VS Code.
2. Open a terminal in the project root.
3. Run `python main.py` (or `py main.py` on Windows).
4. Choose a menu option and follow the prompts.
5. Run tests using `python -m unittest discover -s tests -v`.

### 8. Testing
The included unit tests cover searching, category browsing, BFS/DFS behavior, Dijkstra path endpoints, Floyd–Warshall diagonal distances, LCS, knapsack capacity, and category allocation. Run the tests locally and record the actual output/screenshots in the final report.

### 9. Expected Outputs
- Search displays matching book records.
- Category browsing lists books in the selected category.
- BFS/DFS returns books reachable from the chosen starting book.
- Dijkstra prints a lowest-cost path when one exists.
- Floyd–Warshall prints a table-like set of all-pairs distances.
- Knapsack recommends a subset whose total reading time does not exceed the selected capacity.
- Category allocation spreads slots across available categories until slots or books run out.

### 10. Limitations
The catalogue is small and illustrative. Reading time and utility scores are estimates. The project does not learn user preferences, connect to a live library, or provide a web interface. Algorithm performance and recommendation quality have not been evaluated on a large real-world dataset.

### 11. Future Enhancements
- Import a larger catalogue from CSV or a database.
- Save user preferences and reading history.
- Add a graphical or web interface.
- Compare the recommendation output against a baseline using a documented evaluation dataset.
- Improve resource allocation using a clearly specified optimization objective.

### 12. Conclusion
The prototype combines searchable catalogue data with graph traversal, shortest-path algorithms, LCS, and knapsack selection. It provides a practical base for demonstrating DSA concepts and can be expanded after testing with more data.
