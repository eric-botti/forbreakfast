/**
 * v0 by Vercel.
 * @see https://v0.dev/t/Gz79K0g76jI
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
"use client";
import { Dialog, DialogTrigger, DialogContent} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area";

import React, {useEffect, useState} from "react";



export default function HowToPlay() {
  const [open, setOpen] = useState(true);

  useEffect(() => {
    const handleEnterPress = (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
      }
    };

    // Clear any lingering Enter key events when the component mounts
    window.addEventListener('keydown', handleEnterPress);

    return () => {
      window.removeEventListener('keydown', handleEnterPress);
    };
  }, []);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="ghost" size="icon">
          <CircleHelpIcon className="h-6 w-6"/>
          <span className="sr-only">Help</span>
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[600px] max-h-full overflow-auto">
          <div className="flex flex-col items-center justify-center gap-4 py-4">
          <h2 className="text-2xl font-bold">How to Play</h2>
          <div className="space-y-4">
            <div className="text-sm space-y-2">
                <h3 className="text-lg font-medium">Premise</h3>
                <p>
                    You are playing a social deduction game where each player pretends the be the same animal.
                    The catch is that one player, the Chameleon, does not know what animal they are supposed to be.
                </p>
              <h3 className="text-lg font-medium">Rules</h3>
              <p>
                During a round each player gets a turn to describe themselves using an &ldquo;I&ldquo;-statement as if they were the animal.
                The Chameleon must blend in by providing details about the animal using context from other players.
                The rest of the players, the Herd, must be careful not to give away too much information with their responses so that the Chameleon can&lsquo;t deduce the animal.
              </p>
              <p>After all players have spoken, two thing will happen:</p>
              <ol className="list-decimal list-inside">
                  <li>The Chameleon will guess what animal the other players are pretending to be</li>
                  <li>The Herd will vote on who they think the Chameleon is</li>
              </ol>
              <h3 className="text-lg font-medium">Winning</h3>
              <p>The first player to reach 7 points wins, play continues until this is achieved.</p>
              <p>How a member of the Herd can earn points:</p>
              <ul className="list-disc list-inside space-y-1">
                    <li>If they correctly vote for the Chameleon (regardless of how other players vote)</li>
                    <li>If Chameleon is unable to guess the secret animal, all Herd players get a point</li>
              </ul>
              <p>The Chameleon can earn points if:</p>
              <ul className="list-disc list-inside space-y-1">
                  <li>Less than 50% of the herd votes from them</li>
                  <li>They guess the animal correctly</li>
              </ul>
              <p>A player can earn up to 2 points per round</p>
            </div>
          </div>
            <Button onClick={() => setOpen(false)}>Let&lsquo;s Do This</Button>
          </div>
      </DialogContent>
    </Dialog>
  )
}

function CircleHelpIcon(props) {
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
      <circle cx="12" cy="12" r="10" />
      <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
      <path d="M12 17h.01" />
    </svg>
  )
}