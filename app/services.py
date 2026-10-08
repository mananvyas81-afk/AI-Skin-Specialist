from Doctors_Brain import brain_of_the_doctor
from Doctors_Voice import convert_text_to_doctor_audio
from Patients_Voice import transcribe_patient_voice

LOW_CONFIDENCE = 60  # % - below this we ask the user to see a doctor


def analyze_consultation(audio_path, image_path, video_path):
    """Pipeline: image + voice -> preprocessing -> vision model -> prediction + confidence."""
    if not audio_path:
        raise ValueError("Please record or upload a voice description.")
    if not image_path:
        raise ValueError("Please upload a clear skin image to continue.")

    patient_text = transcribe_patient_voice(audio_path)
    result = brain_of_the_doctor(
        patient_text=patient_text,
        image_filepath=image_path,
        video_filepath=video_path,
    )

    rows = [[c, f"{conf:.0f}%"] for c, conf in result["predictions"]]
    guidance = result["guidance"]
    if not result["predictions"] or result["predictions"][0][1] < LOW_CONFIDENCE:
        guidance += " Confidence is low, so please consult a dermatologist."

    return (
        patient_text,
        guidance,
        str(convert_text_to_doctor_audio(guidance)),
        result["preprocessed_image"],
        "\n".join(result["quality_notes"]),
        rows,
    )
