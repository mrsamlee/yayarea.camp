import datetime
import signal
import json
import sys
import os
import argparse
from dateutil.relativedelta import relativedelta
from dateutil import tz
from camply.search import SearchReserveCalifornia
from camply.containers import SearchWindow
from campsites_map import get_rec_to_campsites_map

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Search operation timed out")

def generate_monthly_search_windows(start_date, end_date):
    """
    Generate a list of monthly search windows between start_date and end_date.
    """
    search_windows = []
    current_date = start_date.replace(day=1)  # Start from first day of month
    
    while current_date <= end_date:
        # Calculate the last day of the current month
        if current_date.month == 12:
            next_month = current_date.replace(year=current_date.year + 1, month=1)
        else:
            next_month = current_date.replace(month=current_date.month + 1)
        
        month_end = next_month - datetime.timedelta(days=1)
        
        # Don't go beyond our end_date
        actual_end = min(month_end, end_date)
        
        # Only create window if it overlaps with our date range
        if current_date <= end_date and actual_end >= start_date:
            search_windows.append((current_date, actual_end))
        
        current_date = next_month
    
    return search_windows

def search_with_timeout(searcher, timeout_seconds=60):
    """
    Run the search with a timeout to prevent hanging.
    """
    # Set up timeout handler
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    
    try:
        results = searcher.get_matching_campsites()
        signal.alarm(0)  # Cancel the alarm
        return results
    except TimeoutError:
        print(f"Search timed out after {timeout_seconds} seconds")
        return []
    except Exception as e:
        signal.alarm(0)  # Cancel the alarm
        raise e
    finally:
        signal.signal(signal.SIGALRM, old_handler)

def build_campground_miles_lookup(camp_data):
    """
    Build a lookup dictionary for campground_id -> miles mapping.
    """
    lookup = {}
    for rec_area_id in camp_data.keys():
        for campground in camp_data.get(rec_area_id):
            lookup[campground.campground_id] = campground.miles
    return lookup

def get_campsite_miles(site, miles_lookup):
    """
    Get the miles from the lookup dictionary for a given site.
    """
    facility_id_str = str(site.facility_id)
    return miles_lookup.get(facility_id_str, 999)

def results_to_json(results, miles_lookup):
    """
    Convert search results to JSON format.
    """
    if not results:
        return []
    
    # Sort results by miles (distance) first
    results.sort(key=lambda site: get_campsite_miles(site, miles_lookup))
    
    json_results = []
    for site in results:
        miles = get_campsite_miles(site, miles_lookup)
        json_results.append({
            'facility_id': str(site.facility_id),
            'facility_name': site.facility_name,
            'recreation_area': site.recreation_area,
            'campsite_site_name': site.campsite_site_name,
            'booking_date': site.booking_date.strftime('%Y-%m-%d'),
            'booking_url': site.booking_url,
            'miles': miles
        })
    
    return json_results

def display_results(results, miles_lookup):
    """
    Display the search results in a formatted way.
    """
    if not results:
        print("No results to display.")
        return

    # Sort results by miles (distance) first
    results.sort(key=lambda site: get_campsite_miles(site, miles_lookup))
    
    # Group results by facility_id to show all available dates
    facility_groups = {}
    for site in results:
        facility_id = str(site.facility_id)
        if facility_id not in facility_groups:
            facility_groups[facility_id] = {
                'site_info': site,
                'dates': []
            }
        facility_groups[facility_id]['dates'].append(site.booking_date)
    
    print(f"\n=== FOUND {len(results)} AVAILABLE CAMPSITES (sorted by miles) ===")
    for facility_id, group in facility_groups.items():
        site = group['site_info']
        dates = group['dates']
        miles = get_campsite_miles(site, miles_lookup)
        
        # Format dates as a list
        date_list = [date.strftime('%Y-%m-%d') for date in sorted(set(dates))]
        dates_str = ', '.join(date_list)
        
        print(f"{site.recreation_area}, {site.facility_name} URL: {site.booking_url} (Miles: {miles}) (Dates: {dates_str})")

