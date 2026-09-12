// Nexus-Agent Mission Control Client-Side Logic (Agent 2: Iris)

let ws;
let actionCount = 0;

function initWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/stream`;
  const statusPulse = document.getElementById('ws-pulse');
  const statusText = document.getElementById('ws-status-text');

  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    statusPulse.classList.add('online');
    statusText.textContent = 'ONLINE (SECURE)';
    console.log('[NEXUS] WebSocket telemetry established.');
  };

  ws.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      handleStreamEvent(payload.type, payload.data);
    } catch (e) {
      console.error('Error parsing stream event', e);
    }
  };

  ws.onclose = () => {
    statusPulse.classList.remove('online');
    statusText.textContent = 'RECONNECTING...';
    setTimeout(initWebSocket, 2000);
  };
}

function handleStreamEvent(type, data) {
  const stream = document.getElementById('stream-logs');
  const statStep = document.getElementById('stat-step');
  const statState = document.getElementById('stat-state');
  const statActions = document.getElementById('stat-actions');

  // Remove empty placeholder on first event
  const emptyState = stream.querySelector('.empty-stream-state');
  if (emptyState) {
    emptyState.remove();
  }

  if (type === 'thought') {
    statStep.textContent = data.step;
    statState.textContent = 'THINKING';
    statState.style.color = 'var(--accent-amber)';

    const card = document.createElement('div');
    card.className = 'thought-card';
    card.innerHTML = `
      <div class="header">✦ STEP ${data.step} // CHAIN-OF-THOUGHT REASONING</div>
      <div class="content">${escapeHtml(data.thought)}</div>
    `;
    stream.appendChild(card);
    stream.scrollTop = stream.scrollHeight;
  } else if (type === 'tool_call') {
    actionCount++;
    statActions.textContent = actionCount;
    statState.textContent = 'EXECUTING';
    statState.style.color = 'var(--accent-cyan)';

    const card = document.createElement('div');
    card.className = 'action-card';
    const tool = data.tool || {};
    card.innerHTML = `
      <div class="header">⚙ ACTION // CALLING TOOL: [${escapeHtml(tool.name)}]</div>
      <pre>${escapeHtml(JSON.stringify(tool.arguments, null, 2))}</pre>
    `;
    stream.appendChild(card);
    stream.scrollTop = stream.scrollHeight;
  } else if (type === 'tool_result') {
    const res = data.result || {};
    const card = document.createElement('div');
    card.className = `observation-card ${res.success ? 'success' : 'failed'}`;
    const headerTitle = res.success ? '✔ OBSERVATION (SUCCESS)' : '✖ OBSERVATION ERROR (SELF-HEALING TRIGGERED)';
    const content = res.success ? res.output : res.error;
    card.innerHTML = `
      <div class="header">${headerTitle}</div>
      <pre>${escapeHtml(content)}</pre>
    `;
    stream.appendChild(card);
    stream.scrollTop = stream.scrollHeight;
  } else if (type === 'task_completed') {
    statState.textContent = 'COMPLETED';
    statState.style.color = 'var(--accent-green)';

    const card = document.createElement('div');
    card.className = 'finish-card';
    card.innerHTML = `
      <h4>MISSION ACCOMPLISHED ✔</h4>
      <div class="summary">${escapeHtml(data.final_output)}</div>
    `;
    stream.appendChild(card);
    stream.scrollTop = stream.scrollHeight;
  } else if (type === 'task_failed') {
    statState.textContent = 'FAILED';
    statState.style.color = 'var(--accent-rose)';
  } else if (type === 'reflection') {
    const reflBox = document.getElementById('reflections-list');
    const item = document.createElement('div');
    item.style.padding = '6px';
    item.style.marginBottom = '6px';
    item.style.background = 'rgba(244, 63, 94, 0.1)';
    item.style.borderLeft = '2px solid var(--accent-rose)';
    item.textContent = data.warning;
    reflBox.appendChild(item);
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

async function loadArsenal() {
  try {
    const res = await fetch('/api/tools');
    const tools = await res.json();
    const list = document.getElementById('tools-list');
    list.innerHTML = '';
    tools.forEach(t => {
      const item = document.createElement('div');
      item.className = 'tool-item';
      item.innerHTML = `
        <span class="tool-name">${t.name}</span>
        <span class="tool-badge">${t.category}</span>
      `;
      list.appendChild(item);
    });
  } catch (e) {
    console.error('Failed to load arsenal', e);
  }
}

function setupEvents() {
  // Preset pills click
  document.querySelectorAll('.preset-tag').forEach(tag => {
    tag.addEventListener('click', () => {
      document.getElementById('goal-input').value = tag.getAttribute('data-prompt');
    });
  });

  // Launch button
  document.getElementById('btn-launch').addEventListener('click', async () => {
    const goal = document.getElementById('goal-input').value.trim();
    if (!goal) {
      alert('Please enter a target goal or prompt.');
      return;
    }

    const provider = document.getElementById('provider-select').value;
    const maxIters = parseInt(document.getElementById('max-iters').value, 10) || 15;

    // Reset counters & stream
    actionCount = 0;
    document.getElementById('stat-actions').textContent = '0';
    document.getElementById('stat-step').textContent = '1';
    document.getElementById('stat-state').textContent = 'INITIALIZING';
    document.getElementById('stream-logs').innerHTML = '';

    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          goal: goal,
          provider: provider,
          max_iterations: maxIters
        })
      });
      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }
    } catch (err) {
      alert(`Launch error: ${err.message}`);
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initWebSocket();
  loadArsenal();
  setupEvents();
});
