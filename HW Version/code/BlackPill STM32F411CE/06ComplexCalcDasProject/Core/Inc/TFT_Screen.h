/*
 * TFTST7735.h
 *
 *  Created on: Nov 2, 2025
 *      Author: dasre
 */
 
#ifndef TFT_SCREEN_H
#define TFT_SCREEN_H
#include "stm32f4xx.h"
#include "main.h"      
#include <stdint.h>
#include "fonts.h"  // Assuming FontDef lives here


#define SCREEN_SPI_PORT hspi1
extern SPI_HandleTypeDef SCREEN_SPI_PORT;

// GpioPin typedef - shared across multiple modules
#ifndef GPIOPIN_TYPEDEF
#define GPIOPIN_TYPEDEF
typedef struct{
    GPIO_TypeDef *port;
    uint16_t pin;
} GpioPin;
#endif

static const GpioPin ScreenCS = {
    .port = SCREEN_CS_GPIO_Port, .pin  = SCREEN_CS_Pin
};

static const GpioPin ScreenDC = {
    .port = SCREEN_D_C_GPIO_Port, .pin  = SCREEN_D_C_Pin
};

static const GpioPin ScreenRST = {
    .port = SCREEN_RST_GPIO_Port, .pin  = SCREEN_RST_Pin
};


// --- Commands ---
#define SCREEN_CASET   0x002A
#define SCREEN_RASET   0x002B
#define SCREEN_RAMWR   0x002C
#define ILI9341


#ifdef ILI9341
  
// default orientation
/*
#define SCREEN_WIDTH  240
#define SCREEN_HEIGHT 320
#define ILI9341_ROTATION (ILI9341_MADCTL_MX | ILI9341_MADCTL_BGR)
*/
// 90
/*
#define SCREEN_WIDTH  320
#define SCREEN_HEIGHT 240
#define ILI9341_ROTATION (ILI9341_MADCTL_MX | ILI9341_MADCTL_MY | ILI9341_MADCTL_MV | ILI9341_MADCTL_BGR)
*/
// 180

#define SCREEN_WIDTH  320
#define SCREEN_HEIGHT 240
#define ILI9341_ROTATION (ILI9341_MADCTL_MV | ILI9341_MADCTL_BGR)
// upside down
/*
#define SCREEN_WIDTH  240
#define SCREEN_HEIGHT 320
#define ILI9341_ROTATION (ILI9341_MADCTL_MY | ILI9341_MADCTL_BGR)
*/

    #define ILI9341_NOP         0x00
    #define ILI9341_SWRESET     0x01

    #define ILI9341_SLPOUT      0x11

    #define ILI9341_INVOFF      0x20
    #define ILI9341_INVON       0x21
    #define ILI9341_GAMSET      0x26
    #define ILI9341_DISPOFF     0x28
    #define ILI9341_DISPON      0x29
    #define ILI9341_CASET       0x2A
    #define ILI9341_RASET       0x2B
    #define ILI9341_RAMWR       0x2C
    #define ILI9341_RAMRD       0x2E

    #define ILI9341_COLMOD      0x3A
    #define ILI9341_MADCTL      0x36
    #define ILI9341_PTLAR       0x30

    #define ILI9341_FRMCTR1     0xB1
    #define ILI9341_DISSET5     0xB6

    #define ILI9341_PWCTR1      0xC0
    #define ILI9341_PWCTR2      0xC1

    #define ILI9341_VMCTR1      0xC5
    #define ILI9341_VMCTR2      0xC7
    #define ILI9341_PWCTRA      0xCB
    #define ILI9341_PWCTRB      0xCF

    #define ILI9341_GMCTRP1     0xE0
    #define ILI9341_GMCTRN1     0xE1
    #define ILI9341_TIMCTRA     0xE8
    #define ILI9341_TIMCTRB     0xEA
    #define ILI9341_PWRSEQ      0xED

    #define ILI9341_GAMDIS      0xF2
    #define ILI9341_PUMPRATIO   0xF7

    #define ILI9341_MADCTL_MY  0x80
    #define ILI9341_MADCTL_MX  0x40
    #define ILI9341_MADCTL_MV  0x20
    #define ILI9341_MADCTL_ML  0x10
    #define ILI9341_MADCTL_RGB 0x00
    #define ILI9341_MADCTL_BGR 0x08
    #define ILI9341_MADCTL_MH  0x04

