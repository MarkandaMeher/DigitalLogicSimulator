// =============================================================
// UnionFind.h — Disjoint Set / Union-Find for Wire Management
// =============================================================
// In a real circuit, multiple wire segments can be physically
// connected to form a single electrical "net". All segments on
// the same net carry the same signal.
//
// Union-Find efficiently answers two questions:
//   1. Are wire A and wire B on the same net?  → find()
//   2. Connect wire A's net to wire B's net    → unite()
//
// With Path Compression + Union by Rank, both operations
// run in O(α(n)) amortized time, where α is the inverse
// Ackermann function — effectively constant for any
// practical input size (α(n) ≤ 4 for n < 10^80).
// =============================================================

#ifndef UNIONFIND_H
#define UNIONFIND_H

#include <vector>
#include <iostream>
#include <numeric>    // for std::iota

class UnionFind {
private:
    // parent[i] = the parent of element i in the forest.
    // If parent[i] == i, then i is a ROOT (representative of its set).
    std::vector<int> parent;

    // rank[i] = an upper bound on the height of the subtree rooted at i.
    // Used to keep the tree balanced during union operations.
    // (NOT the exact height — path compression doesn't update ranks)
    std::vector<int> rank;

    // How many distinct sets (nets) currently exist
    int numSets;

public:
    // ---------------------------------------------------------
    // Constructor: Initialize n elements, each in its own set.
    //
    //   Initially: parent = [0, 1, 2, ..., n-1]
    //              rank   = [0, 0, 0, ..., 0]
    //
    //   Every element is its own root → n distinct sets.
    //
    //   Time: O(n)
    // ---------------------------------------------------------
    explicit UnionFind(int n) : parent(n), rank(n, 0), numSets(n) {
        // Each element starts as its own parent (its own set)
        // iota fills with 0, 1, 2, ..., n-1
        std::iota(parent.begin(), parent.end(), 0);
    }

    // ---------------------------------------------------------
    // find(x): Returns the ROOT (representative) of the set
    //          containing element x.
    //
    //   PATH COMPRESSION: As we walk up the tree to find the
    //   root, we make every node along the path point directly
    //   to the root. This flattens the tree for future queries.
    //
    //   Before find(4):        After find(4):
    //        0                      0
    //        |                    / | \
    //        1                   1  3  4
    //        |
    //        3
    //        |
    //        4
    //
    //   Time: O(α(n)) amortized ≈ O(1) in practice
    // ---------------------------------------------------------
    int find(int x) {
        // Base case: if x is its own parent, it's the root
        if (parent[x] != x) {
            // Recursive call: find the true root
            // PATH COMPRESSION: set parent directly to root
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    // ---------------------------------------------------------
    // unite(x, y): Merge the set containing x with the set
    //              containing y.
    //
    //   UNION BY RANK: Attach the shorter tree under the root
    //   of the taller tree. This keeps the overall tree height
    //   minimal, which speeds up future find() operations.
    //
    //   Returns: true if x and y were in DIFFERENT sets (merged)
    //            false if x and y were ALREADY in the same set
    //
    //   Time: O(α(n)) amortized ≈ O(1) in practice
    // ---------------------------------------------------------
    bool unite(int x, int y) {
        // Step 1: Find the roots of both elements
        int rootX = find(x);
        int rootY = find(y);

        // Step 2: If they share the same root, they're already
        //         on the same net — nothing to do
        if (rootX == rootY) {
            return false;  // Already connected
        }

        // Step 3: UNION BY RANK — attach smaller tree under larger
        if (rank[rootX] < rank[rootY]) {
            // rootX's tree is shorter → attach under rootY
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            // rootY's tree is shorter → attach under rootX
            parent[rootY] = rootX;
        } else {
            // Equal rank → choose one (rootX), increment its rank
            parent[rootY] = rootX;
            rank[rootX]++;
        }

        // One fewer distinct set
        numSets--;
        return true;  // Merge happened
    }

    // ---------------------------------------------------------
    // connected(x, y): Check if x and y are in the same set.
    //
    //   Simply compares their roots.
    //
    //   Time: O(α(n)) amortized
    // ---------------------------------------------------------
    bool connected(int x, int y) {
        return find(x) == find(y);
    }

    // ---------------------------------------------------------
    // getNumSets(): Returns the current number of distinct sets.
    // ---------------------------------------------------------
    int getNumSets() const {
        return numSets;
    }

    // ---------------------------------------------------------
    // printSets(): Debug utility — shows the parent array
    //              and which elements share the same root.
    // ---------------------------------------------------------
    void printSets(int n) const {
        std::cout << "\n--- Union-Find State ---\n";
        std::cout << "Element: ";
        for (int i = 0; i < n; i++) std::cout << i << " ";
        std::cout << "\nParent:  ";
        for (int i = 0; i < n; i++) std::cout << parent[i] << " ";
        std::cout << "\nRank:    ";
        for (int i = 0; i < n; i++) std::cout << rank[i] << " ";
        std::cout << "\nDistinct sets: " << numSets << "\n";
        std::cout << "------------------------\n";
    }
};

#endif // UNIONFIND_H
