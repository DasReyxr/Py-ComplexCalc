// display_ui.c
#include "TFT_Screen.h"
#include "fonts.h"
#include "display_ui.h"
#include "testimg.h"                    
#include "ComplexGJ.h"
#include <string.h>
#include <stdio.h>
/*
* no se guarda la matriz cuando despues de la solucion ingresa el tamaño y vuelve a la pantalla de ingreso de coeficientes y selecciono del mismo tamaño, antes mostraba valores raros ahora directamente muestra ceros
* despues de ingresar por segunda vez una matriz el texto muestra caracteres extraños y muy abajo 
*/
// RGB888 to RGB565 conversion macro (display-specific format)
#define RGB565(r, g, b) (((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3))

// Hex color to RGB565 conversion macro  
#define HEX_TO_RGB565(hex) RGB565(((hex >> 16) & 0xFF), ((hex >> 8) & 0xFF), (hex & 0xFF))

// Color Theme Structure - Descriptive names based on usage
typedef struct {
    uint16_t bg;              // Background color
    uint16_t title;           // Title/header text
    uint16_t primary_text;    // Primary text color
    uint16_t secondary_text;  // Secondary/hint text
    uint16_t button;          // Button/action color
    uint16_t matrix_cell;     // Matrix cell values
    uint16_t matrix_selected; // Selected matrix cell
    uint16_t separator;       // Lines and separators
    uint16_t highlight;       // Navigation/editing mode highlight
    uint16_t input_bg;        // Input/selected background
} ColorTheme;

// Normal Theme - Dark mode
const ColorTheme THEME_NORMAL = {
    .bg =  HEX_TO_RGB565(0x272727), // #272727
    .title = COLOR_CYAN,
    .primary_text = COLOR_WHITE,
    .secondary_text = HEX_TO_RGB565(0x808080),
    .button = COLOR_GREEN,
    .matrix_cell = HEX_TO_RGB565(0x6496FF),
    .matrix_selected = COLOR_YELLOW,
    .separator = HEX_TO_RGB565(0x606060),
    .highlight = COLOR_MAGENTA,
    .input_bg = HEX_TO_RGB565(0x28283C)
};

// Pink Theme - Soft pink aesthetic based on Python UI
const ColorTheme THEME_PINK = {
    .bg = HEX_TO_RGB565(0xFFD4E8),        // #fd1380 - Light pink background
    .title = HEX_TO_RGB565(0xC71585),     // #C71585 - Deep pink for titles
    .primary_text = HEX_TO_RGB565(0x8B4789),  // #8B4789 - Purple text
    .secondary_text = HEX_TO_RGB565(0xD891C9), // #D891C9 - Light purple for hints
    .button = HEX_TO_RGB565(0xFF69B4),    // #FF69B4 - Hot pink for buttons
    .matrix_cell = HEX_TO_RGB565(0xFF69B4),   // #FF69B4 - Hot pink for matrix values
    .matrix_selected = HEX_TO_RGB565(0x8B008B), // #8B008B - Dark magenta for selected (high contrast)
    .separator = HEX_TO_RGB565(0xFFB6D9), // #FFB6D9 - Medium pink for lines
    .highlight = COLOR_MAGENTA, // #FF1493 - Deep pink for highlights
    .input_bg = HEX_TO_RGB565(0xFFF0F8)   // #FFF0F8 - Almost white for input bg
};

// Current theme pointer
ColorTheme currentTheme;        
uint8_t isPinkMode = 0;

// Function to switch theme
void toggleTheme(void) {
    isPinkMode = !isPinkMode;
    currentTheme = isPinkMode ? THEME_PINK: THEME_NORMAL;
}

// Initialize with normal theme
void initTheme(void) {
    currentTheme = //THEME_PINK;
    			   THEME_NORMAL;
    isPinkMode = //1;
    			 0;
}
// Variables externas
extern uint8_t matSize;
extern cplx A[N_MAX][N_MAX];
extern cplx b[N_MAX];
extern cplx x[N_MAX];
extern char buffer[16];
extern uint8_t index_Var;
extern uint8_t editingReal;
extern uint8_t navigating;
// ==================== LEVEL 0: Ingreso de tamaño ====================
void drawLevel0(void) {
    Screen_FillScreen(currentTheme.bg);
    
    // Título
    Screen_WriteString(SCREEN_WIDTH/5, FONT_Height, "INGRESE TAMANO", FONT, currentTheme.title, currentTheme.bg);
    
    // Mostrar buffer con cursor
    char displayStr[20];
    if(index_Var == 0) {
        sprintf(displayStr, "Sistema: _");
    } else {
        sprintf(displayStr, "Sistema: %s", buffer);
    }
    Screen_WriteString(SCREEN_WIDTH/3, 4*FONT_Height, displayStr, FONT, currentTheme.primary_text, currentTheme.bg);
    
    // Rango válido
    Screen_WriteString(SCREEN_WIDTH/3, 7*FONT_Height, "Rango: 2-4", FONT, currentTheme.secondary_text, currentTheme.bg);
    
    // Instrucciones
    Screen_WriteString(SCREEN_WIDTH/4, 9*FONT_Height,  "[S+P] C. Tema", FONT, currentTheme.secondary_text, currentTheme.bg);
    Screen_WriteString(SCREEN_WIDTH/4, 10*FONT_Height, "[0-9] Numero", FONT, currentTheme.secondary_text, currentTheme.bg);
    Screen_WriteString(SCREEN_WIDTH/4, 11*FONT_Height, "[ = ] Confirmar", FONT, currentTheme.button, currentTheme.bg);
    if (navigating) {
        Screen_FillRectangle(SCREEN_WIDTH-FONT_Width,SCREEN_HEIGHT-FONT_Height, FONT_Width,FONT_Height, currentTheme.input_bg);
        Screen_WriteString(SCREEN_WIDTH-FONT_Width, SCREEN_HEIGHT-FONT_Height, "S", FONT, currentTheme.highlight, currentTheme.input_bg);
    }
}

