# Digital Library Search and Book Recommendation

**Course:** Data Structures and Algorithms  
**Project type:** Individual PBL project  
**Language:** Python 3  
**Interface:** Command-line menu  
**Dependencies:** Python standard library only

## Overview

This project is a small educational prototype for searching a book catalogue and recommending books. It uses an example JSON dataset and demonstrates graph algorithms and dynamic programming concepts. It is not a production-scale recommendation engine.

## Features

- Search by title, author, category, or keyword
- Browse books by category
- Graph relationship model using an adjacency list
- BFS and DFS for related-book discovery
- Dijkstra shortest path for non-negative relationship costs
- Floyd–Warshall all-pairs shortest-path calculation
- Longest Common Subsequence (LCS) token comparison for simplified title/keyword similarity
- 0/1 Knapsack to select books within a reading-time limit
- Dynamic-programming category resource allocation for recommendation slots
- Unit tests using Python's built-in `unittest`

## Folder structure

```text
Digital_Library_Search_and_Book_Recommendation/
├── main.py
├── library.py
├── data/
│   └── books.json
├── tests/
│   └── test_library.py
├── docs/
│   └── PROJECT_DOCUMENTATION.md
├── .gitignore
└── README.md
```

## Run in VS Code

1. Install Python 3 if it is not already installed.
2. Open this folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Run:

   ```bash
   python main.py
   ```

   On some Windows systems, use `py main.py`.

5. Follow the menu prompts. Book IDs are shown with the book list.

## Run tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

On some Windows systems, use `py -m unittest discover -s tests -v`.

## Algorithms and expected complexity

Let `V` be the number of books, `E` the number of graph links, `n,m` the lengths of token sequences, and `W` the reading-time capacity.

| Algorithm | Purpose | Typical complexity |
|---|---|---|
| Adjacency list | Store related-book links | O(V + E) storage |
| BFS / DFS | Discover connected related books | O(V + E) |
| Dijkstra with heap | One source to one destination | O((V + E) log V) |
| Floyd–Warshall | All-pairs shortest paths | O(V³) time, O(V²) space |
| LCS | Compare ordered title/keyword tokens | O(nm) time |
| 0/1 Knapsack | Select books under a time capacity | O(NW) time and space in this implementation |
| Resource allocation DP | Allocate slots across categories with a diversity bonus | O(C·S·B) in this implementation (C categories, S slots, B books/category) |

## Dataset and scoring notes

The included records are sample/demo data, not a complete catalogue. Graph links are added when two books share a category or at least one keyword. Edge weights are small positive costs; lower costs indicate a closer relationship under this simplified rule.

For knapsack, reading time is the weight and a transparent demo utility score is used as the value. This score is illustrative and should not be interpreted as a validated measure of book quality or personal preference. LCS is applied to ordered title/keyword tokens as a simplified similarity feature.

## Push to GitHub

If your repository already exists:

1. Open this project folder in VS Code.
2. Use **Source Control** in the left sidebar.
3. If Git is not initialized, choose **Initialize Repository** only if this folder is not already connected to a repository.
4. Stage the files, enter a commit message such as `Add digital library Python project`, and commit.
5. Use **Publish Branch** or **Push** if offered. If this folder is already connected to your intended repository, check the remote before pushing.

Alternatively, use the terminal commands below only after confirming the repository remote is correct:

```bash
git status
git remote -v
```

If no remote is listed, connect your existing GitHub repository using its URL (do not overwrite or force-push an existing repository). GitHub authentication may prompt you to sign in.

## Limitations and future work

- The sample dataset is small and manually curated.
- Recommendations are based on simple, explainable rules rather than user-history learning.
- Reading times and utility values are illustrative.
- The program is a local CLI prototype; it does not currently use a database, web interface, or live external catalogue.
- Future work can include persistent user preferences, CSV/SQLite import, a GUI/web interface, and evaluation with a larger dataset.
