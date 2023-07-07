import React from "react";
import DefectVisualization from "./DefectVisualization";
import MergeRequestsDetails from "./MergeRequestsDetails";

function Dashboard() {
  return (
    <div>
      <DefectVisualization />
      <MergeRequestsDetails />
    </div>
  );
}

export default Dashboard;
