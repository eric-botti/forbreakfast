"use client";

import { Metadata } from 'next';
import { CharacterMaker } from "@/components/component/character-maker";


export default function CharacterCreator() {

  return (
    <main className="w-full md:w-4/5 mx-auto flex flex-col align ">
        <CharacterMaker className="mx-auto"/>
    </main>
  );
}
