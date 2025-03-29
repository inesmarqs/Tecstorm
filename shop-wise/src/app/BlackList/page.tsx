import Link from "next/link";
import RoomIcon from '@mui/icons-material/Room'
import BottomBar from "../BottomBar/bottomBar";
import AddIcon from '@mui/icons-material/Add';
import BlackListItem from "../BlackListItem/page";




export default function BlackList() {

    
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
                <div style={{ fontWeight: "normal" }}>Fazer compras assim, é tão fácil !</div>
            </div>
            <div className="black-list-container">
                <div className="your-black-list-text">Your BlackList: </div>
                <div className="black-list-items-container">
                    <BlackListItem currentItem="BlackList Item 1" />
                </div>
                <div>
                    <AddIcon
                        fontSize="large"
                        style={{
                            color: "black",
                            padding: "10px",
                            cursor: "pointer",
                        }}
                        
                    />
                </div>
                    <BottomBar currentPage="black-list" />
            </div>
        

        </div>
    );
}