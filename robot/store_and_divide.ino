/*
This piece of code allows one to store a sector in an array of bytes (in this case, sector 1) 
and then prints out the values of the array but divided by two. 

This is a mere experiment on memory and operation on the elements.
*/

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN D8      // SDA/SS Pin
#define RST_PIN D3     // RST Pin

MFRC522 mfrc522(SS_PIN, RST_PIN);
byte sector1_data[64];  // Store Sector 1 data (4 blocks * 16 bytes each)

void setup() {
    Serial.begin(115200);
    SPI.begin();
    mfrc522.PCD_Init();
    delay(4);
    mfrc522.PCD_DumpVersionToSerial();  // Dump the MFRC522 version to serial for debugging
    Serial.println("Scan an RFID card...");
}

void loop() {
    if (!mfrc522.PICC_IsNewCardPresent()) return; // Wait for a card
    if (!mfrc522.PICC_ReadCardSerial()) return;   // Read the card

    Serial.println("Card detected! Reading Sector 1...");

    // Authenticate Sector 1 (Blocks 4-7)
    MFRC522::MIFARE_Key key;
    for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;  // Default key (FFFFFFFFFFFF)

    byte bufferLen = 18;
    for (byte block = 4; block <= 7; block++) {
        if (mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid)) != MFRC522::STATUS_OK) {
            Serial.print("Authentication failed for block "); Serial.println(block);
            return;
        }

        if (mfrc522.MIFARE_Read(block, &sector1_data[(block - 4) * 16], &bufferLen) != MFRC522::STATUS_OK) {
            Serial.print("Read failed for block "); Serial.println(block);
            return;
        }
    }

    Serial.println("Sector 1 data saved! Displaying the halves in 5 seconds...");
    
    mfrc522.PICC_HaltA();  // Halt card
    mfrc522.PCD_StopCrypto1(); // Stop encryption
    
    delay(5000); // Wait 5 seconds

    // Display saved Sector 1 data
    Serial.println("Sector 1 Data:");
    for (byte i = 0; i < 64; i++) {
        Serial.printf("%02X ", sector1_data[i]/2); 
        if ((i + 1) % 16 == 0) Serial.println();  // New line every 16 bytes
    }
}
