#!/usr/bin/env python3
"""Space Mission Telemetry Parser - Professional data parsing and analysis tool."""

import xml.etree.ElementTree as ET
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


def parse_xml_file(file_path: str) -> Optional[ET.Element]:
    """Parse XML file and return root element."""
    try:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File '{file_path}' not found.")
        tree = ET.parse(file_path)
        print(f"✓ Successfully parsed: {file_path}")
        return tree.getroot()
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return None
    except ET.ParseError as e:
        print(f"✗ XML parsing error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return None


def extract_mission_data(root: ET.Element) -> List[Dict]:
    """Extract structured mission data from XML."""
    missions = []
    
    for mission in root.findall('mission'):
        mission_data = {
            'id': mission.get('id'),
            'status': mission.get('status'),
            'name': mission.find('name').text,
            'agency': mission.find('agency').text,
            'launch_date': mission.find('launch_date').text,
            'destination': mission.find('destination').text,
            'distance_au': float(mission.find('current_distance_au').text),
            'mission_type': mission.find('mission_type').text,
            'description': mission.find('description').text,
        }
        
        instruments = []
        for instrument in mission.find('instruments').findall('instrument'):
            instruments.append({
                'id': instrument.get('id'),
                'name': instrument.find('name').text,
                'type': instrument.find('type').text,
                'status': instrument.find('status').text,
                'power_watts': float(instrument.find('power_consumption_watts').text)
            })
        mission_data['instruments'] = instruments
        
        telemetry = []
        for reading in mission.find('telemetry_data').findall('reading'):
            telemetry.append({
                'timestamp': reading.get('timestamp'),
                'parameter': reading.find('parameter').text,
                'value': float(reading.find('value').text),
                'unit': reading.find('unit').text
            })
        mission_data['telemetry'] = telemetry
        
        comm = mission.find('communication')
        mission_data['communication'] = {
            'signal_strength_db': float(comm.find('signal_strength_db').text),
            'data_rate_bps': float(comm.find('data_rate_bps').text),
            'light_time_hours': float(comm.find('round_trip_light_time_hours').text)
        }
        
        missions.append(mission_data)
    
    return missions


def display_mission_summary(missions: List[Dict]) -> None:
    """Display formatted summary of all missions."""
    print("\n" + "="*80)
    print(f"{'SPACE MISSION TELEMETRY REPORT':^80}")
    print("="*80)
    print(f"\nTotal Active Missions: {len(missions)}")
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    for i, mission in enumerate(missions, 1):
        print(f"\n{'─'*80}")
        print(f"Mission {i}: {mission['name']} ({mission['id']})")
        print(f"{'─'*80}")
        print(f"  Status:       {mission['status'].upper()}")
        print(f"  Agency:       {mission['agency']}")
        print(f"  Launch Date:  {mission['launch_date']}")
        print(f"  Destination:  {mission['destination']}")
        print(f"  Distance:     {mission['distance_au']:.2f} AU from Earth")
        print(f"  Type:         {mission['mission_type'].replace('_', ' ').title()}")
        print(f"\n  Description:\n    {mission['description']}")
        
        print(f"\n  Instruments ({len(mission['instruments'])} total):")
        for inst in mission['instruments']:
            print(f"    • {inst['name']} ({inst['type']}) - {inst['status']} - {inst['power_watts']}W")
        
        print(f"\n  Latest Telemetry ({len(mission['telemetry'])} readings):")
        for reading in mission['telemetry']:
            print(f"    • {reading['parameter']}: {reading['value']} {reading['unit']}")
        
        print(f"\n  Communication Status:")
        comm = mission['communication']
        print(f"    • Signal Strength: {comm['signal_strength_db']} dB")
        print(f"    • Data Rate: {comm['data_rate_bps']:,.0f} bps")
        print(f"    • Round-trip Light Time: {comm['light_time_hours']:.3f} hours")
    
    print("\n" + "="*80 + "\n")


def export_to_json(missions: List[Dict], output_path: str) -> bool:
    """Export mission data to JSON file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(missions, f, indent=2, ensure_ascii=False)
        print(f"✓ Data successfully exported to: {output_path}")
        return True
    except IOError as e:
        print(f"✗ Error writing JSON file: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point - handles CLI arguments and orchestrates workflow."""
    parser = argparse.ArgumentParser(
        description='Parse and analyze space mission telemetry data from XML files.',
        epilog='Example: python parse_data.py data/missions.xml --export output.json'
    )
    
    parser.add_argument('input_file', type=str, help='Path to XML file with mission data')
    parser.add_argument('--export', type=str, metavar='OUTPUT_FILE', 
                       help='Export parsed data to JSON file')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    root = parse_xml_file(args.input_file)
    if root is None:
        sys.exit(1)
    
    missions = extract_mission_data(root)
    
    if not missions:
        print("✗ No mission data found in XML file.", file=sys.stderr)
        sys.exit(1)
    
    display_mission_summary(missions)
    
    if args.export:
        if not export_to_json(missions, args.export):
            sys.exit(1)
    
    print("✓ Processing complete!")


if __name__ == '__main__':
    main()