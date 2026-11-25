
"use strict";

const form = document.getElementById("predictionForm");
const submitButton = document.getElementById("submitButton");
const errorMessage = document.getElementById("errorMessage");
const resultSection = document.getElementById("result");
const riskLevel = document.getElementById("riskLevel");
const probabilitiesContainer = document.getElementById("probabilities");

// API endpoint
const API_URL = "/predict";

// Input field configuration
const FIELD_IDS = [
 "Age",
 "SystolicBP",
 "DiastolicBP",
 "BS",
 "BodyTemp",
 "HeartRate",
];

// Collect patient measurements
function getPatientData() {
 const data = {};

 for (const field of FIELD_IDS) {
  const input = document.getElementById(field);

  if (!input || input.value.trim() === "") {
   throw new Error(`Please enter ${field}.`);
  }

  const value = Number(input.value);

  if (!Number.isFinite(value)) {
   throw new Error(`Invalid value for ${field}.`);
  }

  data[field] = value;
 }

 return data;
}

// Validate input against backend schema
function validatePatientData(data) {
 const checks = [
  ["Age", data.Age > 0 && data.Age < 120],
  ["Age", Number.isInteger(data.Age)],
  ["SystolicBP", data.SystolicBP > 30 && data.SystolicBP < 300],
  ["SystolicBP", Number.isInteger(data.SystolicBP)],
  ["DiastolicBP", data.DiastolicBP > 20 && data.DiastolicBP < 200],
  ["DiastolicBP", Number.isInteger(data.DiastolicBP)],
  ["BS", data.BS > 1 && data.BS < 35],
  ["BodyTemp", data.BodyTemp > 85 && data.BodyTemp < 110],
  ["HeartRate", data.HeartRate > 25 && data.HeartRate < 250],
  ["HeartRate", Number.isInteger(data.HeartRate)],
 ];

 for (const [field, valid] of checks) {
  if (!valid) {
   throw new Error(`Invalid ${field}. Please check the allowed range.`);
  }
 }

 if (data.SystolicBP <= data.DiastolicBP) {
  throw new Error(
   "Systolic blood pressure must be greater than diastolic blood pressure."
  );
 }
}

// Clear previous messages and results
function clearResult() {
 errorMessage.textContent = "";
 resultSection.style.display = "none";
 riskLevel.textContent = "";
 probabilitiesContainer.replaceChildren();
}

// Show error message
function showError(message) {
 errorMessage.textContent = message;
}

// Update loading state
function setLoading(isLoading) {
 submitButton.disabled = isLoading;

 submitButton.textContent = isLoading
  ? "Analyzing Patient Data..."
  : "Predict Maternal Health Risk";
}

// Format risk category
function formatRiskLevel(level) {
 return String(level)
  .trim()
  .toLowerCase()
  .replace(/\b\w/g, char => char.toUpperCase());
}

// Display prediction result
function displayPrediction(data) {
 if (
  typeof data.risk_level !== "string" ||
  !data.probabilities ||
  typeof data.probabilities !== "object" ||
  Array.isArray(data.probabilities)
 ) {
  throw new Error("The API returned an invalid prediction response.");
 }

 const risk = data.risk_level.trim().toLowerCase();

 const riskColors = {
  "low risk": "#16a34a",
  "mid risk": "#d97706",
  "high risk": "#dc2626",
 };

 riskLevel.textContent = formatRiskLevel(data.risk_level);
 riskLevel.style.color = riskColors[risk] || "#334155";

 probabilitiesContainer.replaceChildren();

 const entries = Object.entries(data.probabilities);

 if (entries.length === 0) {
  throw new Error("No probability values were returned.");
 }

 for (const [label, probability] of entries) {
  if (
   typeof probability !== "number" ||
   !Number.isFinite(probability) ||
   probability < 0 ||
   probability > 1
  ) {
   throw new Error("The API returned an invalid probability value.");
  }

  const percentage = probability * 100;

  // Probability container
  const item = document.createElement("div");
  item.className = "probability";

  // Label and percentage
  const labelRow = document.createElement("div");
  labelRow.className = "probability-label";

  const name = document.createElement("span");
  name.textContent = formatRiskLevel(label);

  const value = document.createElement("strong");
  value.textContent = `${percentage.toFixed(1)}%`;

  labelRow.append(name, value);

  // Progress bar
  const bar = document.createElement("div");
  bar.className = "bar";

  const fill = document.createElement("div");
  fill.className = "fill";
  fill.style.width = `${percentage}%`;

  bar.appendChild(fill);
  item.append(labelRow, bar);

  probabilitiesContainer.appendChild(item);
 }

 resultSection.style.display = "block";

 // Scroll to results
 resultSection.scrollIntoView({
  behavior: "smooth",
  block: "nearest",
 });
}

// Submit form
async function handlePrediction(event) {
 event.preventDefault();

 clearResult();

 let patientData;

 try {
  patientData = getPatientData();
  validatePatientData(patientData);
 } catch (error) {
  showError(error.message);
  return;
 }

 setLoading(true);

 try {
  const response = await fetch(API_URL, {
   method: "POST",
   headers: {
    "Content-Type": "application/json",
    "Accept": "application/json",
   },
   body: JSON.stringify(patientData),
  });

  const data = await response.json();

  if (!response.ok) {
   let message = "Prediction request failed.";

   if (Array.isArray(data.detail)) {
    message = data.detail
     .map(item => item.msg || "Invalid input")
     .join("; ");
   } else if (typeof data.detail === "string") {
    message = data.detail;
   }

   throw new Error(message);
  }

  displayPrediction(data);

 } catch (error) {
  console.error("Prediction error:", error);

  showError(
   error instanceof TypeError
    ? "Unable to connect to the prediction API. Please check that the server is running."
    : error.message
  );

 } finally {
  setLoading(false);
 }
}

// Reset form and prediction
function resetApplication() {
 form.reset();
 clearResult();
}

// Initialize application
if (form) {
 form.addEventListener("submit", handlePrediction);
} else {
 console.error("Prediction form element was not found.");
}

// Optional reset button
const resetButton = document.getElementById("resetButton");

if (resetButton) {
 resetButton.addEventListener("click", resetApplication);
}
