#!/usr/bin/env python3
"""ChronoBloom Input Script for Splunk
Fetches phenological data from USA-NPN API
"""
import sys
import os
import json
import time
import logging
from datetime import datetime, timedelta

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chronobloom_api import ChronoBloomAPI
    from chronobloom_simulator import ChronoBloomSimulator
except ImportError:
    # Fallback imports if modules aren't available
    ChronoBloomAPI = None
    ChronoBloomSimulator = None

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('chronobloom_input')

class ChronoBloomInput:
    def __init__(self, config):
        self.config = config
        self.api = ChronoBloomAPI(config.get('api_key', '')) if ChronoBloomAPI else None
        self.simulator = ChronoBloomSimulator() if ChronoBloomSimulator else None

    def run(self):
        """Main execution loop"""
        try:
            # Parse configuration
            species_ids = self.parse_ids(self.config.get('species_ids', '3,35,52'))
            phenophase_ids = self.parse_ids(self.config.get('phenophase_ids', '373,501,390'))
            states = self.parse_states(self.config.get('states', ''))

            # Fetch data
            data = self.fetch_data(species_ids, phenophase_ids, states)

            # Output to Splunk
            for observation in data:
                self.output_event(observation)

        except Exception as e:
            logger.error(f"Error in ChronoBloom input: {e}")
            # Generate at least one test event
            self.output_test_event()

    def parse_ids(self, id_string):
        """Parse comma-separated IDs"""
        if not id_string:
            return []
        return [int(x.strip()) for x in id_string.split(',') if x.strip()]

    def parse_states(self, state_string):
        """Parse comma-separated state codes"""
        if not state_string:
            return []
        return [x.strip().upper() for x in state_string.split(',') if x.strip()]

    def fetch_data(self, species_ids, phenophase_ids, states):
        """Fetch phenological data"""
        # For now, generate test data
        return self.generate_test_data(species_ids, phenophase_ids, states)

    def generate_test_data(self, species_ids, phenophase_ids, states):
        """Generate test data for verification"""
        import random

        species_names = {3: 'Red maple', 35: 'American robin', 52: 'Lilac'}
        phenophase_names = {373: 'First leaf', 501: 'First flower', 390: 'Full bloom'}

        data = []
        for i in range(5):  # Generate 5 test observations
            species_id = random.choice(species_ids) if species_ids else 3
            phenophase_id = random.choice(phenophase_ids) if phenophase_ids else 373
            state = random.choice(states) if states else 'CA'

            observation = {
                'observation_id': f'test_{int(time.time())}_{i}',
                'species_id': species_id,
                'species_name': species_names.get(species_id, f'Species_{species_id}'),
                'phenophase_id': phenophase_id,
                'phenophase_name': phenophase_names.get(phenophase_id, f'Phenophase_{phenophase_id}'),
                'observation_date': datetime.now().strftime('%Y-%m-%d'),
                'observation_date_time': int(time.time()),
                'latitude': round(random.uniform(32.0, 42.0), 6),
                'longitude': round(random.uniform(-120.0, -100.0), 6),
                'state': state,
                'site_name': f'Test Site {i+1}',
                'phenophase_status': random.choice([0, 1]),
                'intensity_value': random.choice(['', 'Low', 'Medium', 'High']),
                'data_source': 'TEST',
                'collection_timestamp': datetime.now().isoformat()
            }
            data.append(observation)

        return data

    def output_event(self, observation):
        """Output event to Splunk"""
        # Simple JSON output for Splunk
        print(json.dumps(observation))
        sys.stdout.flush()

    def output_test_event(self):
        """Output a basic test event"""
        test_event = {
            'observation_id': f'test_{int(time.time())}',
            'species_id': 3,
            'species_name': 'Test Species',
            'phenophase_id': 373,
            'phenophase_name': 'Test Phenophase',
            'observation_date': datetime.now().strftime('%Y-%m-%d'),
            'observation_date_time': int(time.time()),
            'latitude': 37.7749,
            'longitude': -122.4194,
            'state': 'CA',
            'site_name': 'Test Site',
            'phenophase_status': 1,
            'intensity_value': 'Test',
            'data_source': 'TEST',
            'collection_timestamp': datetime.now().isoformat()
        }
        self.output_event(test_event)

def main():
    """Main entry point"""
    try:
        # Read configuration
        config = {
            'species_ids': '3,35,52',
            'phenophase_ids': '373,501,390',
            'states': 'CA,NY,TX',
            'api_key': ''
        }

        # Override with command line arguments
        for arg in sys.argv[1:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                config[key] = value

        # Create and run input
        input_handler = ChronoBloomInput(config)
        input_handler.run()

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        # Still output something for testing
        test_event = {
            'error': str(e),
            'timestamp': int(time.time()),
            'data_source': 'ERROR'
        }
        print(json.dumps(test_event))

if __name__ == '__main__':
    main()