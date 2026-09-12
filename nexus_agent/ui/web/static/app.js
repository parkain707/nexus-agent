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
      <div class="star-cta" style="margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(16, 185, 129, 0.25); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
        <span style="font-size: 0.8rem; color: #a7f3d0; font-weight: 500;">⭐ Enjoyed this run? Support Nexus-Agent with a star!</span>
        <a href="https://github.com/parkain707/nexus-agent" target="_blank" rel="noopener" style="background: #ffb800; color: #050b14; font-weight: 800; font-size: 0.75rem; padding: 6px 14px; border-radius: 14px; text-decoration: none; box-shadow: 0 0 12px rgba(255, 184, 0, 0.4); display: inline-flex; align-items: center; gap: 4px; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
          ★ Star on GitHub
        </a>
      </div>
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

async function loadSnapshots() {
  try {
    const res = await fetch('/api/snapshots');
    const snaps = await res.json();
    const list = document.getElementById('snapshots-list');
    if (!list) return;
    if (snaps.length === 0) {
      list.innerHTML = '<div class="snapshot-empty" style="font-size: 0.75rem; color: var(--text-muted);">No snapshots recorded yet.</div>';
      return;
    }
    list.innerHTML = '';
    snaps.forEach(s => {
      const item = document.createElement('div');
      item.className = 'tool-item';
      item.style.flexDirection = 'column';
      item.style.alignItems = 'flex-start';
      item.style.gap = '4px';
      item.innerHTML = `
        <div style="display: flex; justify-content: space-between; width: 100%;">
          <span class="tool-name" style="font-size: 0.75rem;">#${s.id} ${escapeHtml(s.file_path)}</span>
          <button class="btn-rollback" data-id="${s.id}" style="background: rgba(244,63,94,0.15); border: 1px solid var(--accent-rose); color: #fecdd3; font-size: 0.65rem; border-radius: 4px; padding: 2px 6px; cursor: pointer;">↺ ROLLBACK</button>
        </div>
        <div style="font-size: 0.65rem; color: var(--text-muted);">${s.created_at}</div>
      `;
      list.appendChild(item);
    });

    document.querySelectorAll('.btn-rollback').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.getAttribute('data-id'), 10);
        if (confirm(`Snapshot #${id} 상태로 코드를 되돌리시겠습니까?`)) {
          const r = await fetch('/api/rollback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ snapshot_id: id })
          });
          const resData = await r.json();
          alert(resData.message || 'Rollback executed successfully!');
          loadSnapshots();
        }
      });
    });
  } catch (e) {
    console.error('Failed to load snapshots', e);
  }
}

function renderMarkdown(text) {
  if (!text) return '';
  let escaped = escapeHtml(text);

  // 1. Code blocks: ```lang \n code ```
  escaped = escaped.replace(/```([a-zA-Z0-9_]*)\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<pre class="code-block" style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 8px; margin: 8px 0; border: 1px solid rgba(0,243,255,0.2); overflow-x: auto; font-family: var(--font-mono); font-size: 0.8rem; color: #a5f3fc;"><div style="font-size: 0.65rem; color: var(--accent-cyan); margin-bottom: 4px;">${lang || 'CODE'}</div><code>${code.trim()}</code></pre>`;
  });

  // 2. Inline code: `code`
  escaped = escaped.replace(/`([^`]+)`/g, '<code style="background: rgba(0,0,0,0.4); padding: 2px 6px; border-radius: 4px; font-family: var(--font-mono); color: #a5f3fc; border: 1px solid rgba(255,255,255,0.08);">$1</code>');

  // 3. Bold: **text**
  escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--accent-cyan); font-weight: 700;">$1</strong>');

  // 4. Italic: *text*
  escaped = escaped.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // 5. Bullet items: - item
  escaped = escaped.replace(/(?:^|\n)\s*-\s+(.*?)(?=(?:\n|$))/g, '\n<div style="display: flex; gap: 8px; margin: 5px 0; align-items: flex-start;"><span style="color: var(--accent-cyan); font-size: 0.9rem;">•</span><div>$1</div></div>');

  // 6. Convert newlines to <br>
  escaped = escaped.replace(/\n/g, '<br>');

  return escaped;
}

function appendChatBubble(sender, message) {
  const container = document.getElementById('chat-messages');
  if (!container) return;

  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${sender === 'user' ? 'user-bubble' : 'agent-bubble'}`;
  const avatar = sender === 'user' ? '👤' : '⚡';
  const author = sender === 'user' ? 'YOU' : 'NEXUS-AGENT';

  bubble.innerHTML = `
    <div class="chat-avatar">${avatar}</div>
    <div class="chat-body">
      <div class="chat-author">${author}</div>
      <div class="chat-text">${renderMarkdown(message)}</div>
    </div>
  `;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

async function sendChatMessage() {
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;

  const provider = document.getElementById('provider-select').value;
  appendChatBubble('user', text);
  input.value = '';

  // Append temporary thinking indicator
  const container = document.getElementById('chat-messages');
  const typing = document.createElement('div');
  typing.id = 'chat-typing-indicator';
  typing.className = 'chat-bubble agent-bubble';
  typing.innerHTML = `
    <div class="chat-avatar">⚡</div>
    <div class="chat-body">
      <div class="chat-author">NEXUS-AGENT</div>
      <div class="chat-text" style="color: var(--accent-cyan);">생각하는 중... 💭</div>
    </div>
  `;
  container.appendChild(typing);
  container.scrollTop = container.scrollHeight;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        session_id: 'browser_session',
        provider: provider
      })
    });
    const indicator = document.getElementById('chat-typing-indicator');
    if (indicator) indicator.remove();

    if (res.ok) {
      const data = await res.json();
      appendChatBubble('agent', data.reply);
    } else {
      appendChatBubble('agent', `[오류] 서버 응답 오류 (${res.status})`);
    }
  } catch (err) {
    const indicator = document.getElementById('chat-typing-indicator');
    if (indicator) indicator.remove();
    appendChatBubble('agent', `[통신 오류] ${err.message}`);
  }
}

function setupEvents() {
  // Mode switcher
  const btnMission = document.getElementById('btn-mode-mission');
  const btnChat = document.getElementById('btn-mode-chat');
  const viewStream = document.getElementById('view-stream');
  const viewChat = document.getElementById('view-chat');

  if (btnMission && btnChat) {
    btnMission.addEventListener('click', () => {
      btnMission.classList.add('active');
      btnChat.classList.remove('active');
      viewStream.style.display = 'flex';
      viewChat.style.display = 'none';
    });

    btnChat.addEventListener('click', () => {
      btnChat.classList.add('active');
      btnMission.classList.remove('active');
      viewStream.style.display = 'none';
      viewChat.style.display = 'flex';
      document.getElementById('chat-input').focus();
    });
  }

  // Chat send
  const btnChatSend = document.getElementById('btn-chat-send');
  const chatInput = document.getElementById('chat-input');
  if (btnChatSend && chatInput) {
    btnChatSend.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendChatMessage();
      }
    });
  }

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

    // Switch to mission view
    if (btnMission && viewStream) {
      btnMission.click();
    }

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
  loadSnapshots();
  setupEvents();
});
