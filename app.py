import datetime
import json
import os

from flask import Flask, redirect, render_template, request, session, url_for

from disney_planner import DisneyLightningLanePlanner

app = Flask(__name__)
app.secret_key = os.urandom(24)


# For the index route - no changes needed
@app.route("/")
def index():
    # Clear session data when starting fresh
    session.clear()
    return render_template("index.html")


# For the user_info route - add current_step=1
@app.route("/user_info", methods=["GET", "POST"])
def user_info():
    if request.method == "POST":
        # Initialize planner
        planner = DisneyLightningLanePlanner()

        # Process form data for number of people
        planner.user_data["adults"] = int(request.form.get("adults", 0))
        planner.user_data["children"] = int(request.form.get("children", 0))
        planner.user_data["number_of_people"] = (
            planner.user_data["adults"] + planner.user_data["children"]
        )

        # Process Lightning Lane preferences
        planner.user_data["include_single_pass"] = (
            request.form.get("include_single_pass") == "yes"
        )
        planner.user_data["include_premier"] = (
            request.form.get("include_premier") == "yes"
        )

        # Process resort and park hopping info
        planner.user_data["resort_guest"] = request.form.get("resort_guest") == "yes"
        checkin_date_str = request.form.get("checkin_date")
        if checkin_date_str:
            planner.user_data["checkin_date"] = (
                checkin_date_str  # Store as string, will convert later
            )
        planner.user_data["park_hopping"] = request.form.get("park_hopping") == "yes"

        # Store in session
        session["user_data"] = planner.user_data

        # Redirect to travel dates page
        return redirect(url_for("travel_dates"))

    return render_template("user_info.html", current_step=1)


# For the travel_dates route - add current_step=2
@app.route("/travel_dates", methods=["GET", "POST"])
def travel_dates():
    if request.method == "POST":
        # Get planner from session
        planner = DisneyLightningLanePlanner()
        planner.user_data = session.get("user_data", {})

        # Process travel dates
        month = int(request.form.get("month"))
        year = int(request.form.get("year"))
        start_day = int(request.form.get("start_day"))
        num_days = int(request.form.get("num_days"))

        # Generate dates
        travel_dates = []
        current_date = datetime.date(year, month, start_day)
        for _ in range(num_days):
            travel_dates.append(current_date.isoformat())
            current_date += datetime.timedelta(days=1)

        planner.user_data["travel_dates"] = travel_dates

        # Store in session
        session["user_data"] = planner.user_data

        return redirect(url_for("park_selection"))

    return render_template("travel_dates.html", current_step=2)


# For the park_selection route - add current_step=3
@app.route("/park_selection", methods=["GET", "POST"])
def park_selection():
    if request.method == "POST":
        # Get planner from session
        planner = DisneyLightningLanePlanner()
        planner.user_data = session.get("user_data", {})

        # Process park selections
        parks = []
        for i in range(len(planner.user_data["travel_dates"])):
            park = request.form.get(f"park_{i}")
            parks.append(park)

        planner.user_data["parks"] = parks

        # Initialize selected_single_passes dictionary
        planner.user_data["selected_single_passes"] = {}
        for park in planner.user_data["parks"]:
            planner.user_data["selected_single_passes"][park] = []

        # Store in session
        session["user_data"] = planner.user_data

        # If user wants Single Pass, redirect to attraction selection page
        if planner.user_data["include_single_pass"]:
            return redirect(url_for("single_pass_selection"))
        else:
            return redirect(url_for("results"))

    # Parse dates from session for template
    user_data = session.get("user_data", {})
    dates = []

    for date_str in user_data.get("travel_dates", []):
        date = datetime.date.fromisoformat(date_str)
        dates.append(
            {"date_str": date_str, "formatted": date.strftime("%A, %B %d, %Y")}
        )

    return render_template("park_selection.html", dates=dates, current_step=3)