// ==================== LEVEL 1: Ingreso de coeficientes ====================
void drawLevel1(uint8_t colMat, uint8_t rowMat) {
    Screen_FillScreen(currentTheme.bg);
    
    // Título
    char title[24];
    sprintf(title, "DATOS %dx%d", matSize, matSize);
    Screen_WriteString(SCREEN_WIDTH/16, 2, title, FONT, currentTheme.title, currentTheme.bg);
    
    // Calcular espaciado
    int cellWidth = FONT_Width * 4 + 4; 
    int startX = 8;
    int startY = FONT_Height + 6;
    int rowHeight = FONT_Height + 2;
    
    // Dibujar matriz aumentada [A|b]
    for(uint8_t i = 0; i < matSize; i++) {
        int y = startY + i * rowHeight;
        
        // Coeficientes de A
        for(uint8_t j = 0; j < matSize; j++) {
            int x = startX + j * cellWidth;
            
            // Determinar si esta celda está seleccionada
            uint8_t isSelected = (i == colMat && j == rowMat);
            uint16_t color = isSelected ? currentTheme.matrix_selected : currentTheme.matrix_cell;
            uint16_t bgColor = isSelected ? currentTheme.input_bg : currentTheme.bg;
            
            // Convertir número a string (solo parte real para matriz compacta)
            char numStr[8];
            int idx = 0;
            ftoa_simple(A[i][j].r, numStr, &idx, 1);
            numStr[idx] = '\0';
            
            // Dibujar rectángulo de selección
            if(isSelected) {
                Screen_FillRectangle(x-1, y-1, cellWidth-2, 11, bgColor);
            }
            
            Screen_WriteString(x, y, numStr, FONT, color, bgColor);
        }
        
        // Separador |
        int sepX = startX + matSize * cellWidth;
        Screen_WriteString(sepX, y, "|", FONT, currentTheme.separator, currentTheme.bg);
        
        // Vector b (constantes)
        int bX = sepX + 10;
        uint8_t isConstSelected = (i == colMat && rowMat == matSize);
        uint16_t bColor = isConstSelected ? currentTheme.matrix_selected : currentTheme.button;
        uint16_t bBgColor = isConstSelected ? currentTheme.input_bg : currentTheme.bg;
        
        char bStr[8];
        int idx = 0;
        ftoa_simple(b[i].r, bStr, &idx, 1);
        bStr[idx] = '\0';
        
        if(isConstSelected) {
            Screen_FillRectangle(bX-1, y-1, cellWidth-2, 11, bBgColor);
        }
        
        Screen_WriteString(bX, y, bStr, FONT, bColor, bBgColor);
    }
    
    // Panel de edición en la parte inferior
    int panelY = startY + matSize * rowHeight + 8;
    
    // Línea separadora
    Screen_FillRectangle(0, panelY - 2, 128, 1, currentTheme.separator);
    
    // Mostrar posición actual
    char posStr[24];

    if(rowMat < matSize) {
        sprintf(posStr, "A[%d][%d]", colMat + 1, rowMat + 1);
    } else {
        sprintf(posStr, "b[%d]", colMat + 1);
    }
    Screen_WriteString(0, panelY, posStr, FONT, currentTheme.title, currentTheme.bg);
    
    // Mostrar qué parte se está editando
    
    panelY += rowHeight;
    char realStr[16];
    char imagStr[16];
    
    if(navigating){
    	if(rowMat < matSize){
		sprintf(realStr, "Real %.4f", A[colMat][rowMat].r);
		sprintf(imagStr, "Imag j%.4f", A[colMat][rowMat].i);
		}
    	else{
    		sprintf(realStr, "Real %.4f", b[colMat].r);
			sprintf(imagStr, "Imag j%.4f", b[colMat].i);
    	}
    	Screen_WriteString(FONT_Width*7, panelY-rowHeight, "READ", FONT, currentTheme.highlight, currentTheme.bg);
        Screen_WriteString(0, panelY, realStr, FONT, currentTheme.primary_text, currentTheme.bg);
        Screen_WriteString(0, panelY+rowHeight, imagStr, FONT, currentTheme.primary_text, currentTheme.bg);
        Screen_WriteString(FONT_Width*5, panelY+(rowHeight)*2, "[WASD] Mov", FONT, currentTheme.highlight, currentTheme.bg);
    }
    else {
        if (editingReal) {
            // Editing real part: show buffer as real, imag as last entered
            if (index_Var == 0) {
                sprintf(realStr, "Real %.4f", (rowMat < matSize) ? A[colMat][rowMat].r : b[colMat].r);
            } else {
                sprintf(realStr, "Real %s", buffer);
            }
            Screen_WriteString(FONT_Width*12, panelY, "<<", FONT, currentTheme.button, currentTheme.bg);
            sprintf(imagStr, "Imag j%.4f", (rowMat < matSize) ? A[colMat][rowMat].i : b[colMat].i);

        } else {
            // Editing imaginary part
            sprintf(realStr, "Real %.4f", (rowMat < matSize) ? A[colMat][rowMat].r : b[colMat].r);
            
            if (index_Var == 0) {
                sprintf(imagStr, "Imag j%.4f", (rowMat < matSize) ? A[colMat][rowMat].i : b[colMat].i);
            } else {
                sprintf(imagStr, "Imag j%s", buffer);
            }
            Screen_WriteString(120, panelY+rowHeight, "<<", FONT, currentTheme.button, currentTheme.bg);
        }
        Screen_WriteString(FONT_Width*7, panelY-rowHeight, "WRITE", FONT, currentTheme.matrix_selected, currentTheme.bg);
        Screen_WriteString(0, panelY, realStr, FONT, currentTheme.primary_text, currentTheme.bg);
        Screen_WriteString(0, panelY+rowHeight, imagStr, FONT, currentTheme.primary_text, currentTheme.bg);
    }
    
    // Controles en la parte más baja
    Screen_WriteString(0, panelY+(rowHeight)*2, "[=]OK", FONT, currentTheme.button, currentTheme.bg);
/*
    if(isPinkMode)
    Screen_DrawImage(120, panelY+14, 30, 30, (uint16_t*)IE8BITPK);
    else
    Screen_DrawImage(120, panelY+14, 30, 30, (uint16_t*)IE8BITBK);
  */                                              

}

