// Chrome Extension Service Worker
chrome.runtime.onInstalled.addListener(() => {
  console.log('News Collector Extension installed');
});

// 處理來自 popup 的訊息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'subscribe') {
    // 可以在這裡添加額外的邏輯
    console.log('New subscription:', request.data);
  }
});
