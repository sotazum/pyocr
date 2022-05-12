# pyocr

Recognize text at a specified position in a video and writes it to Excel, allowing automatic saving of question text to Excel for quizzes on the web, such as screenshot videos where different sentences appear at the same position in a sequence. Since the system recognizes that the question text switches on the screen in chronological order, the same text is never saved in Excel.

video_to_frame.py: Break down the input video into frames.
ocr.py, ocr_many.py: Recognize text and write it to Excel.
