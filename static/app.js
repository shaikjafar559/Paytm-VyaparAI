// Global state
let currentLang = 'hi';
let isListening = false;
let recognition = null;
let salesChartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
  initDashboard();
  setupSpeechRecognition();
});

// Set active voice language
function setLanguage(lang) {
  currentLang = lang;
  const btnHi = document.getElementById('lang-btn-hi');
  const btnEn = document.getElementById('lang-btn-en');
  
  if (lang === 'hi') {
    btnHi.className = 'px-2 py-0.5 rounded font-bold bg-paytm-cyan text-slate-950 transition';
    btnEn.className = 'px-2 py-0.5 rounded font-medium text-slate-300 hover:text-white transition';
    document.getElementById('user-input-text').placeholder = 'माइक दबाकर बोलें या यहाँ लिखें...';
  } else {
    btnEn.className = 'px-2 py-0.5 rounded font-bold bg-paytm-cyan text-slate-950 transition';
    btnHi.className = 'px-2 py-0.5 rounded font-medium text-slate-300 hover:text-white transition';
    document.getElementById('user-input-text').placeholder = 'Speak or type your question here...';
  }

  if (recognition) {
    recognition.lang = lang === 'hi' ? 'hi-IN' : 'en-IN';
  }
}

// Fetch dashboard data & initialize chart
async function initDashboard() {
  try {
    const res = await fetch('/api/dashboard');
    const data = await res.json();

    // Render Inventory
    renderInventory(data.inventory);

    // Render Sales Chart
    renderChart(data.hourly_sales);
  } catch (err) {
    console.error('Error fetching dashboard:', err);
  }
}

// Render inventory items with reorder triggers
function renderInventory(items) {
  const container = document.getElementById('inventory-list');
  if (!container) return;

  container.innerHTML = items.map(item => {
    let badgeClass = 'bg-emerald-100 text-emerald-800 border-emerald-200';
    let statusText = 'पर्याप्त (Healthy)';
    let isAlert = false;

    if (item.status === 'critical_low') {
      badgeClass = 'bg-red-100 text-red-700 border-red-200 animate-pulse';
      statusText = 'अति कम (Critical)';
      isAlert = true;
    } else if (item.status === 'low') {
      badgeClass = 'bg-amber-100 text-amber-800 border-amber-200';
      statusText = 'कम (Low)';
      isAlert = true;
    }

    return `
      <div class="flex items-center justify-between p-2.5 rounded-xl border ${isAlert ? 'border-amber-200 bg-amber-50/40' : 'border-slate-100 bg-slate-50/60'} hover:bg-white transition shadow-2xs">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-lg ${isAlert ? 'bg-amber-100 text-amber-700' : 'bg-slate-200 text-slate-600'} flex items-center justify-center font-bold text-xs">
            ${item.category[0]}
          </div>
          <div>
            <div class="font-bold text-xs sm:text-sm text-slate-800">${item.name}</div>
            <div class="text-[11px] text-slate-500">${item.name_hi} • ₹${item.price}/${item.unit}</div>
          </div>
        </div>
        <div class="text-right">
          <div class="text-xs font-bold ${isAlert ? 'text-red-600' : 'text-slate-800'}">
            ${item.current_stock} ${item.unit} शेष
          </div>
          <span class="inline-block mt-0.5 text-[10px] font-semibold px-2 py-0.5 rounded-full border ${badgeClass}">
            ${statusText}
          </span>
        </div>
      </div>
    `;
  }).join('');
}

// Render Hourly Sales Chart
function renderChart(hourlyData) {
  const ctx = document.getElementById('salesChart');
  if (!ctx) return;

  const labels = hourlyData.map(d => d.hour);
  const data = hourlyData.map(d => d.sales);

  if (salesChartInstance) {
    salesChartInstance.destroy();
  }

  salesChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Sales (₹)',
        data: data,
        backgroundColor: labels.map(l => l.includes('8 PM') || l.includes('6 PM') ? '#00b9f1' : '#002970'),
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 10 } } },
        y: { 
          beginAtZero: true, 
          ticks: { font: { size: 9 }, callback: value => '₹' + value } 
        }
      }
    }
  });
}

