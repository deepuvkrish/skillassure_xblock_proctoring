# skillassure_xblock_proctoring
Proctoring code for skillassure project created using openedX
This script defines an ProctoringXBlock class that inherits from the XBlock class. The exam_id field is used to store the ID of the exam being proctored.

The start_proctoring method is used to start the proctoring process. It sends a request to the proctoring API with the exam ID and an authorization token. If the API returns a successful response, the exam ID is stored in the exam_id field.

The stop_proctoring method is used to stop the proctoring process. It sends a request to the proctoring API with the exam ID and an authorization token. If the API returns a successful response, the exam_id field is cleared.

The submit_exam method is used to submit the exam to the proctoring service. It sends a request to the proctoring API with the exam ID and an authorization
