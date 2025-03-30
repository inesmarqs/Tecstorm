"use client";

export default function InvalidItemPopUp({ itemName, onClose,onAlternative }: 
    { itemName: string; onClose: () => void; onAlternative: () => void; }) {

  return (
    <div className="popup-overlay">
      <div className="popup">
        <h2>Warning!</h2>
        <p>The last added item (<strong>{itemName}</strong>) has been flagged!</p>
        <div style={{ display: "flex" ,gap:"3rem",justifyContent:"center"}}>

            <button onClick={onAlternative}>Ask for alternative</button>
            <button onClick={onClose}>Keep it anyway</button>
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
