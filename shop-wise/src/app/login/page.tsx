import Link from "next/link";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

export default function Login() {
  return (
    
      <div className="login">
        <div className="login-container">
            <div className="login-header">ShopWise Login</div>
            <Box
                component="form"
                sx={{ '& .MuiTextField-root': { m: 1, width: '25ch',borderColor:'#fffff'} }}
                noValidate
                autoComplete="off"
                className="login-form"
                >
                <div>
                    <TextField
                    required
                    id="outlined-required"
                    label="Required"
                    defaultValue="Username"

                    sx={{
                        '& .MuiInputBase-root': {
                          color: '#ffffff', // Text color inside the input field
                        },
                        '& .MuiInputLabel-root': {
                          color: '#ffffff', // Label color (without required asterisk)
                        },
                        '& .MuiInputLabel-root.Mui-required': {
                          color: '#fffff', // Color of the "required" asterisk
                        },
                        '& .MuiOutlinedInput-root': {
                          '& fieldset': {
                            borderColor: '#ffffff', // Outline color of the TextField
                          },
                          '&:hover fieldset': {
                            borderColor: '#5cecc4', // Outline color on hover
                          },
                          '&.Mui-focused fieldset': {
                            borderColor: '#5cecc4', // Outline color when focused
                          },
                        },
                        paddingBottom: 5, // Add margin bottom to the TextField
                      }}
                    />
                    <TextField
                    required
                    id="outlined-required"
                    label="Required"
                    defaultValue="Password"
 
                    sx={{
                        '& .MuiInputBase-root': {
                          color: '#ffffff', // Text color inside the input field
                        },
                        '& .MuiInputLabel-root': {
                          color: '#ffffff', // Label color (without required asterisk)
                        },
                        '& .MuiInputLabel-root.Mui-required': {
                          color: '#fffff', // Color of the "required" asterisk
                        },
                        '& .MuiOutlinedInput-root': {
                          '& fieldset': {
                            borderColor: '#ffffff', // Outline color of the TextField
                          },
                          '&:hover fieldset': {
                            borderColor: '#5cecc4', // Outline color on hover
                          },
                          '&.Mui-focused fieldset': {
                            borderColor: '#5cecc4', // Outline color when focused
                          },
                        },
                      }}
                    />
                </div>
            </Box>
            <nav className="nav login primary">    
                <Link href="/BlackList">Login</Link>
            </nav>
        </div>

      </div>
 
  );
}