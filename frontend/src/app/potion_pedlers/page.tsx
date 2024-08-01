'use client'

import {Metadata} from "next";
import { Ingredients } from "@/components/component/ingredients";
import {useState} from "react";


// Returns a list of random ingredients to initialize the marketplace
function randomIngredients(count= 6 ) {
    const ingredients = [
      {
        id: 0,
        name: "Ironwood Root",
        description: "A sturdy root imbued with earthen magic",
        quantity: 3,
      },
      {
        id: 1,
        name: "Mana Pearl",
        description: "A rare crystal fruit that grows in the deepest parts of the ocean",
        quantity: 2,
      },
      {
        id: 2,
        name: "Aether Droplet",
        description: "A rare shimmering droplet that falls from the sky",
        quantity: 1,
      },
      {
        id: 4,
        name: "Phoenix Flower",
        description: "A fiery flower that grows where a phoenix has risen from its ashes",
        quantity: 1,
      },
    ]

    // Randomly select ingredients from the list
    const marketplace = []
    for (let i = 0; i < count; i++) {
      const randomIndex = Math.floor(Math.random() * ingredients.length)
      marketplace.push(ingredients[randomIndex])
    }

    return marketplace;
}



export default function PotionPeddlers() {
  const [playerInventory, setPlayerInventory] = useState([])
  const [marketplace, setMarketplace] = useState(randomIngredients())

  return (
    <main className="w-full md:w-4/5 mx-auto">
        <Ingredients playerInventory={playerInventory} marketplace={marketplace} />
    </main>
    
  );
}
