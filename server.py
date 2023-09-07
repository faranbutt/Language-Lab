import replicate
import argparse
import os
import numpy as np
np.bool = bool
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource
from flask_restful import Api
from flask import jsonify, make_response, send_file
cwd = os.getcwd()
import requests
from bs4 import BeautifulSoup, Comment
import base64
import os
PAT = os.environ.get("PAT")
import re
import random





from flask import Flask, request, jsonify
from flask_cors import CORS
import argparse
import os
cwd = os.getcwd()
import numpy as np
np.bool = bool
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource
from flask_restful import Api
from flask import jsonify, make_response, send_file
import requests
from bs4 import BeautifulSoup, Comment
import base64
import wave
import array
from io import BytesIO
import openai
openai.api_key = os.environ.get("OPENAI_API_KEY")
print("key:", openai.api_key)

PAT = os.environ.get("PAT")
print("PAT:", PAT)


from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)






def create_app():
    app = Flask(__name__)  # static_url_path, static_folder, template_folder...
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*"}})


    api = Api(app)



    

    @app.route('/speechtotext', methods=['POST'])
    def speechtotext():
        audio_bytes_64 = request.json.get('audio')
        MODEL_ID = 'whisper'
        MODEL_VERSION_ID = 'ccfd40cc37c448ef87fd5f166e7cb16e'
        userDataObject = resources_pb2.UserAppIDSet(user_id='openai', app_id='transcription')
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            audio=resources_pb2.Audio(
                                base64=base64.b64decode(audio_bytes_64)
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)


        output = post_model_outputs_response.outputs[0].data.text.raw
        return jsonify({'text': output})
    

    #returns audio in the format of 'data:audio/wav;base64,' + base64_encoded
    @app.route('/texttospeech', methods=['POST'])
    def texttospeech():
        text = request.json.get('text')

        userDataObject = resources_pb2.UserAppIDSet(user_id='eleven-labs', app_id='audio-generation')

        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                model_id='speech-synthesis',
                version_id='7b8ef26f9dc048869cbef1cd4ecb93e4',  # This is optional. Defaults to the latest model version
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=text
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        # Since we have one input, one output will exist here
        output = post_model_outputs_response.outputs[0]
        audio_raw = output.data.audio.base64
        sample_rate = output.data.audio.audio_info.sample_rate

        base64_encoded = base64.b64encode(audio_raw).decode('utf-8')
        src = 'data:audio/wav;base64,' + base64_encoded

        return jsonify({'audio': src, 'sample_rate': sample_rate})



    @app.route('/randomsentence', methods=['POST'])
    def randomsentence():
        print("used random sentence")
        language = request.json.get('language')
        print("used random sentence:", language)

        sentences = [
            {
                "original":"Hello, how are you?",
                "translated":{
                    "german":"Hallo, wie geht's dir?",
                    "french":"Bonjour, comment ça va?",
                    "hindi":"नमस्ते, आप कैसे हैं?"
                }
            },
            {
                "original":"I love reading books.",
                "translated":{
                    "german":"Ich liebe es, Bücher zu lesen.",
                    "french":"J'aime lire des livres.",
                    "hindi":"मुझे किताबें पढ़ना पसंद है।"
                }
            },
            {
                "original":"The sky is blue.",
                "translated":{
                    "german":"Der Himmel ist blau.",
                    "french":"Le ciel est bleu.",
                    "hindi":"आसमान नीला है।"
                }
            },
            {
                "original":"What is your name?",
                "translated":{
                    "german":"Wie heißt du?",
                    "french":"Comment vous appelez-vous?",
                    "hindi":"आपका नाम क्या है?"
                }
            },
            {
                "original":"The cat is sleeping.",
                "translated":{
                    "german":"Die Katze schläft.",
                    "french":"Le chat dort.",
                    "hindi":"बिल्ली सो रही है।"
                }
            },
            {
                "original":"Dinner is ready.",
                "translated":{
                    "german":"Das Abendessen ist fertig.",
                    "french":"Le dîner est prêt.",
                    "hindi":"खाना तैयार है।"
                }
            },
            {
                "original":"I am learning a new language.",
                "translated":{
                    "german":"Ich lerne eine neue Sprache.",
                    "french":"J'apprends une nouvelle langue.",
                    "hindi":"मैं एक नई भाषा सीख रहा हूँ।"
                }
            },
            {
                "original":"Can you help me?",
                "translated":{
                    "german":"Kannst du mir helfen?",
                    "french":"Pouvez-vous m'aider?",
                    "hindi":"क्या आप मेरी मदद कर सकते हैं?"
                }
            },
            {
                "original":"She sings beautifully.",
                "translated":{
                    "german":"Sie singt wunderschön.",
                    "french":"Elle chante magnifiquement.",
                    "hindi":"वह सुंदरता से गाती है।"
                }
            },
            {
                "original":"It's raining outside.",
                "translated":{
                    "german":"Es regnet draußen.",
                    "french":"Il pleut dehors.",
                    "hindi":"बाहर बारिश हो रही है।"
                }
            }
        ]


        choice = random.choice(sentences)

        return jsonify({'original': choice['original'], 'translated': choice['translated'][language]})





    return app







def start_server():
    print("Starting server...")
    parser = argparse.ArgumentParser()

    #python server.py --host 127.0.0.1 --port 8000 --debug

    # API flag
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="The host to run the server",
    )
    parser.add_argument(
        "--port",
        default=os.environ.get("PORT"),
        help="The port to run the server",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run Flask in debug mode",
    )

    args = parser.parse_args()

    server_app = create_app()

    server_app.run(debug=args.debug, host=args.host, port=args.port)


if __name__ == "__main__":
    start_server()
