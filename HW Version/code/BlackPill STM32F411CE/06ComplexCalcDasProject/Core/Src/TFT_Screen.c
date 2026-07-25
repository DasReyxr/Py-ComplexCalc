#include "TFT_Screen.h"

/*

 A3 CS OUT
 A4 DC OUT
 A5 SCK AFR
 A6 RES OUT
 A7 MOSI AFR
 
*/

/*----------- Static Functions -----------*/
static inline void gpioWrite(const GpioPin *gpio, uint8_t state);
static inline void modeSel(uint8_t data);
static inline void csSet(uint8_t high);
static inline void rstSet(uint8_t high);

/*----------- Public Functions -----------*/


void Screen_Init(void) {
    // HW reset
    rstSet(0);
    delay_ms(5);
    rstSet(1);
    delay_ms(50);

    csSet(0);

    #ifdef ILI9341
    WriteCommand_8b(ILI9341_SWRESET);
    delay_ms(1000);

    // POWER CONTROL A
    WriteCommand_8b(ILI9341_PWCTRA);
    {
        uint8_t data[] = { 0x39, 0x2C, 0x00, 0x34, 0x02 };
        Screen_WriteData(data, sizeof(data));
    }

    // POWER CONTROL B
    WriteCommand_8b(ILI9341_PWCTRB);
    {
        uint8_t data[] = { 0x00, 0xC1, 0x30 };
        Screen_WriteData(data, sizeof(data));
    }

    // DRIVER TIMING CONTROL A
    WriteCommand_8b(ILI9341_TIMCTRA);
    {
        uint8_t data[] = { 0x85, 0x00, 0x78 };
        Screen_WriteData(data, sizeof(data));
    }

    // DRIVER TIMING CONTROL B
    WriteCommand_8b(ILI9341_TIMCTRB);
    {
        uint8_t data[] = { 0x00, 0x00 };
        Screen_WriteData(data, sizeof(data));
    }

    // POWER ON SEQUENCE CONTROL
    WriteCommand_8b(ILI9341_PWRSEQ);
    {
        uint8_t data[] = { 0x64, 0x03, 0x12, 0x81 };
        Screen_WriteData(data, sizeof(data));
    }

    // PUMP RATIO CONTROL
    WriteCommand_8b(ILI9341_PUMPRATIO);
    {
        uint8_t data[] = { 0x20 };
        Screen_WriteData(data, sizeof(data));
    }

    // POWER CONTROL,VRH[5:0]
    WriteCommand_8b(ILI9341_PWCTR1);
    {
        uint8_t data[] = { 0x23 };
        Screen_WriteData(data, sizeof(data));
    }

    // POWER CONTROL,SAP[2:0];BT[3:0]
    WriteCommand_8b(ILI9341_PWCTR2);
    {
        uint8_t data[] = { 0x10 };
        Screen_WriteData(data, sizeof(data));
    }

    // VCM CONTROL
    WriteCommand_8b(ILI9341_VMCTR1);
    {
        uint8_t data[] = { 0x3E, 0x28 };
        Screen_WriteData(data, sizeof(data));
    }

    // VCM CONTROL 2
    WriteCommand_8b(ILI9341_VMCTR2);
    {
        uint8_t data[] = { 0x86 };
        Screen_WriteData(data, sizeof(data));
    }

    // MEMORY ACCESS CONTROL
    WriteCommand_8b(ILI9341_MADCTL);
    {
        uint8_t data[] = { 0x48 };
        Screen_WriteData(data, sizeof(data));
    }

    // PIXEL FORMAT
    WriteCommand_8b(ILI9341_COLMOD);
    {
        uint8_t data[] = { 0x55 };
        Screen_WriteData(data, sizeof(data));
    }

    // FRAME RATIO CONTROL, STANDARD RGB COLOR
    WriteCommand_8b(ILI9341_FRMCTR1);
    {
        uint8_t data[] = { 0x00, 0x18 };
        Screen_WriteData(data, sizeof(data));
    }

    // DISPLAY FUNCTION CONTROL
    WriteCommand_8b(ILI9341_DISSET5);
    {
        uint8_t data[] = { 0x08, 0x82, 0x27 };
        Screen_WriteData(data, sizeof(data));
    }

    // 3GAMMA FUNCTION DISABLE
    WriteCommand_8b(ILI9341_GAMDIS);
    {
        uint8_t data[] = { 0x00 };
        Screen_WriteData(data, sizeof(data));
    }

    // GAMMA CURVE SELECTED
    WriteCommand_8b(ILI9341_GAMSET);
    {
        uint8_t data[] = { 0x01 };
        Screen_WriteData(data, sizeof(data));
    }

    // POSITIVE GAMMA CORRECTION
    WriteCommand_8b(ILI9341_GMCTRP1);
    {
        uint8_t data[] = { 0x0F, 0x31, 0x2B, 0x0C, 0x0E, 0x08, 0x4E, 0xF1,
                           0x37, 0x07, 0x10, 0x03, 0x0E, 0x09, 0x00 };
        Screen_WriteData(data, sizeof(data));
    }

    // NEGATIVE GAMMA CORRECTION
    WriteCommand_8b(ILI9341_GMCTRN1);
    {
        uint8_t data[] = { 0x00, 0x0E, 0x14, 0x03, 0x11, 0x07, 0x31, 0xC1,
                           0x48, 0x08, 0x0F, 0x0C, 0x31, 0x36, 0x0F };
        Screen_WriteData(data, sizeof(data));
    }

    // EXIT SLEEP
    WriteCommand_8b(ILI9341_SLPOUT);
    HAL_Delay(120);

    // TURN ON DISPLAY
    WriteCommand_8b(ILI9341_DISPON);

    // MADCTL
    WriteCommand_8b(ILI9341_MADCTL);
    {
        uint8_t data[] = { ILI9341_ROTATION };
        Screen_WriteData(data, sizeof(data));
    }
    #endif

    #ifdef ST7735
        WriteCommand_8b(ST7735_SWRESET);
        delay_ms(150);

        WriteCommand_8b(ST7735_SLPOUT);
        delay_ms(500);

        WriteCommand_8b(ST7735_FRMCTR1); // Frame rate ctrl - normal mode
        Screen_WriteData((uint8_t[]){0x01, 0x2C, 0x2D}, 3);

        WriteCommand_8b(ST7735_FRMCTR2); // Frame rate ctrl - idle mode
        Screen_WriteData((uint8_t[]){0x01, 0x2C, 0x2D}, 3);

        WriteCommand_8b(ST7735_FRMCTR3); // Frame rate ctrl - partial mode
        Screen_WriteData((uint8_t[]){0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D}, 6);

        WriteCommand_8b(ST7735_INVCTR); // Display inversion ctrl
        Screen_WriteData((uint8_t[]){0x07}, 1); // No inversion

        WriteCommand_8b(ST7735_PWCTR1); // Power control
        Screen_WriteData((uint8_t[]){0xA2, 0x02, 0x84}, 3); // -4.6V, AUTO mode

        WriteCommand_8b(ST7735_PWCTR2); // Power control
        Screen_WriteData((uint8_t[]){0xC5}, 1); // VGH25=2.4C VGSEL=-10 VGH=3*AVDD

        WriteCommand_8b(ST7735_PWCTR3); // Power control
        Screen_WriteData((uint8_t[]){0x0A, 0x00}, 2); // Opamp current small, boost freq

        WriteCommand_8b(ST7735_PWCTR4); // Power control
        Screen_WriteData((uint8_t[]){0x8A, 0x2A}, 2); // BCLK/2, Opamp current small & medium low

        WriteCommand_8b(ST7735_PWCTR5); // Power control
        Screen_WriteData((uint8_t[]){0x8A, 0xEE}, 2);

        WriteCommand_8b(ST7735_VMCTR1); // Power control
        Screen_WriteData((uint8_t[]){0x0E}, 1);

        WriteCommand_8b(ST7735_INVOFF); // Don't invert display

        WriteCommand_8b(ST7735_MADCTL); // Memory access control
        Screen_WriteData((uint8_t[]){ST7735_ROTATION}, 1);

        WriteCommand_8b(ST7735_COLMOD); // Color mode
        Screen_WriteData((uint8_t[]){0x05}, 1); // 16-bit color

        WriteCommand_8b(ST7735_CASET); // Column addr set
        Screen_WriteData((uint8_t[]){0x00, 0x00, 0x00, 0x7F}, 4); // XSTART=0, XEND=127

        WriteCommand_8b(ST7735_RASET); // Row addr set
        Screen_WriteData((uint8_t[]){0x00, 0x00, 0x00, 0x9F}, 4); // YSTART=0, YEND=159

        WriteCommand_8b(ST7735_GMCTRP1); // Gamma Adjustments (pos. polarity)
        Screen_WriteData((uint8_t[]){
            0x02, 0x1c, 0x07, 0x12,
            0x37, 0x32, 0x29, 0x2d,
            0x29, 0x25, 0x2B, 0x39,
            0x00, 0x01, 0x03, 0x10
        }, 16);

        WriteCommand_8b(ST7735_GMCTRN1); // Gamma Adjustments (neg. polarity)
        Screen_WriteData((uint8_t[]){
            0x03, 0x1d, 0x07, 0x06,
            0x2E, 0x2C, 0x29, 0x2D,
            0x2E, 0x2E, 0x37, 0x3F,
            0x00, 0x00, 0x02, 0x10
        }, 16);

        WriteCommand_8b(ST7735_NORON); // Normal display on
        delay_ms(10);

        WriteCommand_8b(ST7735_DISPON); // Main screen turn on
        delay_ms(100);

        Screen_FillScreen(COLOR_BLACK);
    #endif
    csSet(1);
}


