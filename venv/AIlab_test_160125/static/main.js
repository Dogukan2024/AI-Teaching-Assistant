// Toggle Resource Dropdown
const resourcesButton = document.getElementById('resources-button');
const resourcesDropdown = document.getElementById('resources-dropdown');

resourcesButton.addEventListener('click', () => {
    resourcesDropdown.classList.toggle('dropdown-visible');
});


// PDF Viewer Functionality
function openPDF(filename) {
    const pdfFrame = document.getElementById('pdf-frame');
    if (pdfFrame) {
        pdfFrame.src = `/static/resources/${filename}`;
    } else {
        console.error('PDF Viewer iframe not found!');
    }
}

// Initialize Socket.IO Connection
const socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function () {
    console.log('✅ Connected to the server');
});

// 🪙 Selected coin type
let selected_coin = "";

// 🪙 Handle Coin Selection
function selectCoin(cointype) {
    document.querySelectorAll('#coin-balance div').forEach(coin => {
        coin.classList.remove('coin-selected');
    });
    const selectedCoinElement = document.getElementById(`${cointype}-coin`);
    if (selectedCoinElement) {
        selectedCoinElement.classList.add('coin-selected');
        selected_coin = cointype;
    }
}


// 🪙 Update Coin Balance
function updateCoinBalance(cointype) {
    const coinElement = document.getElementById(`${cointype}-coin`);
    if (coinElement) {
        const coinValueElement = coinElement.querySelector('it');
        let currentValue = parseInt(coinValueElement.textContent, 10) || 0;

        if (currentValue > 0) {
            currentValue -= 1;
            coinValueElement.textContent = currentValue;
            console.log(`💰 ${cointype} coin used. Remaining: ${currentValue}`);
        } else {
            alert(`❌ Not enough ${cointype} coins!`);
        }
    }
}

// 📨 Function to Add Chat Messages
function addMessageToChat(msg, type, isMarkdown = false) {
    const chatContainer = document.getElementById("chat-container");
    const li = document.createElement("li");

    if (isMarkdown) {
        // Use marked.js to parse Markdown into HTML
        li.innerHTML = marked.parse(msg);
    } else {
        li.textContent = msg;
    }

    switch (type) {
        case 'client':
            li.classList.add('message-client');
            break;
        case 'server':
            li.classList.add('message-server');
            break;
        case 'error':
            li.classList.add('message-error');
            break;
        case 'system':
            li.classList.add('message-system');
            break;
        default:
            li.classList.add('message-server');
    }

    chatContainer.appendChild(li);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll
}

// 📨 Function to Send Message
function sendMessage() {
    const userInput = document.getElementById('chat-input');
    const userMessage = userInput.value.trim();

    if (!userMessage) {
        alert("❌ Please enter a message!");
        return;
    }

    if (!selected_coin) {
        alert("🪙 Please select a coin before sending a message!");
        return;
    }

    // Decrease the selected coin balance
    updateCoinBalance(selected_coin);

    // Display User Message
    addMessageToChat(userMessage, "client");
    userInput.value = '';

    // Create Assistant Placeholder
    const assistantMessageElement = document.createElement('li');
    assistantMessageElement.classList.add('message-server');
    document.getElementById("chat-container").appendChild(assistantMessageElement);

    // Emit User Message to Socket.IO
    console.log('🛠️ Sending message to server:', userMessage);
    socket.emit('message', JSON.stringify({
        type: 'message',
        content: userMessage,
        selected_coin: selected_coin
    }));

    // Handle Streaming Response
    let assistantResponse = '';
    socket.off('message'); // Prevent duplicate listeners
    socket.on('message', function (data) {
        console.log('🔄 Received from server:', data);

        if (typeof data === 'string') {
            data = JSON.parse(data); // Ensure proper parsing
        }

        if (data.type === 'stream') {
            assistantResponse += data.content;
            // Render Markdown dynamically with each chunk
            const formattedResponse = marked.parse(assistantResponse);
            assistantMessageElement.innerHTML = formattedResponse;
            console.log('📥 Chunk added:', data.content);
            document.getElementById("chat-container").scrollTop = document.getElementById("chat-container").scrollHeight;
        }

        if (data.type === 'error') {
            addMessageToChat('❌ Error: ' + data.content, 'error');
        }

        if (data.type === 'done') {
            console.log('✅ Streaming complete');
        }
    });
}

// 🛠️ Resizable Panels
function setupResizers() {
    const resizerLeft = document.getElementById('resizer-left');
    const resizerRight = document.getElementById('resizer-right');
    const resourcesPanel = document.getElementById('resources-panel');
    const chatPanel = document.getElementById('chat-panel');

    let isResizingLeft = false;
    let isResizingRight = false;

    resizerLeft.addEventListener('mousedown', () => {
        isResizingLeft = true;
        document.body.style.cursor = 'ew-resize';
    });

    resizerRight.addEventListener('mousedown', () => {
        isResizingRight = true;
        document.body.style.cursor = 'ew-resize';
    });

    document.addEventListener('mousemove', (e) => {
        if (isResizingLeft) {
            const newWidth = e.clientX;
            if (newWidth > 150 && newWidth < window.innerWidth * 0.4) {
                resourcesPanel.style.flex = `0 0 ${newWidth}px`;
            }
        }

        if (isResizingRight) {
            const totalWidth = window.innerWidth;
            const newWidth = totalWidth - e.clientX;
            if (newWidth > 150 && newWidth < window.innerWidth * 0.4) {
                chatPanel.style.flex = `0 0 ${newWidth}px`;
            }
        }
    });

    document.addEventListener('mouseup', () => {
        isResizingLeft = false;
        isResizingRight = false;
        document.body.style.cursor = 'default';
    });
}

// 🛠️ Initialize Resizers
setupResizers();
