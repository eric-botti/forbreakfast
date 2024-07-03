import { Metadata } from 'next';
import App from "@/components/component/app";

export const metadata: Metadata = {
  title: 'for breakfast'
};

export default function Home() {
  return (
    <main className="w-full md:w-4/5 mx-auto">
        <App />
    </main>
    
  );
}
