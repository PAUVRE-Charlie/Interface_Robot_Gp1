float v_max = 1;
float a_max = 0.5;
float dy = 5;
float t = dy/v_max;
float tau = v_max/a_max;
float to = 0.01;

void setup() {
}

void loop() {
  if (t < tau) {
    t = sqrt(dy/a_max);
    tau = t;
    int v[2*int(t/to)];
    for (i=0,i<len(v),i++) {
      if (i*to<=tau) {
        v[i] = a_max*i*to;
      }
      else { v[i] = v[i-1]-a_max*to; }
    }
  else {
    int v[int((t+tau)/to)];
    for (i=0,i<len(v),i++) {
      if (i*to<=tau) {
        v[i] = a_max*i*to;
      }
      if (i*to >= t)
        v[i] = v[i-1]-a_max*to ;
      }
    else {v[i] = v_max;}
   }
  v;

}



