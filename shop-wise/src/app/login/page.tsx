"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import {useClient} from "../context/ClientContext"; // Adjust the import path as necessary
import Link from "next/link";



export default function Login() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const router = useRouter();
    const { setClientId } = useClient();

    const handleLogin = async () => {
        console.log("Username:", username);
        console.log("Password:", password);
        try {
        const response = await fetch("http://192.168.1.136:8000/login", {
            method: "POST",
            headers: {
            "username": username,
            "password": password,
            },
        });

        if (!response.ok) {
            throw new Error("Login failed");
        }


        const clientId = await response.json();
        console.log("Client ID:", clientId);
        setClientId(clientId); 

        router.push("/BlackList");

    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  return (
    <div className="login">
      <div className="login-container">
        <div className="login-header">ShopWise Login</div>
        <Box
          component="form"
          sx={{
            '& .MuiTextField-root': {
              m: 1,
              width: '25ch',
            }
          }}
          noValidate
          autoComplete="off"
          className="login-form"
        >
          <div>
            <TextField
              required
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              
              sx={{
                '& .MuiInputBase-root': { color: '#ffffff' },
                '& .MuiInputLabel-root': { color: '#ffffff' },
                '& .MuiOutlinedInput-root': {
                  '& fieldset': { borderColor: '#ffffff' },
                  '&:hover fieldset': { borderColor: '#5cecc4' },
                  '&.Mui-focused fieldset': { borderColor: '#5cecc4' },
                },
                mb: 2,
              }}
            />
            <TextField
              required
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}

              sx={{
                '& .MuiInputBase-root': { color: '#ffffff' },
                '& .MuiInputLabel-root': { color: '#ffffff' },
                '& .MuiOutlinedInput-root': {
                  '& fieldset': { borderColor: '#ffffff' },
                  '&:hover fieldset': { borderColor: '#5cecc4' },
                  '&.Mui-focused fieldset': { borderColor: '#5cecc4' },
                },
              }}
            />
          </div>
        </Box>

        <nav className="nav login primary" onClick={handleLogin}>
            <div >Login</div>
        </nav>
      </div>
    </div>
  );
}
