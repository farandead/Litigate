document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("input-form").addEventListener("submit", handleSubmit);
    document.getElementById("start-new-session").addEventListener("click", async function() {
        try {
            const response = await fetch("/chat/start_chat_session", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                // Include any necessary data in the body, if your endpoint requires it
                // body: JSON.stringify({}),
            });

            if (response.ok) {
                // If the session is successfully started
                const data = await response.json();
                console.log("New chat session started:", data);

                // Optionally: Store the session ID in sessionStorage or handle it as needed
                sessionStorage.setItem("session_id", data.session_id);

                // Redirect to the new chat page
                window.location.href = '/chat'; // Adjust the URL as needed
            } else {
                throw new Error('Failed to start a new session');
            }
        } catch (error) {
            console.error("Error starting new chat session:", error);
        }
    });
    
    fetchChatHistories();
    // const sessionId = sessionStorage.getItem("session_id");
    // console.log('Session ID:', sessionId); // Check the session ID
    // fetchAndDisplayConversations(sessionId) 
});
function fetchChatHistories() {
    fetch('chat/fetch_chat_histories')
        .then(response => response.json())
        .then(data => {
            const chatHistoryPanel = document.getElementById('chat-history-panel');
            data.forEach(chat => {
                const chatRow = document.createElement('div');
                chatRow.className = 'chat-history-row';
                chatRow.innerHTML = `
                    <div class="chat-history-link" data-session-id="${chat.session_id}">
                        <p class="user-chats">${chat.user_snippet}</p>
                        <p class="ai-chats">${chat.ai_snippet}</p>
                    </div>
                `;
                chatHistoryPanel.appendChild(chatRow);

                // Add click event listener to the new chat history row
                chatRow.querySelector('.chat-history-link').addEventListener('click', function(event) {
                    event.preventDefault(); // Prevent the default anchor action
                    const sessionId = this.getAttribute('data-session-id');
                    fetchAndDisplayConversations(sessionId);
                });
            });
        })
        .catch(error => console.error('Error fetching chat histories:', error));
}

async function handleSubmit(event) {
    event.preventDefault(); // Prevent default form submission behavior

    const userInput = document.getElementById("user_input").value;
    if (!userInput.trim()) return; // Ignore empty submissions

    // Check if a new session should be started
    if (!sessionStorage.getItem("session_id")) {
        await startNewChatSession(userInput);
    } else {
        sendUserInput(userInput);
    }

    // Clear the input field after submission
    document.getElementById("user_input").value = "";
}

async function startNewChatSession(firstMessage) {
    try {
        const response = await fetch("chat/start_chat_session", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({}),
        });

        if (response.ok) {
            const data = await response.json();
            console.log("New chat session started:", data);
            sessionStorage.setItem("session_id", data.session_id);
            
            // Now send the first message
            sendUserInput(firstMessage);
        } else {
            throw new Error('Failed to start a new session');
        }
    } catch (error) {
        console.error("Error starting new chat session:", error);
    }
}

async function sendUserInput(userInput) {
    const response = await fetch("chat/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_input: userInput }),
    });

    if (response.ok) {
        const data = await response.json();
        const aiResponse = data.ai_response;

        // Save interaction
       

        // Update UI with user input and AI response
        await saveInteraction(userInput, aiResponse);

        appendUserInput(userInput);
        appendAiResponse(aiResponse);
    } else {
        console.error("Failed to submit or get a response");
    }
}

function saveInteraction(userInput, aiResponse) {
    fetch("chat/save_interaction", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_input: userInput,
            ai_response: aiResponse,
        }),
    })
    .then((response) => response.json())
    .then((data) => console.log("Success:", data))
    .catch((error) => console.error("Error:", error));
}

function appendUserInput(userInput,callback) {
    const outputContainer = document.getElementById("output");
    const userDiv = document.createElement("div");
    userDiv.classList.add("responses-person");

    userDiv.innerHTML = `
        <div class="responses-structure-img responses-structure-img-person">
            <img src="static/img/person-circle.svg" alt="User">
        </div>
        <div class="responses-structure-info">
            <div class="responses-heading">You</div>
            <div class="responses-response">${userInput}</div>
        </div>
    `;

    outputContainer.appendChild(userDiv);
    if (callback && typeof callback === 'function') {
        callback();
    }
}
function fetchAndDisplayConversations(sessionId) {
    console.log('Fetching conversations for session:', sessionId); // Confirm the function is called

    fetch(`/chat/get_conversations/${sessionId}`)
        .then(response => response.json())
        .then(conversations => {
            const outputContainer = document.getElementById("output");
            console.log('Conversations fetched:', conversations); // Check the fetched data

            outputContainer.innerHTML = ''; // Clear previous conversations if necessary

            // Use a recursive function to process one message at a time
            function processMessage(index) {
                if (index >= conversations.length) {
                    console.log('All messages displayed.');
                    return; // All messages have been displayed
                }

                const conv = conversations[index];
                const next = () => processMessage(index + 1); // Prepare the next function

                if (conv.type === 'user') {
                    appendUserInput(conv.message, next);
                } else if (conv.type === 'ai') {
                    appendAiResponse(conv.message, next);
                }
            }

            // Start processing messages
            processMessage(0);

        })
        .catch(error => {
            console.error('Error fetching conversations:', error);
        });
}
function displayErrorMessage(message) {
    const outputContainer = document.getElementById("output");
    // Create a simple div to show the error message
    const errorDiv = document.createElement("div");
    errorDiv.classList.add("error-message");
    errorDiv.textContent = message;
    outputContainer.appendChild(errorDiv);
}

function appendAiResponse(aiResponse, callback) {
    const outputContainer = document.getElementById("output");
    const aiDiv = document.createElement("div");
    aiDiv.classList.add("responses-AI");

    aiDiv.innerHTML = `
        <div class="responses-structure-img">
            <img src="static/img/LitigateLogo.png" alt="Logo"> <!-- Adjust the src attribute -->
        </div>
        <div class="responses-structure-info">
            <div class="responses-heading">Litigat8</div>
            <div class="responses-response"></div> <!-- Empty, for typewriter effect -->
        </div>
    `;

    outputContainer.appendChild(aiDiv);

    // Find the newly added response container for the typewriter effect
    const responseContainer = aiDiv.querySelector(".responses-response");
    // Start the typewriter effect and provide a callback if one is given
    typeWriter(responseContainer, aiResponse, 0, callback);

;
}

function typeWriter(element, text, i, callback) {
    if (i < text.length) {
        element.innerHTML = text.substring(0, i + 1) + '<span class="cursor" aria-hidden="true"></span>';
        setTimeout(() => typeWriter(element, text, i + 1, callback), 10); // Adjust typing speed here
    } else {
        element.innerHTML = text; // Optionally remove the cursor at the end
        if (callback) callback(); // Call callback function if provided
    }
}