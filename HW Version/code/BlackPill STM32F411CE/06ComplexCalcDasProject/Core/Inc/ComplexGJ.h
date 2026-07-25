#ifndef ComplexGJ_H
#define ComplexGJ_H

#include <math.h>

// --- Constants ---
#define N_MAX 4
#define EPSILON 1e-7f

// --- Error Codes ---
#define SOLVER_SUCCESS           0
#define SOLVER_ERR_INVALID_SIZE  1
#define SOLVER_ERR_SINGULAR      2

// --- Complex Number Type ---
typedef struct {
    float r;  // Real part
    float i;  // Imaginary part
} cplx;

// --- Complex Arithmetic Operations ---
static inline cplx c_add(cplx a, cplx b) { 
    return (cplx){a.r + b.r, a.i + b.i}; 
}

static inline cplx c_sub(cplx a, cplx b) { 
    return (cplx){a.r - b.r, a.i - b.i}; 
}

static inline cplx c_mul(cplx a, cplx b) {
    return (cplx){a.r*b.r - a.i*b.i, a.r*b.i + a.i*b.r};
}

static inline cplx c_div(cplx a, cplx b) {
    float den = b.r*b.r + b.i*b.i;
    return (cplx){(a.r*b.r + a.i*b.i)/den, (a.i*b.r - a.r*b.i)/den};
}

static inline float c_mag(cplx a) {
    return sqrtf(a.r*a.r + a.i*a.i);
}

// --- Linear System Solver ---
int solve_complex_system(int n, cplx A[N_MAX][N_MAX], cplx b[N_MAX], cplx x[N_MAX]);

// --- String Formatting Functions ---
void cplx_to_str(cplx num, char* buffer, int* index);
void ftoa_simple(float f, char* buf, int* index, int digits);
void itoa_simple(int n, char* buf, int* index);

#endif
