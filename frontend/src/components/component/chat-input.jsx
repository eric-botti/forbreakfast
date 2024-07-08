import {Textarea} from "../ui/textarea";
import {Button} from "../ui/button";
import React from "react";

function CalcBasis(num) {
    // If the number is divisible by 3, return 1/4
    if (num <= 2 || num === 4) {
      return "w-1/3";
    }
    else {
        return "w-1/4";
    }
}

export default function ChatInput( {handleSendMessage, newMessage, setNewMessage, choices} ) {

    return (
<div className="bg-background border-t px-4 py-3">
    {choices ? (
        <div className={`flex flex-wrap justify-center gap-2 w-full items-center`}>
            {choices.map((option) => (
              <Button
                  key={option}
                  variant={"outline"}
                  className={`${CalcBasis(choices.length)} px-4 py-2 text-sm`}
                  onClick={() => handleSendMessage(option)}
              >
                {option}
              </Button>
            ))}
        </div>
        ) : (
        <div className="relative">
        <Textarea
            placeholder="Type your message..."
            value={newMessage}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                handleSendMessage(newMessage);
              }
            }}
            onChange={(e) => setNewMessage(e.target.value)}
            className="min-h-4 resize-none border border-neutral-400 shadow-sm text-base"
        />
        <Button
          type="button"
          size="icon"
          className="absolute w-8 h-8 top-3 right-3"
          onClick={() => handleSendMessage(newMessage)}
        >
            <SendIcon className="w-4 h-4" />
            <span className="sr-only">Send</span>
        </Button>
    </div> )
    }
</div>
    )
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