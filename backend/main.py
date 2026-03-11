from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import heapq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NavigationRequest(BaseModel):
    station_name: str
    start: str
    destination: str

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
            { "name": "Main Entrance (Bhoiguda)", "x": 23, "y": 88, "category": "Exit" },
            { "name": "Main Entrance (Ganesh Temple)", "x": 50, "y": 15, "category": "Exit" },
            { "name": "FOB 1 (Foot Over Bridge)", "x": 25, "y": 56, "category": "Bridge" },
            { "name": "FOB 2 (Foot Over Bridge)", "x": 54, "y": 56, "category": "Bridge" },
            
            # Additional Granular Facilities matching Blueprint
            { "name": "Ticket Counter (Bhoiguda)", "x": 30, "y": 88, "category": "Utility" },
            { "name": "Parcel Office (Bhoiguda)", "x": 18, "y": 88, "category": "Utility" },
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
            {"start": "Main Entrance (Bhoiguda)", "end": "Ticket Counter (Bhoiguda)"},
            {"start": "Main Entrance (Bhoiguda)", "end": "Parcel Office (Bhoiguda)"},
            {"start": "Ticket Counter (Bhoiguda)", "end": "WP_PF10_Stairs_FOB1"},
            
            # FOB 1 Main Spine (Vertical across tracks)
            {"start": "WP_PF10_Stairs_FOB1", "end": "WP_PF89_Stairs_FOB1"},
            {"start": "WP_PF89_Stairs_FOB1", "end": "WP_PF67_Stairs_FOB1"},
            {"start": "WP_PF67_Stairs_FOB1", "end": "FOB 1 (Foot Over Bridge)"}, # FOB1 is at PF4/5
            {"start": "FOB 1 (Foot Over Bridge)", "end": "WP_PF45_Stairs_FOB1"},
            {"start": "WP_PF45_Stairs_FOB1", "end": "WP_PF23_Stairs_FOB1"},
            {"start": "WP_PF23_Stairs_FOB1", "end": "WP_PF1_Stairs_FOB1"},

            # FOB 1 Stairs to Platforms (Horizontal)
            {"start": "WP_PF10_Stairs_FOB1", "end": "Platform 10"},
            {"start": "WP_PF89_Stairs_FOB1", "end": "Platform 8/9"},
            {"start": "WP_PF67_Stairs_FOB1", "end": "Platform 6/7"},
            {"start": "WP_PF45_Stairs_FOB1", "end": "Platform 4/5"},
            {"start": "WP_PF23_Stairs_FOB1", "end": "Platform 2/3"},
            {"start": "WP_PF1_Stairs_FOB1", "end": "Platform 1"},

            # FOB 2 Main Spine (Vertical across tracks)
            {"start": "WP_PF10_Stairs_FOB2", "end": "WP_PF89_Stairs_FOB2"},
            {"start": "WP_PF89_Stairs_FOB2", "end": "WP_PF67_Stairs_FOB2"},
            {"start": "WP_PF67_Stairs_FOB2", "end": "FOB 2 (Foot Over Bridge)"}, # FOB2 is at PF4/5
            {"start": "FOB 2 (Foot Over Bridge)", "end": "WP_PF45_Stairs_FOB2"},
            {"start": "WP_PF45_Stairs_FOB2", "end": "WP_PF23_Stairs_FOB2"},
            {"start": "WP_PF23_Stairs_FOB2", "end": "WP_PF1_Stairs_FOB2"},

            # FOB 2 Stairs to Platforms (Horizontal)
            {"start": "WP_PF10_Stairs_FOB2", "end": "Platform 10"},
            {"start": "WP_PF89_Stairs_FOB2", "end": "Platform 8/9"},
            {"start": "WP_PF67_Stairs_FOB2", "end": "Platform 6/7"},
            {"start": "WP_PF45_Stairs_FOB2", "end": "Platform 4/5"},
            {"start": "WP_PF23_Stairs_FOB2", "end": "Platform 2/3"},
            {"start": "WP_PF1_Stairs_FOB2", "end": "Platform 1"},

            # FOB 3 Main Spine (Vertical across tracks)
            {"start": "WP_PF10_Stairs_FOB3", "end": "WP_PF89_Stairs_FOB3"},
            {"start": "WP_PF89_Stairs_FOB3", "end": "WP_PF67_Stairs_FOB3"},
            {"start": "WP_PF67_Stairs_FOB3", "end": "FOB 3 (Foot Over Bridge)"}, # FOB3 is at PF4/5
            {"start": "FOB 3 (Foot Over Bridge)", "end": "WP_PF45_Stairs_FOB3"},
            {"start": "WP_PF45_Stairs_FOB3", "end": "WP_PF23_Stairs_FOB3"},
            {"start": "WP_PF23_Stairs_FOB3", "end": "WP_PF1_Stairs_FOB3"},

            # FOB 3 Stairs to Platforms (Horizontal)
            {"start": "WP_PF10_Stairs_FOB3", "end": "Platform 10"},
            {"start": "WP_PF89_Stairs_FOB3", "end": "Platform 8/9"},
            {"start": "WP_PF67_Stairs_FOB3", "end": "Platform 6/7"},
            {"start": "WP_PF45_Stairs_FOB3", "end": "Platform 4/5"},
            {"start": "WP_PF23_Stairs_FOB3", "end": "Platform 2/3"},
            {"start": "WP_PF1_Stairs_FOB3", "end": "Platform 1"},

            # Intra-Platform Granular Facility connections (Left-to-Right layout logic)
            {"start": "Platform 10", "end": "Waiting Room (PF 10)"},
            {"start": "Platform 10", "end": "Escalator (PF 10)"},
            {"start": "WP_PF10_Stairs_FOB3", "end": "Stairs (PF 10, FOB 3)"},
            {"start": "Platform 8/9", "end": "Toilet (PF 8/9)"},
            {"start": "WP_PF89_Stairs_FOB3", "end": "Escalator (PF 8/9, FOB 3)"},
            {"start": "Platform 6/7", "end": "Book Stall (PF 6/7)"},
            {"start": "WP_PF67_Stairs_FOB3", "end": "Toilet (PF 6/7)"},
            {"start": "Platform 4/5", "end": "Waiting Room (PF 4/5)"},
            {"start": "WP_PF45_Stairs_FOB3", "end": "Stairs (PF 4/5, FOB 3)"},
            {"start": "Platform 2/3", "end": "Toilet (PF 2/3)"},
            {"start": "Platform 2/3", "end": "Food Plaza (PF 2/3)"},
            {"start": "WP_PF23_Stairs_FOB3", "end": "Stairs (PF 2/3, FOB 3)"},
            {"start": "Platform 1", "end": "KFC Stall (PF 1)"},
            {"start": "Platform 1", "end": "IRCTC Lounge (PF 1)"},
            {"start": "Platform 1", "end": "Cloak Room (PF 1)"},
            {"start": "WP_PF1_Stairs_FOB3", "end": "Retiring Room (PF 1)"},
            
            # Connect Ganesh Temple Side
            {"start": "Main Entrance (Ganesh Temple)", "end": "Helpline/Enquiry"},
            {"start": "Main Entrance (Ganesh Temple)", "end": "Auto Stand (Ganesh Temple)"},
            {"start": "Helpline/Enquiry", "end": "WP_Ganesh_Corridor"},
            {"start": "WP_Ganesh_Corridor", "end": "WP_PF1_Stairs_FOB2"},
            {"start": "WP_PF1_Stairs_FOB3", "end": "WP_Right_Corridor"},
            {"start": "WP_Right_Corridor", "end": "General Ticket Booking"},
            {"start": "WP_Right_Corridor", "end": "WP_Ganesh_Corridor"} # Walk along the bottom
        ]
    },
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

            { "name": "Platform 1", "x": 45, "y": 26, "category": "Platform" },

            { "name": "Cloak Room", "x": 20, "y": 39, "category": "Utility" },
            { "name": "Food Stall 2", "x": 30, "y": 39, "category": "Food" },
            { "name": "Water Cooler", "x": 38, "y": 36, "category": "Utility" },
            { "name": "Platform 2", "x": 45, "y": 33, "category": "Platform" },
            { "name": "Waiting Room", "x": 50, "y": 39, "category": "Utility" },
            { "name": "Platform 3", "x": 45, "y": 45, "category": "Platform" },
            { "name": "PF2/3 Stairs", "x": 70, "y": 39, "category": "Stairs" },

            { "name": "Platform 4", "x": 45, "y": 53, "category": "Platform" },
            { "name": "Canteen", "x": 21, "y": 64, "category": "Food" },
            { "name": "Entry 2", "x": 34, "y": 64, "category": "Exit" },
            { "name": "Tea Stall", "x": 43, "y": 64, "category": "Food" },
            { "name": "Help Desk", "x": 57, "y": 64, "category": "Utility" },
            { "name": "Exit 2", "x": 68, "y": 64, "category": "Exit" },
            { "name": "PF4 Stairs", "x": 71, "y": 64, "category": "Stairs" },
            { "name": "PF4 Escalator", "x": 78, "y": 64, "category": "Stairs" },

            { "name": "Bridge_J1", "x": 74, "y": 16, "category": "Waypoint" },
            { "name": "Bridge_J2", "x": 74, "y": 39, "category": "Waypoint" },
            { "name": "Bridge_J3", "x": 74, "y": 64, "category": "Waypoint" }
        ],
        "edges": [
            # Top Concourse (Horizontal)
            {"start": "Exit 1", "end": "Seating Area"},
            {"start": "Seating Area", "end": "Food Stall 1"},
            {"start": "Food Stall 1", "end": "Entry 1"},
            {"start": "Entry 1", "end": "Reservation Counter"},
            {"start": "Reservation Counter", "end": "Toilet 1"},
            {"start": "Toilet 1", "end": "PF1 Stairs"},
            {"start": "PF1 Stairs", "end": "Bridge_J1"},
            {"start": "Bridge_J1", "end": "PF1 Escalator"},
            {"start": "Entry 1", "end": "Platform 1"},

            # Middle Island (Horizontal)
            {"start": "Cloak Room", "end": "Food Stall 2"},
            {"start": "Food Stall 2", "end": "Water Cooler"},
            {"start": "Water Cooler", "end": "Platform 2"},
            {"start": "Platform 2", "end": "Waiting Room"},
            {"start": "Platform 2", "end": "Platform 3"},
            {"start": "Waiting Room", "end": "PF2/3 Stairs"},
            {"start": "PF2/3 Stairs", "end": "Bridge_J2"},
            {"start": "Platform 3", "end": "PF2/3 Stairs"},

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
            {"start": "Bridge_J2", "end": "Bridge_J3"}
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
            {"start": "Top bridge", "end": "Bridge_J1"},
            {"start": "Bridge_J1", "end": "Bridge_J2"},
            {"start": "Bridge_J2", "end": "Bridge_J3"},
            {"start": "Bridge_J3", "end": "Bridge_J4"},
            
            # Top row connections 
            {"start": "Top Left Corner", "end": "Top bridge"},
            {"start": "Top bridge", "end": "Top Stairs"},
            {"start": "Top Stairs", "end": "Top Right Corner"},
            
            # P4/P5 Horizontal Level (Bridge_J1)
            {"start": "Waiting Room", "end": "Stairs P4/P5 Left"},
            {"start": "Stairs P4/P5 Left", "end": "Bridge_J1"},
            {"start": "Bridge_J1", "end": "Stairs P4/P5 Right"},
            {"start": "Stairs P4/P5 Right", "end": "Platform 5"},
            {"start": "Platform 5", "end": "Food Stall Right"},
            
            # Platform 4 - Needs to connect independently to the spine, directly to J2
            {"start": "Platform 4", "end": "Bridge_J2"},
            
            # P2/P3 Horizontal Level (Bridge_J2 & Bridge_J3)
            # The diagram shows P2/P3 Stairs dropping to P2 and P3. Let's align them to J3.
            {"start": "Food Stall Left", "end": "Stairs P2/P3 Left"},
            {"start": "Stairs P2/P3 Left", "end": "Bridge_J3"},
            {"start": "Bridge_J3", "end": "Stairs P2/P3 Right"},
            {"start": "Stairs P2/P3 Right", "end": "Platform 3"},
            
            # P2/Toilet Horizontal Level (Bridge_J3)
            {"start": "Toilet Left", "end": "Food Stall Left"},
            {"start": "Platform 2", "end": "Food Stall Left"},
            {"start": "Food Stall Left", "end": "Stairs P2 Left"},
            {"start": "Stairs P2 Left", "end": "Bridge_J3"},
            {"start": "Platform 2", "end": "Stairs P2 Left"},
            
            # P1 Horizontal Level / Bottom stairs (Bridge_J4)
            {"start": "Stairs Bottom", "end": "Bridge_J4"},
            {"start": "Stairs Bottom", "end": "Platform 1"},
            
            # Bottom row connections
            {"start": "Help Desk", "end": "Reservation Counter"},
            {"start": "Reservation Counter", "end": "Entry 1"},
            {"start": "Entry 1", "end": "PF1 Toilet"},
            {"start": "Stairs Bottom", "end": "Reservation Counter"}
        ]
    },
    "Gadwal Station": {
        "nodes": [
            {"name": "Entrance 1", "x": 12, "y": 55, "category": "Exit"},
            {"name": "Entrance 2", "x": 94, "y": 14, "category": "Exit"},
            {"name": "Toilet", "x": 12, "y": 11, "category": "Utility"},
            {"name": "Waiting Room", "x": 10, "y": 75, "category": "Utility"},
            {"name": "Food Stall", "x": 91, "y": 66, "category": "Food"},
            {"name": "Platform 1", "x": 24, "y": 75, "category": "Platform"},
            {"name": "Platform 2", "x": 77, "y": 14, "category": "Platform"},
            {"name": "P1 Stairs Bottom North", "x": 24, "y": 25, "category": "Stairs"},
            {"name": "P1 Stairs Bottom South", "x": 24, "y": 64, "category": "Stairs"},
            {"name": "P2 Stairs Bottom", "x": 77, "y": 46, "category": "Stairs"},
            {"name": "FOB Landing P1", "x": 32, "y": 40, "category": "Waypoint"},
            {"name": "FOB Landing P2", "x": 68, "y": 40, "category": "Waypoint"},
            {"name": "FOB Middle", "x": 50, "y": 40, "category": "Waypoint"},
            {"name": "WP P1 North", "x": 24, "y": 11, "category": "Waypoint"},
            {"name": "WP P1 Middle", "x": 24, "y": 55, "category": "Waypoint"},
            {"name": "WP P2 South", "x": 77, "y": 66, "category": "Waypoint"}
        ],
        "edges": [
            # P1 Side paths (No crossing tracks)
            {"start": "Entrance 1", "end": "WP P1 Middle"},
            {"start": "WP P1 Middle", "end": "Platform 1"},
            {"start": "Platform 1", "end": "Waiting Room"},
            {"start": "WP P1 Middle", "end": "P1 Stairs Bottom South"},
            {"start": "P1 Stairs Bottom South", "end": "FOB Landing P1"},
            {"start": "P1 Stairs Bottom North", "end": "FOB Landing P1"},
            {"start": "P1 Stairs Bottom North", "end": "WP P1 North"},
            {"start": "WP P1 North", "end": "Toilet"},
            {"start": "P1 Stairs Bottom North", "end": "WP P1 Middle"},
            
            # The Foot Over Bridge (FOB) linking the two sides
            {"start": "FOB Landing P1", "end": "FOB Middle"},
            {"start": "FOB Middle", "end": "FOB Landing P2"},
            
            # P2 Side paths (No crossing tracks)
            {"start": "FOB Landing P2", "end": "P2 Stairs Bottom"},
            {"start": "P2 Stairs Bottom", "end": "Platform 2"},
            {"start": "Platform 2", "end": "Entrance 2"},
            {"start": "P2 Stairs Bottom", "end": "WP P2 South"},
            {"start": "WP P2 South", "end": "Food Stall"}
        ]
    }
}

