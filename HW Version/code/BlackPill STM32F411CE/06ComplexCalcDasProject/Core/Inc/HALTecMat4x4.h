/*
 * HALTecMat4x4.h
 *
 *  Created on: Dec 17, 2025
 *      Author: dasre
 */

#ifndef INC_HALTECMAT4X4_H_
#define INC_HALTECMAT4X4_H_

#include <stm32f4xx.h>
#include "main.h"
#include <stdint.h>

// GpioPin typedef - shared across multiple modules
#ifndef GPIOPIN_TYPEDEF
#define GPIOPIN_TYPEDEF
typedef struct{
    GPIO_TypeDef *port;
    uint16_t pin;
} GpioPin;
#endif

// Matrix keypad row pins (PB4-PB7) - Output
static const GpioPin KeypadRow0 = {
    .port = GPIOB, .pin = GPIO_PIN_4
};

static const GpioPin KeypadRow1 = {
    .port = GPIOB, .pin = GPIO_PIN_5
};

static const GpioPin KeypadRow2 = {
    .port = GPIOB, .pin = GPIO_PIN_6
};

static const GpioPin KeypadRow3 = {
    .port = GPIOB, .pin = GPIO_PIN_7
};

// Matrix keypad column pins (PB12-PB15) - Input with pull-up
static const GpioPin KeypadCol0 = {
    .port = GPIOB, .pin = GPIO_PIN_12
};

static const GpioPin KeypadCol1 = {
    .port = GPIOB, .pin = GPIO_PIN_13
};

static const GpioPin KeypadCol2 = {
    .port = GPIOB, .pin = GPIO_PIN_14
};

static const GpioPin KeypadCol3 = {
    .port = GPIOB, .pin = GPIO_PIN_15
};

extern char* gotKey(void);
extern char* toggleAlternateMode(void);
extern void config4x4(void);


#endif /* INC_HALTECMAT4X4_H_ */
