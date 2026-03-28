# 🚌 Smart Bus Routing - Graph (Edge Blocking + A\*)

## 📌 Description

This project is an **interactive bus routing system** with edge-level controls, built using:

- `Python`
- `Tkinter / CustomTkinter` (GUI)
- `NetworkX` (graph structure)
- `A* Algorithm` (pathfinding)

It allows users to:

- Select start and end nodes
- Find the shortest path between them
- Block specific **edges** (simulate roadblocks)
- Highlight a predefined bus line (Line B1)
- Visualize detours automatically

---

## ⚙️ Features

- Interactive graph visualization
- A\* shortest path algorithm
- Block specific edges dynamically
- Highlight Line B edges
- Draw detour paths in orange
- Final path visualization in green
- Distance / cost calculation

---

## 🧠 Algorithm Used

The project uses the **A\*** (A-Star) algorithm:

- Combines actual distance + heuristic (Euclidean distance)
- Efficient for shortest path finding even with blocked edges

---

## 🖥️ How to Run

### 1. Install dependencies:

External libraries:

- customtkinter
- networkx

Built-in modules:

- tkinter
- heapq
- math

```bash
pip install customtkinter networkx
```

### 2. Run the program:

```bash
python gui.py
```

---

## 🎮 How to Use

### Option 1: Manual Input

- Enter **Start node**
- Enter **End node**
- Click **Find Path**

### Block an Edge

- Enter the edge to block in the format: Node1 Node2
- Click Block Edge
- Detour path will automatically be calculated (orange edges)

### Highlight Line B

- Click **Line B**
- Nodes and edges will appear in blue

### Fianl Path

- Click Final Path
- All used paths and detours turn green

### Clear All

- Click Clear to reset nodes, paths, and blocked edges

---

## 🎨 Color Legend

🔵 Blue → Normal edges / Line B
🔴 Red → Blocked edges
🟠 Orange → Detour path
🟩 Green → Final path

---

## 📂 Project Structure

```
project/
│
├── Evolver Ferizaj.xlsx
├── gui.py
├── map.jpg
├── README.md
```

---

## 🚀 Future Improvements

- Load graph dynamically from CSV
- Animate bus movement along path
- Support multiple bus lines simultaneously
- Show estimated time along with distance
- Add zoom & pan on the canvas

---

## 👩‍💻 Author

Azra Maksuti

---

## 📜 License

This project is for educational purposes.
