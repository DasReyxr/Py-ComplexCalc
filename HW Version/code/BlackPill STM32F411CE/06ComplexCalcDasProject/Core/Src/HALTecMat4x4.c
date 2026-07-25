#include "HALTecMat4x4.h"

/*----------- Private Functions -----------*/
static inline void gpioWrite(const GpioPin *gpio, uint8_t state);
static inline uint8_t gpioRead(const GpioPin *gpio);

#define ROWS 4
#define COLS 4
#define ROW_INIT 6
#define COL_END 8
uint8_t toggle_Altern = 0;

// Array of row pins for easier iteration
static const GpioPin* rowPins[ROWS] = {
    &KeypadRow0, &KeypadRow1, &KeypadRow2, &KeypadRow3
};

// Array of column pins for easier iteration
static const GpioPin* colPins[COLS] = {
    &KeypadCol0, &KeypadCol1, &KeypadCol2, &KeypadCol3
};

char *keyHexa[ROWS][COLS]={
{"7","8","9","D"},
{"4","5","6","-"},
{"1","2","3","T"},
{"F","0",".","="},
};
char *keyHexaAltern[ROWS][COLS]={
{" ","W"," ","I"},
{"L"," ","R","P"},
{" ","B"," "," "},
{" "," "," ","S"},
};

uint8_t keyPolling_Trasposed[ROWS][COLS]={
// 1110 X | 1100 X| 1010 X | 0110 X
	{0XEE,0XDE,0XBE,0X7E}, // X 1110 
	{0XED,0XDD,0XBD,0X7D}, // X 1100
	{0XEB,0XDB,0XBB,0X7B}, // X 1010
	{0XE7,0XD7,0XB7,0X77}, // X 0110
};

uint8_t keyPolling[COLS][ROWS] = {
    {0xEE, 0xED, 0xEB, 0xE7},
    {0xDE, 0xDD, 0xDB, 0xD7},
    {0xBE, 0xBD, 0xBB, 0xB7},
    {0x7E, 0x7D, 0x7B, 0x77},
};


uint8_t rowPinsHEX[ROWS] = {0XE,0XD,0XB,0X7};

/*----------- Private Functions -----------*/
static inline void gpioWrite(const GpioPin *gpio, uint8_t state)
{
    if(state)
        gpio->port->BSRR = gpio->pin;
    else
        gpio->port->BSRR = (uint32_t)gpio->pin << 16;
}

static inline uint8_t gpioRead(const GpioPin *gpio)
{
    return (gpio->port->IDR & gpio->pin) ? 1 : 0;
}

// Set all row pins to a specific pattern (using bitmask)
static void setRowPattern(uint8_t pattern)
{
    // Pattern bits: bit 3 = row3, bit 2 = row2, bit 1 = row1, bit 0 = row0
    gpioWrite(rowPins[0], pattern & 0x01);
    gpioWrite(rowPins[1], pattern & 0x02);
    gpioWrite(rowPins[2], pattern & 0x04);
    gpioWrite(rowPins[3], pattern & 0x08);
}

// Read all column pins and return as a bitmask
static uint8_t readColPattern(void)
{
    uint8_t pattern = 0;
    pattern |= (gpioRead(colPins[0]) ? 0x01 : 0);
    pattern |= (gpioRead(colPins[1]) ? 0x02 : 0);
    pattern |= (gpioRead(colPins[2]) ? 0x04 : 0);
    pattern |= (gpioRead(colPins[3]) ? 0x08 : 0);
    return pattern;
}

/*----------- Public Functions -----------*/

char* gotKey(void){
	// Start with all rows high so the scan is stable and no accidental press is seen.
	setRowPattern(0x0F);
	for(uint8_t i = 0; i<ROWS; i++){
		// Set the row pattern (activate one row at a time)
		// rowPinsHEX[i] contains the bit pattern for each row (0xE, 0xD, 0xB, 0x7)
		setRowPattern(rowPinsHEX[i]);
		
		// Small delay for signal stabilization (debounce)
		for(volatile uint32_t dly = 0; dly < 100; dly++);
		
		// Read the column pattern
		uint8_t colPattern = readColPattern();
		
		// Check if any column is pressed (not all high)
		if(colPattern != 0x0F){
			// Reconstruct the key code from row and column patterns
			// Shift row pattern left by 4 bits and OR with column pattern
			uint8_t key = (rowPinsHEX[i] << 4) | colPattern;
			
			// Check if function key (alternate mode toggle) was pressed
			if(key == 0x7E){
				toggle_Altern ^= 1;
				// Wait for key release
				while(readColPattern() != 0x0F);
				return "F";
			}
			
			// Search for the key in the polling matrix
			for(uint8_t j = 0; j<COLS; j++){
				if(key == keyPolling[i][j])	{
					// Wait for key release
					while(readColPattern() != 0x0F);
					
					if(toggle_Altern == 0){
						return keyHexa[i][j];
					}
					if(toggle_Altern == 1){
						return keyHexaAltern[i][j];
					}
				}
			}
		}
	}
	return NULL; // No key pressed
}



