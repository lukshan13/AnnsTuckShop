$(document).ready(function(){
	$('select[name="Forest_Email_Domain_Form"]').change(function() {
		if ($(this).val() == "sch_staff"){
			$("._staff").attr('disabled', false);
			$("._student").attr('disabled', true);
			$( "._staff" ).prop( "checked", true );
		}
		if ($(this).val() == "sch_student"){
			$("._staff").attr('disabled', true);
			$("._student").attr('disabled', false);
			$("._student-default" ).prop( "checked", true );
		}
	});
})