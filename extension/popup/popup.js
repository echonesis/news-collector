document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('subscriptionForm');
  const status = document.getElementById('status');
  
  // 載入儲存的設定
  loadSavedSettings();
  
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
      topic: document.getElementById('topic').value,
      frequency: document.getElementById('frequency').value,
      email: document.getElementById('email').value
    };
    
    try {
      // 儲存到本地
      await saveSettings(formData);
      
      // 發送到後端 API
      const response = await fetch('https://news-collector-deiu.onrender.com/api/subscriptions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        showStatus('訂閱成功！', 'success');
        form.reset();
      } else {
        throw new Error('API 請求失敗');
      }
    } catch (error) {
      console.error('Error:', error);
      showStatus('訂閱失敗，請檢查網路連線', 'error');
    }
  });
  
  function showStatus(message, type) {
    status.textContent = message;
    status.className = `status ${type}`;
    status.style.display = 'block';
    
    setTimeout(() => {
      status.style.display = 'none';
    }, 3000);
  }
  
  async function saveSettings(data) {
    return new Promise((resolve) => {
      chrome.storage.sync.set({
        lastEmail: data.email,
        lastFrequency: data.frequency
      }, resolve);
    });
  }
  
  async function loadSavedSettings() {
    return new Promise((resolve) => {
      chrome.storage.sync.get(['lastEmail', 'lastFrequency'], (result) => {
        if (result.lastEmail) {
          document.getElementById('email').value = result.lastEmail;
        }
        if (result.lastFrequency) {
          document.getElementById('frequency').value = result.lastFrequency;
        }
        resolve();
      });
    });
  }
});
