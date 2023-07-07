import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

function DefectVisualization() {
  const [defectData, setDefectData] = useState([]);
  const [interval, setInterval] = useState("Month");
  const [category, setCategory] = useState("Author");
  const [isLoading, setIsLoading] = useState(true);
  const lineChartContainer = useRef(null);
  const barChartContainer = useRef(null);
  const [lineChartInstance, setLineChartInstance] = useState(null);
  const [barChartInstance, setBarChartInstance] = useState(null);

  useEffect(() => {
    fetchDefectData();
  }, [interval, category]);

  const fetchDefectData = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("/defects", {
        params: {
          interval: interval,
          category: category,
        },
      });
      setDefectData(response.data);
      setIsLoading(false);
    } catch (error) {
      console.error("Error fetching defect data:", error);
    }
  };

  useEffect(() => {
    if (lineChartContainer && lineChartContainer.current) {
      if (lineChartInstance) {
        lineChartInstance.destroy();
      }

      if (category === "Trending") {
        const sortedData = defectData.sort((a, b) => a.interval - b.interval); // Sort data based on 'interval' field
        const labels = sortedData.map((item) => item.interval);
        const data = sortedData.map((item) => item.count);

        const newLineChartInstance = new Chart(lineChartContainer.current, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Total Defects",
                data: data,
                fill: false,
                borderColor: "rgba(255, 99, 132, 0.2)",
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true, // Start the y-axis from 0
              },
            },
          },
        });

        setLineChartInstance(newLineChartInstance);
      }
    }

    if (barChartContainer && barChartContainer.current) {
      if (barChartInstance) {
        barChartInstance.destroy();
      }

      if (category !== "Trending") {
        const groupedData = defectData.reduce((accumulator, item) => {
          const key = item.category;
          if (!accumulator[key]) {
            accumulator[key] = 0;
          }
          accumulator[key] += item.count;
          return accumulator;
        }, {});

        const labels = Object.keys(groupedData);
        const data = Object.values(groupedData);

        const newBarChartInstance = new Chart(barChartContainer.current, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                label: category,
                data: data,
                backgroundColor: "rgba(255, 99, 132, 0.2)",
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true, // Start the y-axis from 0
              },
            },
          },
        });

        setBarChartInstance(newBarChartInstance);
      }
    }
  }, [lineChartContainer, barChartContainer, defectData]);

  return isLoading ? (
    <div>Loading...</div>
  ) : (
    <div className="flex flex-row items-start justify-center">
      <div className="flex flex-col items-center mr-4 pr-4">
        <div className="flex flex-row items-center mb-4">
          <label htmlFor="interval" className="mr-2">
            Interval:
          </label>
          <select
            id="interval"
            value={interval}
            onChange={(e) => setInterval(e.target.value)}
            className="border border-gray-300 rounded-md p-1"
          >
            <option value="Year">Year</option>
            <option value="Quarter">Quarter</option>
            <option value="Month">Month</option>
            <option value="Week">Week</option>
          </select>
        </div>
        {category === "Trending" ? (
          <div className="w-full max-w-3xl mb-4">
            <canvas ref={lineChartContainer} className="w-120 h-96" />
          </div>
        ) : (
          <div className="w-full max-w-3xl mb-4">
            <canvas ref={barChartContainer} className="w-120 h-96" />
          </div>
        )}
      </div>
      <div className="flex flex-col items-center pr-4">
        <div className="flex flex-row items-center mb-4">
          <label htmlFor="category" className="mr-2">
            Category:
          </label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="border border-gray-300 rounded-md p-1"
          >
            <option value="Trending">Trending</option>
            <option value="Defect Type">Defect Type</option>
            <option value="Defect Severity">Defect Severity</option>
            <option value="Author">Author</option>
            <option value="Detected by">Detected by</option>
            <option value="Service">Service</option>
          </select>
        </div>
      </div>
    </div>
  );
}

export default DefectVisualization;
