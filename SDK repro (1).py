# Databricks notebook source
# MAGIC %md
# MAGIC # Repro for Milan
# MAGIC
# MAGIC sdsadssdasdadsadsads
# MAGIC 
# MAGIC klkl

# COMMAND ----------



# COMMAND ----------

# MAGIC %pip install azure.cognitiveservices.speech

# COMMAND ----------

import azure.cognitiveservices.speech as speechsdk

# COMMAND ----------

# MAGIC %md
# MAGIC # Speech to text
# MAGIC
# MAGIC Just a little testing of Magic commands

# COMMAND ----------

cognitive_service_key = "f3c90cd249814933940169a72f7608d5"
endpoint = "westeurope"
path_for_the_file = (
    "/dbfs/FileStore/shared_uploads/miszopinski@microsoft.com/audio2-2.wav"
)

# COMMAND ----------

import azure.cognitiveservices.speech as speechsdk


def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(
        subscription=cognitive_service_key, region=endpoint
    )
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(filename=path_for_the_file)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(
            "No speech could be recognized: {}".format(
                speech_recognition_result.no_match_details
            )
        )
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


recognize_from_microphone()

# COMMAND ----------

# MAGIC %md
# MAGIC #end of repro for Milan
# MAGIC
# MAGIC and a little more :)

# COMMAND ----------

# MAGIC %md
# MAGIC # text to speech

# COMMAND ----------

import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="f3c90cd249814933940169a72f7608d5", region="westeurope"
)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

speech_synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config
)

# Get text from the console and synthesize to the default speaker.
print("initializing")
text = "blah blah only testing purposes"

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

# COMMAND ----------

# MAGIC %md
# MAGIC # translation

# COMMAND ----------

import azure.cognitiveservices.speech as speechsdk


def recognize_from_microphone():
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription="f3c90cd249814933940169a72f7608d5", region="westeurope"
    )
    speech_translation_config.speech_recognition_language = "en-US"

    target_language = "pl"
    speech_translation_config.add_target_language(target_language)

    audio_config = speechsdk.audio.AudioConfig(
        filename="/dbfs/FileStore/shared_uploads/miszopinski@microsoft.com/audio2-2.wav"
    )
    translation_recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=speech_translation_config, audio_config=audio_config
    )

    print("Speak into your microphone.")
    translation_recognition_result = (
        "czesc witam bardzo serdecznie takie tam testowanko"
    )

    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("Recognized: {}".format(translation_recognition_result.text))
        print(
            """Translated into '{}': {}""".format(
                target_language,
                translation_recognition_result.translations[target_language],
            )
        )
    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(
            "No speech could be recognized: {}".format(
                translation_recognition_result.no_match_details
            )
        )
    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


recognize_from_microphone()

# COMMAND ----------

# MAGIC %sh
# MAGIC nslookup westeurope.stt.speech.microsoft.com

# COMMAND ----------

# MAGIC %sh
# MAGIC telnet westeurope.stt.speech.microsoft.com

# COMMAND ----------

# MAGIC %sh
# MAGIC nslookup http://www.microsoft.com/pkiops

# COMMAND ----------

# MAGIC %sh
# MAGIC pip install httplib2

# COMMAND ----------

import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": "ff3c90cd249814933940169a72f7608d5",
}

params = urllib.parse.urlencode(
    {
        # Request parameters
        "visualFeatures": "Categories",
        "details": "{string}",
        "language": "en",
        "model-version": "latest",
    }
)

try:
    conn = http.client.HTTPSConnection("westus.api.cognitive.microsoft.com")
    conn.request("POST", "/vision/v3.2/analyze?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
