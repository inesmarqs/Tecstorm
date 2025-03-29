import Link from "next/link";
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import ListAltIcon from '@mui/icons-material/ListAlt';

interface BottomBarProps {
    currentPage: string;
}

export default function BottomBar({ currentPage }: BottomBarProps) {
    return (
        <div className="bottom-bar-container">
            <div className="bottom-bar">
                <Link href="/profile" className="bottom-bar-icon">
                    <AccountBoxIcon 
                    fontSize="large" 
                    style={{ color: currentPage === "profile" ? "#5cecc4" : "white" }} />
                </Link>
                <Link href="/cart" className="bottom-bar-icon">
                    <ShoppingCartIcon 
                    fontSize="large" 
                    style={{ color: currentPage === "cart" ? "#5cecc4" : "white" }} />
                </Link>
                <Link href="/black-list" className="bottom-bar-icon">
                    <ListAltIcon 
                    fontSize="large" 
                    style={{ color: currentPage === "black-list" ? "#5cecc4" : "white" }} />
                </Link>
            </div>
        </div>
    );
}