def save_results_to_json(results, miles_lookup, search_criteria, batch_name="default", append=False):
    """
    Save search results to results.json in the root folder.
    """
    json_results = results_to_json(results, miles_lookup)
    
    # Get current time in Pacific Time
    pacific_tz = tz.gettz('US/Pacific')
    pacific_time = datetime.datetime.now(pacific_tz)
    
    if append and os.path.exists('results.json'):
        # Load existing results and append
        with open('results.json', 'r') as f:
            existing_data = json.load(f)
        
        # Combine results
        combined_results = existing_data.get('results', []) + json_results
        total_results = len(combined_results)
        
        # Update with latest batch info
        output_data = {
            "last_updated": pacific_time.isoformat(),
            "last_updated_pst": pacific_time.strftime('%Y-%m-%d %I:%M %p %Z'),
            "total_results": total_results,
            "search_criteria": search_criteria,
            "batch_name": batch_name,
            "batch_results": len(results),
            "results": combined_results
        }
    else:
        # Create new results file
        output_data = {
            "last_updated": pacific_time.isoformat(),
            "last_updated_pst": pacific_time.strftime('%Y-%m-%d %I:%M %p %Z'),
            "total_results": len(results),
            "search_criteria": search_criteria,
            "batch_name": batch_name,
            "batch_results": len(results),
            "results": json_results
        }
    
    with open('results.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Results saved to results.json ({len(results)} campsites from {batch_name}) - {pacific_time.strftime('%Y-%m-%d %I:%M %p %Z')}")

def main():
    """
    Main function to run the campsite search and save results.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Search for campsite availability')
    parser.add_argument('--start-date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('--batch-name', type=str, default='default', help='Name for this batch (for logging)')
    
    args = parser.parse_args()
    
    print(f"Starting campsite search (Batch: {args.batch_name})...")
    
    camp_data = get_rec_to_campsites_map()
    
    # Build efficient lookup dictionary once
    miles_lookup = build_campground_miles_lookup(camp_data)

    # Search parameters - use command line args or defaults
    if args.start_date and args.end_date:
        start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d').date()
        print(f"Using provided dates: {start_date} to {end_date}")
    else:
        # Default behavior for backward compatibility
        start_date = datetime.date.today() + relativedelta(days=1)
        end_date = start_date + relativedelta(months=6)
        print(f"Using default dates: {start_date} to {end_date}")
    
    consecutive_nights = 2  # Look for 2 consecutive nights
    weekends_only = True    # Only search for weekend availability (Friday-Saturday)

    search_criteria = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "consecutive_nights": consecutive_nights,
        "weekends_only": weekends_only
    }

    print(f"Searching for {consecutive_nights} consecutive nights from {start_date} to {end_date}")
    if weekends_only:
        print("Weekends only: Friday-Saturday")

    # Collect all campground IDs
    campground_ids = []
    for rec_area_id in camp_data.keys():
        for campground in camp_data.get(rec_area_id):
            campground_ids.append(campground.campground_id)

    # Generate monthly search windows
    monthly_windows = generate_monthly_search_windows(start_date, end_date)
    print(f"Searching {len(monthly_windows)} monthly windows...")

    all_results = []
    
    try:
        for i, (window_start, window_end) in enumerate(monthly_windows, 1):
            if window_start == window_end:
                continue

            print(f"Searching month {i}/{len(monthly_windows)}: {window_start.strftime('%Y-%m-%d')} -> {window_end.strftime('%Y-%m-%d')}")
            
            # Create search window for this month
            search_window = SearchWindow(start_date=window_start, end_date=window_end)
            
            searcher = SearchReserveCalifornia(
                search_window=search_window,
                recreation_area=[],  # We're using specific campgrounds instead
                campgrounds=campground_ids,
                nights=consecutive_nights,  # Number of consecutive nights
                weekends_only=weekends_only  # Only search weekends
            )
            
            # Use timeout wrapper to prevent hanging (1 minute per month)
            try:
                month_results = search_with_timeout(searcher, timeout_seconds=60)
                month_results = [result for result in month_results if "Hike" not in result.campsite_site_name]
            except Exception as e:
                print(f"  Error during search for {window_start.strftime('%Y-%m')}: {e}")
                print(f"  Error type: {type(e).__name__}")
                month_results = []
            
            if month_results:
                all_results.extend(month_results)
                print(f"  Found {len(month_results)} sites for {window_start.strftime('%Y-%m')}")
                print(f"  Total results so far: {len(all_results)}")
            else:
                print(f"  No sites found for {window_start.strftime('%Y-%m')}")
        
        # Save results to JSON
        save_results_to_json(all_results, miles_lookup, search_criteria, args.batch_name, append=False)
        
        # Display results in console
        if all_results:
            display_results(all_results, miles_lookup)
        else:
            print("No campsites found matching criteria.")
            
    except TimeoutError as e:
        print(f"Search timed out: {e}")
        if all_results:
            print(f"\nPartial results found before timeout ({len(all_results)} sites):")
            save_results_to_json(all_results, miles_lookup, search_criteria, args.batch_name, append=False)
            display_results(all_results, miles_lookup)
    except ConnectionError as e:
        print(f"Network connection error: {e}")
        if all_results:
            print(f"\nPartial results found before connection error ({len(all_results)} sites):")
            save_results_to_json(all_results, miles_lookup, search_criteria, args.batch_name, append=False)
            display_results(all_results, miles_lookup)
    except Exception as e:
        print(f"Unexpected error during search: {e}")
        print(f"Error type: {type(e).__name__}")
        
        if all_results:
            print(f"\nPartial results found before error ({len(all_results)} sites):")
            save_results_to_json(all_results, miles_lookup, search_criteria, args.batch_name, append=False)
            display_results(all_results, miles_lookup)
        else:
            # No results at all - create empty results file
            print("No results found, creating empty results file...")
            save_results_to_json([], miles_lookup, search_criteria, args.batch_name, append=False)

if __name__ == "__main__":
    main()