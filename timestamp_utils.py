import datetime
import re

def convert_relative_to_exact_timestamp(timestamp_string):
    try:
        # Attempt to parse the timestamp as an exact datetime
        exact_timestamp = datetime.datetime.strptime(timestamp_string, '%d/%m/%Y, lúc: %H giờ %M phút')
        exact_timestamp = exact_timestamp.replace(microsecond=0)  # Remove milliseconds
        return exact_timestamp
    except ValueError:
        # If parsing as an exact datetime fails, check if it's a relative timestamp
        if "trước" in timestamp_string:
            # Get the numerical value (e.g., 1 in "about 1 hour ago")
            match = re.search(r'\d+', timestamp_string)
            if match:
                num_value = int(match.group())
                # Define time deltas for different relative time units
                if "giờ" in timestamp_string:
                    time_delta = datetime.timedelta(hours=num_value)
                elif "ngày" in timestamp_string:
                    time_delta = datetime.timedelta(days=num_value)
                elif "tuần" in timestamp_string:
                    time_delta = datetime.timedelta(weeks=num_value)
                elif "phút" in timestamp_string:
                    time_delta = datetime.timedelta(minutes=num_value)
                else:
                    # For other relative time units, assume it's a day ago
                    time_delta = datetime.timedelta(days=1)
                # Calculate the exact timestamp based on the relative time
                exact_timestamp = datetime.datetime.now() - time_delta
                exact_timestamp = exact_timestamp.replace(microsecond=0)  # Remove milliseconds
                return exact_timestamp
        elif "Vừa xong" in timestamp_string:
            # If the timestamp says "Vừa xong," set it to the current time
            exact_timestamp = datetime.datetime.now()
            exact_timestamp = exact_timestamp.replace(microsecond=0)  # Remove milliseconds
            return exact_timestamp
                
        # Return None if it's neither an exact nor a recognized relative timestamp
        return None



