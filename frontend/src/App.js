import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [matchedQuestion, setMatchedQuestion] = useState('');
  const [source, setSource] = useState('');
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Load chat history on component mount
  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('/history');
      const data = await response.json();
      setHistory(data.history || []);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch('/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      });

      if (response.ok) {
        const data = await response.json();
        setAnswer(data.answer);
        setMatchedQuestion(data.matched_question);
        setSource(data.source);
        setQuestion('');
        fetchHistory(); // Refresh history
      } else {
        setAnswer('Sorry, there was an error processing your question.');
        setSource('error');
      }
    } catch (error) {
      console.error('Error:', error);
      setAnswer('Sorry, there was an error connecting to the server.');
      setSource('error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuestionClick = (q) => {
    setQuestion(q);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Professional AI Chatbot</h1>
        <p>Ask me about productivity, remote work, startups, and more!</p>
      </header>

      <main className="App-main">
        <div className="chat-container">
          <div className="chat-history">
            <h3>Recent Questions</h3>
            {history.length === 0 ? (
              <p>No chat history yet. Ask a question to get started!</p>
            ) : (
              <ul>
                {history.map((item, index) => (
                  <li key={index} onClick={() => handleQuestionClick(item.question)}>
                    <strong>Q:</strong> {item.question}<br />
                    <strong>A:</strong> {item.answer.substring(0, 50)}...
                    {item.source === 'openrouter' && <span className="source-tag">AI</span>}
                    {item.source === 'knowledge_base' && <span className="source-tag">KB</span>}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="chat-interface">
            <form onSubmit={handleSubmit} className="question-form">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a professional question..."
                disabled={isLoading}
              />
              <button type="submit" disabled={isLoading}>
                {isLoading ? 'Thinking...' : 'Ask'}
              </button>
            </form>

            {matchedQuestion && (
              <div className="matched-question">
                <p>Matched question: <em>"{matchedQuestion}"</em></p>
              </div>
            )}

            {answer && (
              <div className="answer">
                <h3>Answer:</h3>
                <p>{answer}</p>
                {source === 'openrouter' && (
                  <div className="ai-badge">
                    <small>AI-generated answer</small>
                  </div>
                )}
                {source === 'knowledge_base' && (
                  <div className="kb-badge">
                    <small>From knowledge base</small>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;