// ==================== LEVEL 2: Resultados ====================
void drawLevel2(uint8_t success) {
    Screen_FillScreen(currentTheme.bg);
    
    if(success) {
        // Título
        Screen_WriteString(45, 5, "SOLUCION:", Font_7x10, currentTheme.title, currentTheme.bg);
        
        int startY = 20;
        int rowHeight = 16;
        
        // Mostrar cada solución
        for(uint8_t i = 0; i < matSize; i++) {
            int y = startY + i * rowHeight;
            
            // Variable (xi =)
            uint8_t posy = 8;
            char varStr[20];
            // Valor (parte real)
            char realStr[20];
            int idx = 0;
            char imagStr[2];
            // Parte imaginaria
            if(x[i].i != 0.0f) {
                
                int idx = 0;
                if(x[i].i > 0) {
                    imagStr[idx++] = '+';
                }

                imagStr[idx++] = 'j';                
                sprintf(varStr, "x%d = %.2f %s%.2f", i + 1,x[i].r,imagStr,x[i].i);
            }
            else sprintf(varStr, "x%d = %.2f", i + 1, x[i].r);
                      

            Screen_WriteString(8, y, varStr, Font_7x10, currentTheme.primary_text, currentTheme.bg);             

            y+=15;
        }
        
        // Instrucciones
        int instrY = startY + matSize * rowHeight + 10;
        Screen_WriteString(10, instrY, "Presione [T] para", Font_7x10, currentTheme.secondary_text, currentTheme.bg);
        Screen_WriteString(10, instrY + 10, "nuevo sistema", Font_7x10, currentTheme.secondary_text, currentTheme.bg);
        
    } else {
        // Error: sistema sin solución
        Screen_WriteString(20, 40, "SISTEMA SIN", Font_7x10, COLOR_RED, currentTheme.bg);
        Screen_WriteString(25, 55, "SOLUCION", Font_7x10, COLOR_RED, currentTheme.bg);
        Screen_WriteString(15, 80, "Matriz singular", Font_7x10, currentTheme.secondary_text, currentTheme.bg);
        Screen_WriteString(10, 100, "Presione [T]", Font_7x10, currentTheme.secondary_text, currentTheme.bg);
        Screen_WriteString(10, 110, "para reintentar", Font_7x10, currentTheme.secondary_text, currentTheme.bg);
    }
}

// Función auxiliar: Limpiar solo el área del buffer (actualización parcial)
void updateBufferDisplay(const char* buffer) {
    // Borrar área anterior
    Screen_FillRectangle(60, 90, 60, 10, currentTheme.bg);
    // Escribir nuevo buffer
    Screen_WriteString(60, 90, buffer, Font_7x10, currentTheme.primary_text, currentTheme.bg);
}
