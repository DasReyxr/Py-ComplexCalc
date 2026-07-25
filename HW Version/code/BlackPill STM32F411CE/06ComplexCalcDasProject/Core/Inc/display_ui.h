#ifndef DISPLAY_UI_H
#define DISPLAY_UI_H
#include <stdint.h>
#include "TFT_Screen.h"

#ifdef ILI9341
#define FONT Font_11x18 
#define FONT_Height 18
#define FONT_Width 11
#elif ST7735
#define FONT Font_7x10
#define FONT_Height 10
#define FONT_Width 7

#endif

void toggleTheme(void);
void initTheme(void);
// Funciones de dibujado para cada nivel
void toggleTheme(void);
void drawLevel0(void);
void drawLevel1(uint8_t colMat, uint8_t rowMat);
void drawLevel2(uint8_t success);

// Función auxiliar para actualización parcial
void updateBufferDisplay(const char* buffer);

#endif // DISPLAY_UI_H