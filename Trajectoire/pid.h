//PID constants
float kp_d = 2;
float ki_d = 5;
float kd_d = 1;

float kp_g = 2;
float ki_g = 5;
float kd_g = 1;

float error_d, error_g;
float lastError_d, lastError_g;
float cumError_d, rateError_d, cumError_g, rateError_g;

void computePID(float vg_mes, float vd_mes, float *vg, float *vd, float elapsedTime) {


    error_d = vd - vd_mes;                                // determine error
    cumError_d += error_d * elapsedTime;                // compute integral
    rateError_d = (error_d - lastError_d) / elapsedTime;   // compute derivative

    error_g = vg - vg_mes;                                // determine error
    cumError_g += error_g * elapsedTime;                // compute integral
    rateError_g = (error_g - lastError_g) / elapsedTime;   // compute derivative

    vd = kp_d * error_d + ki_d * cumError_d + kd_d * rateError_d;
    vg = kp_g * error_g + ki_g * cumError_g + kd_g * rateError_g;                //PID output               

    lastError_d = error_d;                                //remember current error
    lastError_g = error_g;

    return;                                        
}