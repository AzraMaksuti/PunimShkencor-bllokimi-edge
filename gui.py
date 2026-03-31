import tkinter as tk
import customtkinter as ctk
import networkx as nx
import heapq
import math

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")  

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Bus Routing - Graph")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)  
        self.grid_rowconfigure(0, weight=1)

        self.graph = nx.Graph()
        self.blocked_edges = set()
        self.used_edges = set() 

        self.frame = ctk.CTkFrame(self, width=250, height=screen_height)
        self.frame.grid(row=0, column=0, sticky="n")
        self.frame.grid_propagate(False)

        self.label=ctk.CTkLabel(self.frame, text="Routing - Line B1", font=("Verdana", 16))
        self.label.pack(pady=(20, 5))
        self.frame.grid(row=0, column=0)

        self.start = ctk.CTkEntry(self.frame, placeholder_text="Start")
        self.start.pack(pady=5)

        self.end = ctk.CTkEntry(self.frame, placeholder_text="End")
        self.end.pack(pady=5)

        self.find_path_button=ctk.CTkButton(self.frame, text="Find Path", command=self.run_a_star)
        self.find_path_button.pack(padx=10, pady=5)

        self.clear_button=ctk.CTkButton(self.frame, text="Clear", command=self.clear_all)
        self.clear_button.pack(padx=10, pady=5)

        self.line_B_button=ctk.CTkButton(self.frame, text="Line B", command=self.highlight_linja_b)
        self.line_B_button.pack(padx=10, pady=5)

        self.block_entry = ctk.CTkEntry(self.frame, placeholder_text="Edge to block")
        self.block_entry.pack(padx=10, pady=5)

        self.block_edge_button=ctk.CTkButton(self.frame, text="Block Edge", command=self.block_input_edge)
        self.block_edge_button.pack(padx=10, pady=5)

        self.result = ctk.CTkLabel(self.frame, text="Result", wraplength=200,justify="left")
        self.result.pack(padx=10, pady=10)
        self.result.configure(width=200)

        self.legend_box = ctk.CTkTextbox(self.frame, width=220, height=120)
        self.legend_box.pack(padx=10, pady=10)
        self.legend_box.configure(state="normal")

        self.legend_box.insert("0.0", "Blue → Normal edge\n", "blue")
        self.legend_box.insert("end", "Red → Blocked edge\n", "red")
        self.legend_box.insert("end", "Orange → Detour path\n", "orange")
        self.legend_box.insert("end", "Green → Final path\n", "green")

        self.legend_box.tag_config("blue", foreground="blue")
        self.legend_box.tag_config("red", foreground="red")
        self.legend_box.tag_config("orange", foreground="orange")
        self.legend_box.tag_config("green", foreground="green")

        self.legend_box.configure(state="disabled") 
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nsew")

        self.final_path_button=ctk.CTkButton(self.frame, text="Final Path", command=self.final_path)
        self.final_path_button.pack(padx=10, pady=5)

        self.resultPath = ctk.CTkLabel(self.frame, text="Final Path...", wraplength=200,justify="left", text_color="green")
        self.resultPath.pack(padx=10, pady=10)
        self.resultPath.configure(width=200)

        self.linja_b_nodes = ["49", "23", "32", "54", "34", "50", "17", "55", "16","15"]
        self.linja_b_edges = [("49", "23"), ("23", "32"), ("32", "54"), ("54", "34"), ("34", "50"), ("50", "17"), ("17", "55"), ("55", "16")]

        self.create_graph_manual()

        self.update_idletasks()
        canvas_width = self.canvas.winfo_width() or 1000
        canvas_height = self.canvas.winfo_height() or 600

        pos = nx.kamada_kawai_layout(self.graph)

        xs = [x for x, y in pos.values()]
        ys = [y for x, y in pos.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        self.positions = {
            node: (
                int((x - min_x) / (max_x - min_x) * (canvas_width - 40) + 20),
                int((y - min_y) / (max_y - min_y) * (canvas_height - 40) + 20)
            )
            for node, (x, y) in pos.items()
        }
        self.line_b_active = False
        self.selected = []

        self.draw_graph()
        self.canvas.bind("<Button-1>", self.on_click)

    def create_graph_manual(self):
        edges = [
            ("1", "59", 310), ("35", "59", 53), ("35", "2", 120), ("35", "36", 405),
            ("60", "59", 421), ("36", "60", 36), ("2", "38", 420), ("38", "39", 238),
            ("39", "25", 791), ("39", "3", 573), ("3", "4", 1660), ("4", "40", 1220),
            ("40", "41", 1130), ("4", "41", 1080), ("41", "5", 1091), ("5", "57", 1500),
            ("57", "36", 176), ("5", "31", 592), ("31", "56", 1630), ("31", "30", 1580),
            ("30", "28", 336), ("28", "29", 410), ("29", "9", 445), ("9", "10", 2004),
            ("10", "11", 1062), ("10", "12", 554), ("11", "12", 1470), ("13", "14", 1250),
            ("14", "51", 440), ("14", "7", 390), ("1", "26", 276), ("53", "8", 190),
            ("61", "53", 1260), ("42", "53", 170), ("7", "18", 194), ("42", "27", 674),
            ("18", "17", 268), ("17", "50", 139), ("50", "52", 356), ("51", "18", 326),
            ("57", "43", 689), ("60", "6", 264), ("6", "1", 438), ("6", "7", 226),
            ("60", "43", 287), ("13", "15", 1812), ("52", "16", 220), ("16", "15", 1310),
            ("15", "21", 1170), ("21", "20", 1080), ("20", "45", 226), ("20", "44", 228),
            ("44", "45", 145), ("45", "22", 1010), ("44", "19", 1250), ("19", "22", 547),
            ("22", "32", 300), ("19", "34", 300), ("32", "23", 963), ("23", "49", 538),
            ("49", "24", 421), ("34", "54", 762), ("24", "25", 854), ("25", "37", 247),
            ("37", "38", 435), ("37", "26", 208), ("26", "54", 382), ("26", "33", 400),
            ("55", "17", 376), ("17", "33", 210), ("33", "34", 729), ("34", "50", 618),
            ("36", "43", 432), ("43", "61", 258), ("61", "6", 493), ("28", "27", 771),
            ("27", "9", 1060), ("27", "8", 658), ("8", "7", 1570), ("49", "47", 885),
            ("47", "24", 618), ("56", "46", 1370), ("56", "30", 2120), ("2", "39", 520),
            ("24", "54", 1410), ("24", "32", 1530), ("32", "54", 777), ("32", "34", 550),
            ("52", "55", 125), ("8", "58", 1520), ("13", "58", 1570), ("12", "58", 3390),
            ("13", "48", 5570), ("51", "55", 445), ("16", "55", 110)
        ]
        for u, v, w in edges:
            time = w / 332.24 
            self.graph.add_edge(u, v, weight=time)
            self.graph.add_edge(v, u, weight=time)

    
    def draw_graph(self):
        self.node_items = {}
        self.canvas.delete("all")

        for u, v, data in self.graph.edges(data=True):
            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]
            if (u, v) in self.blocked_edges or (v, u) in self.blocked_edges:
                color = "red"  
                width = 3
            else:
                color = "#cccccc"
                width = 1
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

        for node, (x, y) in self.positions.items():
            circle = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="#3498DB")
            self.node_items[circle] = node
            self.canvas.create_text(x, y, text=node, font=("Arial", 14), fill="black")

    def on_click(self, event):
        clicked = self.canvas.find_closest(event.x, event.y)[0]
        if clicked in self.node_items:
            node = self.node_items[clicked]
            self.selected.append(node)
            if len(self.selected) == 2:
                s, e = self.selected
                self.start.delete(0, "end")
                self.start.insert(0, s)
                self.end.delete(0, "end")
                self.end.insert(0, e)
                self.run_a_star()
                self.selected = []

    def a_star(self, start, end, graph=None, blocked_edges=None):
        if graph is None:
            graph = self.graph
        if blocked_edges is None:
            blocked_edges = set()

        def heuristic(u, v):
            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]
            return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

        dist = {node: float('inf') for node in graph.nodes}
        dist[start] = 0
        prev = {node: None for node in graph.nodes}

        pq = [(heuristic(start, end), start)]
        visited = set()

        while pq:
            _, u = heapq.heappop(pq)
            if u == end:
                break
            if u in visited:
                continue
            visited.add(u)

            for v in graph.neighbors(u):
                if (u, v) in blocked_edges or (v, u) in blocked_edges:
                    continue
                w = graph[u][v]['weight']
                tentative = dist[u] + w
                if tentative < dist[v]:
                    dist[v] = tentative
                    prev[v] = u
                    heapq.heappush(pq, (tentative + heuristic(v, end), v))

        path = []
        cur = end
        while cur:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        if path[0] != start:
            return [], float('inf')
        return path, dist[end]

    def run_a_star(self):
        s = self.start.get().strip()
        e = self.end.get().strip()

        self.canvas.delete("path")
        self.canvas.delete("line_b_final")

        if getattr(self, "line_b_active", False):
            path, total_cost = self.compute_line_b_with_detours()

            if not path:
                self.result.configure(text="No valid Line B path!")
                return

            self.canvas.delete("path")

            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                x1, y1 = self.positions[u]
                x2, y2 = self.positions[v]
                self.canvas.create_line(x1, y1, x2, y2, fill="green", width=3, tags="path")
            minutes = int(total_cost)
            seconds = int((total_cost - minutes) * 60)
            self.result.configure(
                text=f"Line B Detour:\n{' -> '.join(path)} Time: {minutes} min {seconds} sec")
            return
        if s == "" or e == "":
            self.result.configure(text="Write start & end nodes!")
            return
        if s not in self.graph or e not in self.graph:
            self.result.configure(text="Invalid nodes")
            return
        path, cost = self.a_star(s, e, blocked_edges=self.blocked_edges)
        self.canvas.delete("path")
        if path:
            self.draw_path(path, color="blue")
            minutes = int(cost)
            seconds = int((cost - minutes) * 60)
            self.result.configure(text=f"{' -> '.join(path)} | Time: {minutes} min {seconds} sec")
        else:
            self.result.configure(text="No path")

    def draw_path(self, path, color="red"):
        for i in range(len(path)-1):
            u, v= path[i], path[i+1]
            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]

            self.used_edges.add((u, v))
            self.used_edges.add((v, u))

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=3, tags="path")

    def clear_all(self):
        self.line_b_active = False
        self.start.delete(0, "end")
        self.end.delete(0, "end")
        self.block_entry.delete(0, "end")
        self.canvas.delete("path")
        self.result.configure(text="")
        self.selected = []
        self.blocked_edges = set()
        self.resultPath.configure(text="")
        self.draw_graph()

    def block_input_edge(self):
        entry = self.block_entry.get().strip()
        if not entry:
            self.result.configure(text="Enter edge to block (e.g., 5 6)")
            return
        try:
            u, v = entry.split()
        except:
            self.result.configure(text="Edge must have two nodes separated by space")
            return
        if not self.graph.has_edge(u, v):
            self.result.configure(text="Edge does not exist")
            return

        self.blocked_edges.add((u, v))
        self.blocked_edges.add((v, u))

        x1, y1 = self.positions[u]
        x2, y2 = self.positions[v]
        self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3, tags="blocked_edge")

        detour_path, detour_cost = self.a_star(u, v, blocked_edges=self.blocked_edges)
        if detour_path and len(detour_path) > 1:
            for i in range(len(detour_path)-1):
                self.used_edges.add((detour_path[i], detour_path[i+1]))
                self.used_edges.add((detour_path[i+1], detour_path[i]))
            self.draw_path(detour_path, color="orange")
            minutes = int(detour_cost)
            seconds = int((detour_cost - minutes) * 60)
            self.result.configure(text=f"Detour from {u} to {v}: {' -> '.join(detour_path)} | Time: {minutes} min {seconds} sec ")
        else:
            self.result.configure(text="No alternative path found for this edge")

    def highlight_linja_b(self):
        self.line_b_active = True 
        self.draw_graph()

        total_time = 0
        counted_edges = set()
        for u, v in self.linja_b_edges:
            if (u, v) not in counted_edges and (v, u) not in counted_edges:
                if self.graph.has_edge(u, v):
                    total_time += self.graph[u][v]['weight']
                    counted_edges.add((u,v))
        for circle, node in self.node_items.items():
            if node in self.linja_b_nodes:
                self.canvas.itemconfig(circle, fill="#3498DB")
            elif any(node in edge for edge in self.blocked_edges):
                self.canvas.itemconfig(circle, fill="#3498DB")
            else:
                self.canvas.itemconfig(circle, fill="#3498DB")
        for u, v in self.linja_b_edges:
            if u in self.positions and v in self.positions:
                x1, y1 = self.positions[u]
                x2, y2 = self.positions[v]
                self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3, tags="linja_b")
        for u, v in self.blocked_edges:
            if u < v: 
                x1, y1 = self.positions[u]
                x2, y2 = self.positions[v]
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3, tags="blocked_edge")

        minutes = int(total_time)
        seconds = int((total_time - minutes) * 60)  
        self.result.configure(text=f"Line B nodes: {' -> '.join(self.linja_b_nodes)} | Total Time: {minutes} min {seconds} sec")

        if hasattr(self, "used_edges"):
            for u, v in self.used_edges:
                if u < v:
                    x1, y1 = self.positions[u]
                    x2, y2 = self.positions[v]
                    self.canvas.create_line(x1, y1, x2, y2, fill="green", width=3, tags="final_path")
                    
        

    def final_path(self):
        self.canvas.delete("final_path")

        if getattr(self, "line_b_active", False):
            total_time = 0
            nodes_in_path = []
            final_edges = set()

            for u, v in self.linja_b_edges:
                if (u, v) in self.blocked_edges or (v, u) in self.blocked_edges:
                    continue
                final_edges.add((u, v))
                total_time += self.graph[u][v]['weight']
                if u not in nodes_in_path:
                    nodes_in_path.append(u)
                if v not in nodes_in_path:
                    nodes_in_path.append(v)

            for u, v in self.used_edges:
                if (u, v) not in final_edges and (v, u) not in final_edges:
                    final_edges.add((u, v))
                    total_time += self.graph[u][v]['weight']
                    if u not in nodes_in_path:
                        nodes_in_path.append(u)
                    if v not in nodes_in_path:
                        nodes_in_path.append(v)

            for u, v in final_edges:
                if u in self.positions and v in self.positions:
                    x1, y1 = self.positions[u]
                    x2, y2 = self.positions[v]
                    self.canvas.create_line(x1, y1, x2, y2, fill="green", width=3, tags="final_path")

            for u, v in self.blocked_edges:
                if u in self.positions and v in self.positions:
                    x1, y1 = self.positions[u]
                    x2, y2 = self.positions[v]
                    self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3, tags="final_path")

            minutes = int(total_time)
            seconds = int((total_time - minutes) * 60)
            self.resultPath.configure(text=f"Line B Final Path + Detours\nTime: {minutes} min {seconds} sec")
            return

        if not hasattr(self, "used_edges") or not self.used_edges:
            self.resultPath.configure(text="No path or detour drawn yet!")
            return

        nodes_in_path = []
        total_time = 0
        final_edges = set()

        for u, v in self.used_edges:
            if (u, v) in self.blocked_edges or (v, u) in self.blocked_edges:
                continue
            final_edges.add((u, v))
            total_time += self.graph[u][v]['weight']
            if u not in nodes_in_path:
                nodes_in_path.append(u)
            if v not in nodes_in_path:
                nodes_in_path.append(v)

    # Vizato final path në green
        for u, v in final_edges:
            if u in self.positions and v in self.positions:
                x1, y1 = self.positions[u]
                x2, y2 = self.positions[v]
                self.canvas.create_line(x1, y1, x2, y2, fill="green", width=3, tags="final_path")
        minutes = int(total_time)
        seconds = int((total_time - minutes) * 60)
        self.resultPath.configure(text=f"Final Path (green):\n{' -> '.join(nodes_in_path)}\nTime: {minutes} min {seconds} sec")
app = App()
app.mainloop()