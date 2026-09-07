from Doctors_Brain import brain_of_the_doctor
from Doctors_Voice import convert_text_to_doctor_audio
from Patients_Voice import transcribe_patient_voice


def analyze_consultation(audio_path, image_path, video_path):
    """Create a patient transcript, cautious AI guidance, and spoken response."""
    if not audio_path:
        raise ValueError("Please record or upload a voice description.")
    if not image_path:
        raise ValueError("Please upload a clear skin image to continue.")

    patient_text = transcribe_patient_voice(audio_path)
    guidance = brain_of_the_doctor(
        patient_text=patient_text,
        image_filepath=image_path,
        video_filepath=video_path,
    )
    return patient_text, guidance, str(convert_text_to_doctor_audio(guidance))
