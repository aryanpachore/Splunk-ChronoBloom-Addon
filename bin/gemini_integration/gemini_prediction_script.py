import os
import splunklib.client as splunk_client
from splunklib.results import JSONResultsReader
import google.generativeai as genai
from dotenv import load_dotenv
import json
import datetime
import sys

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Splunk Connection Details
# IMPORTANT: For production, avoid hardcoding passwords.
# Consider using Splunk's credential store or environment variables for sensitive info.
SPLUNK_HOST = os.getenv("SPLUNK_HOST", "localhost") # Default to localhost if not in .env
SPLUNK_PORT = int(os.getenv("SPLUNK_PORT", 8089)) # Default to 8089 if not in .env
SPLUNK_USERNAME = os.getenv("SPLUNK_USERNAME", "") # Default to admin if not in .env
SPLUNK_PASSWORD = os.getenv("SPLUNK_PASSWORD", "") # *** REPLACE WITH YOUR SPLUNK ADMIN PASSWORD ***

# Gemini API Key (loaded from .env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.", file=sys.stderr)
    print("Please create a .env file in your project root with GEMINI_API_KEY=\"YOUR_KEY\"", file=sys.stderr)
    sys.exit(1) # Exit if API key is missing

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "models/gemini-1.5-flash-latest" # Or "gemini-1.5-pro-latest" if available and preferred, check API docs for current models

def log_message(message, level="INFO"):
    """Helper function for consistent logging."""
    print(f"[{datetime.datetime.now().isoformat()}] [{level}] {message}")

def fetch_splunk_data():
    """
    Fetches recent phenophase data from Splunk that Gemini can use for predictions.
    Customize the SPL search query to retrieve relevant features for your predictions.
    """
    log_message("Attempting to connect to Splunk and fetch data...")
    try:
        service = splunk_client.connect(
            host=SPLUNK_HOST,
            port=SPLUNK_PORT,
            username=SPLUNK_USERNAME,
            password=SPLUNK_PASSWORD
        )

        # --- CUSTOMIZE YOUR SPLUNK SEARCH HERE ---
        # Added 'search ' at the beginning to explicitly define it as a search command
        search_query = """
        search index=main sourcetype=chronobloom phenophase_status=1
        """
        # Define the time range for the Splunk search (e.g., last 30 days)
        kwargs_export = {"earliest_time": "0", "latest_time": "now", "output_mode": "json"}
        search_results = service.jobs.export(search_query, **kwargs_export)

        reader = JSONResultsReader(search_results)
        data = [entry for entry in reader]
        log_message(f"Fetched {len(data)} records from Splunk.")
        return data

    except Exception as e:
        log_message(f"Error fetching data from Splunk: {e}", level="ERROR")
        return None

