"use client";

import RoomIcon from "@mui/icons-material/Room";
import BottomBar from "../BottomBar/bottomBar";
import { useEffect } from "react";
import { useWebSocket } from "@/app/context/WebSocketContext"; // Import WebSocket context

export default function Cart() {
  const { cartData } = useWebSocket();

  useEffect(() => {
    if (cartData && cartData.cart_products.length > 0) {
      const lastItem = cartData.cart_products[cartData.cart_products.length - 1];

      if (lastItem.product_flagged) {
        alert(`Warning: The last added item (${lastItem.name}) has been flagged!`);
      }
    }
  }, [cartData]); 

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

        <ul style={{ color: "black" }}>
          {cartData && cartData.cart_products.length > 0 ? (
            cartData.cart_products.map((item, index) => (
              <li
                key={index}
                style={{
                  color: item.product_flagged ? "orange" : "black",
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

        <div className="shopping-cart-total">
          Total: ${cartData?.total_cart_price ?? 0}
        </div>

        <BottomBar currentPage="cart" />
      </div>
    </div>
  );
}
