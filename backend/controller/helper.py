def extract_info_from_title(title):
    # Assuming the title is in the format "[Service] General information of merge request"
    try:
        parts = title.split('] ')
        service = parts[0][1:]  # Remove the opening bracket
        general_info = parts[1]
    except IndexError:
        # If the title does not follow the expected format, return default values
        service = "Unknown"
        general_info = title
    return service, general_info


def extract_info_from_changes(changes):
    # List to hold all defects
    defects = []

    # Iterate through each change
    for change in changes['changes']:
        # Extract file path
        file_path = change['new_path']

        # Iterate through each diff line
        for i, line in enumerate(change['diff'].split('\n')):
            # Look for lines starting with '+', which represent additions in the diff
            if line.startswith('+'):
                # Extract line number (assuming it starts from 1)
                line_number = i + 1

                # Add defect to the list
                defect = f"{file_path}:{line_number}:{line}"
                defects.append(defect)

    # Join all defects into a single string
    defects_str = "\n".join(defects)
    return defects_str



def extract_info_from_note(note):
    # Check if the note's body follows the expected format
    try:
        parts = note.body.split('] ')
        defect_type_label = parts[0][1:]  # Remove the opening bracket
        defect_severity = parts[1]
        detail = parts[2]
    except IndexError:
        # If the note's body does not follow the expected format, return default values
        defect_type_label = "Unknown"
        defect_severity = "Unknown"
        detail = note.body
    return defect_type_label, defect_severity, detail