def generate_gemini_prediction(pheno_data):
    """
    Sends phenological data to Gemini for prediction.
    The quality of the prediction is highly dependent on the prompt.
    """
    if not pheno_data:
        log_message("No phenological data provided to Gemini for prediction.", level="WARNING")
        return [{"error": "No data available for prediction."}]

    log_message(f"Preparing prompt for Gemini with {len(pheno_data)} data points...")

    # --- CRITICAL: CUSTOMIZE YOUR GEMINI PROMPT ---
    # This is the most important part for getting useful predictions.
    # Be explicit about:
    # 1. Your role (e.g., "AI phenology expert")
    # 2. The data format you're providing.
    # 3. What kind of prediction you need (species, phenophase, location, time horizon).
    # 4. The desired output format (e.g., JSON structure).
    # 5. Any constraints or assumptions.

    # Convert the list of Splunk data dictionaries to a JSON string for the prompt
    data_summary_json = json.dumps(pheno_data, indent=2)

    prompt_text = f"""
    You are an AI assistant specializing in agricultural phenological predictions, providing actionable insights for farmers.
    Below is a JSON array of recent phenological observations. Each observation includes:
    - `_time`: Splunk event timestamp.
    - `observation_date`: The recorded date of the observation (YYYY-MM-DD).
    - `species_name`: The name of the plant or animal species (e.g., "Lilac", "Red maple", "American robin").
    - `phenophase_name`: The specific phenophase observed (e.g., "First flower", "Full bloom", "First leaf", "First arrival").
    - `phenophase_status`: 1 for observed.
    - `state`: The US State where the observation was made (e.g., "NY", "CA", "TX").
    - `site_name`: The name of the observation site.
    - `latitude`, `longitude`: Geographic coordinates of the observation.

    **Recent Phenological Observations Data:**
    ```json
    {data_summary_json}
    ```

    Based on this historical and recent phenological data, predict the following key dates for the **upcoming (next) season** (assuming the next natural cycle based on current date):

    1.  **For Lilac in New York:** What is the most probable "First flower" date?
    2.  **For Red maple in California:** What is the most probable "First leaf" date?
    3.  **For American robin in Texas:** What is the most probable "First arrival" date for nesting behavior?

    **Provide your predictions as a JSON array of objects, strictly adhering to the following structure:**

    ```json
    [
      {{
        "predicted_species": "Lilac",
        "predicted_phenophase": "First flower",
        "predicted_state": "New York",
        "predicted_date": "YYYY-MM-DD",
        "confidence_score": 0.X,  // Optional: A confidence score between 0.0 and 1.0 (if deducible)
        "notes": "Any specific reasoning or assumptions made for this prediction, e.g., 'assuming average spring temperatures.'"
      }},
      {{
        "predicted_species": "Red maple",
        "predicted_phenophase": "First leaf",
        "predicted_state": "California",
        "predicted_date": "YYYY-MM-DD",
        "confidence_score": 0.X,
        "notes": "..."
      }},
      {{
        "predicted_species": "American robin",
        "predicted_phenophase": "First arrival",
        "predicted_state": "Texas",
        "predicted_date": "YYYY-MM-DD",
        "confidence_score": 0.X,
        "notes": "..."
      }}
    ]
    ```
    If you cannot make a reasonable prediction for a specific item, state "Cannot predict" in the `predicted_date` field and provide a reason in `notes`.
    """

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        # For long prompts, consider using generate_content(contents=[{"role": "user", "parts": [{ "text": prompt_text }]}]).
        # Also, check token limits for the chosen model.
        response = model.generate_content(prompt_text)
        prediction_text = response.text
        log_message(f"Gemini raw response received. Attempting to parse JSON:\n{prediction_text[:500]}...", level="DEBUG") # Log first 500 chars

        # Attempt to parse the response as JSON.
        # Gemini sometimes includes conversational text before/after JSON,
        # so robust parsing might be needed for production.
        try:
            # Find the first and last curly brace to isolate the JSON array
            json_start = prediction_text.find('[')
            json_end = prediction_text.rfind(']')
            if json_start != -1 and json_end != -1 and json_end > json_start:
                json_string = prediction_text[json_start : json_end + 1]
                predictions = json.loads(json_string)
                log_message("Successfully parsed Gemini response as JSON.")
                return predictions
            else:
                raise json.JSONDecodeError("JSON array delimiters not found or invalid.", prediction_text, 0)
        except json.JSONDecodeError as e:
            log_message(f"Gemini response was not a valid JSON array. Error: {e}", level="ERROR")
            log_message(f"Raw Gemini output: {prediction_text}", level="ERROR")
            return [{"error": "Gemini response not parsable as JSON array.", "raw_response": prediction_text}]

    except Exception as e:
        log_message(f"Error calling Gemini API: {e}", level="ERROR")
        return [{"error": f"Failed to get prediction from Gemini: {e}"}]

def ingest_predictions_to_splunk(predictions):
    """
    Ingests the prediction results back into Splunk.
    Each prediction will be a separate event in the 'predictions' index.
    """
    if not predictions:
        log_message("No predictions to ingest to Splunk.", level="WARNING")
        return

    log_message(f"Attempting to ingest {len(predictions)} predictions to Splunk...")
    try:
        service = splunk_client.connect(
            host=SPLUNK_HOST,
            port=SPLUNK_PORT,
            username=SPLUNK_USERNAME,
            password=SPLUNK_PASSWORD
        )

        # Ensure the 'predictions' index exists in Splunk.
        # This script won't create it, so ensure it's manually created in Splunk Web if not present.
        if "predictions" not in service.indexes:
            log_message("Splunk index 'predictions' does not exist. Please create it in Splunk Web (Settings > Indexes).", level="ERROR")
            return

        myindex = service.indexes["predictions"]

        for pred in predictions:
            # Add a timestamp and source info for Splunk events.
            # Embed the entire prediction dictionary as a JSON string for easy parsing with spath in Splunk.
            event_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "source": "gemini_prediction_script",
                "sourcetype": "chrono_predictions",
                "prediction": pred # Embed the prediction object here
            }
            # Submit the event as a JSON string to Splunk
            myindex.submit(json.dumps(event_data), sourcetype="chrono_predictions", host=SPLUNK_HOST)
        log_message(f"Successfully ingested {len(predictions)} predictions to Splunk's 'predictions' index.")
    except Exception as e:
        log_message(f"Error ingesting data to Splunk: {e}", level="ERROR")

if __name__ == "__main__":
    log_message("Starting Gemini Prediction Script.")
    
    # Configure Gemini (this line should already be there)
    genai.configure(api_key=GEMINI_API_KEY)

    

    # MODEL_NAME is defined globally, not inside main, but ensure it's set to "gemini-pro"
    # (The script will attempt to use this model after listing others)

    pheno_data = fetch_splunk_data()

    if pheno_data:
        predictions = generate_gemini_prediction(pheno_data)

        if predictions and not any("error" in p for p in predictions):
            ingest_predictions_to_splunk(predictions)
            log_message("Gemini Prediction process completed successfully.")
        else:
            log_message("Failed to generate valid predictions or an error occurred during prediction. Check logs above for details.", level="ERROR")
    else:
        log_message("No data fetched from Splunk to generate predictions. Aborting.", level="WARNING")
    log_message("Gemini Prediction Script finished.")
