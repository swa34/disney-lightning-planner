# Disney Lightning Lane Planner - Flask Web Application

This web application helps Disney World visitors plan their Lightning Lane strategy for their trip. It provides cost estimates, recommendations, and tips based on user input about their travel details.

## Features

- Multi-step form for collecting trip details:
  - Party size and composition
  - Lightning Lane preferences (Single Pass, Premier)
  - Travel dates
  - Park selection for each day
  - Attraction preferences

- Personalized recommendations:
  - Multiple cost scenarios for comparison
  - Park-specific attraction recommendations
  - Custom tips based on selected parks
  - Daily cost breakdown

- Responsive design for both desktop and mobile use

## Project Structure

```
disney-lightning-planner/
├── app.py                 # Main Flask application
├── disney_planner.py      # Core planner logic
├── templates/             # HTML templates
│   ├── base.html          # Base template with shared elements
│   ├── index.html         # Welcome page
│   ├── user_info.html     # Basic trip info form
│   ├── travel_dates.html  # Date selection form
│   ├── park_selection.html # Park choices for each day
│   ├── single_pass_selection.html # Lightning Lane selection
│   └── results.html       # Final recommendations page
└── static/               
    └── style.css          # Additional custom styles
```

## Setup & Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install flask
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Visit `http://localhost:5000` in your browser

## Usage

1. Start by entering your party size and Lightning Lane preferences
2. Enter your travel dates and number of days
3. Select which park you'll visit on each day
4. Choose Lightning Lane Single Pass attractions (if applicable)
5. View your personalized recommendations and cost breakdown

## Notes

- This is an unofficial planning tool and is not affiliated with Walt Disney World Resort or the Walt Disney Company
- Prices and attraction information are for demonstration purposes and may not reflect actual current values
- The application stores all user data in the Flask session and does not maintain a database

## Future Enhancements

- User accounts to save multiple trip plans
- Integration with actual Lightning Lane pricing API
- Wait time predictions based on historical data
- Mobile app version
- Integration with Disney World dining reservations