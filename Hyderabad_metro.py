import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import heapq
import matplotlib.pyplot as plt
import networkx as nx

class Passenger:
    def __init__(self, name, age, phone, source_station, destination_station):
        self.name = name
        self.age = age
        self.phone = phone
        self.source_station = source_station
        self.destination_station = destination_station  

class ListNode:
    def __init__(self, passenger):
        self.passenger = passenger
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_passenger(self, passenger):
        new_node = ListNode(passenger)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def find_passenger(self, passenger_name):
        current = self.head
        while current:
            if current.passenger.name == passenger_name:
                return current.passenger
            current = current.next
        return None

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name):
        self.vertices[name] = {}

    def add_edge(self, src, dest, weight):
        self.vertices[src][dest] = weight
        self.vertices[dest][src] = weight

def dijkstra(graph, start):
    distances = {vertex: float('inf') for vertex in graph.vertices}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph.vertices[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

def list_all_stations(graph):
    stations = list(graph.vertices.keys())
    formatted_stations = "\n".join(f"{i + 1}. {station}" for i, station in enumerate(stations))
    return formatted_stations

def show_metro_map(graph):
    lines = ["*" * 60, "        Hyderabad Metro Map", "       ------------------", "-" * 50]

    for station, connections in graph.vertices.items():
        line = f"\n{station} =>"

        for neighbor, weight in connections.items():
            line += f"\n\t{neighbor:<25} {weight}"

        lines.append(line)

    lines.extend(["-" * 50, "-" * 50])
    return "\n".join(lines)

def get_shortest_distance(graph, source, destination):
    source_name = get_station_name(source.upper())
    destination_name = get_station_name(destination.upper())

    if not source_name or not destination_name:
        return "Invalid station code(s). Please enter valid codes."

    distances = dijkstra(graph, source_name)

    if destination_name not in distances:
        return f"No path found from {source_name} to {destination_name}."

    distance = distances[destination_name]
    return f"SHORTEST DISTANCE FROM {source_name} TO {destination_name} IS {distance}KM"

def get_shortest_time(graph, source, destination):
    source_name = get_station_name(source.upper())
    destination_name = get_station_name(destination.upper())

    if not source_name or not destination_name:
        return "Invalid station code(s). Please enter valid codes."

    distances = dijkstra(graph, source_name)

    if destination_name not in distances:
        return f"No path found from {source_name} to {destination_name}."

    shortest_path = get_shortest_path_distance(graph, source_name, destination_name)
    total_time = (len(shortest_path) - 1) * 5
    return f"TIME FROM {source_name} TO {destination_name} IS {total_time} MINUTES"

def get_shortest_path_distance(graph, source, destination):
    distances = dijkstra(graph, source)
    path = [destination]
    current_vertex = destination

    while current_vertex != source:
        for neighbor, weight in graph.vertices[current_vertex].items():
            if distances[current_vertex] == distances[neighbor] + weight:
                path.append(neighbor)
                current_vertex = neighbor

    return path[::-1]

def showpath(graph, source, destination):
    source_name = get_station_name(source.upper())
    destination_name = get_station_name(destination.upper())

    if not source_name or not destination_name:
        return "Invalid station code(s). Please enter valid codes."

    path_distance = get_shortest_path_distance(graph, source_name, destination_name)
    path_stations = path_distance
    path_stations = [station for station in path_stations if station]

    return path_stations

def is_valid_station(graph, input_value, input_type):
    if input_type == "code":
        return get_station_name(input_value) in graph.vertices
    return False
def get_station_name(station_code):
    station_mapping = {
       "CH": "Charminar",
        "PJ": "Panjagutta",
        "MH": "Mehdipatnam",
        "ER": "Erragada",
        "OU": "Osmaina University",
        "JH": "Jubliee Hills",
        "BL": "Balapur",
        "GF": "Golconda Fort",
        "LB": "LB Nagar",
        "MK": "Manikonda",
        "AL": "Alwal",
        "BH": "Banjara Hills",
        "AM": "Ameerpet",
        "SA": "Shamshabad",
        "AT": "Attapur",
        "NA": "Narsingi",
        "FK": "Falaknuma",
        "GW": "Gachibowli",
        "MP": "Madhapur",
        "SR": "Secunderabad",
    }

    return station_mapping.get(station_code, None)

def draw_metro_graph(graph):
    G = nx.Graph()
    for station, connections in graph.vertices.items():
        for neighbor, weight in connections.items():
            G.add_edge(station, neighbor, weight=weight)

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    labels = {k: f"{v}KM" for k, v in labels.items()}
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=8, font_color='black', font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)
    plt.title("Hyderabad Metro Stations")
    plt.show()

