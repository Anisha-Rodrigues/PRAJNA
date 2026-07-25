const BASE_URL = "http://127.0.0.1:8000/api";

async function handleResponse(res) {
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`API error: ${res.status} - ${errorText}`);
  }

  return res.json();
}

export async function sendQuery(query, language, officerId, sessionId) {
  const res = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      language,
      officer_id: officerId,
      session_id: sessionId,
    }),
  });

  return handleResponse(res);
}

export async function getNetwork() {
  const res = await fetch(`${BASE_URL}/network`);
  return handleResponse(res);
}

export async function getFir(firId) {
  const res = await fetch(`${BASE_URL}/fir/${encodeURIComponent(firId)}`);
  return handleResponse(res);
}

export async function getSuspect(id) {
  const res = await fetch(`${BASE_URL}/suspect/${encodeURIComponent(id)}`);
  return handleResponse(res);
}

export async function getPressure() {
  const res = await fetch(`${BASE_URL}/pressure`);
  return handleResponse(res);
}

export async function saveMemory(
  officerId,
  query,
  response,
  outcome,
  sessionId = null
) {
  const res = await fetch(`${BASE_URL}/memory`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      officer_id: officerId,
      query: query,
      response: {
        answer: response,
      },
      outcome: outcome,
      session_id: sessionId,
    }),
  });

  return handleResponse(res);
}
export async function getMemory(officerId) {
  const res = await fetch(
    `${BASE_URL}/memory/${encodeURIComponent(officerId)}`
  );
  return handleResponse(res);
}

export async function getAlerts() {
  const res = await fetch(`${BASE_URL}/alerts`);
  return handleResponse(res);
}
