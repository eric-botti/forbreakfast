import { useEffect, useRef } from 'react';

export function useWebSocketChat(playerName) {
  const ws = useRef(null);
  const host = process.env.NEXT_PUBLIC_API_HOST || 'localhost';
  const url = `ws://${host}:5230/ws/${playerName}`;

  useEffect(() => {
    // Initialize WebSocket connection
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log('WebSocket connection established');
    };

    ws.current.onclose = () => {
      console.log('WebSocket connection closed');
    };

    // Clean up the WebSocket connection when the component unmounts
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [url]);

  const sendMessage = (message) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ message }));
    } else {
      console.error('WebSocket is not connected');
    }
  };

  const onMessageReceived = (callback) => {
    if (ws.current) {
      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        callback(data);
      };
    }
  };

  return { sendMessage, onMessageReceived };
}