#endif
#ifdef ST7735
    // --- Screen ----
    #define SCREEN_WIDTH  128
    #define SCREEN_HEIGHT 160
    // --- Commands ---

    #define SCREEN_WIDTH  128
    #define SCREEN_HEIGHT 160
    #define ST7735_NOP     0x0000
    #define ST7735_SWRESET 0x0001
    #define ST7735_RDDID   0x0004
    #define ST7735_RDDST   0x0009

    #define ST7735_SLPIN   0x0010
    #define ST7735_SLPOUT  0x0011
    #define ST7735_PTLON   0x0012
    #define ST7735_NORON   0x0013

    #define ST7735_INVOFF  0x0020
    #define ST7735_INVON   0x0021
    #define ST7735_GAMSET  0x0026
    #define ST7735_DISPOFF 0x0028
    #define ST7735_DISPON  0x0029
    #define ST7735_CASET   0x002A
    #define ST7735_RASET   0x002B
    #define ST7735_RAMWR   0x002C
    #define ST7735_RAMRD   0x002E

    #define ST7735_PTLAR   0x0030
    #define ST7735_COLMOD  0x003A
    #define ST7735_MADCTL  0x0036

    #define ST7735_FRMCTR1 0x00B1
    #define ST7735_FRMCTR2 0x00B2
    #define ST7735_FRMCTR3 0x00B3
    #define ST7735_INVCTR  0x00B4
    #define ST7735_DISSET5 0x00B6

    #define ST7735_PWCTR1  0x00C0
    #define ST7735_PWCTR2  0x00C1
    #define ST7735_PWCTR3  0x00C2
    #define ST7735_PWCTR4  0x00C3
    #define ST7735_PWCTR5  0x00C4
    #define ST7735_VMCTR1  0x00C5

    #define ST7735_RDID1   0x00DA
    #define ST7735_RDID2   0x00DB
    #define ST7735_RDID3   0x00DC
    #define ST7735_RDID4   0x00DD

    #define ST7735_PWCTR6  0x00FC

    #define ST7735_GMCTRP1 0x00E0
    #define ST7735_GMCTRN1 0x00E1

    #define ST7735_MADCTL_MY  0x0080
    #define ST7735_MADCTL_MX  0x0040
    #define ST7735_MADCTL_MV  0x0020
    #define ST7735_MADCTL_ML  0x0010
    #define ST7735_MADCTL_RGB 0x0000
    #define ST7735_MADCTL_BGR 0x0008
    #define ST7735_MADCTL_MH  0x0004

    #define ST7735_NORMAL (ST7735_MADCTL_MX | ST7735_MADCTL_MY | ST7735_MADCTL_RGB)
    #define ST7735_ROTATE_90 (ST7735_MADCTL_MY | ST7735_MADCTL_MV | ST7735_MADCTL_RGB)
    #define ST7735_ROTATE_180 (ST7735_MADCTL_RGB)
    #define ST7735_ROTATE_270 (ST7735_MADCTL_MX | ST7735_MADCTL_MV | ST7735_MADCTL_RGB)
    #define ST7735_ROTATION ST7735_ROTATE_90

    #endif

extern void config(void);
extern void confRCC(void);
extern void confGPIO(void);
extern void confSPI(void);
// ------- INITIALIZATION -----------
/* D/CX = 0 => Command
    D/CX = 1 => Data*/
#define DCX_CMD  0
#define DCX_DATA 1
// ---- COLORS ----
#define COLOR_BLACK   0x0000
#define COLOR_WHITE   0xFFFF
#define COLOR_RED     0xF800
#define COLOR_CYAN    0x07ff
#define COLOR_MAGENTA 0xF81F
#define COLOR_GREEN   0x07E0
#define COLOR_BLUE    0x001F
#define COLOR_YELLOW  0xFFE0
#define COLOR_PINK    0xFC18
#define COLOR_PURPLE  0x8010
#define COLOR_ORANGE  0xFD20



void Screen_Init(void);
void Screen_DrawPixel(uint16_t, uint16_t, uint16_t);

void Screen_WriteChar(uint16_t, uint16_t, char, FontDef,
                uint16_t, uint16_t);

void Screen_WriteString(uint16_t, uint16_t, const char*, FontDef,
                    uint16_t, uint16_t);

void Screen_WriteData(uint8_t* data, uint16_t size);

void Screen_FillRectangle(uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint16_t color);

void Screen_FillScreen(uint16_t color);


void Screen_FillCircle(uint16_t x0, uint16_t y0, uint16_t r, uint16_t color);
void Screen_DrawCircle(uint16_t x0, uint16_t y0, uint16_t r, uint16_t color);


// ----- Hardware Functions -----
void delay_ms(volatile uint32_t);   
// ----- Communication Functions -----
// ----- Overloaded Functions -----
void spiWrite_8b_Vector(uint8_t*, uint16_t);
void spiWrite_8b(uint8_t);
void WriteCommand_8b(uint8_t);

void SetAddressWindow(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1);




#endif