void Screen_WriteData(uint8_t* data, uint16_t size) {
    // Leave CS control to the caller. Set DC for data then write buffer.
    modeSel(DCX_DATA);
    spiWrite_8b_Vector(data, size);
}


void SetAddressWindow(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1) {



    WriteCommand_8b(SCREEN_CASET); // CASET (Column Address Set)
    uint8_t data[] = { (x0 >> 8) & 0xFF, x0 & 0xFF, (x1 >> 8) & 0xFF, x1 & 0xFF };
    Screen_WriteData(data, sizeof(data));

    WriteCommand_8b(SCREEN_RASET); // RASET (Row Address Set)
    data[0] = (y0 >> 8) & 0xFF; data[1] = y0 & 0xFF;
    data[2] = (y1 >> 8) & 0xFF; data[3] = y1 & 0xFF;
    Screen_WriteData(data, sizeof(data));

    WriteCommand_8b(SCREEN_RAMWR); // RAMWR (start writing pixels)
}


void Screen_FillRectangle(uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint16_t color) {
    // clipping
    if((x >= SCREEN_WIDTH) || (y >= SCREEN_HEIGHT)) return;
    if((x + w - 1) >= SCREEN_WIDTH ) w = SCREEN_WIDTH  - x;
    if((y + h - 1) >= SCREEN_HEIGHT) h = SCREEN_HEIGHT - y;

    csSet(0);
    SetAddressWindow(x, y, x+w-1, y+h-1);
    
    uint8_t data[] = { color >> 8, color & 0xFF };

    modeSel(DCX_DATA);
    
    uint32_t totalPixels = (uint32_t)w * (uint32_t)h;
    for(uint32_t i = 0; i < totalPixels; i++) {
        while(!(SPI1->SR & SPI_SR_TXE));
        spiWrite_8b_Vector(data, 2);
    }
    
    while(SPI1->SR & SPI_SR_BSY);  // Wait for last transmission to complete
    csSet(1);
}