// Setup Speech Recognition
function setupSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    console.warn('Web Speech Recognition API not supported in this browser.');
    return;
  }

  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = currentLang === 'hi' ? 'hi-IN' : 'en-IN';

  recognition.onstart = () => {
    isListening = true;
    updateVoiceUI(true, 'सुन रहा हूँ (Listening)...');
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    console.log('Recognized speech:', transcript);
    askCopilot(transcript);
  };

  recognition.onerror = (event) => {
    console.error('Speech error:', event.error);
    updateVoiceUI(false);
  };

  recognition.onend = () => {
    isListening = false;
    updateVoiceUI(false);
  };
}

// Toggle Voice Listening
function toggleVoiceRecording() {
  if (!recognition) {
    alert('Speech recognition is not supported in this browser. Please use Chrome/Edge or type your question below.');
    return;
  }

  if (isListening) {
    recognition.stop();
  } else {
    try {
      recognition.lang = currentLang === 'hi' ? 'hi-IN' : 'en-IN';
      recognition.start();
    } catch (e) {
      console.warn('Recognition start issue:', e);
    }
  }
}

// Update UI during voice activity
function updateVoiceUI(active, text = '') {
  const micBtn = document.getElementById('mic-btn');
  const bar = document.getElementById('voice-indicator-bar');
  const statusText = document.getElementById('voice-status-text');

  if (active) {
    micBtn.classList.add('pulse-glow', 'bg-red-500');
    micBtn.classList.remove('bg-paytm-blue');
    bar.classList.remove('hidden');
    if (statusText && text) statusText.textContent = text;
  } else {
    micBtn.classList.remove('pulse-glow', 'bg-red-500');
    micBtn.classList.add('bg-paytm-blue');
    bar.classList.add('hidden');
  }
}

// Main function to ask Copilot
async function askCopilot(queryText) {
  if (!queryText || !queryText.trim()) return;

  appendUserMessage(queryText);
  updateVoiceUI(true, 'AI विचार कर रहा है (Processing)...');

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: queryText,
        lang: currentLang,
        voice_gender: 'male'
      })
    });

    const data = await res.json();
    appendAIMessage(data);

    // Play Voice Audio
    if (data.audio_data_uri) {
      playAudio(data.audio_data_uri);
    } else {
      updateVoiceUI(false);
    }
  } catch (err) {
    console.error('Chat error:', err);
    updateVoiceUI(false);
  }
}

// Play audio from data URI
function playAudio(dataUri) {
  const audio = document.getElementById('tts-audio-player');
  if (!audio) return;

  audio.src = dataUri;
  updateVoiceUI(true, 'बोल रहा हूँ (Speaking)...');
  
  audio.onended = () => {
    updateVoiceUI(false);
  };
  audio.onerror = () => {
    updateVoiceUI(false);
  };

  audio.play().catch(e => {
    console.warn('Audio auto-play prevented:', e);
    updateVoiceUI(false);
  });
}

