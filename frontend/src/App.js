import logo from './logo.svg';
import './App.css';
import React, {useState, useRef, useEffect} from 'react';

function App() {
  const [isRecording, setRecording] = useState(false);
  const ws = useRef(null);
  const mediaRecorder = useRef(null);
  let chunks = useRef([]);

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({video: false, audio: true}).then( stream => {
      mediaRecorder.current = new MediaRecorder(stream);
      mediaRecorder.current.ondataavailable = e => {
        if (e.data) {
          e.data.arrayBuffer().then(buffer => {
            console.log(e.data);
            ws.current.send(e.data);
          });
          chunks.current.push(e.data);
          
          // ws.current.send(e.data.text());
          // console.log('sending data', e.data.text());
        }
      }
    })
    
    
    ws.current = new WebSocket('ws://localhost:8000/ws');
    ws.current.onopen = () => {
      console.log('ws opened')
    };
    ws.current.onmessage = e => {
      const message = JSON.parse(e.data);
      console.log('e', message.value);
    };
    ws.current.onclose = () => console.log('ws closed');

    return () => {
        ws.current.close();
    };
  }, []);

  useEffect(() => {
      if (!isRecording) {
        if (mediaRecorder.current !== null) mediaRecorder.current.stop();
        return

      };
      if (isRecording && ws.current.readyState === 1) {
        mediaRecorder.current.start(5000);
        console.log('starting recording')
      };


  }, [isRecording]);

  return (
    <div className='container'>
      <div className='box'>
        <h2>Max</h2>
        <button onClick={() => setRecording(!isRecording)}>
                {isRecording ? "Stop" : "Start"}
        </button>
      </div>
      <div className='box'>
        <h2>Output</h2>
      </div>
    </div>
    )
  }

export default App;
