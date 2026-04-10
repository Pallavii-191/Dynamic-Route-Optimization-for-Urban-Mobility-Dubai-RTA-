import streamlit as st
import heapq
import math
import time

# --- 1. Graph & Algorithm Logic ---


class RTANetwork:
    def __init__(self):
        self.graph = {}
        self.heuristic_data = {}

    def add_node(self, node, lat, lon):
        self.heuristic_data[node] = (lat, lon)
        if node not in self.graph:
            self.graph[node] = []

    def add_route(self, source, dest, base_time, traffic_multiplier):
        actual_time = base_time * traffic_multiplier
        self.graph[source].append((dest, actual_time))


def calculate_heuristic(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)


def dijkstra(network, start, target):
    min_heap = [(0, start)]
    visited = set()
    distances = {node: float('inf') for node in network.graph}
    distances[start] = 0
    path_tree = {}

    start_time = time.perf_counter()
    while min_heap:
        current_time, current_node = heapq.heappop(min_heap)

        if current_node == target:
            exec_time = time.perf_counter() - start_time
            return current_time, reconstruct_path(path_tree, start, target), exec_time

        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor, travel_time in network.graph.get(current_node, []):
            new_time = current_time + travel_time
            if new_time < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_time
                path_tree[neighbor] = current_node
                heapq.heappush(min_heap, (new_time, neighbor))
    return float('inf'), [], 0


def a_star(network, start, target):
    min_heap = [(0, 0, start)]
    visited = set()
    path_tree = {}

    start_time = time.perf_counter()
    while min_heap:
        f_score, current_time, current_node = heapq.heappop(min_heap)

        if current_node == target:
            exec_time = time.perf_counter() - start_time
            return current_time, reconstruct_path(path_tree, start, target), exec_time

        visited.add(current_node)

        for neighbor, travel_time in network.graph.get(current_node, []):
            if neighbor in visited:
                continue
            new_time = current_time + travel_time
            h_score = calculate_heuristic(
                network.heuristic_data[neighbor], network.heuristic_data[target])
            f_score = new_time + h_score

            if neighbor not in path_tree:  # Simplified for demonstration
                path_tree[neighbor] = current_node
            heapq.heappush(min_heap, (f_score, new_time, neighbor))
    return float('inf'), [], 0


def reconstruct_path(path_tree, start, target):
    path = []
    current = target
    while current in path_tree:
        path.insert(0, current)
        current = path_tree[current]
    path.insert(0, start)
    return path

# --- 2. Initialize Data ---


def build_network(traffic_multiplier):
    net = RTANetwork()
    # Add Nodes (Simulated Lat/Lon)
    nodes = {
        "BurJuman": (25.250, 55.300), "Union": (25.266, 55.315),
        "Al_Rigga": (25.265, 55.325), "ADCB": (25.245, 55.295),
        "Max": (25.235, 55.285), "World_Trade_Ctr": (25.225, 55.280),
        "Emirates_Towers": (25.215, 55.275), "Fin_Centre": (25.205, 55.270),
        "Burj_Khalifa": (25.195, 55.265)
    }
    for name, coords in nodes.items():
        net.add_node(name, coords[0], coords[1])

    # Add Edges (Routes)
    edges = [
        ("BurJuman", "Union", 5.0), ("Union", "Al_Rigga", 3.0),
        ("BurJuman", "ADCB", 4.0), ("ADCB", "Max", 3.5),
        ("Max", "World_Trade_Ctr", 3.0), ("World_Trade_Ctr", "Emirates_Towers", 2.5),
        ("Emirates_Towers", "Fin_Centre", 2.0), ("Fin_Centre", "Burj_Khalifa", 3.5)
    ]
    for src, dst, time_cost in edges:
        net.add_route(src, dst, time_cost, traffic_multiplier)
    return net


# --- 3. Streamlit UI ---
st.set_page_config(page_title="Dubai RTA Optimization", layout="wide")
st.title("🚇 Dynamic Route Optimization for Urban Mobility (Dubai RTA)")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Route Selection")
    start_node = st.selectbox("Select Origin Station", [
                              "BurJuman", "Union", "Al_Rigga", "ADCB", "Max", "World_Trade_Ctr", "Emirates_Towers", "Fin_Centre", "Burj_Khalifa"], index=0)
    end_node = st.selectbox("Select Destination Station", [
                            "BurJuman", "Union", "Al_Rigga", "ADCB", "Max", "World_Trade_Ctr", "Emirates_Towers", "Fin_Centre", "Burj_Khalifa"], index=8)

with col2:
    st.subheader("Network Conditions")
    traffic_level = st.slider("Traffic Congestion Multiplier",
                              min_value=0.5, max_value=3.0, value=1.0, step=0.1)
    if traffic_level > 1.5:
        st.error("Heavy Congestion Detected!")
    elif traffic_level < 1.0:
        st.success("Clear Routes - Faster than normal!")
    else:
        st.info("Normal Traffic Conditions.")

with col3:
    st.subheader("Execution")
    run_algo = st.button("Calculate Optimal Route",
                         type="primary", use_container_width=True)

if run_algo:
    if start_node == end_node:
        st.warning("Origin and Destination cannot be the same.")
    else:
        st.markdown("### Results")
        network = build_network(traffic_level)

        # Run Dijkstra
        d_time, d_path, d_exec = dijkstra(network, start_node, end_node)
        # Run A*
        a_time, a_path, a_exec = a_star(network, start_node, end_node)

        r1, r2 = st.columns(2)
        with r1:
            st.success(f"**Dijkstra's Algorithm**")
            st.write(f"⏱️ **Total Transit Time:** {d_time:.2f} mins")
            st.write(f"⚡ **Execution Speed:** {d_exec:.6f} seconds")
            st.write(f"🛣️ **Path:** {' ➔ '.join(d_path)}")

        with r2:
            st.info(f"**A* Search (Heuristic)**")
            st.write(f"⏱️ **Total Transit Time:** {a_time:.2f} mins")
            st.write(f"⚡ **Execution Speed:** {a_exec:.6f} seconds")
            st.write(f"🛣️ **Path:** {' ➔ '.join(a_path)}")
