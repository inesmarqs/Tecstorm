export default function CartItems() {
    return (
        <div className="cart-items">
            <div className="cart-item">
                <div className="cart-item-name">Item 1</div>
                <div className="cart-item-quantity">Quantity: 1</div>
                <div className="cart-item-price">$10.00</div>
            </div>
            <div className="cart-item">
                <div className="cart-item-name">Item 2</div>
                <div className="cart-item-quantity">Quantity: 2</div>
                <div className="cart-item-price">$20.00</div>
            </div>
        </div>
    );
}