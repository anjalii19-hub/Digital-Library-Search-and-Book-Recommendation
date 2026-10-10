"""Core data model and DSA algorithms for the digital library."""
import json
import re
from collections import defaultdict, deque


def load_books(path):
    """Load book records from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        books = json.load(f)
    return books


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


class Library:
    def __init__(self, books):
        self.books = books
        self.by_id = {b["id"]: b for b in books}
        self.graph = {b["id"]: {} for b in books}
        self._build_graph()

    def _build_graph(self):
        """Connect books sharing a category or keywords; lower cost means closer relation."""
        for i, first in enumerate(self.books):
            for second in self.books[i + 1:]:
                shared_keywords = set(first["keywords"]) & set(second["keywords"])
                same_category = first["category"].casefold() == second["category"].casefold()
                if same_category or shared_keywords:
                    # Explicit, explainable relationship weight (always positive).
                    cost = max(1, 4 - len(shared_keywords) - int(same_category))
                    self.graph[first["id"]][second["id"]] = cost
                    self.graph[second["id"]][first["id"]] = cost

    def search(self, query):
        q = query.casefold().strip()
        if not q:
            return self.books[:]
        return [b for b in self.books
                if q in b["title"].casefold()
                or q in b["author"].casefold()
                or q in b["category"].casefold()
                or any(q in k.casefold() for k in b["keywords"])]

    def categories(self):
        return sorted({b["category"] for b in self.books})

    def by_category(self, category):
        return [b for b in self.books if b["category"].casefold() == category.casefold()]

    def related_bfs(self, start_id):
        if start_id not in self.by_id:
            return []
        visited, order = {start_id}, []
        queue = deque([start_id])
        while queue:
            current = queue.popleft()
            for neighbor in sorted(self.graph[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    order.append(self.by_id[neighbor])
                    queue.append(neighbor)
        return order

    def related_dfs(self, start_id):
        if start_id not in self.by_id:
            return []
        visited, order, stack = {start_id}, [], [start_id]
        while stack:
            current = stack.pop()
            for neighbor in sorted(self.graph[current], reverse=True):
                if neighbor not in visited:
                    visited.add(neighbor)
                    order.append(self.by_id[neighbor])
                    stack.append(neighbor)
        return order

    def dijkstra(self, start_id, end_id):
        """Return (distance, path) using Dijkstra for non-negative edge weights."""
        if start_id not in self.by_id or end_id not in self.by_id:
            return None
        import heapq
        distances = {node: float("inf") for node in self.graph}
        previous = {}
        distances[start_id] = 0
        heap = [(0, start_id)]
        while heap:
            distance, node = heapq.heappop(heap)
            if distance != distances[node]:
                continue
            if node == end_id:
                break
            for neighbor, weight in self.graph[node].items():
                candidate = distance + weight
                if candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    previous[neighbor] = node
                    heapq.heappush(heap, (candidate, neighbor))
        if distances[end_id] == float("inf"):
            return None
        path, node = [], end_id
        while node != start_id:
            path.append(node)
            node = previous[node]
        path.append(start_id)
        return distances[end_id], list(reversed(path))

    def floyd_warshall(self):
        """Return a nested dict of shortest costs between every pair of books."""
        nodes = list(self.graph)
        dist = {u: {v: (0 if u == v else self.graph[u].get(v, float("inf")))
                    for v in nodes} for u in nodes}
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    @staticmethod
    def lcs_length(first, second):
        """LCS length for two token sequences, using O(n*m) time and O(m) space."""
        a, b = tokens(first), tokens(second)
        dp = [0] * (len(b) + 1)
        for x in a:
            previous_diagonal = 0
            for j, y in enumerate(b, start=1):
                old = dp[j]
                if x == y:
                    dp[j] = previous_diagonal + 1
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                previous_diagonal = old
        return dp[-1]

    def compare_titles(self, first_id, second_id):
        if first_id not in self.by_id or second_id not in self.by_id:
            return None
        first, second = self.by_id[first_id], self.by_id[second_id]
        a = " ".join([first["title"]] + first["keywords"])
        b = " ".join([second["title"]] + second["keywords"])
        length = self.lcs_length(a, b)
        denom = max(len(tokens(a)), len(tokens(b)), 1)
        return length, length / denom

    def recommend_knapsack(self, time_limit):
        """Choose a high-utility set of books under a reading-time limit."""
        if time_limit <= 0:
            return []
        # Utility is a transparent demo score: 1 + keyword count + category popularity.
        category_counts = defaultdict(int)
        for b in self.books:
            category_counts[b["category"]] += 1
        candidates = [b for b in self.books if b["reading_time"] <= time_limit]
        weights = [b["reading_time"] for b in candidates]
        values = [1 + len(b["keywords"]) + category_counts[b["category"]] for b in candidates]
        n, cap = len(candidates), time_limit
        dp = [[0] * (cap + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            w, v = weights[i - 1], values[i - 1]
            for c in range(cap + 1):
                dp[i][c] = dp[i - 1][c]
                if w <= c:
                    dp[i][c] = max(dp[i][c], v + dp[i - 1][c - w])
        chosen, c = [], cap
        for i in range(n, 0, -1):
            if dp[i][c] != dp[i - 1][c]:
                chosen.append(candidates[i - 1])
                c -= weights[i - 1]
        return list(reversed(chosen))

    def resource_allocation(self, slots):
        """Use DP to allocate a limited number of slots across categories.

        Each category can contribute 0..min(available books, slots) books.
        The utility of a category's first selected book receives a small diversity
        bonus; later books use their ordinary demo utility. This favors coverage
        while still allowing extra slots to go to useful categories.
        """
        if slots <= 0:
            return []
        groups = defaultdict(list)
        for book in self.books:
            groups[book["category"]].append(book)
        categories = sorted(groups)
        if not categories:
            return []

        # Higher utility is only an illustrative project score, not a quality claim.
        category_counts = {c: len(groups[c]) for c in categories}
        def utility(book):
            return 1 + len(book["keywords"]) + category_counts[book["category"]]

        # dp[i][s] = maximum utility using first i categories and exactly s slots.
        n = len(categories)
        capacity = min(slots, len(self.books))
        dp = [[float("-inf")] * (capacity + 1) for _ in range(n + 1)]
        decisions = [[0] * (capacity + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for i, category in enumerate(categories, start=1):
            books = sorted(groups[category], key=utility, reverse=True)
            values = [utility(b) + (2 if j == 0 else 0) for j, b in enumerate(books)]
            prefix = [0]
            for value in values:
                prefix.append(prefix[-1] + value)
            for used in range(capacity + 1):
                for take in range(min(len(books), used) + 1):
                    prior = dp[i - 1][used - take]
                    if prior == float("-inf"):
                        continue
                    score = prior + prefix[take]
                    if score > dp[i][used]:
                        dp[i][used] = score
                        decisions[i][used] = take

        # Use as many slots as possible up to the number of available books.
        used = capacity
        selected_by_category = {}
        for i in range(n, 0, -1):
            category = categories[i - 1]
            take = decisions[i][used]
            selected_by_category[category] = take
            used -= take

        selected = []
        for category in categories:
            books = sorted(groups[category], key=utility, reverse=True)
            selected.extend(books[:selected_by_category.get(category, 0)])
        return selected
