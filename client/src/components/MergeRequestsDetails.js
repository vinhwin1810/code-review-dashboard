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
    field: "detail",
    headerName: "Discussion Details",
    flex: 4,
  },
];

function MergeRequestsDetails() {
  const [mergeRequests, setMergeRequests] = useState([]);

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_URL}/merge_requests`)
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
        getRowId={(row) => `${row.title}_${row.create_date}`}
        pagination
        rowHeight={100}
      />
    </div>
  );
}

export default MergeRequestsDetails;
