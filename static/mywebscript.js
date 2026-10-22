/* Submit text asynchronously so the result appears without a page reload. */
"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("emotion-form");
  const input = document.getElementById("textToAnalyze");
  const button = document.getElementById("analyze-button");
  const status = document.getElementById("status");
  const resultPanel = document.getElementById("result");
  const resultText = document.getElementById("result-text");

  if (!form || !input || !button || !status || !resultPanel || !resultText) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = input.value.trim();

    resultPanel.hidden = true;
    resultText.textContent = "";
    if (!text) {
      status.textContent = "Please enter a statement before analyzing.";
      input.focus();
      return;
    }

    button.disabled = true;
    status.textContent = "Analyzing your statement…";

    try {
      const url = new URL("/emotionDetector", window.location.origin);
      url.searchParams.set("textToAnalyze", text);
      const response = await fetch(url, {
        headers: { Accept: "text/plain" },
      });
      const message = await response.text();

      if (!response.ok) {
        throw new Error(message || "The analysis could not be completed.");
      }

      resultText.textContent = message;
      resultPanel.hidden = false;
      status.textContent = "Analysis complete.";
    } catch (error) {
      status.textContent = error instanceof Error
        ? error.message
        : "Unable to analyze the statement. Please try again.";
    } finally {
      button.disabled = false;
    }
  });
});
