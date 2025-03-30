"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation"; 
import RoomIcon from "@mui/icons-material/Room";
import AddIcon from "@mui/icons-material/Add";
import BottomBar from "../BottomBar/bottomBar";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import { useClient } from "../context/ClientContext";


export default function BlackList() {
  const [showAddItem, setShowAddItem] = useState(false);
  const [newItem, setNewItem] = useState(""); 
  const [blacklist, setBlacklist] = useState<string[]>([]); 

  const { clientId } = useClient();
    

  useEffect(() => {
    const fetchBlacklist = async () => {
      try {
        const response = await fetch("http://193.236.212.127:8000/getBlackList", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "client-id": String(clientId),
          },
        });
    
        const data = await response.json();
        console.log("Fetched Blacklist Data:", data); // Debugging line
    
        if (Array.isArray(data.blacklist)) {
          setBlacklist(data.blacklist); // ✅ Extract the array
        } else {
          console.error("API did not return an array:", data);
          setBlacklist([]); // Ensure it's always an array
        }
      } catch (error) {
        console.error("Error fetching blacklist:", error);
      }
    };
    
  
    fetchBlacklist();
  }, [clientId]); 
  

  const handleAddNewItem = async () => {
      if (!newItem.trim()) {
      console.error("No allergen name provided!");
      return;
      }
  
      if (!clientId) {
      console.error("Client ID is missing:", clientId);
      return;
      }
  
      try {
      const response = await fetch("http://193.236.212.127:8000/addToBlackList", {
          method: "POST",
          headers: {
              "Content-Type": "application/json", 
              "client-id": String(clientId),      
            },
          body: JSON.stringify(newItem),
      });
  
      if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Failed to add item: ${errorText}`);
      }
  
      console.log("Item added successfully!");
      setBlacklist([...blacklist, newItem]); 
      setNewItem(""); 
      setShowAddItem(false); 
  
      } catch (error) {
      console.error("Error adding item:", error);
      }
  };
  

  // Handle deleting an item from the blacklist
  const handleDeleteItem = (itemToDelete: string) => {
    setBlacklist(blacklist.filter(item => item !== itemToDelete));

    try{
        fetch("http://193.236.212.127:8000/removeFromBlackList", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            "client-id": String(clientId),
            },
            body: JSON.stringify(itemToDelete),
        });
    }catch(error){
        console.error("Error deleting item:", error);
    }
  };

  // Show add item form
  const handleAddItem = () => {
    setShowAddItem(true);
  };

  return (
    <div className="black-list">
      <div className="location-container">
        <div className="location">TecStorm</div>
        <div className="location-icon">
          <RoomIcon style={{ color: "black" }} />
        </div>
      </div>

      <div className="black-list-text">
        <div style={{ fontSize: "1.3rem" }}>Olá, Diogo Falcão </div>
        <div style={{ fontWeight: "normal" }}>
          Fazer compras assim, é tão fácil !
        </div>
      </div>

      <div className="black-list-container">
        <div className="your-black-list-text">Your BlackList: </div>

        {/* Render list of items */}
        <div className="black-list-items-container">
          {blacklist.map((item, index) => (
            <div key={index} className="black-list-item">
              <span style={{flex:"1"}}>{item}</span>
              <DeleteOutlineIcon
                fontSize="medium"
                style={{
                  color: "black",
                  padding: "10px",
                  cursor: "pointer",
                }}
                onClick={() => handleDeleteItem(item)} 
              />
            </div>
          ))}
        </div>

        {/* Show the AddNewItem form if showAddItem is true */}
        {showAddItem && (
          <div className="add-new-item">
            <Box
              component="form"
              sx={{ '& > :not(style)': { m: 1, width: '15ch' } }}
              noValidate
              autoComplete="off"
            >
              <TextField 
                id="standard-basic" 
                label="New Restriction" 
                variant="standard" 
                value={newItem}
                onChange={(e) => setNewItem(e.target.value)} 
              />
            </Box>
            <div className="nav add" onClick={handleAddNewItem}>Add</div>
          </div>
        )}

        <AddIcon
          fontSize="large"
          style={{
            color: "black",
            padding: "10px",
            cursor: "pointer",
          }}
          onClick={handleAddItem} 
        />

        <BottomBar currentPage="black-list" />
      </div>
    </div>
  );
}
