const $ = id => document.getElementById(id);
const form = $("predictionForm"), button = $("submitButton");
const error = $("errorMessage"), result = $("result");
const riskLevel = $("riskLevel"), probabilities = $("probabilities");
const fields = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"];
const rules = {
  Age: [0, 120, true], SystolicBP: [30, 300, true],
  DiastolicBP: [20, 200, true], BS: [1, 35],
  BodyTemp: [85, 110], HeartRate: [25, 250, true]
};

function clearResult() {
  error.textContent = "";
  result.style.display = "none";
  riskLevel.textContent = "";
  probabilities.replaceChildren();
}

function getPatientData() {
  const data = Object.fromEntries(fields.map(id => [id, Number($(id).value)]));
  for (const [id, [min, max, integer]] of Object.entries(rules)) {
    const value = data[id];
    if (!$(id).value.trim() || !Number.isFinite(value) || value <= min || value >= max || (integer && !Number.isInteger(value)))
      throw new Error(`Invalid ${id}. Check the allowed range.`);
  }
  if (data.SystolicBP <= data.DiastolicBP)
    throw new Error("Systolic BP must exceed diastolic BP.");
  return data;
}

const titleCase = v => String(v).trim().toLowerCase().replace(/\b\w/g, c => c.toUpperCase());

function displayPrediction(data) {
  if (typeof data.risk_level !== "string" || !data.probabilities || typeof data.probabilities !== "object")
    throw new Error("Invalid prediction response.");

  const colors = { "low risk": "#16a34a", "mid risk": "#d97706", "high risk": "#dc2626" };
  const risk = data.risk_level.trim().toLowerCase();
  riskLevel.textContent = titleCase(risk);
  riskLevel.style.color = colors[risk] || "#334155";
  probabilities.replaceChildren();

  Object.entries(data.probabilities).forEach(([label, probability]) => {
    if (typeof probability !== "number" || probability < 0 || probability > 1)
      throw new Error("Invalid probability value.");
    const percent = probability * 100;
    const item = document.createElement("div");
    item.className = "probability";
    item.innerHTML = `<div class="probability-label"><span></span><strong>${percent.toFixed(1)}%</strong></div>
                      <div class="bar"><div class="fill"></div></div>`;
    item.querySelector("span").textContent = titleCase(label);
    item.querySelector(".fill").style.width = `${percent}%`;
    probabilities.append(item);
  });

  result.style.display = "block";
  result.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function handlePrediction(e) {
  e.preventDefault();
  clearResult();
  let patientData;
  try { patientData = getPatientData(); }
  catch (err) { error.textContent = err.message; return; }

  button.disabled = true;
  button.querySelector("span").textContent = "Analyzing...";

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(patientData)
    });
    const data = await res.json();
    if (!res.ok) {
      const detail = data.detail;
      throw new Error(Array.isArray(detail) ? detail.map(x => x.msg || "Invalid input").join("; ") : detail || "Prediction failed.");
    }
    displayPrediction(data);
  } catch (err) {
    error.textContent = err instanceof TypeError
      ? "Unable to connect to the prediction API."
      : err.message;
  } finally {
    button.disabled = false;
    button.querySelector("span").textContent = "Generate Risk Assessment";
  }
}

form?.addEventListener("submit", handlePrediction);
$("resetButton")?.addEventListener("click", () => { form.reset(); clearResult(); });
