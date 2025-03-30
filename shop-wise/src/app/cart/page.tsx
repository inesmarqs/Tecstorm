"use client";

import RoomIcon from "@mui/icons-material/Room";
import BottomBar from "../BottomBar/bottomBar";
import { useEffect, useState } from "react";

export default function Cart() {
    const [messages, setMessages] = useState<string[]>([]);
    
      useEffect(() => {
        const socket = new WebSocket("ws://192.168.1.136:8000/ws");
 
    
        socket.onopen = () => {
          console.log("Connected to WebSocket server");
          socket.send("Hello Server!");
        };
    
        socket.onmessage = (event) => {
          console.log("Message from server:", event.data);
          setMessages((prev) => [...prev, event.data]);
        };
    
        socket.onerror = (error) => {
          console.error("WebSocket error:", error);
        };
    
        socket.onclose = () => {
          console.log("WebSocket connection closed");
        };
    
       
      }, []);
    
    return (
        <div className="black-list">
            <div className="location-container">
                <div className="location">TecStorm</div>
                <div className="location-icon">
                    <RoomIcon style={{ color: "black" }} />
                </div>
            </div>

            <div className="black-list-container">
                <div className="your-black-list-text">Your Shopping Cart: </div>
                <div className="black-list-items-container"></div>
                <h2>WebSocket Messages</h2>
                    <ul style={{color: "black"}}>
                        {messages.map((msg, index) => (
                        <li key={index}>{msg}</li>
                        ))}
                    </ul>
                <div className="shopping-cart-total">Total:</div>
                <BottomBar currentPage="cart" />
            </div>
        </div>
        );
}