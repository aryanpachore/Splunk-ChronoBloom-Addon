<img width="100" alt="App Icon" src="https://github.com/user-attachments/assets/5c73192e-ee2e-474e-ab97-9747b6d07510" />   

## Splunk-ChronoBloom-Addon

**Real-time insights into environmental phenological events using Splunk Enterprise.**

## Overview and Purpose

The `Splunk-ChronoBloom-Addon` is a project developed as a hackathon submission focused on integrating **phenological observation data** into Splunk Enterprise. Phenology is the scientific study of cyclic and seasonal natural phenomena (e.g., plant flowering, insect emergence, bird migration) and provides vital indicators of climate change and local environmental shifts.

This add-on aims to bridge the gap between critical environmental data and actionable insights by:
* Ingesting phenological data (currently simulated for demonstration).
* Providing interactive dashboards for visualization and analysis.
* Offering basic anomaly detection and AI-driven predictions for agricultural and scientific use cases.

The ultimate goal is to empower environmental scientists, agricultural planners, public health officials, conservation agencies, and climate researchers by allowing them to track trends, detect anomalies, and correlate these biological events with other relevant datasets within the familiar Splunk interface.

---

## Dashboard Components

The `ChronoBloom Phenology Explorer` dashboard is designed to provide a multi-faceted view of phenological observations.

### Global Filters
* **Select Time Range:** Allows users to dynamically adjust the time window for all panels on the dashboard, from predefined presets (e.g., "Last 7 days") to custom ranges.
* **Filter by Species:** A dropdown filter to narrow down all panels to observations related to specific species (e.g., "Red maple", "Lilac", "American robin").
* **Filter by State:** A dropdown filter to narrow down all panels to observations from particular US states (e.g., "CA", "NY", "TX").

### Panels

1.  **Welcome to ChronoBloom Insights**
    * **Use:** Provides a welcoming introduction to the dashboard, explaining its purpose and highlighting the key types of insights available. It sets the context for users.

2.  **Latest Phenological Events**
    * **Use:** Displays a table of the most recent individual phenological observations, including timestamps, species, phenophase, status (observed/not observed), location, and coordinates.
    * **Benefit:** Offers real-time monitoring of incoming data, allowing for quick inspection of raw events and detailed investigation via drilldowns.

3.  **Geospatial Distribution of Observations (Heatmap by Species)**
    * **Use:** Visualizes the geographical concentration of phenological observations on a map. Areas with a higher density of observations appear more intensely colored. The "by Species" aspect attempts to show this density broken down per species.
    * **Benefit:** Helps identify regions of high activity, data collection efforts, or areas experiencing particular environmental conditions.

4.  **Potential Phenological Not-Observed Anomalies**
    * **Use:** Displays a table of phenological events where a specific phenophase (`phenophase_status=0`, meaning "Not Observed") was recorded. This serves as a basic anomaly detection mechanism, flagging potential delays or unusual absences of expected biological events.
    * **Benefit:** Allows scientists and farmers to quickly spot potential deviations from normal patterns, which could indicate environmental stress or climate impact.

5.  **Phenophase Occurrences by Day of Year**
    * **Use:** A scatter plot visualizing the Day of Year (DOY) when specific phenophases were observed, plotted against the observation date. This helps in understanding the seasonality and identifying if events are occurring earlier or later than expected within the year.
    * **Benefit:** Crucial for climate change studies and agricultural planning to analyze shifts in seasonal timing.

6.  **Observations Trend Over Time**
    * **Use:** A column chart showing the total count of phenological observations over time (e.g., daily counts).
    * **Benefit:** Provides a high-level overview of activity patterns, helping to identify periods of increased data collection or specific biological events.

7.  **Phenophase Status Breakdown**
    * **Use:** A pie chart illustrating the proportion of "Observed" vs. "Not Observed" phenophase statuses within the selected time range.
    * **Benefit:** Gives a quick summary of the overall health or activity of observed phenophases, aiding conservation efforts and resource management.

8.  **Top Species by Observations**
    * **Use:** A bar chart displaying the species with the highest number of observations.
    * **Benefit:** Helps identify the most active or frequently studied species, guiding research and monitoring efforts.

9.  **Observations by State**
    * **Use:** A table listing the count of observations per US state.
    * **Benefit:** Provides geographical context at a state level, useful for regional planning and comparison.

10. **Farmers' Phenology Predictions**
    * **Use:** A table displaying predictions generated by the integrated Gemini AI model, including predicted species, phenophase, state, and target dates.
    * **Benefit:** Offers proactive insights for agricultural planning (e.g., likely bloom dates for specific crops), enabling better decision-making for planting, pest management, and harvesting.

11. **Recent ChronoBloom Alert Triggers**
    * **Use:** Shows a table of recent instances where predefined Splunk alerts (e.g., "Red Maple First Flower Not Observed Alert") have been triggered.
    * **Benefit:** Allows users to monitor critical conditions directly from the dashboard, ensuring timely awareness of significant deviations.

