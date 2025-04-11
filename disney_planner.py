import datetime


class DisneyLightningLanePlanner:
    def __init__(self):
        # Park costs for Multi Pass (per person)
        self.multi_pass_costs = {
            "Magic Kingdom": {"min": 15, "max": 39, "june_min": 35, "june_max": 39},
            "EPCOT": {"min": 15, "max": 35, "june_min": 25, "june_max": 30},
            "Hollywood Studios": {"min": 15, "max": 35, "june_min": 30, "june_max": 35},
            "Animal Kingdom": {"min": 15, "max": 30, "june_min": 20, "june_max": 25},
        }

        # Updated Park costs for Single Pass attractions (per person)
        self.single_pass_costs = {
            "Magic Kingdom": {
                "Seven Dwarfs Mine Train": {"min": 15, "max": 20},
                "TRON Lightcycle / Run": {"min": 19, "max": 22},
            },
            "EPCOT": {"Guardians of the Galaxy: Cosmic Rewind": {"min": 16, "max": 19}},
            "Hollywood Studios": {
                "Star Wars: Rise of the Resistance": {"min": 20, "max": 25},
                "Mickey & Minnie's Runaway Railway": {"min": 15, "max": 18},
            },
            "Animal Kingdom": {"Avatar Flight of Passage": {"min": 15, "max": 18}},
        }

        # Park costs for Premier Pass (per person)
        self.premier_pass_costs = {
            "Magic Kingdom": {"min": 329, "max": 449},
            "EPCOT": {"min": 169, "max": 249},
            "Hollywood Studios": {"min": 269, "max": 349},
            "Animal Kingdom": {"min": 129, "max": 199},
        }

        # Recommended attractions
        self.recommended_attractions = {
            "Magic Kingdom": {
                "Tier 1": ["Tiana's Bayou Adventure", "Peter Pan's Flight"],
                "Tier 2": ["Space Mountain", "Big Thunder Mountain", "Haunted Mansion"],
            },
            "EPCOT": {
                "Tier 1": ["Frozen Ever After", "Remy's Ratatouille Adventure"],
                "Tier 2": [
                    "Soarin'",
                    "Mission: SPACE",
                    "Test Track (reopening summer 2025)",
                ],
            },
            "Hollywood Studios": {
                "Tier 1": ["Slinky Dog Dash"],
                "Tier 2": [
                    "Millennium Falcon: Smugglers Run",
                    "Toy Story Mania",
                    "Tower of Terror",
                ],
            },
            "Animal Kingdom": {
                # No tiers for Animal Kingdom
                "Recommended": [
                    "Na'vi River Journey",
                    "Kilimanjaro Safaris",
                    "Expedition Everest",
                ]
            },
        }

        # Tips for each park
        self.park_tips = {
            "Magic Kingdom": [
                "Arrive early (30+ minutes before park opening) if not using Lightning Lane",
                "Multi Pass is most valuable at Magic Kingdom due to the high number of attractions",
                "Consider booking Tiana's Bayou Adventure early as it sells out quickly",
                "TRON and Seven Dwarfs Mine Train both require Single Pass for Lightning Lane access",
                "If you have Early Entry, use that time for one premium attraction and buy Single Pass for the other",
                "Save some Tier 2 selections for later in the day",
            ],
            "EPCOT": [
                "Try for Guardians of the Galaxy virtual queue at 7 AM if not using Single Pass",
                "World Showcase attractions typically have shorter lines during meal times",
                "Consider dining reservations during peak crowd times (12-2 PM)",
                "Test Track is expected to reopen in summer 2025 as a Tier 1 attraction",
                "Evening is ideal for exploring World Showcase with shorter lines",
            ],
            "Hollywood Studios": [
                "This park has the highest demand for Lightning Lane passes",
                "Early morning arrival (45+ minutes before opening) is essential without Lightning Lane",
                "Rise of the Resistance is the highest priority Single Pass in all of Disney World",
                "Mickey & Minnie's Runaway Railway is available as Single Pass but typically has shorter waits",
                "Use single rider line for Millennium Falcon if available and your group doesn't mind separation",
                "Shows like Indiana Jones and Frozen Sing-Along can provide air-conditioned breaks",
            ],
            "Animal Kingdom": [
                "This park is most manageable without Lightning Lane passes",
                "Flight of Passage is worth the Single Pass cost",
                "Kilimanjaro Safaris is best experienced in morning for better animal viewing",
                "The park often closes earlier than other parks, check times during your visit",
                "Consider river raft rides for afternoon cooling (expect to get wet)",
            ],
        }

        # General Lightning Lane tips
        self.general_tips = [
            "Resort guests can book Lightning Lane 7 days before check-in at 7 AM ET",
            "Off-site guests can book 3 days before park visit at 7 AM ET",
            "After using your first Lightning Lane, book your next one immediately",
            "You can modify existing Lightning Lane reservations without canceling",
            "June is high season, so prices will trend toward the higher end",
            "Lightning Lane Multi Pass includes ride photos for the day",
            "You can purchase up to 2 Single Passes per day total across all parks",
            "Consider Early Theme Park Entry (resort guests) or rope drop strategies to maximize your day",
            "Afternoon thunderstorms are common in June - plan indoor activities from 2-5 PM",
        ]

        # User data
        self.user_data = {
            "number_of_people": 0,
            "adults": 0,
            "children": 0,
            "resort_guest": False,
            "parks": [],
            "travel_dates": [],
            "park_hopping": False,
            "include_single_pass": True,
            "include_premier": True,
            "selected_single_passes": {},  # Will store user's selected Single Pass rides for each park
        }

    def calculate_costs(self):
        """Calculate costs for different Lightning Lane scenarios."""
        # Define scenarios based on user preferences
        scenarios = {
            "scenario2": {
                "name": "Multi Pass Only (Budget Option)",
                "total_min": 0,
                "total_max": 0,
                "daily": [],
            }
        }

        # Add scenario 1 if user wants Single Pass
        if self.user_data["include_single_pass"]:
            scenarios["scenario1"] = {
                "name": "Multi Pass + Selected Single Passes",
                "total_min": 0,
                "total_max": 0,
                "daily": [],
            }

        # Add scenario 3 if user wants Premier Pass
        if self.user_data["include_premier"]:
            scenarios["scenario3"] = {
                "name": "Premier Pass (Premium Option)",
                "total_min": 0,
                "total_max": 0,
                "daily": [],
            }

        # Always include scenario 4 but adjust based on user preferences
        strategy_name = "Mixed Strategy (Recommended)"
        if not self.user_data["include_single_pass"]:
            strategy_name = "Mixed Strategy (No Single Passes)"
        scenarios["scenario4"] = {
            "name": strategy_name,
            "total_min": 0,
            "total_max": 0,
            "daily": [],
        }

        # Determine if any dates are in June (for seasonal pricing)
        is_june = any(date.month == 6 for date in self.user_data["travel_dates"])

        for i, park in enumerate(self.user_data["parks"]):
            date = self.user_data["travel_dates"][i]

            # Use June pricing if travel date is in June
            price_key_suffix = "june_" if date.month == 6 else ""

            # Get Multi Pass costs
            multi_min = self.multi_pass_costs[park][
                f"{price_key_suffix}min" if price_key_suffix else "min"
            ]
            multi_max = self.multi_pass_costs[park][
                f"{price_key_suffix}max" if price_key_suffix else "max"
            ]

            # Scenario 1: Multi Pass + Selected Single Passes (if included)
            if self.user_data["include_single_pass"] and "scenario1" in scenarios:
                daily_min = multi_min * self.user_data["adults"]
                daily_max = multi_max * self.user_data["adults"]

                # Add costs for user-selected Single Pass attractions
                selected_passes = self.user_data["selected_single_passes"].get(park, [])
                for attraction in selected_passes:
                    single_min = self.single_pass_costs[park][attraction]["min"]
                    single_max = self.single_pass_costs[park][attraction]["max"]
                    daily_min += single_min * self.user_data["adults"]
                    daily_max += single_max * self.user_data["adults"]

                scenarios["scenario1"]["daily"].append(
                    {
                        "park": park,
                        "date": date,
                        "min": daily_min,
                        "max": daily_max,
                        "single_passes": selected_passes,
                    }
                )
                scenarios["scenario1"]["total_min"] += daily_min
                scenarios["scenario1"]["total_max"] += daily_max

            # Scenario 2: Multi Pass Only
            daily_min = multi_min * self.user_data["adults"]
            daily_max = multi_max * self.user_data["adults"]

            scenarios["scenario2"]["daily"].append(
                {"park": park, "date": date, "min": daily_min, "max": daily_max}
            )
            scenarios["scenario2"]["total_min"] += daily_min
            scenarios["scenario2"]["total_max"] += daily_max

            # Scenario 3: Premier Pass (if included)
            if self.user_data["include_premier"] and "scenario3" in scenarios:
                premier_min = (
                    self.premier_pass_costs[park]["min"] * self.user_data["adults"]
                )
                premier_max = (
                    self.premier_pass_costs[park]["max"] * self.user_data["adults"]
                )

                scenarios["scenario3"]["daily"].append(
                    {"park": park, "date": date, "min": premier_min, "max": premier_max}
                )
                scenarios["scenario3"]["total_min"] += premier_min
                scenarios["scenario3"]["total_max"] += premier_max

        # Scenario 4: Mixed Strategy (adjusted based on preferences)
        for i, park in enumerate(self.user_data["parks"]):
            date = self.user_data["travel_dates"][i]
            daily_min = 0
            daily_max = 0
            selected_passes = []

            # Use June pricing if travel date is in June
            price_key_suffix = "june_" if date.month == 6 else ""

            if park in ["Magic Kingdom", "Hollywood Studios"]:
                # Multi Pass for these parks
                multi_min = self.multi_pass_costs[park][
                    f"{price_key_suffix}min" if price_key_suffix else "min"
                ]
                multi_max = self.multi_pass_costs[park][
                    f"{price_key_suffix}max" if price_key_suffix else "max"
                ]
                daily_min += multi_min * self.user_data["adults"]
                daily_max += multi_max * self.user_data["adults"]

                # Add Single Pass if user wants them and has selected some
                if self.user_data["include_single_pass"]:
                    user_selected = self.user_data["selected_single_passes"].get(
                        park, []
                    )
                    for attraction in user_selected:
                        single_min = self.single_pass_costs[park][attraction]["min"]
                        single_max = self.single_pass_costs[park][attraction]["max"]
                        daily_min += single_min * self.user_data["adults"]
                        daily_max += single_max * self.user_data["adults"]
                        selected_passes.append(attraction)
            elif park == "EPCOT":
                # Multi Pass only for EPCOT
                multi_min = self.multi_pass_costs[park][
                    f"{price_key_suffix}min" if price_key_suffix else "min"
                ]
                multi_max = self.multi_pass_costs[park][
                    f"{price_key_suffix}max" if price_key_suffix else "max"
                ]
                daily_min += multi_min * self.user_data["adults"]
                daily_max += multi_max * self.user_data["adults"]
            elif park == "Animal Kingdom":
                if self.user_data["include_single_pass"]:
                    # Only use Single Passes selected by user for Animal Kingdom
                    user_selected = self.user_data["selected_single_passes"].get(
                        park, []
                    )
                    for attraction in user_selected:
                        single_min = self.single_pass_costs[park][attraction]["min"]
                        single_max = self.single_pass_costs[park][attraction]["max"]
                        daily_min += single_min * self.user_data["adults"]
                        daily_max += single_max * self.user_data["adults"]
                        selected_passes.append(attraction)

            scenarios["scenario4"]["daily"].append(
                {
                    "park": park,
                    "date": date,
                    "min": daily_min,
                    "max": daily_max,
                    "single_passes": (
                        selected_passes if self.user_data["include_single_pass"] else []
                    ),
                }
            )
            scenarios["scenario4"]["total_min"] += daily_min
            scenarios["scenario4"]["total_max"] += daily_max

        return scenarios

    def get_booking_dates(self):
        """Return a list of dates when Lightning Lane selections become available."""
        is_resort = self.user_data.get("resort_guest", False)
        booking_dates = []

        for date in self.user_data["travel_dates"]:
            offset = 7 if is_resort else 3
            booking_date = date - datetime.timedelta(days=offset)
            booking_dates.append(booking_date)

        return booking_dates

    def get_booking_date(self):
        """Calculate the earliest date the user can book Lightning Lane passes."""
        if self.user_data.get("resort_guest") and self.user_data.get("checkin_date"):
            checkin = datetime.date.fromisoformat(self.user_data["checkin_date"])
            return checkin - datetime.timedelta(days=7)
        else:
            # Off-site: only show individual dates per park
            return None

    def get_trip_milestones(self):
        """Returns key date milestones based on check-in date for resort guests."""
        if not self.user_data.get("resort_guest") or not self.user_data.get(
            "checkin_date"
        ):
            return {}

        checkin = datetime.date.fromisoformat(self.user_data["checkin_date"])

        return {
            "Dining Reservations (ADR Date)": checkin - datetime.timedelta(days=60),
            "Online Check-in": checkin - datetime.timedelta(days=60),
            "Final Payment Due": checkin - datetime.timedelta(days=30),
            "MagicBand Order Deadline": checkin - datetime.timedelta(days=10),
            "Memory Maker Discount Deadline": checkin - datetime.timedelta(days=3),
            "Reservations Available": checkin - datetime.timedelta(days=499),
        }
