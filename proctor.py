import json
import requests
from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment


class ProctoringXBlock(XBlock):
    """
    A custom XBlock for proctoring exams in Open edX.
    """
    # XBlock fields
    exam_id = Integer(help="The ID of the exam being proctored.", scope=Scope.user_state)
    def start_proctoring(self, exam_id):
        """
        Start the proctoring process for the specified exam ID.
        """
        self.exam_id = exam_id
        url = "http://proctoring.api/start_proctoring"
        data = {"exam_id": exam_id}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
    def stop_proctoring(self):
        """
        Stop the proctoring process for the current exam ID.
        """
        if self.exam_id is not None:
            url = "http://proctoring.api/stop_proctoring"
            data = {"exam_id": self.exam_id}
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
    def submit_exam(self):
        """
        Submit the exam for the current exam ID.
        """
        if self.exam_id is not None:
            url = "http://proctoring.api/submit_exam"
            data = {"exam_id": self.exam_id}
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
    def studio_view(self, context=None):
        """
        The primary view of the ProctoringXBlock for course staff.
        """
        html = """
            <div>
                <label for="exam_id">Exam ID:</label>
                <input type="number" id="exam_id" name="exam_id">
                <button id="start_proctoring">Start Proctoring</button>
                <button id="stop_proctoring">Stop Proctoring</button>
                <button id="submit_exam">Submit Exam</button>
            </div>
            <script>
                $(function() {
                    $("#start_proctoring").click(startProctoring);
                    $("#stop_proctoring").click(stopProctoring);
                    $("#submit_exam").click(submitExam);
                });
                function startProctoring() {
                    var exam_id = $("#exam_id").val();
                    $.ajax({
                        url: "start_proctoring",
                        type: "POST",
                        data: {exam_id: exam_id},
                        success: function(response) {
                            alert("Proctoring started for exam " + exam_id);
                        },
                        error: function(xhr, status, error) {
                            alert(xhr.responseText);
                        }
                    });
                }
                function stopProctoring() {
                    $.ajax({
                        url: "stop_proctoring",
                        type: "POST",
                        success: function(response) {
                            alert("Proctoring stopped");
                        },
                        error: function(xhr, status, error) {
                            alert(xhr.responseText);
                        }
                    });
                }
                function submitExam() {
                    $.ajax({
                        url: "submit_exam",
                        type: "POST",
                        success: function(response) {
                            alert("Exam submitted");
                        },
                        error: function(xhr, status, error) {
                            alert(xhr.responseText
                            }
                    });
                }
            </script>
        """
        frag = Fragment(html)
        frag.add_css("""
            label {
                display: inline-block;
                width: 100px;
            }
            input {
                width: 150px;
            }
            button {
                margin-left: 10px;
            }
        """)
        return frag

    def student_view(self, context=None):
        """
        The primary view of the ProctoringXBlock for students.
        """
        html = """
            <div>
                <p>Proctoring is currently in progress for this exam.</p>
                <p>Please complete the exam before the proctoring session ends.</p>
            </div>
        """
        frag = Fragment(html)
        return frag

    def submit_studio_form(self, data, suffix=''):
        """
        Handle a form submission from the ProctoringXBlock studio view.
        """
        if "exam_id" in data:
            self.start_proctoring(data["exam_id"])

    @XBlock.handler
    def start_proctoring(self, request, suffix=''):
        """
        Handle a request to start proctoring for an exam.
        """
        if request.method == "POST":
            exam_id = request.POST.get("exam_id")
            if exam_id is not None:
                self.start_proctoring(int(exam_id))
                return HttpResponse(status=204)
        return HttpResponseBadRequest()

    @XBlock.handler
    def stop_proctoring(self, request, suffix=''):
        """
        Handle a request to stop proctoring for the current exam.
        """
        if request.method == "POST":
            self.stop_proctoring()
            return HttpResponse(status=204)
        return HttpResponseBadRequest()

    @XBlock.handler
    def submit_exam(self, request, suffix=''):
        """
        Handle a request to submit the current exam.
        """
        if request.method == "POST":
            self.submit_exam()
            return HttpResponse(status=204)
        return HttpResponseBadRequest()

    @staticmethod
    def workbench_scenarios():
        """
        Define the scenarios for the ProctoringXBlock in the workbench.
        """
        return [
            ("ProctoringXBlock",
            """<proctoring/>
            """),
        ]
