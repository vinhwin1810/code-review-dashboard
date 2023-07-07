import React, { useEffect, useState } from "react";
import axios from "axios";

function MergeRequestsDetails() {
  const [mergeRequests, setMergeRequests] = useState([]);
  const [discussions, setDiscussions] = useState([]); // state variable to hold discussions
  const [selectedMR, setSelectedMR] = useState(null); // state variable to hold the selected MR

  useEffect(() => {
    axios
      .get("/merge_requests")
      .then((response) => setMergeRequests(response.data))
      .catch((error) =>
        console.error("Error fetching merge request data:", error)
      );
  }, []);

  const handleRowClick = (mr) => {
    setSelectedMR(mr);
    axios
      .get(`/merge_requests/${mr.id}/discussions`)
      .then((response) => setDiscussions(response.data))
      .catch((error) =>
        console.error(
          `Error fetching discussions for merge request ${mr.id}:`,
          error
        )
      );
  };

  return (
    <div>
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Title
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Author
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Service Type
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Create Date
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Resolve Date
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Defect Severity
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Detected By
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Discussion Details
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {mergeRequests.map((mr, index) => (
            <tr
              key={index}
              onClick={() => handleRowClick(mr)}
              className="cursor-pointer hover:bg-gray-200"
            >
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {mr.title}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {mr.author}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {mr.service_type}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {mr.create_date}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {mr.resolve_date}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {mr.defect_severity}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {mr.detected_by}
              </td>
              <td className="px-6 py-4 whitespace-normal text-sm text-gray-500 max-h-[100px] overflow-auto">
                {mr.discussions.map((discussion, index) => (
                  <p key={index} className="mb-2">
                    <span className="font-semibold">
                      [{discussion.defect_type_label}]
                    </span>
                    <span className="ml-1">[{discussion.defect_severity}]</span>
                    <span className="ml-1">{discussion.detail}</span>
                  </p>
                ))}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-8">
        {discussions.map((discussion, index) => (
          <div
            key={index}
            className="mb-4 p-4 border rounded shadow-sm bg-white"
          >
            <span className="inline-block mr-2 px-2 py-1 text-xs font-semibold text-white bg-green-500 rounded">
              {discussion.defect_type_label}
            </span>
            <span className="inline-block mr-2 px-2 py-1 text-xs font-semibold text-white bg-red-500 rounded">
              {discussion.defect_severity}
            </span>
            <p className="mt-2 text-gray-700">{discussion.detail}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MergeRequestsDetails;
