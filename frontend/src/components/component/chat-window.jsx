// ChatWindow.js
"use client";

import React, {useEffect, useState} from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import ChatMessage from "@/components/component/chat-message";
import ChatInput from "@/components/component/chat-input";
import HowToPlay from "@/components/component/how-to-play";
import { useWebSocketChat} from "@/components/component/WebSocket";

export default function ChatWindow({ name }) {
  const [messages, setMessages] = useState([]);

  const [newMessage, setNewMessage] = useState("");

  const { sendMessage, onMessageReceived } = useWebSocketChat(name);

  const choices = null

  const handleSendMessage = async (message) => {
    if (message.trim() !== "") {
      const newMessageObj = {
        id: messages.length + 1,
        sender: "You",
        content: message,
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
  <ChatInput handleSendMessage={handleSendMessage} newMessage={newMessage} setNewMessage={setNewMessage} choices={choices} />
  </div>
</div>

  );
}