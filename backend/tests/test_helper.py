import unittest
import sys
sys.path.append('/Users/vinhpham/Desktop/code-review-dashboard/backend')
from controller import helper

class TestHelper(unittest.TestCase):
    def test_extract_info_from_title(self):
        title = "[Service] General information of merge request"
        service, general_info = helper.extract_info_from_title(title)
        self.assertEqual(service, "Service")
        self.assertEqual(general_info, "General information of merge request")

        title = "General information of merge request without service"
        service, general_info = helper.extract_info_from_title(title)
        self.assertIsNone(service)
        self.assertEqual(general_info, "General information of merge request without service")

    def test_extract_info_from_discussion(self):
        discussion = {
            "defect_severity": "Medium",
            "defect_type_label": "Security",
            "detail": "Discussing the security implications of the bug fix is crucial to ensure that the patch not only addresses the issue at hand, but also does not introduce any new vulnerabilities or weaken existing security measures. It is important to thoroughly analyze and test the fix in a controlled environment before deploying it to production systems."
        }

        # Pack the details into a single string as your function would expect
        discussion_string = f'[{discussion["defect_type_label"]}] [{discussion["defect_severity"]}] {discussion["detail"]}'

        defect_type_label, defect_severity, detail = helper.extract_info_from_discussion(discussion_string)
        
        self.assertEqual(defect_type_label, discussion["defect_type_label"])
        # self.assertEqual(defect_severity, discussion["defect_severity"])
        self.assertEqual(detail, discussion["detail"])
        # Add more test cases for different input scenarios

if __name__ == "__main__":
    unittest.main()
