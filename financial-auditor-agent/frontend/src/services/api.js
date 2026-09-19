const API_BASE = "http://localhost:8088/api";

export async function startAuditJob(ticker, horizon = "3-5 years", concern = "General") {
  const res = await fetch(`${API_BASE}/audit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ticker, horizon, concern }),
  });
  if (!res.ok) {
    throw new Error(`Audit initiation failed: ${res.statusText}`);
  }
  return await res.json();
}

export function connectAuditStream(taskId, onStep, onComplete, onError) {
  const url = `${API_BASE}/audit/${taskId}/stream`;
  const eventSource = new EventSource(url);

  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.type === "step_update" || data.type === "init") {
        onStep(data);
      } else if (data.type === "complete") {
        onComplete(data.result);
        eventSource.close();
      }
    } catch (e) {
      console.error("Failed to parse SSE message", e);
    }
  };

  eventSource.addEventListener("complete", (event) => {
    try {
      const data = JSON.parse(event.data);
      onComplete(data.result);
      eventSource.close();
    } catch (e) {
      console.error("Error handling complete event", e);
    }
  });

  eventSource.onerror = (err) => {
    console.error("SSE Connection error", err);
    if (onError) onError(err);
    eventSource.close();
  };

  return () => {
    eventSource.close();
  };
}
