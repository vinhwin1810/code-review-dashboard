def extract_info_from_title(title):
    # Assuming the title is in the format "[Service] General information of merge request"
    parts = title.split('] ')
    service = parts[0][1:]  # Remove the opening bracket
    general_info = parts[1]
    return service, general_info

def extract_info_from_discussion(discussion):
    # Assuming the discussion is in the format "[Defect Type Label] [Defect Severity] Detail of discussion"
    parts = discussion.split('] ')
    defect_type_label = parts[0][1:]  # Remove the opening bracket
    defect_severity, detail = parts[1].split('] ')
    return defect_type_label, defect_severity, detail