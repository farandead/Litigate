// chatFunctions.test.js
import { fetchChatHistories } from './index.js'; // Ensure the path to your JS file is correct

beforeEach(() => {
  fetchMock.resetMocks(); // Use fetchMock for resetting mocks
  document.body.innerHTML = '<div id="chat-history-panel"></div>'; // Setup mock DOM
});

test('fetchChatHistories populates chat history', async () => {
  // Mock fetch response with fetchMock
  fetchMock.mockResponseOnce(JSON.stringify([
    { session_id: '123', user_snippet: 'User message snippet', ai_snippet: 'AI message snippet' }
  ]));

  await fetchChatHistories(); // Call the function

  // Assertions
  const chatHistoryPanel = document.getElementById('chat-history-panel');
  expect(chatHistoryPanel.children.length).toBe(1);
  expect(chatHistoryPanel.innerHTML).toContain('User message snippet');
  expect(chatHistoryPanel.innerHTML).toContain('AI message snippet');
});


test('handleSubmit prevents submission with empty input', () => {
    document.body.innerHTML = `
      <form id="input-form">
        <input id="user_input" value="" />
      </form>
    `;
  
    const mockEvent = { preventDefault: jest.fn() };
    document.getElementById("input-form").addEventListener("submit", handleSubmit);
    
    // Mock submission
    const form = document.getElementById("input-form");
    form.dispatchEvent(new Event('submit', mockEvent));
  
    // Verify preventDefault was called, indicating submission was blocked
    expect(mockEvent.preventDefault).toHaveBeenCalled();
  });
  
