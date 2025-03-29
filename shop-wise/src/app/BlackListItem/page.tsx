import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
interface BlackListItemProps {
    currentItem: string;
}

export default function BlackListItem({ currentItem }: BlackListItemProps) {
    return (
        <div className="black-list-item">
            <div style={{flex:"1"}}>{currentItem}</div>
            <DeleteOutlineIcon
                fontSize="medium"
                style={{
                    color: "black",
                    padding: "10px",
                    cursor: "pointer",
                    alignSelf:"end",
                }}  
                />
        </div>
    );
}