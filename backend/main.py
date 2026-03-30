from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import math
import heapq
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("navisphere")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

frontend_dist = os.path.join(os.path.dirname(__file__), "../frontend/dist")

app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_dist, "index.html"))

class NavigationRequest(BaseModel):
    station_name: str
    start: str
    destination: str

# Node Alias Mapping: translates common frontend display names to exact backend node names.
# Only add an alias if the frontend name DIFFERS from the backend node name.
# NOTE: Secunderabad nodes have been renamed to match frontend – no aliases needed.
NODE_ALIASES = {}

# Mirroring the frontend coordinates and adding logical graph edges
STATION_GRAPHS = {
    "Secunderabad Junction": {
        "nodes": [
            { "name": "Platform 1", "x": 45, "y": 38, "category": "Platform" },
            { "name": "Platform 2/3", "x": 45, "y": 47, "category": "Platform" },
            { "name": "Platform 4/5", "x": 45, "y": 55, "category": "Platform" },
            { "name": "Platform 6/7", "x": 45, "y": 64, "category": "Platform" },
            { "name": "Platform 8/9", "x": 45, "y": 73, "category": "Platform" },
            { "name": "Platform 10", "x": 45, "y": 81, "category": "Platform" },
            { "name": "Main Entrance", "x": 23, "y": 88, "category": "Exit" },
            { "name": "Main Entrance (Ganesh Temple)", "x": 50, "y": 15, "category": "Exit" },
            { "name": "FOB 1 (Foot Over Bridge)", "x": 25, "y": 56, "category": "Bridge" },
            { "name": "FOB 2 (Foot Over Bridge)", "x": 54, "y": 56, "category": "Bridge" },
            
            # Additional Granular Facilities matching Blueprint
            { "name": "Ticket Counter", "x": 30, "y": 88, "category": "Utility" },
            { "name": "Parcel Office", "x": 18, "y": 88, "category": "Utility" },
            { "name": "Waiting Room (PF 10)", "x": 42, "y": 81, "category": "Utility" },
            { "name": "Escalator (PF 10)", "x": 65, "y": 81, "category": "Stairs" },
            { "name": "Toilet (PF 8/9)", "x": 60, "y": 73, "category": "Utility" },
            { "name": "Book Stall (PF 6/7)", "x": 35, "y": 64, "category": "Food" },
            { "name": "Waiting Room (PF 4/5)", "x": 40, "y": 55, "category": "Utility" },
            { "name": "Toilet (PF 2/3)", "x": 35, "y": 47, "category": "Utility" },
            { "name": "Food Plaza (PF 2/3)", "x": 60, "y": 47, "category": "Food" },
            { "name": "KFC Stall (PF 1)", "x": 38, "y": 38, "category": "Food" },
            { "name": "IRCTC Lounge (PF 1)", "x": 32, "y": 38, "category": "Utility" },
            { "name": "Cloak Room (PF 1)", "x": 58, "y": 38, "category": "Utility" },
            { "name": "Helpline/Enquiry", "x": 40, "y": 15, "category": "Utility" },
            { "name": "Auto Stand (Ganesh Temple)", "x": 60, "y": 15, "category": "Exit" },

            # Right-Side Facilities (FOB 3)
            { "name": "FOB 3 (Foot Over Bridge)", "x": 82, "y": 56, "category": "Bridge" },
            { "name": "Stairs (PF 10, FOB 3)", "x": 82, "y": 81, "category": "Stairs" },
            { "name": "Escalator (PF 8/9, FOB 3)", "x": 82, "y": 73, "category": "Stairs" },
            { "name": "Toilet (PF 6/7)", "x": 82, "y": 64, "category": "Utility" },
            { "name": "Stairs (PF 6/7, FOB 3)", "x": 82, "y": 64, "category": "Stairs" },
            { "name": "Stairs (PF 4/5, FOB 3)", "x": 82, "y": 55, "category": "Stairs" },
            { "name": "Stairs (PF 2/3, FOB 3)", "x": 82, "y": 47, "category": "Stairs" },
            { "name": "Retiring Room (PF 1)", "x": 82, "y": 38, "category": "Utility" },
            { "name": "General Ticket Booking", "x": 82, "y": 15, "category": "Utility" },

            # Invisible Waypoints (must match frontend exact names)
            { "name": "WP_PF10_Stairs_FOB1", "x": 25, "y": 81, "category": "Waypoint" },
            { "name": "WP_PF89_Stairs_FOB1", "x": 25, "y": 73, "category": "Waypoint" },
            { "name": "WP_PF67_Stairs_FOB1", "x": 25, "y": 64, "category": "Waypoint" },
            { "name": "WP_PF45_Stairs_FOB1", "x": 25, "y": 55, "category": "Waypoint" },
            { "name": "WP_PF23_Stairs_FOB1", "x": 25, "y": 47, "category": "Waypoint" },
            { "name": "WP_PF1_Stairs_FOB1", "x": 25, "y": 38, "category": "Waypoint" },

            { "name": "WP_PF10_Stairs_FOB2", "x": 54, "y": 81, "category": "Waypoint" },
            { "name": "WP_PF89_Stairs_FOB2", "x": 54, "y": 73, "category": "Waypoint" },
            { "name": "WP_PF67_Stairs_FOB2", "x": 54, "y": 64, "category": "Waypoint" },
            { "name": "WP_PF45_Stairs_FOB2", "x": 54, "y": 55, "category": "Waypoint" },
            { "name": "WP_PF23_Stairs_FOB2", "x": 54, "y": 47, "category": "Waypoint" },
            { "name": "WP_PF1_Stairs_FOB2", "x": 54, "y": 38, "category": "Waypoint" },

            { "name": "WP_PF10_Stairs_FOB3", "x": 82, "y": 81, "category": "Waypoint" },
            { "name": "WP_PF89_Stairs_FOB3", "x": 82, "y": 73, "category": "Waypoint" },
            { "name": "WP_PF67_Stairs_FOB3", "x": 82, "y": 64, "category": "Waypoint" },
            { "name": "WP_PF45_Stairs_FOB3", "x": 82, "y": 55, "category": "Waypoint" },
            { "name": "WP_PF23_Stairs_FOB3", "x": 82, "y": 47, "category": "Waypoint" },
            { "name": "WP_PF1_Stairs_FOB3", "x": 82, "y": 38, "category": "Waypoint" },

            { "name": "WP_Ganesh_Corridor", "x": 54, "y": 15, "category": "Waypoint" },
            { "name": "WP_Right_Corridor", "x": 82, "y": 15, "category": "Waypoint" }
        ],
        "edges": [
            # Bhoiguda Side
            {"start": "Main Entrance",   "end": "Ticket Counter"},
            {"start": "Main Entrance",   "end": "Parcel Office"},
            {"start": "Ticket Counter",  "end": "WP_PF10_Stairs_FOB1"},
            
            # FOB 1 Main Spine
            {"start": "WP_PF10_Stairs_FOB1", "end": "WP_PF89_Stairs_FOB1"},
            {"start": "WP_PF89_Stairs_FOB1", "end": "WP_PF67_Stairs_FOB1"},
            {"start": "WP_PF67_Stairs_FOB1", "end": "FOB 1 (Foot Over Bridge)"},
            {"start": "FOB 1 (Foot Over Bridge)", "end": "WP_PF45_Stairs_FOB1"},
            {"start": "WP_PF45_Stairs_FOB1", "end": "WP_PF23_Stairs_FOB1"},
            {"start": "WP_PF23_Stairs_FOB1", "end": "WP_PF1_Stairs_FOB1"},

            # FOB 2 Main Spine
            {"start": "WP_PF10_Stairs_FOB2", "end": "WP_PF89_Stairs_FOB2"},
            {"start": "WP_PF89_Stairs_FOB2", "end": "WP_PF67_Stairs_FOB2"},
            {"start": "WP_PF67_Stairs_FOB2", "end": "FOB 2 (Foot Over Bridge)"},
            {"start": "FOB 2 (Foot Over Bridge)", "end": "WP_PF45_Stairs_FOB2"},
            {"start": "WP_PF45_Stairs_FOB2", "end": "WP_PF23_Stairs_FOB2"},
            {"start": "WP_PF23_Stairs_FOB2", "end": "WP_PF1_Stairs_FOB2"},

            # FOB 3 Main Spine
            {"start": "WP_PF10_Stairs_FOB3", "end": "WP_PF89_Stairs_FOB3"},
            {"start": "WP_PF89_Stairs_FOB3", "end": "WP_PF67_Stairs_FOB3"},
            {"start": "WP_PF67_Stairs_FOB3", "end": "FOB 3 (Foot Over Bridge)"},
            {"start": "FOB 3 (Foot Over Bridge)", "end": "WP_PF45_Stairs_FOB3"},
            {"start": "WP_PF45_Stairs_FOB3", "end": "WP_PF23_Stairs_FOB3"},
            {"start": "WP_PF23_Stairs_FOB3", "end": "WP_PF1_Stairs_FOB3"},

            # Bridges Connecting Horizontally
            {"start": "FOB 1 (Foot Over Bridge)", "end": "FOB 2 (Foot Over Bridge)"},
            {"start": "FOB 2 (Foot Over Bridge)", "end": "FOB 3 (Foot Over Bridge)"},

            # --- PF 10 LEVEL (y=81) Strict Contiguous Horizontal Routing ---
            {"start": "WP_PF10_Stairs_FOB1", "end": "Waiting Room (PF 10)"},
            {"start": "Waiting Room (PF 10)", "end": "Platform 10"},
            {"start": "Platform 10", "end": "WP_PF10_Stairs_FOB2"},
            {"start": "WP_PF10_Stairs_FOB2", "end": "Escalator (PF 10)"},
            {"start": "Escalator (PF 10)", "end": "WP_PF10_Stairs_FOB3"},
            {"start": "WP_PF10_Stairs_FOB3", "end": "Stairs (PF 10, FOB 3)"},

            # --- PF 8/9 LEVEL (y=73) ---
            {"start": "WP_PF89_Stairs_FOB1", "end": "Platform 8/9"},
            {"start": "Platform 8/9", "end": "WP_PF89_Stairs_FOB2"},
            {"start": "WP_PF89_Stairs_FOB2", "end": "Toilet (PF 8/9)"},
            {"start": "Toilet (PF 8/9)", "end": "WP_PF89_Stairs_FOB3"},
            {"start": "WP_PF89_Stairs_FOB3", "end": "Escalator (PF 8/9, FOB 3)"},

            # --- PF 6/7 LEVEL (y=64) ---
            {"start": "WP_PF67_Stairs_FOB1", "end": "Book Stall (PF 6/7)"},
            {"start": "Book Stall (PF 6/7)", "end": "Platform 6/7"},
            {"start": "Platform 6/7", "end": "WP_PF67_Stairs_FOB2"},
            {"start": "WP_PF67_Stairs_FOB2", "end": "WP_PF67_Stairs_FOB3"},
            {"start": "WP_PF67_Stairs_FOB3", "end": "Stairs (PF 6/7, FOB 3)"},
            {"start": "Stairs (PF 6/7, FOB 3)", "end": "Toilet (PF 6/7)"},

            # --- PF 4/5 LEVEL (y=55) ---
            {"start": "WP_PF45_Stairs_FOB1", "end": "Waiting Room (PF 4/5)"},
            {"start": "Waiting Room (PF 4/5)", "end": "Platform 4/5"},
            {"start": "Platform 4/5", "end": "WP_PF45_Stairs_FOB2"},
            {"start": "WP_PF45_Stairs_FOB2", "end": "WP_PF45_Stairs_FOB3"},
            {"start": "WP_PF45_Stairs_FOB3", "end": "Stairs (PF 4/5, FOB 3)"},

            # --- PF 2/3 LEVEL (y=47) ---
            {"start": "WP_PF23_Stairs_FOB1", "end": "Toilet (PF 2/3)"},
            {"start": "Toilet (PF 2/3)", "end": "Platform 2/3"},
            {"start": "Platform 2/3", "end": "WP_PF23_Stairs_FOB2"},
            {"start": "WP_PF23_Stairs_FOB2", "end": "Food Plaza (PF 2/3)"},
            {"start": "Food Plaza (PF 2/3)", "end": "WP_PF23_Stairs_FOB3"},
            {"start": "WP_PF23_Stairs_FOB3", "end": "Stairs (PF 2/3, FOB 3)"},

            # --- PF 1 LEVEL (y=38) ---
            {"start": "WP_PF1_Stairs_FOB1", "end": "IRCTC Lounge (PF 1)"},
            {"start": "IRCTC Lounge (PF 1)", "end": "KFC Stall (PF 1)"},
            {"start": "KFC Stall (PF 1)", "end": "Platform 1"},
            {"start": "Platform 1", "end": "WP_PF1_Stairs_FOB2"},
            {"start": "WP_PF1_Stairs_FOB2", "end": "Cloak Room (PF 1)"},
            {"start": "Cloak Room (PF 1)", "end": "WP_PF1_Stairs_FOB3"},
            {"start": "WP_PF1_Stairs_FOB3", "end": "Retiring Room (PF 1)"},

            # Connect Ganesh Temple Side — chained left-to-right:
            # Helpline(40) ↔ Main Entrance(50) ↔ WP_Ganesh_Corridor(54) ↔ Auto Stand(60)
            {"start": "Main Entrance (Ganesh Temple)", "end": "Helpline/Enquiry"},
            {"start": "Main Entrance (Ganesh Temple)", "end": "WP_Ganesh_Corridor"},
            {"start": "WP_Ganesh_Corridor", "end": "Auto Stand (Ganesh Temple)"},
            {"start": "WP_Ganesh_Corridor", "end": "WP_PF1_Stairs_FOB2"},
            {"start": "WP_PF1_Stairs_FOB3", "end": "WP_Right_Corridor"},
            {"start": "WP_Right_Corridor", "end": "General Ticket Booking"},
            {"start": "Auto Stand (Ganesh Temple)", "end": "WP_Right_Corridor"}
        ]
    },  # Closing Secunderabad Junction Edges
    "Lingampally": {
        "nodes": [
            { "name": "Exit 1", "x": 18, "y": 16, "category": "Exit" },
            { "name": "Seating Area", "x": 25, "y": 16, "category": "Utility" },
            { "name": "Food Stall 1", "x": 34, "y": 16, "category": "Food" },
            { "name": "Entry 1", "x": 45, "y": 16, "category": "Exit" },
            { "name": "Reservation Counter", "x": 54, "y": 16, "category": "Utility" },
            { "name": "Toilet 1", "x": 64, "y": 16, "category": "Utility" },
            { "name": "PF1 Stairs", "x": 70, "y": 16, "category": "Stairs" },
            { "name": "PF1 Escalator", "x": 78, "y": 16, "category": "Stairs" },

            { "name": "Platform 1", "x": 49, "y": 16, "category": "Platform" },

            { "name": "Cloak Room", "x": 20, "y": 36, "category": "Utility" },
            { "name": "Food Stall 2", "x": 30, "y": 36, "category": "Food" },
            { "name": "Water Cooler", "x": 38, "y": 36, "category": "Utility" },
            { "name": "Waiting Room", "x": 50, "y": 36, "category": "Utility" },
            { "name": "PF2/3 Stairs", "x": 70, "y": 36, "category": "Stairs" },
            { "name": "P2,P3", "x": 65, "y": 36, "category": "Platform" },
            { "name": "Platform 4", "x": 50, "y": 53, "category": "Platform" },
            { "name": "Canteen", "x": 21, "y": 53, "category": "Food" },
            { "name": "Entry 2", "x": 34, "y": 53, "category": "Exit" },
            { "name": "Tea Stall", "x": 43, "y": 53, "category": "Food" },
            { "name": "Help Desk", "x": 57, "y": 53, "category": "Utility" },
            { "name": "Exit 2", "x": 68, "y": 53, "category": "Exit" },
            { "name": "PF4 Stairs", "x": 71, "y": 53, "category": "Stairs" },
            { "name": "PF4 Escalator", "x": 78, "y": 53, "category": "Stairs" },

            { "name": "Bridge_J1", "x": 74, "y": 16, "category": "Waypoint" },
            { "name": "Bridge_J2", "x": 74, "y": 36, "category": "Waypoint" },
            { "name": "Bridge_J3", "x": 74, "y": 53, "category": "Waypoint" }
        ],
        "edges": [
            # Top Concourse (Horizontal)
            {"start": "Exit 1", "end": "Seating Area"},
            {"start": "Seating Area", "end": "Food Stall 1"},
            {"start": "Food Stall 1", "end": "Entry 1"},
            {"start": "Entry 1", "end": "Platform 1"},
            {"start": "Platform 1", "end": "Reservation Counter"},
            {"start": "Reservation Counter", "end": "Toilet 1"},
            {"start": "Toilet 1", "end": "PF1 Stairs"},
            {"start": "PF1 Stairs", "end": "Bridge_J1"},
            {"start": "Bridge_J1", "end": "PF1 Escalator"},

            # Middle Island (Horizontal)
            {"start": "Cloak Room", "end": "Food Stall 2"},
            {"start": "Food Stall 2", "end": "Water Cooler"},
            {"start": "Water Cooler", "end": "Waiting Room"},
            {"start": "Waiting Room", "end": "P2,P3"},
            {"start": "P2,P3", "end": "PF2/3 Stairs"},
            {"start": "PF2/3 Stairs", "end": "Bridge_J2"},

            # Bottom Concourse (Horizontal)
            {"start": "Canteen", "end": "Entry 2"},
            {"start": "Entry 2", "end": "Tea Stall"},
            {"start": "Tea Stall", "end": "Platform 4"},
            {"start": "Platform 4", "end": "Help Desk"},
            {"start": "Help Desk", "end": "Exit 2"},
            {"start": "Exit 2", "end": "PF4 Stairs"},
            {"start": "PF4 Stairs", "end": "Bridge_J3"},
            {"start": "Bridge_J3", "end": "PF4 Escalator"},

            # The Main Pedestrian Bridge (Vertical: J1 -> J2 -> J3)
            {"start": "Bridge_J1", "end": "Bridge_J2"},
            {"start": "Bridge_J2", "end": "Bridge_J3"},
            
            # Missing platform transit connections
            {"start": "PF4 Escalator", "end": "Platform 4"},
            {"start": "Platform 4", "end": "PF4 Stairs"}
        ]
    },
    "Medchal Station": {
        "nodes": [
            { "name": "Top Left Corner", "x": 20, "y": 10, "category": "Utility" },
            { "name": "Top Stairs", "x": 58, "y": 10, "category": "Stairs" },
            { "name": "Top Right Corner", "x": 80, "y": 10, "category": "Utility" },
            { "name": "Top bridge", "x": 47, "y": 10, "category": "Utility" },

            { "name": "Waiting Room", "x": 20, "y": 29, "category": "Utility" },
            { "name": "Food Stall Right", "x": 92, "y": 31, "category": "Food" },
            { "name": "Stairs P4/P5 Left", "x": 39, "y": 32, "category": "Stairs" },
            { "name": "Stairs P4/P5 Right", "x": 52, "y": 32, "category": "Stairs" },
            { "name": "Platform 5", "x": 75, "y": 25, "category": "Platform" },

            { "name": "Platform 4", "x": 68, "y": 37, "category": "Platform" },

            { "name": "Food Stall Left", "x": 28, "y": 53, "category": "Food" },
            { "name": "Stairs P2/P3 Left", "x": 40, "y": 53, "category": "Stairs" },
            { "name": "Stairs P2/P3 Right", "x": 50, "y": 53, "category": "Stairs" },

            { "name": "Toilet Left", "x": 9, "y": 53, "category": "Utility" },
            { "name": "Platform 2", "x": 65, "y": 60, "category": "Platform" },
            { "name": "Stairs P2 Left", "x": 43, "y": 65, "category": "Stairs" },
            { "name": "Platform 3", "x": 75, "y": 52, "category": "Platform" },

            { "name": "Platform 1", "x": 67, "y": 80, "category": "Platform" },
            { "name": "Stairs Bottom", "x": 45, "y": 83, "category": "Stairs" },

            { "name": "Reservation Counter", "x": 40, "y": 93, "category": "Utility" },
            { "name": "Entry 1", "x": 60, "y": 93, "category": "Exit" },
            { "name": "Help Desk", "x": 16, "y": 93, "category": "Utility" },
            { "name": "PF1 Toilet", "x": 85, "y": 93, "category": "Utility" },

            { "name": "Bridge_J1", "x": 46, "y": 32, "category": "Waypoint" },
            { "name": "Bridge_J2", "x": 45, "y": 53, "category": "Waypoint" },
            { "name": "Bridge_J3", "x": 45, "y": 65, "category": "Waypoint" },
            { "name": "Bridge_J4", "x": 45, "y": 83, "category": "Waypoint" }
        ],
        "edges": [
            # Main Bridge Spine Vertical Connections
            {"start": "Top bridge", "end": "Bridge_J1", "weight": 1},
            {"start": "Bridge_J1", "end": "Bridge_J2", "weight": 1},
            {"start": "Bridge_J2", "end": "Bridge_J3", "weight": 1},
            {"start": "Bridge_J3", "end": "Bridge_J4", "weight": 1},
            
            # Top row connections 
            {"start": "Top Left Corner", "end": "Top bridge", "weight": 1},
            {"start": "Top bridge", "end": "Top Stairs", "weight": 1},
            {"start": "Top Stairs", "end": "Top Right Corner", "weight": 1},
            
            # P4/P5 Horizontal Level (Bridge_J1)
            {"start": "Waiting Room", "end": "Stairs P4/P5 Left", "weight": 1},
            {"start": "Stairs P4/P5 Left", "end": "Bridge_J1", "weight": 1},
            {"start": "Bridge_J1", "end": "Stairs P4/P5 Right", "weight": 1},
            {"start": "Stairs P4/P5 Right", "end": "Platform 5", "weight": 10},
            {"start": "Platform 5", "end": "Food Stall Right", "weight": 1},
            
            # P4/P5 Routing - Track crossing edges are weighted extremely high to "block" them.
            {"start": "Platform 4", "end": "Platform 5", "weight": 500},
            {"start": "Platform 4", "end": "Food Stall Right", "weight": 500},
            {"start": "Platform 4", "end": "Stairs P4/P5 Right", "weight": 10},
            {"start": "Platform 4", "end": "Stairs P4/P5 Left", "weight": 10},
            
            # P2/P3 Horizontal Level
            {"start": "Food Stall Left", "end": "Stairs P2/P3 Left", "weight": 1},
            {"start": "Stairs P2/P3 Left", "end": "Bridge_J2", "weight": 1},
            {"start": "Bridge_J2", "end": "Stairs P2/P3 Right", "weight": 1},
            {"start": "Stairs P2/P3 Right", "end": "Platform 3", "weight": 10},
            
            # P2/Toilet Horizontal Level
            {"start": "Toilet Left", "end": "Food Stall Left", "weight": 1},
            {"start": "Food Stall Left", "end": "Stairs P2 Left", "weight": 500}, # Illegal crossing
            {"start": "Stairs P2 Left", "end": "Bridge_J3", "weight": 1},
            {"start": "Platform 2", "end": "Stairs P2 Left", "weight": 10},
            
            # P1 Horizontal Level / Bottom stairs (Bridge_J4)
            {"start": "Stairs Bottom", "end": "Bridge_J4", "weight": 1},
            {"start": "Stairs Bottom", "end": "Platform 1", "weight": 10},
            
            # Bottom row connections
            {"start": "Help Desk", "end": "Reservation Counter", "weight": 1},
            {"start": "Reservation Counter", "end": "Entry 1", "weight": 1},
            {"start": "Entry 1", "end": "PF1 Toilet", "weight": 1},
            {"start": "Stairs Bottom", "end": "Reservation Counter", "weight": 1}
        ]
    },
    "Gadwal Station": {
        "nodes": [
            {"name": "Entrance 1", "x": 9,  "y": 55, "category": "Exit"},
            {"name": "Entrance 2", "x": 94, "y": 14, "category": "Exit"},
            {"name": "Toilet",     "x": 12, "y": 11, "category": "Utility"},
            {"name": "Reservation Counter", "x": 10, "y": 75, "category": "Utility"},
            {"name": "Food Stall",  "x": 91, "y": 66, "category": "Food"},
            {"name": "Platform 1",  "x": 24, "y": 75, "category": "Platform"},
            {"name": "Platform 2",  "x": 80, "y": 14, "category": "Platform"},
            {"name": "P1 Stairs Bottom North", "x": 18, "y": 36, "category": "Stairs"},
            {"name": "P1 Stairs Bottom South", "x": 24, "y": 64, "category": "Stairs"},
            {"name": "P2 Stairs Bottom",       "x": 85, "y": 35, "category": "Stairs"},
            
            {"name": "WP_Bridge_P1_Landing", "x": 30, "y": 40, "category": "Waypoint"},
            {"name": "WP_Bridge_P2_Landing", "x": 70, "y": 42, "category": "Waypoint"}
        ],
        "edges": [
            # Platform 1 Clique (Any node to Any node directly on the same side)
            {"start": "Toilet", "end": "Entrance 1"},
            {"start": "Toilet", "end": "Reservation Counter"},
            {"start": "Toilet", "end": "Platform 1"},
            {"start": "Toilet", "end": "P1 Stairs Bottom North"},
            {"start": "Toilet", "end": "P1 Stairs Bottom South"},
            
            {"start": "Entrance 1", "end": "Reservation Counter"},
            {"start": "Entrance 1", "end": "Platform 1"},
            {"start": "Entrance 1", "end": "P1 Stairs Bottom North"},
            {"start": "Entrance 1", "end": "P1 Stairs Bottom South"},
            
            {"start": "Reservation Counter", "end": "Platform 1"},
            {"start": "Reservation Counter", "end": "P1 Stairs Bottom North"},
            {"start": "Reservation Counter", "end": "P1 Stairs Bottom South"},
            
            {"start": "Platform 1", "end": "P1 Stairs Bottom North"},
            {"start": "Platform 1", "end": "P1 Stairs Bottom South"},
            
            {"start": "P1 Stairs Bottom North", "end": "P1 Stairs Bottom South"},

            # Platform 2 Clique
            {"start": "Entrance 2", "end": "Platform 2"},
            {"start": "Entrance 2", "end": "P2 Stairs Bottom"},
            {"start": "Entrance 2", "end": "Food Stall"},
            
            {"start": "Platform 2", "end": "P2 Stairs Bottom"},
            {"start": "Platform 2", "end": "Food Stall"},
            
            {"start": "P2 Stairs Bottom", "end": "Food Stall"},

            # The Foot Over Bridge (FOB) - Direct horizontal crossing
            {"start": "WP_Bridge_P1_Landing", "end": "WP_Bridge_P2_Landing"},

            # Vertical Linkages (Stairs to Bridge)
            {"start": "P1 Stairs Bottom North", "end": "WP_Bridge_P1_Landing"},
            {"start": "P1 Stairs Bottom South", "end": "WP_Bridge_P1_Landing"},
            {"start": "Entrance 1", "end": "WP_Bridge_P1_Landing"}, # (User identified as vertical connector)
            {"start": "Platform 1", "end": "WP_Bridge_P1_Landing"}, # (User identified as vertical connector)
            
            {"start": "P2 Stairs Bottom", "end": "WP_Bridge_P2_Landing"}
        ]
    },
    "Begumpet Station": {
        "nodes": [
            { "name": "Main Entrance", "x": 8.5, "y": 61.5, "category": "Exit" },
            { "name": "2nd Entrance / Exit", "x": 88.0, "y": 39.5, "category": "Exit" },
            { "name": "Help Desk", "x": 8.5, "y": 18.5, "category": "Utility" },
            { "name": "Waiting / Reservation Center (RC)", "x": 8.5, "y": 42.5, "category": "Utility" },
            { "name": "Ticket Counter (T)", "x": 8.5, "y": 88.5, "category": "Utility" },
            { "name": "Platform 1", "x": 22.7, "y": 66.5, "category": "Platform" },
            { "name": "Platform 2", "x": 88.0, "y": 75.5, "category": "Platform" },
            { "name": "FOB Stairs West", "x": 22.7, "y": 46.0, "category": "Stairs" },
            { "name": "FOB Stairs East", "x": 88.0, "y": 49.0, "category": "Stairs" }
        ],
        "edges": [
            # Platform 1 Clique (Direct Euclidean connections on the same side)
            {"start": "Main Entrance", "end": "Platform 1"},
            {"start": "Main Entrance", "end": "Waiting / Reservation Center (RC)"},
            {"start": "Main Entrance", "end": "Help Desk"},
            {"start": "Main Entrance", "end": "Ticket Counter (T)"},
            {"start": "Main Entrance", "end": "FOB Stairs West"},
            
            {"start": "Platform 1", "end": "Waiting / Reservation Center (RC)"},
            {"start": "Platform 1", "end": "Help Desk"},
            {"start": "Platform 1", "end": "Ticket Counter (T)"},
            {"start": "Platform 1", "end": "FOB Stairs West"},
            
            {"start": "Waiting / Reservation Center (RC)", "end": "Help Desk"},
            {"start": "Waiting / Reservation Center (RC)", "end": "Ticket Counter (T)"},
            {"start": "Waiting / Reservation Center (RC)", "end": "FOB Stairs West"},
            
            {"start": "Help Desk", "end": "Ticket Counter (T)"},
            {"start": "Help Desk", "end": "FOB Stairs West"},
            
            {"start": "Ticket Counter (T)", "end": "FOB Stairs West"},

            # Platform 2 Clique
            {"start": "2nd Entrance / Exit", "end": "Platform 2"},
            {"start": "2nd Entrance / Exit", "end": "FOB Stairs East"},
            {"start": "Platform 2", "end": "FOB Stairs East"},

            # The Foot Over Bridge (FOB) - Direct horizontal crossing
            {"start": "FOB Stairs West", "end": "FOB Stairs East"}
        ]
    }
}

