
uint32_t session_start_msec;
uint32_t nextSec;
uint32_t currentSec;

uint32_t ITI = 10000; //both trial and iti are 5s long

uint32_t currentMov;
uint32_t nextMov;

bool online = false;
char start_c = 's'; 
char end_c = 'e';

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  //Serial.println(online);
  char data = Serial.read();

  if(data == end_c){ //end session
      online = false;  
    }

  if(online){
    currentSec = millis(); //assigning up here is creating drift effect
    currentMov = millis();
    
    if((currentSec  > nextSec)){
      Serial.print(F("$SY,")); 
      Serial.println(currentSec - session_start_msec);
      nextSec = currentSec + 1000;
     
      }

      
     if(currentMov > nextMov){
      
        Serial.print(F("$MV,"));
        Serial.print(currentMov - session_start_msec);
        Serial.print(",");
        Serial.print(random(0,2));
        Serial.print(",");
        Serial.println(random(0,2));
        nextMov = currentMov + ITI;
      //  break;
        
      } 
    }
  else if(data == start_c){   //begin session
    session_start_msec = millis();
    currentMov = millis();
    nextMov = currentMov + ITI;
    nextSec = session_start_msec + 1000;
    online = true;
    Serial.print("$SY1,");
    Serial.println(session_start_msec);
    }
   
    

}









