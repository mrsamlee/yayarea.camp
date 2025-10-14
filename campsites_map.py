from dataclasses import dataclass
from typing import List

@dataclass
class Campsite:
    """Data structure representing a campsite with all its properties."""
    park_name: str
    time_to: str
    miles: int
    campground_name: str
    url: str
    rec: str
    campground_id: str

def get_rec_to_campsites_map():
    """
    Returns a map where the key is Rec and the value is a list of Campsite objects.
    Data parsed from BayAreaCampsites.csv
    """
    return {
        "703": [
            Campsite("Salt Point SP", "2h12m", 100, "Woodside Lower Loop (sites 31-70)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/703/649", "703", "649"),
            Campsite("Salt Point SP", "2h12m", 100, "Woodside Upper Loop (sites 71-109)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/703/614", "703", "614")
        ],
        "718": [
            Campsite("Sonoma Coast State Park", "1h22m", 70, "Bodega Dunes", "https://www.reservecalifornia.com/Web/Default.aspx#!park/718/2061", "718", "2061"),
            Campsite("Sonoma Coast State Park", "1h22m", 70, "Wright's Beach (sites 1-27)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/718/706", "718", "706")
        ],
        "705": [
            Campsite("Samuel P. Taylor SP", "49m", 30, "Creekside Loop (sites 1-25)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/705/653", "705", "653"),
            Campsite("Samuel P. Taylor SP", "49m", 30, "Orchard Hill Loop (sites 26-59)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/705/657", "705", "657")
        ],
        "652": [
            Campsite("Half Moon Bay SP", "33m", 23, "Francis Beach Campground", "https://www.reservecalifornia.com/Web/Default.aspx#!park/652/498", "652", "498")
        ],
        "695": [
            Campsite("Portola Redwoods SP", "1h11m", 50, "Portola Campground (sites 1-4, 20-45)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/695/628", "695", "628"),
            Campsite("Portola Redwoods SP", "1h11m", 50, "Portola Campground (sites 5-19, 46-53)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/695/629", "695", "629")
        ],
        "3": [
            Campsite("Big Basin Campgrounds", "1h15m", 56, "Lower Blooms Creek (sites 103-138)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/3/332", "3", "332"),
            Campsite("Big Basin Campgrounds", "1h15m", 56, "Sempervirens Campground (sites 157-188)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/3/335", "3", "335"),
            Campsite("Big Basin Campgrounds", "1h15m", 56, "Huckleberry Campground (sites 42-75)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/3/336", "3", "336"),
            Campsite("Big Basin Campgrounds", "1h15m", 56, "Wastahi Campground (sites 76-102)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/3/337", "3", "337"),
            Campsite("Big Basin Campgrounds", "1h15m", 56, "Upper Blooms Creek (sites 139-156)", "https://www.reservecalifornia.com/Web/Default.aspx#!park/3/339", "3", "339")
        ],
        "672": [
            Campsite("Manresa SB", "1h30m", 86, "Willow Camps (sites 1-26) - Walk In From Parking Lot", "https://www.reservecalifornia.com/Web/Default.aspx#!park/672/564", "672", "564"),
            Campsite("Manresa SB", "1h30m", 86, "Bay & Lupine Camps (sites 27-65) - Walk In From Parking Lot", "https://www.reservecalifornia.com/Web/Default.aspx#!park/672/565", "672", "565")
        ]
    }

def get_recreation_gov_campsites():
    """
    Returns a list of Recreation.gov campsite objects.
    Includes Yosemite and Bay Area campgrounds.
    """
    return [
        Campsite(
            park_name="Golden Gate NRA",
            time_to="30m",
            miles=15,
            campground_name="Kirby Cove",
            url="https://www.recreation.gov/camping/campgrounds/232491",
            rec="recreation_gov",
            campground_id="232491"
        ),
        Campsite(
            park_name="Yosemite National Park",
            time_to="3h30m",
            miles=180,
            campground_name="Upper Pines",
            url="https://www.recreation.gov/camping/campgrounds/232447",
            rec="recreation_gov",
            campground_id="232447"
        ),
        Campsite(
            park_name="Yosemite National Park",
            time_to="3h30m",
            miles=180,
            campground_name="Lower Pines",
            url="https://www.recreation.gov/camping/campgrounds/232450",
            rec="recreation_gov",
            campground_id="232450"
        ),
        Campsite(
            park_name="Yosemite National Park",
            time_to="3h15m",
            miles=170,
            campground_name="Wawona",
            url="https://www.recreation.gov/camping/campgrounds/232446",
            rec="recreation_gov",
            campground_id="232446"
        )
    ]
