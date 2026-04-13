import pyautogui
import pytesseract
import time


def main():
    # Point to the tesseract engine : needed to extract words from the images
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\samson.carter\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    
    x, y , w, h = DetermineScreenshotArea()

    print(f" {x}, {y}, {w}, {h}")
    
    # Take a screenshot of the top left corner (100x100 pixels)
    screenshot = pyautogui.screenshot(region=(x, y, w, h))

    # Try to read it
    print(pytesseract.image_to_string(screenshot))

    print("Starting Transcription... Press Ctrl+C to stop and save")

    last_text = ""

    with open("meeting_transcript.txt", "a") as f:
        try:
            while True:
                # 1. Take the screenshot of hte caption area
                screenshot = pyautogui.screenshot(region=(x, y, w, h))

                # 2. Convert pixels to a string
                # strip/remove whitespace and newlines
                current_text = pytesseract.image_to_string(screenshot).strip()

                # 3. Logic: Only record if there is text and it's NEW 
                if current_text and current_text != last_text:
                    #check if the new text is just a subset of the old (to handle scrolling)
                    if current_text not in last_text:
                        print(f"Captured: {current_text}") #DEBUG REMOVE ONCE WORKING
                        f.write(current_text + "\n")
                        f.flush() # Forces the text into the file immeidately
                        last_text = current_text

                    # Wait a moment before checking again
                    time.sleep(1.5)

        except KeyboardInterrupt:
            print("\nITranscription Stopped. File Saved.")


def DetermineScreenshotArea():
    print("Position the mouse at the TOP LEFT corner of the caption area.")
    time.sleep(3) # gives you three seconds to get in position
    top_left = pyautogui.position()
    print(f"Top Left captured: {top_left}")

    print("\nNow move to the BOTTOM RIGHT of the caption area.")
    time.sleep(3)
    bottom_right = pyautogui.position()
    print(f"Bottom Right captured: {bottom_right}")

    # Calcuate the Width and Height for this region
    width = bottom_right.x - top_left.x
    height = bottom_right.y - top_left.y

    print(f"\nYour CAPTION REGION is: ({top_left.x}, {top_left.y}, {width}, {height})")

    return (top_left.x, top_left.y, width, height)


if __name__ == '__main__':
    main()


# Updates
# 1) Code is able to extract the area of the CC space at the launch of the program and read the text taht is within the given space
# 2) 