def get_shortest_path(nodes, edges, start, end):
    graph = {n['name']: [] for n in nodes}
    node_map = {n['name']: n for n in nodes}
    for e in edges:
        if e['start'] in node_map and e['end'] in node_map:
            if 'weight' in e:
                # Use explicit weight * 1000 to dominate Euclidean distances
                d = float(e['weight']) * 1000.0
            else:
                d = math.sqrt((node_map[e['end']]['x'] - node_map[e['start']]['x'])**2 + 
                              (node_map[e['end']]['y'] - node_map[e['start']]['y'])**2)
            graph[e['start']].append((e['end'], d))
            graph[e['end']].append((e['start'], d))

    queue = [(0, start, [])]
    distances = {n['name']: float('inf') for n in nodes}
    
    if start not in distances: return None # Safety check if name mismatch
    distances[start] = 0
    
    while queue:
        (cost, current, path) = heapq.heappop(queue)
        
        # Optimization: skip if we've already found a better path in a previous iteration
        if cost > distances[current]: continue
        
        # FINAL TERMINATION: stop immediately when the destination is reached
        if current == end: 
            full_path = path + [current]
            # Double-check that the last node is precisely the requested destination
            if full_path[-1] == end:
                return full_path
            return None
        
        # In case we encounter a terminal node without outward edges gracefully
        if current not in graph: continue

        for (neighbor, weight) in graph[current]:
            if cost + weight < distances[neighbor]:
                distances[neighbor] = cost + weight
                heapq.heappush(queue, (cost + weight, neighbor, path + [current]))
    return None