# For the single_pass_selection route - add current_step=4
@app.route("/single_pass_selection", methods=["GET", "POST"])
def single_pass_selection():
    # Get planner from session
    planner = DisneyLightningLanePlanner()
    planner.user_data = session.get("user_data", {})

    if request.method == "POST":
        # Process selected single passes
        for i, park in enumerate(planner.user_data["parks"]):
            selected_attractions = request.form.getlist(f"attractions_{i}")
            planner.user_data["selected_single_passes"][park] = selected_attractions

        # Store in session
        session["user_data"] = planner.user_data

        return redirect(url_for("results"))

    # Prepare park and date information for template
    parks_info = []
    for i, park in enumerate(planner.user_data["parks"]):
        date = datetime.date.fromisoformat(planner.user_data["travel_dates"][i])

        attractions = []
        for attraction, cost in planner.single_pass_costs[park].items():
            attractions.append(
                {"name": attraction, "min_cost": cost["min"], "max_cost": cost["max"]}
            )

        parks_info.append(
            {
                "index": i,
                "name": park,
                "date": date.strftime("%A, %B %d, %Y"),
                "attractions": attractions,
            }
        )

    return render_template(
        "single_pass_selection.html", parks_info=parks_info, current_step=4
    )


# For the results route - add current_step=5
@app.route("/results")
def results():
    # Get planner from session
    planner = DisneyLightningLanePlanner()
    planner.user_data = session.get("user_data", {})

    # Convert ISO format dates back to datetime objects
    travel_dates = []
    for date_str in planner.user_data["travel_dates"]:
        travel_dates.append(datetime.date.fromisoformat(date_str))
    planner.user_data["travel_dates"] = travel_dates

    # Calculate costs
    scenarios = planner.calculate_costs()

    # Convert datetime objects to strings for JSON serialization
    for scenario_key, scenario in scenarios.items():
        for i, daily in enumerate(scenario["daily"]):
            scenario["daily"][i]["date"] = daily["date"].strftime("%A, %B %d, %Y")

    # Get park recommendations and tips
    park_recommendations = {}

    for i, park in enumerate(planner.user_data["parks"]):
        date = planner.user_data["travel_dates"][i]

        # Get recommended attractions
        if park == "Animal Kingdom":
            recommended = {
                "tiers": False,
                "attractions": planner.recommended_attractions[park]["Recommended"],
            }
        else:
            recommended = {
                "tiers": True,
                "tier1": planner.recommended_attractions[park]["Tier 1"],
                "tier2": planner.recommended_attractions[park]["Tier 2"],
            }

        # Get single pass information
        single_passes = []
        if planner.user_data["include_single_pass"]:
            selected = planner.user_data["selected_single_passes"].get(park, [])

            for attraction in selected:
                cost_range = planner.single_pass_costs[park][attraction]
                single_passes.append(
                    {
                        "name": attraction,
                        "min": cost_range["min"],
                        "max": cost_range["max"],
                    }
                )

        # Get premier pass info
        premier_info = None
        if planner.user_data["include_premier"]:
            premier_cost = planner.premier_pass_costs[park]
            premier_info = {"min": premier_cost["min"], "max": premier_cost["max"]}

        # Get tips
        tips = planner.park_tips[park]

        # Create park recommendation
        park_recommendations[park] = {
            "date": date.strftime("%A, %B %d, %Y"),
            "recommended": recommended,
            "single_passes": single_passes,
            "premier_info": premier_info,
            "tips": tips,
        }
    booking_dates = planner.get_booking_dates()
    booking_date = planner.get_booking_date()

    # Pass the zip function to the template
    return render_template(
        "results.html",
        user_data=planner.user_data,
        scenarios=scenarios,
        park_recommendations=park_recommendations,
        general_tips=planner.general_tips,
        zip=zip,
        booking_dates=booking_dates,  # already for off-site guests
        booking_date=booking_date,  # new line
        current_step=5,
    )


@app.route("/restaurants")
def restaurant_finder():
    """Page for the restaurant finder tool"""
    return render_template("restaurant_finder.html")


@app.route("/dining-calculator")
def dining_calculator():
    """Page for the dining cost calculator tool"""
    return render_template("restaurant_calculator.html")


@app.route("/contact")
def contact():
    """Page for the contact information"""
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