def get_shortest_path(nodes, edges, start, end):
    graph = {n['name']: [] for n in nodes}
    node_map = {n['name']: n for n in nodes}
    for e in edges:
        if e['start'] in node_map and e['end'] in node_map:
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
        if current == end: return path + [current]
        
        # In case we encounter a terminal node without outward edges gracefully
        if current not in graph: continue

        for (neighbor, weight) in graph[current]:
            if cost + weight < distances[neighbor]:
                distances[neighbor] = cost + weight
                heapq.heappush(queue, (cost + weight, neighbor, path + [current]))
    return None

@app.post("/navigate")
async def navigate(req: NavigationRequest):
    if req.station_name not in STATION_GRAPHS:
        raise HTTPException(status_code=400, detail="Station not supported")
        
    station_data = STATION_GRAPHS[req.station_name]
    nodes = station_data["nodes"]
    edges = station_data["edges"]
    
    # Fast-fail if node names don't match
    if not any(n["name"] == req.start for n in nodes) or not any(n["name"] == req.destination for n in nodes):
        raise HTTPException(status_code=404, detail="Start or Destination node not found in graph")
        
    path = get_shortest_path(nodes, edges, req.start, req.destination)
    if not path: 
        raise HTTPException(status_code=404, detail="Path not found")
        
    return {"path": path}