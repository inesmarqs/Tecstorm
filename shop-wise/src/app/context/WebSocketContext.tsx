"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useClient } from "@/app/context/ClientContext"; // Import ClientContext

type CartItem = {
  product_id: number;
  name: string;
  brand: string;
  product_flagged: boolean;
  product_total: number;
  product_quantity: number;
};

type CartData = {
  client_id: number;
  cart_products: CartItem[];
  total_cart_price: number;
};

const WebSocketContext = createContext<{ cartData: CartData | null }>({
  cartData: null,
});

export const WebSocketProvider = ({ children }: { children: React.ReactNode }) => {
  const [cartData, setCartData] = useState<CartData | null>(null);
  const { clientId } = useClient();
  const backendUrl = "http://193.236.212.127:8000"; // Your backend URL

  useEffect(() => {
    if (!clientId) return;

    const socket = new WebSocket(`${backendUrl.replace("http", "ws")}/ws`);

    socket.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    socket.onmessage = async (event) => {
      console.log("Message from server:", event.data);

      try {
        const response = await fetch(`${backendUrl}/get/${clientId}/shopping_cart/products`);
        if (response.ok) {
          const data: CartData = await response.json();
          setCartData(data);
        } else {
          console.error("Failed to fetch cart data");
        }
      } catch (error) {
        console.error("Error fetching cart data:", error);
      }
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    return () => socket.close();
  }, [clientId]);

  return (
    <WebSocketContext.Provider value={{ cartData }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => useContext(WebSocketContext);
