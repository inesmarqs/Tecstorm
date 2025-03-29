import RoomIcon from "@mui/icons-material/Room";
import BottomBar from "../BottomBar/bottomBar";

export default function Cart() {
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
                <div className="shopping-cart-total">Total:</div>
                <BottomBar currentPage="cart" />
            </div>
        </div>
        );
}