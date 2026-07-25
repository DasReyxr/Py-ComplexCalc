/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "TFT_Screen.h"
#include "HALTecMat4x4.h"
#include "fonts.h"
#include "display_ui.h"
#include <stdlib.h>
#include <string.h>
#include "ComplexGJ.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
SPI_HandleTypeDef hspi1;

/* USER CODE BEGIN PV */
uint8_t level = 0 ;

// Buffer
#define BUFFER_SIZE 16
uint8_t index_Var = 0;
char buffer[BUFFER_SIZE];
uint8_t navigating = 0;
// Matriz y tama;o de matriz
uint8_t matSize;
cplx A[N_MAX][N_MAX] = {0};
cplx b[N_MAX] = {0};
cplx x[N_MAX] = {0};

// Variables de control de pantalla
uint8_t needsRedraw = 1;
uint8_t editingReal = 1; // 1 = editando real, 0 = editando imaginario
double real = 0.0, imag = 0.0;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_SPI1_Init(void);
/* USER CODE BEGIN PFP */
uint8_t readPad(char *);

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_SPI1_Init();
  /* USER CODE BEGIN 2 */
 
	char *keypress = NULL;
	char *endptr;
	uint8_t messageReady = 1;
	// Matriz
	uint8_t colMat = 0, rowMat = 0;
	double real, imag = 0.0;
	memset(buffer, 0, sizeof(buffer));
  __HAL_SPI_ENABLE(&hspi1);

    Screen_Init();
    initTheme();
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
    switch (level){
    case 0:
        // Dibujar pantalla solo cuando sea necesario
        if(needsRedraw) {
            drawLevel0();
            needsRedraw = 0;
        }
        
        keypress = gotKey();
        messageReady = readPad(keypress);
        
        if(messageReady == 0){
            // Actualizar solo el buffer en pantalla

            break;
        }

        // Conversión a entero
        matSize = (uint8_t)strtol(buffer, &endptr, 10);

        if ((endptr == buffer) || (matSize == 0)) {
            level = 0;
            needsRedraw = 1;
        }
        else if(matSize > N_MAX ) matSize = N_MAX;
        else if(matSize<2) matSize = 2;

        if(matSize >= 2 && matSize <= N_MAX) {
        	drawLevel0();


        	memset(buffer, 0, sizeof(buffer));
            index_Var = 0;
            colMat = 0;
            rowMat = 0;
            editingReal = 1;
            level = 1;
            needsRedraw = 1;
        }

        break;

    case 1:
        if(needsRedraw) {
            drawLevel1(colMat, rowMat);
            needsRedraw = 0;
        }
        
        keypress = gotKey();
        messageReady = readPad(keypress);
        
		// Si se presionó una tecla pero no es un mensaje completo
		if(messageReady == 2) {
			// Buffer cambió (se agregó/borró un dígito)
			needsRedraw = 1;
			break;
		}
		
		
		// Si no hay nada en el buffer, permitir navegación
        if(index_Var == 0 && navigating) {
            switch (*keypress){
                case 'W':
                    if(colMat > 0) colMat--;
                    needsRedraw = 1;
                    break;
                case 'B':
                    if(colMat < matSize - 1) colMat++;
                    needsRedraw = 1;
                    break;
                case 'L':
                    if(rowMat > 0) rowMat--;
                    needsRedraw = 1;
                    break;
                case 'R':
                    if(rowMat < matSize) rowMat++;
                    needsRedraw = 1;
                    break;            }
            break;
        }
        
        // Si hay mensaje (se presionó un número o tecla especial)
        if(messageReady == 1) {
            if(*keypress == '=') {
                if(editingReal) {
                    // Termina ingreso de parte real, pasa a imaginario
                    if(index_Var > 0) {
                        // Solo guardar si hay datos en el buffer
                        real = strtod(buffer, &endptr);
                        if(rowMat < matSize) A[colMat][rowMat].r = real;
                        else b[colMat].r = real;
                    }
                    memset(buffer, 0, sizeof(buffer));
                    index_Var = 0;
                    editingReal = 0;
                    needsRedraw = 1;
                } else {
                    // Termina ingreso de parte imaginaria, guarda y avanza
                    if(index_Var > 0) {
                        // Solo guardar si hay datos en el buffer
                        imag = strtod(buffer, &endptr);
                        if(rowMat < matSize) A[colMat][rowMat].i = imag;
                        else b[colMat].i = imag;
                    }
                    // Reset y avanzar
                    memset(buffer, 0, sizeof(buffer));
                    index_Var = 0;
                    editingReal = 1;
                    real = 0.0;
                    imag = 0.0;
                    // Avanzar a siguiente celda (por COLUMNAS primero)
                    rowMat++;
                    if(rowMat > matSize) {
                        rowMat = 0;
                        colMat++;
                    }
                    // Si terminamos, ir a resolver
                    if(colMat >= matSize) {
                        level = 2;
                    }
                    needsRedraw = 1;
                }
            } else if(*keypress == 'I') {
                // Tecla I: terminar parte real y pasar a imaginaria
                if(editingReal) {
                    if(index_Var > 0) {
                        real = strtod(buffer, &endptr);
                        if(rowMat < matSize) A[colMat][rowMat].r = real;
                        else b[colMat].r = real;
                    }
                    memset(buffer, 0, sizeof(buffer));
                    index_Var = 0;
                    editingReal = 0;
                    needsRedraw = 1;
                }
            }
        }
        break;

    case 2:
        // Resolver el sistema
        int success = solve_complex_system(matSize, A, b, x);
        drawLevel2(success == 0);
        
        // Esperar tecla para volver
        messageReady = 0;
        while(!(messageReady)){
            keypress = gotKey();
            messageReady = readPad(keypress);
        }
        
        // // Reset para nuevo sistema - limpiar matrices
        // memset(A, 0, sizeof(A));
        // memset(b, 0, sizeof(b));
        // memset(x, 0, sizeof(x));
        level = 0;
         matSize = 0;
        colMat = 0;  // Reset matrix position
        rowMat = 0;  // Reset matrix position
        memset(buffer, 0, sizeof(buffer));
        index_Var = 0;
        editingReal = 1;
        needsRedraw = 1;
        break;

		}
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief SPI1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI1_Init(void)
{

  /* USER CODE BEGIN SPI1_Init 0 */

  /* USER CODE END SPI1_Init 0 */

  /* USER CODE BEGIN SPI1_Init 1 */

  /* USER CODE END SPI1_Init 1 */
  /* SPI1 parameter configuration*/
  hspi1.Instance = SPI1;
  hspi1.Init.Mode = SPI_MODE_MASTER;
  hspi1.Init.Direction = SPI_DIRECTION_2LINES;
  hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi1.Init.NSS = SPI_NSS_SOFT;
  hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_2;
  hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi1.Init.CRCPolynomial = 10;
  if (HAL_SPI_Init(&hspi1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI1_Init 2 */

  /* USER CODE END SPI1_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  /* USER CODE BEGIN MX_GPIO_Init_1 */

  /* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(SCREEN_CS_GPIO_Port, SCREEN_CS_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, SCREEN_RST_Pin|SCREEN_D_C_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, ROW1_Pin|ROW2_Pin|ROW3_Pin|ROW4_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pins : SCREEN_CS_Pin SCREEN_RST_Pin SCREEN_D_C_Pin */
  GPIO_InitStruct.Pin = SCREEN_CS_Pin|SCREEN_RST_Pin|SCREEN_D_C_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pins : COL1_Pin COL2_Pin COL3_Pin COL4_Pin */
  GPIO_InitStruct.Pin = COL1_Pin|COL2_Pin|COL3_Pin|COL4_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pins : ROW1_Pin ROW2_Pin ROW3_Pin ROW4_Pin */
  GPIO_InitStruct.Pin = ROW1_Pin|ROW2_Pin|ROW3_Pin|ROW4_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /* USER CODE BEGIN MX_GPIO_Init_2 */

  /* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */


uint8_t readPad(char *keypress){

    if (keypress == NULL) return 0;
    char key = *keypress;

    // Handle control keys
    if (key == '=') {
        /*if (level < 2) level++;
        if (level == 2) level--;*/
        return 1;
    }
	if (*keypress == '-') {
    // Only allow '-' as the first character in the buffer
    if (index_Var == 0) {
        buffer[index_Var++] = '-';
        return 2;} 
	else return 0; // Ignore if not at start
	}
    if (key == 'T') { // Back
        if (level > 0) level--; 
        memset(buffer, 0, sizeof(buffer));
        index_Var = 0;
        return 2;
    }
    if (key == 'D') {
        if (index_Var > 0) { // Backspace
            index_Var--;
            buffer[index_Var] = 0;
        }
        return 2;
    }
    if (key == 'I') {
        return 1;
    }
    if (key == 'F') { // Alt Mode
        navigating ^= 1;
        return 2;
    }
    if (key == 'S'){ // Solve
        level = 2; 
        return 2;
    }
    if (key == 'P') {
        toggleTheme(); //Pink Mode
        needsRedraw = 1;
        return 2;
    }

    // Handle numbers and dot
    if ((key >= '0' && key <= '9') || key == '.') {
        if (index_Var < BUFFER_SIZE) {
            buffer[index_Var++] = key;
        }
        return 2;
    }

    // Unknown key
    return 0;
					}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}
#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
