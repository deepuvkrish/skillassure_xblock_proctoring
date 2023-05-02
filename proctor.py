import os
import requests
import json
from xblock.core import XBlock
from xblock.fields import Scope, Integer

class ProctoringXBlock(XBlock):
    exam_id = Integer(default=0, scope=Scope.user_state_summary)

    def start_proctoring(self, exam_id):
        # Call the proctoring API to start the proctoring process
        proctoring_url = os.environ.get('PROCTORING_URL')
        proctoring_key = os.environ.get('PROCTORING_KEY')
        data = {'exam_id': exam_id}
        headers = {'Authorization': f'Bearer {proctoring_key}'}
        response = requests.post(f'{proctoring_url}/proctoring/start', data=json.dumps(data), headers=headers)
        response_data = response.json()
        if response.status_code == 200:
            # Save the exam ID for future reference
            self.exam_id = exam_id
        else:
            # Log an error message
            self.log.error('Failed to start proctoring: %s', response_data['message'])

    def stop_proctoring(self):
        # Call the proctoring API to stop the proctoring process
        proctoring_url = os.environ.get('PROCTORING_URL')
        proctoring_key = os.environ.get('PROCTORING_KEY')
        data = {'exam_id': self.exam_id}
        headers = {'Authorization': f'Bearer {proctoring_key}'}
        response = requests.post(f'{proctoring_url}/proctoring/stop', data=json.dumps(data), headers=headers)
        response_data = response.json()
        if response.status_code == 200:
            # Clear the exam ID
            self.exam_id = 0
        else:
            # Log an error message
            self.log.error('Failed to stop proctoring: %s', response_data['message'])

    def submit_exam(self):
        # Call the proctoring API to submit the exam
        proctoring_url = os.environ.get('PROCTORING_URL')
        proctoring_key = os.environ.get('PROCTORING_KEY')
        data = {'exam_id': self.exam_id}
        headers = {'Authorization': f'Bearer {proctoring_key}'}
        response = requests.post(f'{proctoring_url}/proctoring/submit', data=json.dumps(data), headers=headers)
        response_data = response.json()
        if response.status_code == 200:
            # Clear the exam ID
            self.exam_id = 0
        else:
            # Log an error message
            self.log.error('Failed to submit exam: %s', response_data['message'])

