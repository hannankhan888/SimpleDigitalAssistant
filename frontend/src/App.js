import logo from './logo.svg';
import './App.css';
import React from 'react';

class App extends React.Component {
  componentDidMount() {
    const ws = new WebSocket('ws://localhost:8000/ws')
    ws.onmessage = this.onMessage

    this.setState({
      ws: ws,
      // Create an interval to send echo messages to the server
      interval: setInterval(() => ws.send('echo'), 1000)
    })
  }

  componentWillUnmount() {
    const {ws, interval} = this.state;
    ws.close()
    clearInterval(interval)
  }

  onMessage = (ev) => {
    
    console.log(JSON.parse(ev.data))
  }

  render() {
    return (
      <div className="container">
    <div className="box">
      <h2>Max</h2>
      <button> Start/Stop </button>
    </div>
    <div className="box">
      <h2>Output</h2>
    </div>

    </div>
    )
  }
}

export default App;
