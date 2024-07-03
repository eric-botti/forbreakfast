// ChatWindow.js
"use client";

import React, {useEffect, useState} from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import ChatMessage from "@/components/component/chat-message";
import HowToPlay from "@/components/component/how-to-play";
import { useWebSocketChat} from "@/components/component/WebSocket";

export default function ChatWindow({ name }) {
  const [messages, setMessages] = useState([]);

  const [newMessage, setNewMessage] = useState("");

  const { sendMessage, onMessageReceived } = useWebSocketChat();



  const handleSendMessage = async () => {
    if (newMessage.trim() !== "") {
      const newMessageObj = {
        id: messages.length + 1,
        sender: "You",
        content: newMessage,
      };

      sendMessage(newMessageObj);
      setMessages([...messages, newMessageObj]);

      setNewMessage("");
    }
  };

  useEffect(() => {
    onMessageReceived((newBotMessageObj) => {
      console.log('Received message:', newBotMessageObj);
      setMessages(messages => [...messages, newBotMessageObj]);
    });
  }, []);


  return (
<div className="h-screen">
  <div className="flex flex-col h-full lg:max-w-screen-lg mx-auto my-50 bg-background">
    <div className="flex justify-end px-3 pt-3">
      <HowToPlay className="relative" />
    </div>
    <h1 className="text-3xl font-bold text-center pb-3">Chameleon</h1>

    <div className="flex-1 overflow-auto p-4">
      <ScrollArea className="h-full px-5">
        <div className="grid gap-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
        </div>
      </ScrollArea>
    </div>
  <div className="bg-background border-t px-4 py-3">
    <div className="relative">
      <Textarea
        placeholder="Type your message..."
        value={newMessage}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            handleSendMessage();
          }
        }}
        onChange={(e) => setNewMessage(e.target.value)}
        className="min-h-4 rounded-2xl resize-none border border-neutral-400 shadow-sm"
      />
        <Button
          type="button"
          size="icon"
          className="absolute w-8 h-8 top-3 right-3"
          onClick={handleSendMessage}
        >
          <SendIcon className="w-4 h-4" />
          <span className="sr-only">Send</span>
        </Button>
      </div>
    </div>
  </div>
</div>

  );
}

function SendIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m22 2-7 20-4-9-9-4Z" />
      <path d="M22 2 11 13" />
    </svg>
  )
}