import React, { useEffect, useState } from "react";
import axios from "axios";
import { DataGrid } from "@mui/x-data-grid";

const columns = [
  { field: "title", headerName: "Title", flex: 1 },
  { field: "author", headerName: "Author", flex: 1 },
  { field: "service_type", headerName: "Service Type", flex: 1 },
  { field: "create_date", headerName: "Create Date", flex: 0.8 },
  { field: "resolve_date", headerName: "Resolve Date", flex: 0.8 },
  { field: "defect_severity", headerName: "Defect Severity", flex: 1 },
  { field: "detected_by", headerName: "Detected By", flex: 1 },
  {
    field: "discussions",
    headerName: "Discussion Details",
    flex: 4,
    renderCell: (params) => {
      return (
        <div style={{ overflow: "auto" }}>
          {params.value.map((discussion, index) => (
            <p key={index}>
              <span className="font-semibold">
                [{discussion.defect_type_label}]
              </span>
              <span className="ml-1">[{discussion.defect_severity}]</span>
              <span className="ml-1">{discussion.detail}</span>
            </p>
          ))}
        </div>
      );
    },
  },
];

function MergeRequestsDetails() {
  const [mergeRequests, setMergeRequests] = useState([]);
  const [discussions, setDiscussions] = useState([]); // state variable to hold discussions

  useEffect(() => {
    axios
      .get("/merge_requests")
      .then((response) => setMergeRequests(response.data))
      .catch((error) =>
        console.error("Error fetching merge request data:", error)
      );
  }, []);

  return (
    <div style={{ height: "100%", width: "100%" }}>
      <DataGrid
        rows={mergeRequests}
        columns={columns}
        rowsPerPageOptions={[5, 10, 20]}
        getRowId={(row) => row.title}
        pagination
        rowHeight={100}
      />

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
