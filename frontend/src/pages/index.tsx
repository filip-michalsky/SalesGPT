import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import Header from '../components/ui/Header'; // Adjust the import path as necessary

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.push('/chat');
  }, [router]);

  return (
    <div>
      <Header />
      <div className="flex justify-center items-center h-screen">
        <div className="spinner"></div>
        <p>Redirecting...</p>
      </div>
    </div>
  );
}