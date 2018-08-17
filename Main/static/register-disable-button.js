
$(document).ready(function(){
	$('select[name="Forest_Email_Domain"]').change(function() {
		if ($(this).val() == "sch_staff"){
			$("._staff").attr('disabled', false);
			$("._student").attr('disabled', true);
		}
		if ($(this).val() == "sch_student"){
			$("._staff").attr('disabled', true);
			$("._student").attr('disabled', false);
		}
			});