import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [outputText, setOutputText] = useState('');
  const [videoSrc, setVideoSrc] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: input }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error: ${response.status} ${response.statusText}\n${errorText}`);
      }

      const data = await response.json();
      setOutputText(data.text);
      setVideoSrc(`http://localhost:5000/videos/${data.video}`);
    } catch (error) {
      setError(error.message);
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setInput('');
    setOutputText('');
    setVideoSrc('');
    setError(null);
  };

  return (
    <div className="container">
      <div className="main">
        {isLoading && <div className="loading">Loading...</div>}
        <div className="output">
          {error && <div className="error">{error}</div>}
          <ReactMarkdown>{outputText}</ReactMarkdown>
          {videoSrc && <video src={videoSrc} controls />}
        </div>
        <div className="input">
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter Topic"
            />
            <button type="submit">Submit</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