// Append User Chat Bubble
function appendUserMessage(text) {
  const container = document.getElementById('chat-messages');
  const bubble = document.createElement('div');
  bubble.className = 'flex justify-end';
  bubble.innerHTML = `
    <div class="bg-paytm-blue text-white p-3 rounded-2xl rounded-tr-none max-w-[85%] text-xs sm:text-sm shadow-sm">
      ${escapeHtml(text)}
    </div>
  `;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

// Append AI Chat Bubble with Markdown and Action Buttons
function appendAIMessage(data) {
  const container = document.getElementById('chat-messages');
  const bubble = document.createElement('div');
  bubble.className = 'chat-bubble-ai p-3.5 rounded-2xl rounded-tl-none shadow-sm space-y-2';

  // Format markdown-like text to HTML
  let formattedText = data.display_text
    .replace(/^### (.*$)/gim, '<h4 class="font-bold text-paytm-blue text-sm mb-1">$1</h4>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/```text([\s\S]*?)```/g, '<div class="p-2.5 bg-slate-100 rounded-lg text-xs font-mono border border-slate-200 my-2 whitespace-pre-wrap">$1</div>')
    .replace(/\n/g, '<br/>');

  // Action Buttons if relevant
  let actionButtonsHtml = '';
  if (data.intent === 'whatsapp_campaign') {
    const promoText = data.action && data.action.text ? encodeURIComponent(data.action.text) : '';
    actionButtonsHtml = `
      <div class="pt-2 flex space-x-2">
        <button onclick="openWhatsAppModal('${promoText}')" class="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-3 py-1.5 rounded-lg flex items-center space-x-1 shadow-sm">
          <span>📲 व्हाट्सएप पर भेजें (Send Promo)</span>
        </button>
      </div>
    `;
  } else if (data.intent === 'inventory_alert') {
    actionButtonsHtml = `
      <div class="pt-2 flex space-x-2">
        <button onclick="triggerReorderModal()" class="bg-paytm-blue hover:bg-paytm-blue/90 text-white text-xs font-bold px-3 py-1.5 rounded-lg flex items-center space-x-1 shadow-sm">
          <span>📦 डिस्ट्रीब्यूटर को री-ऑर्डर भेजें</span>
        </button>
      </div>
    `;
  }

  bubble.innerHTML = `
    <div class="flex items-center justify-between text-paytm-blue font-semibold text-xs border-b border-blue-50 pb-1">
      <span class="flex items-center space-x-1">
        <i data-lucide="sparkles" class="w-3.5 h-3.5 text-paytm-cyan"></i>
        <span>पेटीएम व्यापार AI</span>
      </span>
      <button onclick="playAudio('${data.audio_data_uri || ''}')" class="text-slate-400 hover:text-paytm-blue p-0.5" title="Replay voice">
        <i data-lucide="volume-2" class="w-3.5 h-3.5"></i>
      </button>
    </div>
    <div class="text-slate-700 leading-relaxed text-xs sm:text-sm">
      ${formattedText}
    </div>
    ${actionButtonsHtml}
  `;

  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
  lucide.createIcons();
}

// User text input handler
function sendUserText() {
  const input = document.getElementById('user-input-text');
  const text = input.value.trim();
  if (text) {
    askCopilot(text);
    input.value = '';
  }
}

function handleKeyPress(e) {
  if (e.key === 'Enter') {
    sendUserText();
  }
}

// Simulate Paytm Soundbox Payment
async function triggerSoundboxSimulate() {
  try {
    updateVoiceUI(true, 'साउंडबॉक्स से पुष्टि हो रही है...');
    const res = await fetch('/api/soundbox/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount: 500.0, payer_name: 'Pooja Verma' })
    });
    const data = await res.json();

    // Play iconic soundbox alert + AI tip
    if (data.audio_data_uri) {
      playAudio(data.audio_data_uri);
    }

    // Update Dashboard Metrics live
    document.getElementById('metric-total-rev').textContent = `₹${data.new_total.toLocaleString()}`;
    const upiElem = document.getElementById('metric-upi-rev');
    if (upiElem) {
      const currentUpi = parseInt(upiElem.textContent.replace(/[^0-9]/g, '')) || 24250;
      upiElem.textContent = `₹${(currentUpi + 500).toLocaleString()}`;
    }

    appendAIMessage({
      intent: 'soundbox_alert',
      display_text: `### 🔔 Paytm Soundbox: ₹${data.amount} Received!\n\n` +
                    `✅ **${data.soundbox_text}**\n\n` +
                    `💡 *${data.ai_tip}*`,
      voice_text: `${data.soundbox_text} ${data.ai_tip}`,
      audio_data_uri: data.audio_data_uri
    });

  } catch (err) {
    console.error('Soundbox simulation failed:', err);
    updateVoiceUI(false);
  }
}

// WhatsApp modal handlers
let activeCampaignText = '';
function openWhatsAppModal(encodedText) {
  activeCampaignText = decodeURIComponent(encodedText);
  document.getElementById('whatsapp-preview-text').textContent = activeCampaignText;
  document.getElementById('whatsapp-modal').classList.remove('hidden');
}

function dispatchWhatsAppWeb() {
  const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(activeCampaignText)}`;
  window.open(url, '_blank');
  closeModal('whatsapp-modal');
}

function copyCampaignText() {
  navigator.clipboard.writeText(activeCampaignText);
  alert('संदेश कॉपी कर लिया गया है!');
}

// Reorder Modal handlers
function triggerReorderModal() {
  document.getElementById('reorder-modal').classList.remove('hidden');
}

async function confirmReorderPO() {
  try {
    const res = await fetch('/api/reorder', { method: 'POST' });
    const data = await res.json();
    closeModal('reorder-modal');
    alert(data.message);
  } catch (err) {
    console.error(err);
  }
}

function closeModal(id) {
  document.getElementById(id).classList.add('hidden');
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
