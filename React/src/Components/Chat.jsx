import { useEffect, useState } from "react";
import './chat.css';

function StudyBot() {
    // State to store chat messages (array of objects)
    const [messages, setMessages] = useState([]);
    
    // State to manage input from the user
    const [input, setInput] = useState('');
    
    // State to handle potential errors
    const [error, setError] = useState(null);

    // Retrieve stored chat messages from localStorage when the component loads
    useEffect(() => {
        const storeMessage = localStorage.getItem('chatMessages');
        if (storeMessage) {
            setMessages(JSON.parse(storeMessage));  // Parse JSON string to array of objects
        }
    }, []);

    // Update localStorage whenever messages change
    useEffect(() => {
        localStorage.setItem('chatMessages', JSON.stringify(messages));
    }, [messages]);

    // Function to delete a specific message based on index
    const reset = (indexToDelete) => {
        setMessages(messages.filter((_, index) => index !== indexToDelete));
    };

    // Handle user input and send messages to the backend
    const handleSendMessages = async (e) => {
        e.preventDefault();  // Prevent the form from reloading the page

        if (input.trim() === "") return;  // Do nothing if the input is empty

        try {

            // Send a POST request to the API with the user's question and conversation history
            const response = await fetch('/api/disease-check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: input,      // User's question (input)
                    conversation: messages  // Send entire conversation (chat history)
                }),
            });
            

            // Parse the JSON response from the backend
            const data = await response.json();
            const reply = data.results;  // Extract the 'notes' field (bot's reply)

            // Update the message list with the user's input and bot's reply
            setMessages([...messages,
                { role: 'user', content: input },  // User message object
                { role: 'bot', content: reply }     // Bot response object
            ]);
            
            setInput("");  // Clear input field after sending message
        } catch (error) {
            console.error("Error sending message:", error);
            setError("Failed to send message. Try again!");  // Display error to the user
        }
    };

    // Reset the entire chat
    const resetMessages = () => {
        setMessages([]);  // Clear all messages
        localStorage.removeItem('chatMessages');  // Remove stored messages from localStorage
    };

    return (
        <>
            <div className="chat-container">
                
                {/* Message Display */}
                <div>
                    {messages.map((message, index) => (
                        <div key={index} className={`message ${message.role}`}>
                            <span>{message.content}</span>
                            <button
                                className="delete-button"
                                onClick={() => reset(index)}  // Delete a specific message
                            >
                                ✖
                            </button>
                        </div>
                    ))}
                </div>
 
                {/* Input Form to Send Messages */}
                <form className="input-box" onSubmit={handleSendMessages}>
                    <input
                        className='chatbox'
                        placeholder="Ask any question"
                        value={input}  // Bind input state to the text box
                        onChange={(e) => setInput(e.target.value)}  // Update input on change
                    />
                    <button type='submit'>Send</button>
                </form>

                {/* Error Message Display */}
                {error && <p className="error-message">{error}</p>}

                {/* Reset Entire Chat */}
                <button className="reset-button" onClick={resetMessages}>
                    Reset Chat
                </button>
            </div>
        </>
    );
}

export default StudyBot;