void Screen_FillScreen(uint16_t color) {
    Screen_FillRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, color);
}

void Screen_DrawPixel(uint16_t x, uint16_t y, uint16_t color) {
    // Ensure CS is held low while setting window and writing pixel data
    if((x >= SCREEN_WIDTH) || (y >= SCREEN_HEIGHT)) return;

    csSet(0);
    SetAddressWindow(x, y, x+1, y+1);
    uint8_t data[] = { color >> 8, color & 0xFF };
    Screen_WriteData(data, sizeof(data));
    csSet(1);
}

void Screen_WriteChar(uint16_t x, uint16_t y, char ch, FontDef font,
                           uint16_t color, uint16_t bgcolor)
{
    uint32_t i, b, j;

    SetAddressWindow(x, y, x+font.width-1, y+font.height-1);

    for(i = 0; i < font.height; i++) {
        b = font.data[(ch - 32) * font.height + i];
        for(j = 0; j < font.width; j++) {
            if((b << j) & 0x8000)  {
                uint8_t data[] = { color >> 8, color & 0xFF };
                Screen_WriteData(data, sizeof(data));
            } else {
                uint8_t data[] = { bgcolor >> 8, bgcolor & 0xFF };
                Screen_WriteData(data, sizeof(data));
            }
        }
    }
}

void Screen_WriteString(uint16_t x, uint16_t y, const char* str, FontDef font,
                             uint16_t color, uint16_t bgcolor)
{
    csSet(0);
    while(*str) {
        if((x >= SCREEN_WIDTH) || (y >= SCREEN_HEIGHT) || (x + font.width > SCREEN_WIDTH) || (y + font.height > SCREEN_HEIGHT)) {
            break;
        }

        Screen_WriteChar(x, y, *str, font, color, bgcolor);
        x += font.width;
        str++;
    }

    csSet(1);
}


void Screen_FillCircle(uint16_t x0, uint16_t y0, uint16_t r, uint16_t color)
{
    for(int16_t y = -r; y <= r; y++)
    {
        for(int16_t x = -r; x <= r; x++)
        {
            if((x * x + y * y) <= (r * r))
            {
                Screen_DrawPixel(x0 + x, y0 + y, color);
            }
        }
    }
}

