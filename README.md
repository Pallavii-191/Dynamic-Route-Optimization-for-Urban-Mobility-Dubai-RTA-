# 🚇 Dynamic-Route-Optimization-for-Urban-Mobility-Dubai-RTA-
A Python &amp; Streamlit simulation of the Dubai RTA network. Analyzes Dijkstra, A* Search, and Bellman-Ford algorithms using min-heap priority queues to find optimal transit routes under dynamic traffic conditions. Compares the time/space complexity of AI heuristics vs uniform-cost search in urban mobility.

An interactive, Python-based graph traversal simulation designed to optimize public transit routing under dynamic, real-world traffic conditions. This project models a simplified version of the Dubai RTA network and provides a comparative complexity analysis of three foundational pathfinding algorithms.

Built as a Mini Project for the Design & Analysis of Algorithms (DAA) course.

## 🌟 Key Features

* **Real-Time Traffic Injection:** Simulates dynamic network conditions by applying multiplier "weights" to base travel times (representing congestion or shortcuts).
* **Algorithm Comparison:** Simultaneously runs and compares the execution time of different traversal methods to highlight AI optimization.
* **Interactive UI:** A clean, user-friendly frontend built with Streamlit that allows users to select origins, destinations, and adjust traffic parameters on the fly.
* **Algorithmic Implementations:**
  * **Dijkstra's Algorithm:** Uniform-cost search using Min-Heap Priority Queues.
  * **A* Search:** AI heuristic search utilizing geographical Euclidean distance to aggressively prune unnecessary node exploration.
  * **Bellman-Ford Algorithm:** Evaluates negative weight cycles (paradoxical routing/subsidized shortcuts).

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Frontend/Deployment:** Streamlit
* **Core Libraries:** `heapq`, `math`, `time`

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/pallavi-pawar/Dubai-RTA-Dynamic-Route-Optimization.git](https://github.com/pallavi-pawar/Dubai-RTA-Dynamic-Route-Optimization.git)
   cd Dubai-RTA-Dynamic-Route-Optimization
