# Pymaze Search Algorithm

This repository contains implementations of various search algorithms for solving mazes using the **Pymaze** framework. These algorithms are part of homework assignments for the **Introduction to Artificial Intelligence** course (Spring 2024, SKKU).

## Project Overview

The project is divided into two parts:

- **HW1**: Implements **A* Search** and **Uniform Cost Search** algorithms.
- **HW2**: Implements **Greedy Search** and **Q-Learning** algorithms.

Each implementation is designed to efficiently solve maze traversal problems, leveraging heuristic methods, cost-based strategies, and reinforcement learning techniques.

---

## 📂 Folder Structure

- **`hw1/`**  
  Contains the implementations for:
  - **A* Search**: Combines greedy search and uniform cost search using a heuristic function (Manhattan distance).
  - **Uniform Cost Search**: Finds the least expensive path by evaluating cumulative costs.

- **`hw2/`**  
  Contains the implementations for:
  - **Greedy Search**: Focuses on the heuristic value to find a path quickly, though not necessarily optimally.
  - **Q-Learning**: Uses reinforcement learning techniques to learn the optimal policy for navigating mazes.

---

## 🔑 Features

### HW1: Search Algorithms
1. **Uniform Cost Search (UCS)**:
   - Explores paths based on cumulative costs.
   - Guarantees the shortest path if costs are accurate.

2. **A* Search**:
   - Combines UCS with a heuristic function for better efficiency.
   - Uses Manhattan distance as the heuristic function for estimating cost.

### HW2: Advanced Techniques
1. **Greedy Search**:
   - Focuses on reaching the goal quickly by following the heuristic value.

2. **Q-Learning**:
   - Employs a reinforcement learning algorithm to find the optimal policy.
   - Implements an ε-greedy strategy to balance exploration and exploitation.

---

## 🛠️ Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mjayJeong/Pymaze-Search-Algorithm.git
   cd Pymaze-Search-Algorithm

2. **Install dependencies**:
   ```pip install -r requirements.txt