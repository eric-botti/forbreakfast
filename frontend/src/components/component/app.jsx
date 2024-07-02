// app.js
"use client"

import React, { useState } from "react";
import ChatWindow from "@/components/component/chat-window";
import {Welcome} from "@/components/component/welcome";

export default function App() {
  const [name, setName] = useState('');
  const [isNameEntered, setIsNameEntered] = useState(false);

  const handleNameSubmit = (name) => {
    setName(name);
    setIsNameEntered(true);
  };

  return (
    <div>
      {!isNameEntered ? (
        <Welcome onNameSubmit={handleNameSubmit} />
      ) : (
        <ChatWindow name={ name }/>
      )}
    </div>
  );
}