---

## Project Visuals

### Dashboard Screenshots
<img width="1919" height="915" alt="image" src="https://github.com/user-attachments/assets/e46f71ad-1c11-4d9e-ace2-ff4b0d2ee396" />
<img width="1916" height="881" alt="image" src="https://github.com/user-attachments/assets/0d2cf80e-b5f2-4946-8f39-18b4c711d6ea" />
<img width="1912" height="592" alt="image" src="https://github.com/user-attachments/assets/16144a8e-583a-4fd7-b0df-efbaa76d9ae0" />
_An overall view of the ChronoBloom Phenology Explorer dashboard._


<img width="1910" height="846" alt="image" src="https://github.com/user-attachments/assets/4fbfd720-b05b-4f61-a77d-4e29f6c619c1" />


### Demonstration Video

[Watch the ChronoBloom Splunk Addon Prototype Demonstration Here!](https://tinyurl.com/Demonstrationlink)

---

## Installation Guide (Running Project Locally)

To set up and run the Splunk-ChronoBloom-Addon locally, follow these steps:

### 1. Install Splunk Enterprise

If you don't already have it, download and install Splunk Enterprise (Free Trial or Developer License) on your machine.

* **Download Splunk Enterprise:** Visit the official Splunk website to download the appropriate installer for your operating system: [Splunk Enterprise Downloads](https://www.splunk.com/en_us/download/splunk-enterprise.html)
* **Installation:** Follow the on-screen instructions provided by the installer. For most local setups, a "standalone" or "single instance" installation is sufficient. Make sure to note your Splunk username (default `admin`) and password.

### 2. Clone the Repository

Open your Git-enabled terminal or command prompt and clone this project repository:

```bash
git clone git@github.com:aryanpachore/Splunk-ChronoBloom-Addon.git
cd Splunk-ChronoBloom-Addon

3. Deploy the Splunk Add-on
Copy the contents of your cloned repository into the Splunk apps directory.

Navigate to Splunk Apps Directory:

Windows: C:\Program Files\Splunk\etc\apps\

Linux/macOS: /opt/splunk/etc/apps/

Copy the Add-on: Copy the entire Splunk-ChronoBloom-Addon folder (the one you cloned from GitHub, containing default/, bin/, README.md, etc.) into the Splunk apps directory.

4. Configure Gemini API Key and Splunk Credentials
Your prediction script needs access to your Gemini API key and Splunk credentials.

Create .env file: In the root directory of your Splunk-ChronoBloom-Addon folder (the one you cloned from GitHub), create a new file named .env.

Add Credentials: Paste the following into the .env file, replacing the placeholder values with your actual credentials:

GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
SPLUNK_HOST="localhost"
SPLUNK_PORT=8089
SPLUNK_USERNAME="admin"
SPLUNK_PASSWORD="YOUR_SPLUNK_PASSWORD_HERE"
Important: Add /.env to your .gitignore file to prevent accidentally pushing your API key and password to GitHub.

5. Install Python Dependencies
Navigate to the root directory of your Splunk-ChronoBloom-Addon project in your terminal/command prompt and install the necessary Python libraries:

Bash

pip install splunk-sdk google-generativeai python-dotenv
6. Create the 'predictions' Index in Splunk
Your prediction script will ingest data into a dedicated Splunk index.

Log in to Splunk Web: (usually http://localhost:8000).

Navigate: Go to Settings > Indexes.

Create New Index: Click New Index.

Index Name: Enter predictions (all lowercase).

Save: Click Save.

7. Restart Splunk
After placing the app files, configuring inputs.conf, and setting up the prediction index, you need to restart Splunk for all changes to take effect and for the data input scripts to begin running.

From Splunk Web: Go to Settings > Server controls and click Restart Splunk.

From Terminal/Command Prompt (as Administrator):

Windows: Navigate to C:\Program Files\Splunk\bin\ and run splunk restart.

Linux/macOS: Run sudo /opt/splunk/bin/splunk restart.

8. Verify Data Ingestion (ChronoBloom & Predictions)
Log in to Splunk Web: (usually http://localhost:8000).

Go to Search & Reporting:

ChronoBloom Data: Run index=main sourcetype=chronobloom (set time range to "All time"). You should see events from your chronobloom_input.py script.

AI Predictions: Run index=predictions sourcetype=chrono_predictions (set time range to "All time"). You should start seeing events from your gemini_prediction_script.py after its first run (check inputs.conf for its interval, typically 1 hour or 24 hours).

9. Access the Dashboard
Once data is flowing, navigate to the "Apps" menu in Splunk Web.

Click on your Splunk-ChronoBloom-Addon.

You should be directed to the "ChronoBloom Phenology Explorer" dashboard, which will now populate with your data and predictions!
