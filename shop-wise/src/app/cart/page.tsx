"use client";

import RoomIcon from "@mui/icons-material/Room";
import BottomBar from "../BottomBar/bottomBar";
import { useEffect, useState, useRef } from "react";
import { useWebSocket } from "@/app/context/WebSocketContext"; 
import { useClient } from "../context/ClientContext"; 
import InvalidItemPopUp from "../InvalidItemPopUp/InvalidItemPopUp";
import AlternativeItemPopUp from "../AlternativeItemPopUp/AlternativeItemPopUp";

export default function Cart() {
  const { cartData, setCartData } = useWebSocket();
  const { clientId } = useClient();

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

  // State to handle pop-ups
  const [showInvalidPopup, setShowInvalidPopup] = useState(false);
  const [showAlternativePopup, setShowAlternativePopup] = useState(false);
  const [flaggedItem, setFlaggedItem] = useState<CartItem | null>(null);

  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (cartData && cartData.cart_products.length > 0) {
      const lastItem = cartData.cart_products[cartData.cart_products.length - 1];

      if (!lastItem.product_flagged) {
        setFlaggedItem(lastItem);
        setShowInvalidPopup(true);
      }
    }
  }, [cartData, clientId]);

  useEffect(() => {
    const fetchCartData = async () => {
      if (!clientId) return;
      try {
        const response = await fetch(`http://193.236.212.127:8000/get/${clientId}/shopping_cart/products`);
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
    fetchCartData();
  }, [clientId, setCartData]);

  useEffect(() => {
    if (showInvalidPopup && audioRef.current) {
      audioRef.current.play().catch(err => console.error("Error playing sound:", err));
    }
  }, [showInvalidPopup]);


  const handlePay = async () => {
    if (!clientId) return;
    try {
      const response = await fetch("http://193.236.212.127:8000/pay", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "client-id": String(clientId),
        },
      });
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error during payment:", errorText);
        return;
      }
      setCartData(null); 
    } catch (error) {
      console.error("Error during payment:", error);
    }
  }

  return (
    <div className="black-list">
      <div className="location-container">
        <div className="location">TecStorm</div>
        <div className="location-icon">
          <RoomIcon style={{ color: "black" }} />
        </div>
      </div>

      <div className="black-list-container">
        <div className="your-black-list-text">Your Shopping Cart:</div>

        {/* Conditionally render the InvalidItemPopUp */}
        {showInvalidPopup && flaggedItem && (
          <div>

          <audio ref={audioRef}>
                <source src="/notific.wav" type="audio/mpeg" />
              </audio>
            <InvalidItemPopUp 
              itemName={flaggedItem.name} 
              onClose={() => setShowInvalidPopup(false)} 
              onAlternative={() => {
                setShowInvalidPopup(false);
                setShowAlternativePopup(true);
              }} 
            />
          </div>
        )}

        {/* Conditionally render the AlternativeItemPopUp */}
        {showAlternativePopup && flaggedItem && (
          <AlternativeItemPopUp 
            itemName={flaggedItem.name} 
            productId={flaggedItem.product_id}
            onClose={() => setShowAlternativePopup(false)} 
          />
        )}

        <ul style={{ color: "black", flex: "1", fontSize: "1.1rem" }}>
          {cartData && cartData.cart_products.length > 0 ? (
            cartData.cart_products.map((item, index) => (
              <li
                key={index}
                style={{
                  color: item.product_flagged ? "black" : "red",
                  fontWeight: item.product_flagged ? "bold" : "normal",
                }}
              >
                {item.name} ({item.brand}) - {item.product_quantity}x - $
                {item.product_total}
              </li>
            ))
          ) : (
            <li>No items in cart</li>
          )}
        </ul>
        <div style={{display:"flex",alignItems:"center",gap:"1rem",width:"100%",  borderTop: "1.3px solid rgba(95, 95, 95, 0.65)"}}>
          <div className="shopping-cart-total">
            Total: ${cartData?.total_cart_price ?? 0}
          </div>
          <nav className="nav pay" onClick={handlePay}>
            Pay
          </nav>
        </div>

        <BottomBar currentPage="cart" />
      </div>
    </div>
  );
}
