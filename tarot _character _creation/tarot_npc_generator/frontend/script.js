let currentThreadId = null;
let drawnCards = [];

const drawBtn = document.getElementById('draw-btn');
const cardDeck = document.getElementById('card-deck');
const deckAnimation = document.getElementById('deck-animation');
const titleText = document.getElementById('title-text');
const resultArea = document.getElementById('result-area');
const cardsDisplay = document.getElementById('cards-display');
const inputArea = document.getElementById('input-area');
const backgroundInput = document.getElementById('background-input');
const submitBgBtn = document.getElementById('submit-bg');
const profileOutput = document.getElementById('profile-output');
const feedbackArea = document.getElementById('feedback-area');
const feedbackInput = document.getElementById('feedback-input');
const submitFeedbackBtn = document.getElementById('submit-feedback');
const finishBtn = document.getElementById('finish-btn');

function shuffleAnimation() {
    return new Promise((resolve) => {
        const images = ['/data/background/paidui_0.png', '/data/background/paidui_1.png', '/data/background/paidui_2.png'];
        let currentIndex = 0;
        const totalCycles = 10;
        const interval = 100;
        let cycleCount = 0;
        
        deckAnimation.classList.add('shuffling');
        
        const timer = setInterval(() => {
            currentIndex = (currentIndex + 1) % images.length;
            deckAnimation.src = images[currentIndex];
            cycleCount++;
            
            if (cycleCount >= totalCycles) {
                clearInterval(timer);
                deckAnimation.classList.remove('shuffling');
                deckAnimation.src = images[0];
                resolve();
            }
        }, interval);
    });
}

function getCardImageUrl(cardName) {
    const parts = cardName.split('_');
    if (parts.length >= 2) {
        const number = parts[0];
        const name = parts[1];
        return `/data/image/${number}_${name}.png`;
    }
    return '/data/image/default.png';
}

async function drawCards() {
    try {
        drawBtn.disabled = true;
        
        await shuffleAnimation();
        
        const response = await fetch('/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            throw new Error('抽牌失败');
        }
        
        const data = await response.json();
        currentThreadId = data.thread_id;
        drawnCards = data.drawn_cards;
        
        showCards();
        
    } catch (error) {
        console.error('Error:', error);
        alert('抽牌失败，请重试');
        drawBtn.disabled = false;
    }
}

function showCards() {
    cardDeck.style.display = 'none';
    titleText.style.display = 'none';
    resultArea.style.display = 'block';
    
    cardsDisplay.innerHTML = '';
    
    drawnCards.forEach((card, index) => {
        const cardItem = document.createElement('div');
        cardItem.className = 'card-item';
        cardItem.style.animationDelay = `${index * 0.1}s`;
        
        const img = document.createElement('img');
        img.src = getCardImageUrl(card);
        img.alt = card;
        img.onerror = function() {
            this.src = '/data/image/default.png';
        };
        
        if (card.includes('逆位')) {
            img.classList.add('reversed');
        }
        
        const name = document.createElement('div');
        name.className = 'card-name';
        name.textContent = card;
        
        cardItem.appendChild(img);
        cardItem.appendChild(name);
        cardsDisplay.appendChild(cardItem);
    });
    
    inputArea.style.display = 'block';
    profileOutput.style.display = 'none';
    feedbackArea.style.display = 'none';
}

async function submitBackground() {
    const background = backgroundInput.value.trim();
    if (!background) {
        alert('请输入故事背景');
        return;
    }
    
    try {
        submitBgBtn.disabled = true;
        showLoading(submitBgBtn);
        
        const response = await fetch('/continue', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                thread_id: currentThreadId,
                user_background: background
            })
        });
        
        if (!response.ok) {
            throw new Error('生成角色失败');
        }
        
        const data = await response.json();
        showProfile(data.generated_profile);
        
    } catch (error) {
        console.error('Error:', error);
        alert('生成角色失败，请重试');
    } finally {
        submitBgBtn.disabled = false;
        hideLoading(submitBgBtn);
    }
}

function markdownToHtml(text) {
    let html = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^\- (.*$)/gim, '<li>$1</li>')
        .replace(/^\d+\. (.*$)/gim, '<li>$1</li>')
        .replace(/\n/g, '<br>');
    
    html = html.replace(/<li>(.*?)<br>/g, '<ul><li>$1</li></ul>');
    html = html.replace(/<\/ul>\s*<ul>/g, '');
    
    return html;
}

function showProfile(profile) {
    inputArea.style.display = 'none';
    profileOutput.style.display = 'block';
    profileOutput.innerHTML = markdownToHtml(profile);
    feedbackArea.style.display = 'block';
    feedbackInput.value = '';
}

async function submitFeedback() {
    const feedback = feedbackInput.value.trim();
    
    try {
        submitFeedbackBtn.disabled = true;
        finishBtn.disabled = true;
        showLoading(submitFeedbackBtn);
        
        const response = await fetch('/continue', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                thread_id: currentThreadId,
                feedback: feedback
            })
        });
        
        if (!response.ok) {
            throw new Error('重新生成失败');
        }
        
        const data = await response.json();
        showProfile(data.generated_profile);
        
    } catch (error) {
        console.error('Error:', error);
        alert('重新生成失败，请重试');
    } finally {
        submitFeedbackBtn.disabled = false;
        finishBtn.disabled = false;
        hideLoading(submitFeedbackBtn);
    }
}

async function finishSession() {
    try {
        finishBtn.disabled = true;
        showLoading(finishBtn);
        
        await fetch('/continue', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                thread_id: currentThreadId,
                feedback: ''
            })
        });
        
        alert('感谢使用塔罗牌NPC生成器！');
        resetSession();
        
    } catch (error) {
        console.error('Error:', error);
        alert('结束会话失败');
    } finally {
        finishBtn.disabled = false;
        hideLoading(finishBtn);
    }
}

function resetSession() {
    currentThreadId = null;
    drawnCards = [];
    
    cardDeck.style.display = 'block';
    titleText.style.display = 'block';
    resultArea.style.display = 'none';
    cardsDisplay.innerHTML = '';
    backgroundInput.value = '';
    profileOutput.textContent = '';
    feedbackInput.value = '';
}

function showLoading(btn) {
    const originalContent = btn.innerHTML;
    btn.innerHTML = '<span class="loading"></span>';
    btn.dataset.originalContent = originalContent;
}

function hideLoading(btn) {
    if (btn.dataset.originalContent) {
        btn.innerHTML = btn.dataset.originalContent;
        delete btn.dataset.originalContent;
    }
}

drawBtn.addEventListener('click', drawCards);
submitBgBtn.addEventListener('click', submitBackground);
submitFeedbackBtn.addEventListener('click', submitFeedback);
finishBtn.addEventListener('click', finishSession);

backgroundInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        submitBackground();
    }
});