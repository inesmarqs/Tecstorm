"use client";

import { useEffect, useState } from "react";
import { useClient } from "../context/ClientContext";

export default function AlternativeItemPopUp({ itemName, onClose, productId }: { 
  itemName: string; 
  productId: number;
  onClose: () => void; 
}) {

    const [recommendation, setRecommendation] = useState<{ 
        name: string;
        brand: string;
        price: number | string;
        location: string;
    } | null>(null);
    
    const { clientId } = useClient();

    const [showLocation, setShowLocation] = useState(false);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const response = await fetch("http://192.168.1.136:8000/recommendations", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "product-id": String(productId),
                        "client-id": String(clientId),
                    },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch recommendations");
                }

                const data = await response.json();
                console.log("Received recommendations:", JSON.stringify(data, null, 2));

                if (data.response && Array.isArray(data.response) && data.response.length === 4) {
                    setRecommendation({
                        name: data.response[0] || "Unknown Item",
                        brand: data.response[1] || "Unknown Brand",
                        price: data.response[2] !== undefined ? data.response[2] : "N/A",
                        location: "Tecstorm B7",
                    });
                } else {
                    setRecommendation(null);
                }
            } catch (error) {
                console.error("Error fetching recommendations:", error);
                setRecommendation(null);
            }
        };

        fetchRecommendations();
    }, [productId, clientId]);


    const handleTakeMeThere = () => {
        setShowLocation(true);
    }
  
        


    return (
        <div className="popup-overlay">
            <div className="popup">
                <h2>Alternative Suggestion</h2>
                <p>Looking for alternatives to <strong>{itemName}</strong>...</p>
                
                {recommendation ? (
                    <ul>
                        <div style={{ justifySelf: "center" }}>
                            <strong>{recommendation.name}</strong> ({recommendation.brand}) - ${recommendation.price}

                        </div>
                    </ul>
                ) : (
                    <p>No alternatives found.</p>
                )}
                {showLocation && recommendation && (
                    <div style={{ justifySelf: "center" }}>
                        <p style={{fontWeight:"bold"}}>Location: {recommendation.location}</p>
                    </div>
                )}
                <div style={{ display: "flex", justifyContent: "center" ,gap: "3rem"}}>

                    <button onClick={handleTakeMeThere}>Take me there</button>
                    <button onClick={onClose}>Close</button>
                </div>
            </div>
            
            <style jsx>{`
                .popup-overlay {
                    color: black;
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .popup {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                    text-align: center;
                }
                button {
                    margin-top: 10px;
                    padding: 8px 12px;
                    cursor: pointer;
                }
            `}</style>
        </div>
    );
}