void Screen_DrawCircle(uint16_t x0, uint16_t y0, uint16_t r, uint16_t color){
    int16_t x = r;
    int16_t y = 0;
    int16_t err = 0;

    while (x >= y)
    {
        Screen_DrawPixel(x0 + x, y0 + y, color); Screen_DrawPixel(x0 + y, y0 + x, color);
        Screen_DrawPixel(x0 - y, y0 + x, color); Screen_DrawPixel(x0 - x, y0 + y, color);
        Screen_DrawPixel(x0 - x, y0 - y, color); Screen_DrawPixel(x0 - y, y0 - x, color);
        Screen_DrawPixel(x0 + y, y0 - x, color); Screen_DrawPixel(x0 + x, y0 - y, color);
        y++;

        if (err <= 0)
        {
            err += 2 * y + 1;
        }

        if (err > 0)
        {
            x--;
            err -= 2 * x + 1;
        }
    }
}


/*----------- Private Functions -----------*/
static inline void gpioWrite(const GpioPin *gpio, uint8_t state)
{
    if(state)
        gpio->port->BSRR = gpio->pin;
    else
        gpio->port->BSRR = (uint32_t)gpio->pin << 16;
}

static inline void modeSel(uint8_t data)
{

    /* D/CX = 0 => Data (DC LOW)
       D/CX = 1 => Command (DC HIGH)*/

    gpioWrite(&ScreenDC, data);
}

static inline void csSet(uint8_t high)
{
    /* CS LOW to select, CS HIGH to deselect */
    gpioWrite(&ScreenCS, high);
}

static inline void rstSet(uint8_t high)
{
    // RST LOW to reset, RST HIGH for normal operation
    gpioWrite(&ScreenRST, high);
}


void delay_ms(volatile uint32_t ms){
	while(ms--){
		for(volatile uint32_t i =0; i<6000;i++){
		}}
}





void spiWrite_8b_Vector(uint8_t* DATA, uint16_t size){
    for(uint16_t i = 0; i < size; i++){
        while(!(SPI1->SR & SPI_SR_TXE));
        SPI1->DR = DATA[i];
    }
    while(SPI1->SR & SPI_SR_BSY);  // Wait for last byte to complete
}

void spiWrite_8b(uint8_t DATA){
    while(!(SPI1->SR & SPI_SR_TXE));
    SPI1->DR = DATA;
    while(SPI1->SR & SPI_SR_BSY);
}




void WriteCommand_8b(uint8_t cmd) {
    // Leave CS control to the caller. Set DC for command then write byte.
    modeSel(DCX_CMD);
    spiWrite_8b(cmd);
}


//----------- Configuration Functions -----------//
#ifdef BARE_METAL_CONFIG
void confRCC(void){
                 
    RCC->AHB1ENR |= (1<<0); // GPIOA SPI1
    RCC->APB2ENR |=(1<<12);//ENCENDEMOS SPI1
}
void confGPIO(void){
                /*    SCK    |     MOSI*/
	GPIOA->MODER |= (2<<(2*5)| 2<<(2*7)); 
	GPIOA->AFR[0]|= (5<<(4*5)| 5<<(4*7)); 
	
                  /*      CS    |     DC/X |    RESET */
    GPIOA->MODER |= (1<<(2*2))|(1<<(2*3))| (1<<(2*4));
    
    // Set initial states
    GPIOA->BSRR = (1 << (2));  // CS high (inactive)
    GPIOA->BSRR = (1 << (3));  // DC high (data mode)
    GPIOA->BSRR = (1 << (4));  // RST high (active)
}



void confSPI(void){
	// Baud rate: divide by 16 for 1MHz communication (16MHz / 16 = 1MHz)
	SPI1->CR1 |=(3<<3);//BR = 011 -> divide by 16
	
	// Master mode
	SPI1->CR1 |=(1<<2);//activamos modo maestro


    
	// Software NSS management
	SPI1->CR1 |=(1<<9);//ACTIVAMOS SS POR SOFTWARE SSM
	SPI1->CR1 |=(1<<8);//ACTIVAMOS EL SS INTERNO PARA FORZAR UNA HABILITACIÓN EN EL MAESTRO SSI
	// Data frame format: 8-bit (not 16-bit as commented)

    // Enable SPI
    SPI1->CR1 |= (1<<6); // PRENDEMOS EL SPI

}


void config(void){
    confRCC();
    confGPIO();
    confSPI();
}
#endif
