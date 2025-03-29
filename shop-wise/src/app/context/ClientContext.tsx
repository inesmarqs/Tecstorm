"use client";

import { createContext, useContext, useState, useEffect } from "react";

// Define context type
interface ClientContextType {
  clientId: string | null;
  setClientId: (id: string | null) => void;
}

// Create context
const ClientContext = createContext<ClientContextType | undefined>(undefined);

// Custom hook to use the context
export function useClient() {
  const context = useContext(ClientContext);
  if (!context) {
    throw new Error("useClient must be used within a ClientProvider");
  }
  return context;
}

// Provider component
export function ClientProvider({ children }: { children: React.ReactNode }) {
  const [clientId, setClientIdState] = useState<string | null>(null);

  // Load clientId from localStorage on first render
  useEffect(() => {
    const storedClientId = localStorage.getItem("clientId");
    if (storedClientId) {
      setClientIdState(storedClientId);
    }
  }, []);

  // Save clientId to localStorage whenever it changes
  const setClientId = (id: string | null) => {
    setClientIdState(id);
    if (id) {
      localStorage.setItem("clientId", id);
    } else {
      localStorage.removeItem("clientId");
    }
  };

  return (
    <ClientContext.Provider value={{ clientId, setClientId }}>
      {children}
    </ClientContext.Provider>
  );
}
