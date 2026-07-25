#include "ComplexGJ.h"

// ============================================================================
// String Formatting Utilities
// ============================================================================

/**
 * @brief Convert integer to string
 * @param n Integer to convert
 * @param buf Output buffer
 * @param index Current position in buffer (updated after write)
 */
void itoa_simple(int n, char* buf, int* index) {
    if(n == 0) { 
        buf[(*index)++] = '0'; 
        return; 
    }
    
    if(n < 0) { 
        buf[(*index)++] = '-'; 
        n = -n; 
    }
    
    char temp[10];
    int t = 0;
    while(n > 0) { 
        temp[t++] = '0' + (n % 10); 
        n /= 10; 
    }
    
    // Reverse digits
    for(int i = t - 1; i >= 0; i--) {
        buf[(*index)++] = temp[i];
    }
}

/**
 * @brief Convert float to string with fixed decimal places
 * @param f Float to convert (handles sign internally)
 * @param buf Output buffer
 * @param index Current position in buffer (updated after write)
 * @param digits Number of decimal places
 */
void ftoa_simple(float f, char* buf, int* index, int digits) {
    // Handle sign
    if(f < 0) { 
        buf[(*index)++] = '-'; 
        f = -f; 
    }

    // Integer part
    int int_part = (int)f;
    float frac_part = f - int_part;
    itoa_simple(int_part, buf, index);

    // Decimal point
    buf[(*index)++] = '.';

    // Fractional part
    for(int i = 0; i < digits; i++){
        frac_part *= 10;
        int d = (int)frac_part;
        buf[(*index)++] = '0' + d;
        frac_part -= d;
    }
}

/**
 * @brief Convert complex number to string format "a+bi" or "a-bi"
 * @param num Complex number to convert
 * @param buffer Output buffer
 * @param index Current position in buffer (updated after write)
 */
void cplx_to_str(cplx num, char* buffer, int* index) {
    // Real part
    ftoa_simple(num.r, buffer, index, 2);
    
    // Sign for imaginary part
    if(num.i >= 0) {
        buffer[(*index)++] = '+';
    } else {
        buffer[(*index)++] = '-';
    }
    
    // Imaginary part (absolute value, sign already shown)
    ftoa_simple(fabsf(num.i), buffer, index, 2);
    buffer[(*index)++] = 'i';
    buffer[(*index)] = '\0';
}

// ============================================================================
// Linear System Solver (Gaussian Elimination)
// ============================================================================

/**
 * @brief Swap two rows in the augmented matrix [A|b]
 */
static void swap_rows(cplx A[N_MAX][N_MAX], cplx b[N_MAX], int n, int r1, int r2) {
    if(r1 == r2) return;  // Optimization: no swap needed
    
    // Swap matrix rows
    for (int j = 0; j < n; j++) {
        cplx tmp = A[r1][j];
        A[r1][j] = A[r2][j];
        A[r2][j] = tmp;
    }
    
    // Swap vector elements
    cplx tmpb = b[r1];
    b[r1] = b[r2];
    b[r2] = tmpb;
}

/**
 * @brief Solve a system of linear equations with complex coefficients
 *        Uses Gaussian elimination with partial pivoting
 * 
 * @param n Size of the system (must be > 0 and <= N_MAX)
 * @param A Coefficient matrix [n x n] (not modified)
 * @param b Right-hand side vector [n] (not modified)
 * @param x Solution vector [n] (output)
 * @return SOLVER_SUCCESS on success
 *         SOLVER_ERR_INVALID_SIZE if n is out of range
 *         SOLVER_ERR_SINGULAR if matrix is singular (no unique solution)
 */
int solve_complex_system(int n, cplx A[N_MAX][N_MAX], cplx b[N_MAX], cplx x[N_MAX]) {
    // Validate input
    if (n <= 0 || n > N_MAX) {
        return SOLVER_ERR_INVALID_SIZE;
    }

    // Create local copies to preserve originals
    cplx A_work[N_MAX][N_MAX];
    cplx b_work[N_MAX];
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            A_work[i][j] = A[i][j];
        }
        b_work[i] = b[i];
    }

    // Forward elimination with partial pivoting
    for (int k = 0; k < n; k++) {
        // Find pivot (row with largest magnitude in column k)
        int pivot_row = k;
        float max_mag = c_mag(A_work[k][k]);
        
        for (int i = k + 1; i < n; i++) {
            float mag = c_mag(A_work[i][k]);
            if (mag > max_mag) { 
                max_mag = mag; 
                pivot_row = i; 
            }
        }
        
        // Check for singularity
        if (max_mag < EPSILON) {
            return SOLVER_ERR_SINGULAR;
        }

        // Swap rows if necessary
        if (pivot_row != k) {
            swap_rows(A_work, b_work, n, k, pivot_row);
        }

        // Eliminate column k below diagonal
        cplx pivot = A_work[k][k];
        for (int i = k + 1; i < n; i++) {
            cplx multiplier = c_div(A_work[i][k], pivot);
            
            // Update row i
            for (int j = k; j < n; j++) {
                A_work[i][j] = c_sub(A_work[i][j], c_mul(multiplier, A_work[k][j]));
            }
            b_work[i] = c_sub(b_work[i], c_mul(multiplier, b_work[k]));
        }
    }

    // Back substitution
    for (int i = n - 1; i >= 0; i--) {
        cplx sum = {0.0f, 0.0f};
        
        // Sum known values
        for (int j = i + 1; j < n; j++) {
            sum = c_add(sum, c_mul(A_work[i][j], x[j]));
        }
        
        // Solve for x[i]
        x[i] = c_div(c_sub(b_work[i], sum), A_work[i][i]);
    }
    
    return SOLVER_SUCCESS;
}