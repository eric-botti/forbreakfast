// ChatMessage.js

import React from "react";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";

export default function ChatMessage({ message }) {
  let message_div;

  switch (message.sender) {
    case "You":
      message_div = (
          <div className={`rounded-lg p-3 max-w-[70%] bg-primary text-primary-foreground`}>
            <p className="text-base">{message.content}</p>
          </div>
      )
        break;
    case "Game Master":
        message_div = (
            <>
              <div
                className="rounded-lg p-3 md:max-w-[70%] border-l-4 border-complementary-accent bg-complementary"
              >
                <span className="font-semibold text-sm">{message.sender}</span>
                <div className="text-base" dangerouslySetInnerHTML={{ __html: message.content }}></div>
              </div>
            </>
        )
        break;
    default:
      message_div = (<>
              <div
                className="bg-muted rounded-lg p-3 md:max-w-[70%] flex gap-2 items-center"
              >
                <Avatar className="w-10 h-10 rounded-lg">
                    <AvatarImage src={`/avatars/${(message.sender)}.png`} />
                    <AvatarFallback className="bg-background">{message.sender.charAt(0)}</AvatarFallback>
                </Avatar>
                <div>
                    <span className="text-sm font-bold">{message.sender}</span>
                    <div className="text-base" dangerouslySetInnerHTML={{ __html: message.content }}></div>
                </div>
              </div>

            </>
      )
  }


  return (
    <div className={`fade-in flex items-start gap-3 ${message.sender === "You" ? "justify-end" : ""}`}>
      {(message_div)}
    </div>
  );
}

