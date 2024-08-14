//https://www.arducam.com/docs/arducam-mega/arducam-mega-getting-started/packs/C_ApiDoc.html

#include <WiFi.h>
#include <WebServer.h>
#include <SPIFFS.h>
#include <FS.h>
#include "Arducam_Mega.h"

// WiFi credentials
const char* ssid = "SCB-Data-Collection";
const char* password = "Annoy-Frequency5";

// Camera configuration
WebServer server(80);
const int CS = 5;
Arducam_Mega myCAM(CS);

CAM_IMAGE_MODE imageMode = CAM_IMAGE_MODE_HD;

// Image buffer
const size_t bufferSize = 2048;
uint8_t buffer[bufferSize] = { 0 };

// Function to capture and save image
void captureAndSaveImage_before() {
  myCAM.takePicture(imageMode, CAM_IMAGE_PIX_FMT_JPG);
  File file = SPIFFS.open("/image_before.jpg", FILE_WRITE);
  if (!file) {
    Serial.println("Failed to open file for writing");
    return;
  }
  while (myCAM.getReceivedLength()) {
    for (size_t i = 0; i < bufferSize && myCAM.getReceivedLength(); i++) {
      buffer[i] = myCAM.readByte();
    }
    file.write(buffer, bufferSize);
  }
  file.close();
  Serial.println("Image saved to /image_before.jpg");
}

// Function to capture and save image
void captureAndSaveImage_after() {
  myCAM.takePicture(imageMode, CAM_IMAGE_PIX_FMT_JPG);
  File file = SPIFFS.open("/image_after.jpg", FILE_WRITE);
  if (!file) {
    Serial.println("Failed to open file for writing");
    return;
  }
  while (myCAM.getReceivedLength()) {
    for (size_t i = 0; i < bufferSize && myCAM.getReceivedLength(); i++) {
      buffer[i] = myCAM.readByte();
    }
    file.write(buffer, bufferSize);
  }
  file.close();
  Serial.println("Image saved to /image_after.jpg");
}

// Function to handle the root request and provide the image link
void handleRoot() {
  String response = "Image captured! Click <a href=\"/image\">here</a> to view the image.";
  server.send(200, "text/html", response);
}

// Function to serve the captured image
void handleImage_before() {
  File file = SPIFFS.open("/image_before.jpg", FILE_READ);
  if (!file) {
    server.send(500, "text/plain", "Failed to open image file");
    return;
  }
  server.streamFile(file, "image/jpeg");
  file.close();
}

// Function to serve the captured image
void handleImage_after() {
  File file = SPIFFS.open("/image_after.jpg", FILE_READ);
  if (!file) {
    server.send(500, "text/plain", "Failed to open image file");
    return;
  }
  server.streamFile(file, "image/jpeg");
  file.close();
}

void setup() {
  Serial.begin(115200);
  myCAM.begin();
  //Picture Settings
  myCAM.setAutoFocus(1);     // Enable autofocus
  myCAM.setAutoExposure(1);  // Enable auto exposure
  myCAM.setBrightness(CAM_BRIGHTNESS_LEVEL_2);
  myCAM.setSharpness(CAM_SHARPNESS_LEVEL_8);
  myCAM.setAutoISOSensitive(1);
  myCAM.setAutoWhiteBalance(1);
  myCAM.setSaturation(CAM_STAURATION_LEVEL_1);
  myCAM.setContrast(CAM_CONTRAST_LEVEL_1);
  myCAM.setImageQuality(HIGH_QUALITY);

  // Initialize SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("An error has occurred while mounting SPIFFS");
    return;
  }
  SPIFFS.remove("/image_before.jpg");
  SPIFFS.remove("/image_after.jpg");
  // Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Print the IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Capture and save an image
  Serial.println("Image_before started");
  captureAndSaveImage_before();
  delay(2000);
  Serial.println("Image_after started");
  captureAndSaveImage_after();

  // Set up the web server routes
  server.on("/", HTTP_GET, handleRoot);
  server.on("/image_before", HTTP_GET, handleImage_before);
  server.on("/image_after", HTTP_GET, handleImage_after);
  server.begin();
}

void loop() {
  server.handleClient();
}