def fareCalculator(graph, source, destination):
    source_name = get_station_name(source.upper())
    destination_name = get_station_name(destination.upper())

    if not source_name or not destination_name:
        return "Invalid station code(s). Please enter valid codes."

    path_distance = get_shortest_path_distance(graph, source_name, destination_name)
    num_stations = len(path_distance)

    if num_stations == 0:
        return f"No path found from {source_name} to {destination_name}."

    fare = 20 + (num_stations - 1) * 5
    return f"FARE FROM {source_name} TO {destination_name} IS {fare} RUPEES"


class TicketBookingSystem:
    def __init__(self, total_tickets):
        self.total_tickets = total_tickets
        self.available_tickets = total_tickets
        self.passenger_records = LinkedList()
        self.waitlist = Queue()
        self.passenger_details = {}

    def book_tickets(self, num_tickets, passengers):
        if num_tickets <= self.available_tickets:
            for i in range(num_tickets):
                passenger = passengers[i]
                passenger_name = passenger.name
                self.add_passenger(passenger)
                ticket_number = f"Ticket {i + 1}"
                self.passenger_details[passenger_name] = {
                    'ticket_number': ticket_number,
                    'source_station': passenger.source_station,
                    'destination_station': passenger.destination_station
                }
            self.available_tickets -= num_tickets
            return True, []
        else:
            waiting_list = passengers[self.available_tickets:]
            for i in range(self.available_tickets):
                passenger = passengers[i]
                passenger_name = passenger.name
                self.add_passenger(passenger)
                ticket_number = f"Ticket {i + 1}"
                self.passenger_details[passenger_name] = {
                    'ticket_number': ticket_number,
                    'source_station': passenger.source_station,
                    'destination_station': passenger.destination_station
                }
            self.available_tickets = 0
            self.waitlist.enqueue(waiting_list)
            return False, waiting_list

    def check_ticket_availability(self):
        return self.available_tickets

    def get_passenger_details(self, passenger_name):
        current = self.passenger_records.head
        while current:
            if current.passenger.name == passenger_name:
                passenger_age = current.passenger.age
                passenger_phone = current.passenger.phone
                ticket_details = self.passenger_details.get(passenger_name, {}).get('ticket_number', '')
                return passenger_name, passenger_age, passenger_phone, ticket_details
            current = current.next
        return "Passenger not found"
    def add_passenger(self, passenger):
        new_node = ListNode(passenger)
        if not self.passenger_records.head:
            self.passenger_records.head = new_node
        else:
            current = self.passenger_records.head
            while current.next:
                current = current.next
            current.next = new_node

    def process_waiting_list(self, num_tickets):
        passengers_to_book = []
        for _ in range(num_tickets):
            if not self.waitlist.is_empty():
                passengers_to_book.append(self.waitlist.dequeue())

        if passengers_to_book:
            for passenger in passengers_to_book:
                self.passenger_records.add_passenger(passenger)
            self.available_tickets += num_tickets
            return True, []
        else:
            return False, []

    def add_to_waitlist(self, passenger_names):
        for name in passenger_names:
            passenger = self.passenger_records.find_passenger(name)
            if passenger:
                self.waitlist.enqueue(passenger)
            else:
                print(f"Passenger '{name}' not found in records.")

class TicketBookingPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Ticket Booking", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)
        self.stations_text_widget = tk.Text(self, height=20, width=60) 
        self.stations_text_widget.pack(pady=10)
        self.source_station_entry = ttk.Entry(self, width=20)
        ttk.Label(self, text="Enter Source Station Code:").pack()
        self.source_station_entry.pack(pady=5)

        self.destination_station_entry = ttk.Entry(self, width=20)
        ttk.Label(self, text="Enter Destination Station Code:").pack()
        self.destination_station_entry.pack(pady=5)
        button_book_tickets = ttk.Button(self, text="Book Tickets", command=self.book_tickets)
        button_book_tickets.pack(pady=10)

    def show_stations(self):
        stations = list_all_stations(self.controller.metro_graph)
        self.stations_text_widget.delete(1.0, tk.END)
        self.stations_text_widget.insert(tk.END, stations)

    def book_tickets(self, num_tickets, passengers):
        if num_tickets <= self.available_tickets:
            for i in range(num_tickets):
                passenger = passengers[i]
                passenger_name = passenger.name
                self.passenger_records.add_passenger(passenger)
                self.passenger_details[passenger_name] = f"Ticket {i + 1}"
            self.available_tickets -= num_tickets
            self.controller.ticket_booking_system.passenger_details = self.passenger_details

            return True, []
        else:
            waiting_list = passengers[self.available_tickets:]
            for i in range(self.available_tickets):
                passenger = passengers[i]
                passenger_name = passenger.name
                self.passenger_records.add_passenger(passenger)
                self.passenger_details[passenger_name] = f"Ticket {i + 1}"
            self.available_tickets = 0
            self.waitlist.enqueue(waiting_list)
            self.controller.ticket_booking_system.passenger_details = self.passenger_details

            return False, waiting_list
        
    def add_passenger(self, passenger):
     for i in range(self.total_tickets - self.available_tickets, self.total_tickets):
        passenger_name = passenger.name
        ticket_number = f"Ticket {i + 1}"
        self.passenger_details[passenger_name] = {
            'ticket_number': ticket_number,
            'source_station': passenger.source_station,
            'destination_station': passenger.destination_station
        }

        new_node = ListNode(passenger)
        if not self.passenger_records.head:
            self.passenger_records.head = new_node
        else:
            current = self.passenger_records.head
            while current.next:
                current = current.next
            current.next = new_node



class BookingHistoryPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("Ticket Number", "Passenger Name", "Source Station", "Destination Station", "Fare")

        self.load_booking_history()

        button_show_details = ttk.Button(self, text="Show Details", command=self.show_ticket_details)
        button_show_details.pack(pady=10)

        button_back = ttk.Button(self, text="Back to Home", command=self.go_to_start_page)
        button_back.pack(pady=10)

        self.text_widget = tk.Text(self, height=10, width=50)
        self.text_widget.pack(pady=10)

    def load_booking_history(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        passenger_details = self.controller.ticket_booking_system.passenger_details

        if passenger_details:
            for passenger_name, details in passenger_details.items():
                ticket_number = details.get('ticket_number', '')
                source_station = details.get('source_station', '')
                destination_station = details.get('destination_station', '')
                fare = fareCalculator(self.controller.metro_graph, source_station, destination_station).split()[-2]  # Extract fare from the fareCalculator result
                self.tree.insert("", "end", values=(ticket_number, passenger_name, source_station, destination_station, fare))

            self.tree.pack(pady=10)

    def show_ticket_details(self):
        passenger_details = self.controller.ticket_booking_system.passenger_details

        if passenger_details:
            details_text = ""
            for passenger_name, details in passenger_details.items():
                if isinstance(details, dict):
                    ticket_number = details.get('ticket_number', '')
                    source_station = details.get('source_station', '')
                    destination_station = details.get('destination_station', '')
                    fare = fareCalculator(self.controller.metro_graph, source_station, destination_station).split()[-2] 
                    passenger_name, passenger_age, passenger_phone, _ = self.controller.ticket_booking_system.get_passenger_details(passenger_name)

                    details_text += f"Ticket Number: {ticket_number}\n"
                    details_text += f"Passenger Name: {passenger_name}\n"
                    details_text += f"Age: {passenger_age}\n"
                    details_text += f"Phone Number: {passenger_phone}\n"
                    details_text += f"Source Station: {source_station}\n"
                    details_text += f"Destination Station: {destination_station}\n"
                    details_text += f"Fare: {fare} RUPEES\n\n"
                else:
                    details_text += f"Ticket Number: {details}\n"
                    details_text += f"No additional details available.\n\n"

            if details_text:
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, details_text)
            else:
                messagebox.showinfo("No Tickets", "No tickets to display details.")
        else:
            messagebox.showinfo("No Tickets", "No tickets to display details.")

    def go_to_start_page(self):
        self.controller.show_frame("StartPage")

class SeatAvailabilityPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Seat Availability", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)

        button_check_availability = ttk.Button(self, text="Check Seat Availability", command=self.check_seat_availability)
        button_check_availability.pack(pady=10)

        button_back = ttk.Button(self, text="Back to Home", command=self.go_to_start_page)
        button_back.pack(pady=10)

    def check_seat_availability(self):
        available_tickets = self.controller.ticket_booking_system.check_ticket_availability()
        messagebox.showinfo("Seat Availability", f"Available Seats: {available_tickets}")

    def go_to_start_page(self):
        self.controller.show_frame("StartPage")

class MetroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hyderabad Metro App")
        self.geometry("600x400")

        self.metro_graph = Graph()
        self.create_metro_map()
        self.ticket_booking_system = TicketBookingSystem(total_tickets=200)

        self.frames = {}
        for F in (TicketBookingPage, BookingHistoryPage, SeatAvailabilityPage, StartPage):
            frame = F(self, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.frames["StartPage"].ticket_booking_page = self.frames["TicketBookingPage"]

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def create_metro_map(self):
        self.metro_graph.add_vertex("Balapur")
        self.metro_graph.add_vertex("Attapur")
        self.metro_graph.add_vertex("Mehdipatnam")
        self.metro_graph.add_vertex("Gachibowli")
        self.metro_graph.add_vertex("Golconda Fort")
        self.metro_graph.add_vertex("Madhapur")
        self.metro_graph.add_vertex("Ameerpet")
        self.metro_graph.add_vertex("Erragada")
        self.metro_graph.add_vertex("Shamshabad")
        self.metro_graph.add_vertex("Narsingi")
        self.metro_graph.add_vertex("Alwal")
        self.metro_graph.add_vertex("LB Nagar")
        self.metro_graph.add_vertex("Charminar")
        self.metro_graph.add_vertex("Manikonda")
        self.metro_graph.add_vertex("Falaknuma")
        self.metro_graph.add_vertex("Osmaina University")
        self.metro_graph.add_vertex("Secunderabad")
        self.metro_graph.add_vertex("Jubliee Hills")
        self.metro_graph.add_vertex("Panjagutta")
        self.metro_graph.add_vertex("Banjara Hills")

        self.metro_graph.add_edge("Balapur", "Attapur", 8)
        self.metro_graph.add_edge("Attapur", "Mehdipatnam", 10)
        self.metro_graph.add_edge("Mehdipatnam", "Golconda Fort", 8)
        self.metro_graph.add_edge("Mehdipatnam", "Gachibowli", 6)
        self.metro_graph.add_edge("Gachibowli", "Madhapur", 9)
        self.metro_graph.add_edge("Madhapur", "Ameerpet", 7)
        self.metro_graph.add_edge("Ameerpet", "Erragada", 6)
        self.metro_graph.add_edge("Shamshabad", "Narsingi", 15)
        self.metro_graph.add_edge("Narsingi", "Manikonda", 6)
        self.metro_graph.add_edge("Manikonda", "Gachibowli", 7)
        self.metro_graph.add_edge("Gachibowli", "Charminar", 1)
        self.metro_graph.add_edge("Charminar", "LB Nagar", 2)
        self.metro_graph.add_edge("LB Nagar", "Alwal", 5)
        self.metro_graph.add_edge("Charminar", "Falaknuma", 2)
        self.metro_graph.add_edge("Falaknuma", "Osmaina University", 7)
        self.metro_graph.add_edge("Osmaina University", "Secunderabad", 8)
        self.metro_graph.add_edge("Madhapur", "Jubliee Hills", 2)
        self.metro_graph.add_edge("Banjara Hills", "Jubliee Hills", 2)
        self.metro_graph.add_edge("Banjara Hills", "Panjagutta", 3)

class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.ticket_booking_page = controller.frames["TicketBookingPage"]
        label = ttk.Label(self, text="Welcome to Hyderabad Metro", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)

        options_frame = ttk.Frame(self)
        options_frame.pack()

     
        self.text_widget = tk.Text(options_frame, height=10, width=50)
        self.text_widget.grid(row=0, column=0, columnspan=3, pady=10)

        button_list_stations = ttk.Button(options_frame, text="List all stations", command=lambda: self.show_options("List all stations"))
        button_list_stations.grid(row=1, column=0, padx=10)

        button_nodes_edges = ttk.Button(options_frame, text="Nodes and Edges", command=lambda: self.show_options("Nodes and Edges"))
        button_nodes_edges.grid(row=1, column=1, padx=10)

        button_show_map = ttk.Button(options_frame, text="Show the metro map", command=lambda: self.show_options("Show the metro map"))
        button_show_map.grid(row=1, column=2, padx=10)

        button_ticket_booking = ttk.Button(options_frame, text="Ticket booking", command=lambda: self.show_options("Ticket booking"))
        button_ticket_booking.grid(row=2, column=0, padx=10)

        button_booking_history = ttk.Button(options_frame, text="Recent booking history", command=lambda: self.show_options("Recent booking history"))
        button_booking_history.grid(row=2, column=1, padx=10)


        button_check_availability = ttk.Button(options_frame, text="Check seat availability", command=lambda: self.show_options("Check seat availability"))
        button_check_availability.grid(row=2, column=2, padx=10)

        button_exit = ttk.Button(options_frame, text="Exit", command=self.controller.quit)
        button_exit.grid(row=3, column=1, pady=10)

    def show_options(self, option):
        output = ""  

        if option == "List all stations":
           
            stations = list_all_stations(self.controller.metro_graph)
            
            self.text_widget.delete(1.0, tk.END)
            
            self.text_widget.insert(tk.END, stations)

        elif option == "Nodes and Edges":
            
            nodes_and_edges_info = self.get_nodes_and_edges_info()          
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, nodes_and_edges_info)

        elif option == "Show the metro map":
           
            draw_metro_graph(self.controller.metro_graph)

        elif option == "Ticket booking":
           
            self.ticket_booking_page.show_stations()
            source_station_code = tk.simpledialog.askstring("Source Station", "Enter the CODE OF SOURCE STATION:")
            destination_station_code = tk.simpledialog.askstring("Destination Station", "Enter the CODE OF DESTINATION STATION:")

            output += f"Source Station: {get_station_name(source_station_code)}\n"
            output += f"Destination Station: {get_station_name(destination_station_code)}\n"

            output += get_shortest_distance(self.controller.metro_graph, source_station_code, destination_station_code) + "\n"
            output += get_shortest_time(self.controller.metro_graph, source_station_code, destination_station_code) + "\n"
            output += fareCalculator(self.controller.metro_graph, source_station_code, destination_station_code) + "\n"
            path_nodes = showpath(self.controller.metro_graph, source_station_code, destination_station_code)
            output += f"Path nodes: {' => '.join(path_nodes)}\n"

            confirm_booking = tk.messagebox.askquestion("Confirmation", "Do you want to confirm the booking?")
            if confirm_booking == "yes":
                num_tickets = tk.simpledialog.askinteger("Number of Tickets", "Enter the number of tickets:")
                passengers = []
                for _ in range(num_tickets):
                    name = tk.simpledialog.askstring("Passenger Name", "Enter passenger name:")
                    age = tk.simpledialog.askstring("Passenger Age", "Enter passenger age:")
                    phone = tk.simpledialog.askstring("Passenger Phone", "Enter passenger phone number:")
                    passengers.append(Passenger(name, age, phone, source_station_code, destination_station_code))

                success, waiting_list = self.controller.ticket_booking_system.book_tickets(num_tickets, passengers)
                if success:
                    output += "Tickets booked successfully.\n"
                    output += f"TICKETS ARE SENT TO YOUR GIVEN NUMBER\n"
                else:
                    output += f"Tickets not available. Added to waiting list.\n"

                success, _ = self.controller.ticket_booking_system.process_waiting_list(len(waiting_list))
                if success:
                    output += "Waiting list processed successfully.\n"


            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, output)

        elif option == "Recent booking history":
            self.controller.show_frame("BookingHistoryPage")

        elif option == "Check seat availability":
            self.controller.show_frame("SeatAvailabilityPage")

    def get_nodes_and_edges_info(self):
        nodes_info = "Nodes:\n"
        for station in self.controller.metro_graph.vertices:
            nodes_info += f"- {station}\n"

        edges_info = "\nEdges:\n"
        for station, connections in self.controller.metro_graph.vertices.items():
            for neighbor, weight in connections.items():
                edges_info += f"- {station} to {neighbor} (Weight: {weight}KM)\n"

        return nodes_info + edges_info
    
    def go_to_booking_history(self):
        self.controller.show_frame("BookingHistoryPage")
if __name__ == "__main__":  
    app = MetroApp()
    app.mainloop()