@app.post("/navigate")
async def navigate(req: NavigationRequest):
    logger.info(f"[navigate] station='{req.station_name}' start='{req.start}' dest='{req.destination}'")

    if req.station_name not in STATION_GRAPHS:
        return JSONResponse(status_code=400, content={"error": f"Station '{req.station_name}' not supported"})
        
    # Resolve frontend display names → exact backend node names
    start_node = NODE_ALIASES.get(req.start, req.start)
    dest_node  = NODE_ALIASES.get(req.destination, req.destination)
    logger.info(f"[navigate] resolved: start='{start_node}' dest='{dest_node}'")
        
    station_data = STATION_GRAPHS[req.station_name]
    nodes = station_data["nodes"]
    edges = station_data["edges"]
    
    node_names = {n["name"] for n in nodes}
    if start_node not in node_names:
        return JSONResponse(status_code=404, content={"error": f"Start node '{start_node}' not found in graph"})
    if dest_node not in node_names:
        return JSONResponse(status_code=404, content={"error": f"Destination '{dest_node}' not found in graph"})
        
    path = get_shortest_path(nodes, edges, start_node, dest_node)
    logger.info(f"[navigate] path={path}")
    
    if not path or (len(path) == 1 and start_node != dest_node):
        return JSONResponse(status_code=404, content={"error": "Path not found – nodes may be disconnected"})
    
    # Final Validation: Force verification that the path ends at the intended node
    if path[-1] != dest_node:
        logger.error(f"[navigate] Validation failed: expected end '{dest_node}', got '{path[-1]}'")
        return JSONResponse(status_code=500, content={"error": "Pathfinding internal error: destination overshoot detected"})
        
    return {"path": path}