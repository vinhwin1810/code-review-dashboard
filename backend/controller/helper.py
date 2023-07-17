import re


defect_type_labels = [
    "CD::Code Readability Problem", "CD::Conformance Problem", 
    "CD::Data Error Problem", "CD::Error Handling Problem", 
    "CD::Inconsistent Requirements", "CD::Interface Problem", 
    "CD::Logical Problem", "CD::Memory Problem", 
    "CD::Performance Problem", "CD::Resuability Problem"
]

defect_severity = ["DS::Critical", "DS::Major", "DS::Minor"]

def extract_info_from_title(title):
    # Assuming the title is in the format "[Service] General information of merge request"
    try:
        parts = title.split('] ')
        service = parts[0][1:]  # Remove the opening bracket
        general_info = parts[1]
    except IndexError:
        # If the title does not follow the expected format, return default values
        service = ""
        general_info = title
    return service, general_info


def extract_info_from_note(note):
    pattern = r'\[(.*?)\] \[(.*?)\] (.*)'
    match = re.match(pattern, note)
    
    if match:
        defect_type_label, defect_severity_label, detail_of_discussion = match.groups()
        # Check if defect_type_label and defect_severity_label are in their respective lists
        if defect_type_label not in defect_type_labels:
            defect_type_label = "Unknown"
        if defect_severity_label not in defect_severity:
            defect_severity_label = "Unknown"
        return defect_type_label, defect_severity_label, detail_of_discussion
    else:
        return None